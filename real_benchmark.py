"""Real-photo availability and sensitivity diagnostics, not annotated accuracy."""
import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
import cv2
from real_pipeline import decode,detect
ROOT=Path(__file__).parent

def benchmark():
    manifest=json.loads((ROOT/'data/real/manifest.json').read_text())
    rows=[]
    for item in manifest['images']:
        data=(ROOT/'data/real'/item['filename']).read_bytes()
        if hashlib.sha256(data).hexdigest()!=item['sha256']:
            raise ValueError('Sample checksum mismatch')
        image=decode(data)
        base=detect(image)
        dark=detect(cv2.convertScaleAbs(image,alpha=.55))
        blur=detect(cv2.GaussianBlur(image,(15,15),0))
        keys=['detected','reason','left','right','accepted_segments','width_bottom_px','width','height']
        rows.append({'filename':item['filename'],'original':{k:base[k] for k in keys},
                     'darkened':{'detected':dark['detected'],'reason':dark['reason']},
                     'blurred':{'detected':blur['detected'],'reason':blur['reason']}})
    return {'executed_at_utc':datetime.now(timezone.utc).isoformat(),'opencv_version':cv2.__version__,
            'source_commit':manifest['source_commit'],'image_count':len(rows),
            'original_supported_pairs':sum(r['original']['detected'] for r in rows),
            'darkened_supported_pairs':sum(r['darkened']['detected'] for r in rows),
            'blurred_supported_pairs':sum(r['blurred']['detected'] for r in rows),
            'protocol':'Fixed defaults, same six known convenience samples; no learned model, no train/test split. Brightness and blur perturbations reuse each original.',
            'limitations':'No official annotations. Supported-pair counts are not accuracy, IoU, recall or lane correctness. Samples were used during development and are not a held-out evaluation.',
            'results':rows}
if __name__=='__main__':
    r=benchmark()
    (ROOT/'real-results.json').write_text(json.dumps(r,indent=2,allow_nan=False))
    print({k:r[k] for k in ['image_count','original_supported_pairs','darkened_supported_pairs','blurred_supported_pairs']})

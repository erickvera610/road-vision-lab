"""Paired ablation: fixed thresholds versus adaptive illumination on known scenes."""
import json
from pathlib import Path
from datetime import datetime,timezone
import cv2,numpy as np
from real_pipeline import decode,detect
ROOT=Path(__file__).parent

def benchmark():
    rows=[]
    for p in sorted((ROOT/'data/real').glob('*.jpg')):
        image=decode(p.read_bytes())
        for label,modified in [('original',image),('dark_55',cv2.convertScaleAbs(image,alpha=.55)),('dark_35',cv2.convertScaleAbs(image,alpha=.35)),('blur_15',cv2.GaussianBlur(image,(15,15),0))]:
            outputs={mode:detect(modified,mode) for mode in ['fixed','adaptive']}
            rows.append({'image':p.name,'condition':label,**{mode:{'supported_pair':r['detected'],'reason':r['reason'],'width_bottom_px':r['width_bottom_px']} for mode,r in outputs.items()}})
    negatives={'blank':np.zeros((180,320,3),np.uint8),'bright_wall':np.full((180,320,3),230,np.uint8)}
    return {'executed_at_utc':datetime.now(timezone.utc).isoformat(),'comparison':{c:{m:sum(r[m]['supported_pair'] for r in rows if r['condition']==c) for m in ['fixed','adaptive']} for c in ['original','dark_55','dark_35','blur_15']},
        'negative_controls':{name:{mode:detect(im,mode)['detected'] for mode in ['fixed','adaptive']} for name,im in negatives.items()},
        'source_manifest':'data/real/manifest.json','protocol':'Paired known development photos, each unchanged or under fixed brightness/blur transformations. No labels or new test scenes.',
        'limitations':'Output availability is not verified accuracy. Normalization can amplify distractors. These six previously inspected photos are development examples, not an independent robustness benchmark.','cases':rows}
if __name__=='__main__':
    report=benchmark();(ROOT/'lighting-results.json').write_text(json.dumps(report,indent=2,allow_nan=False));print(json.dumps(report['comparison']))

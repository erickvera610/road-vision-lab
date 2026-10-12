"""Reproducible robustness matrix for the six attributed real road images.

Reports detector output availability under controlled perturbations. It does NOT report
lane accuracy because the convenience images do not include independent ground truth.
"""
from pathlib import Path
import json
import cv2
import numpy as np
from real_pipeline import detect

ROOT = Path(__file__).parent
DATA = ROOT/'data'/'real'

def perturb(image, condition):
    if condition == 'original': return image.copy()
    if condition == 'dark_55': return np.clip(image.astype(np.float32)*.55,0,255).astype(np.uint8)
    if condition == 'dark_35': return np.clip(image.astype(np.float32)*.35,0,255).astype(np.uint8)
    if condition == 'bright_125': return np.clip(image.astype(np.float32)*1.25,0,255).astype(np.uint8)
    if condition == 'blur_15': return cv2.GaussianBlur(image,(15,15),0)
    if condition == 'noise_sigma_12':
        rng=np.random.default_rng(20261012)
        return np.clip(image.astype(np.float32)+rng.normal(0,12,image.shape),0,255).astype(np.uint8)
    raise ValueError(condition)

def main():
    manifest=json.loads((DATA/'manifest.json').read_text())
    conditions=('original','dark_55','dark_35','bright_125','blur_15','noise_sigma_12')
    rows=[]
    for item in manifest['images']:
        image=cv2.imread(str(DATA/item['filename']))
        if image is None: raise FileNotFoundError(item['filename'])
        for condition in conditions:
            sample=perturb(image,condition)
            for mode in ('fixed','adaptive'):
                result=detect(sample,mode)
                rows.append({'image':item['filename'],'condition':condition,'lighting':mode,
                             'detected':bool(result['detected']),'accepted_segments':int(result['accepted_segments']),
                             'elapsed_ms':float(result['elapsed_ms']),'reason':result['reason']})
    summary={}
    for condition in conditions:
        summary[condition]={}
        for mode in ('fixed','adaptive'):
            subset=[r for r in rows if r['condition']==condition and r['lighting']==mode]
            summary[condition][mode]={'supported_pairs':sum(r['detected'] for r in subset),'images':len(subset)}
    report={'interpretation':'Supported pair means geometric output availability, not lane accuracy.',
            'ground_truth':'No independent lane annotations are supplied for this six-image convenience set.',
            'summary':summary,'rows':rows}
    (ROOT/'robustness-matrix-results.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()

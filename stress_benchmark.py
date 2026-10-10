"""Include difficult inputs and failures instead of reporting ideal scenes only."""
import json
from pathlib import Path
from pipeline import synthetic_image, run_image

def benchmark():
    rows=[]
    for noise in [0,10,30]:
        for contrast in [230,160,100]:
            for seed in range(5):
                image=synthetic_image(seed,noise)
                image=[[contrast if p==230 else p for p in row] for row in image]
                result=run_image({"image":image,"seed":seed})
                error=abs(result["width_bottom"]-.7*(len(image)-1)) if result["detected"] else None
                rows.append({"noise":noise,"lane_intensity":contrast,"seed":seed,"detected":result["detected"],"width_error_px":error})
    negatives={"blank":[[0]*256 for _ in range(144)],"bright_wall":[[230]*256 for _ in range(144)]}
    return {"conditions":rows,"negative_controls":{k:run_image({"image":v})["detected"] for k,v in negatives.items()},
            "limitations":"Synthetic straight lanes only. Missing detections are retained. These conditions are not real-world accuracy estimates."}
if __name__=="__main__":
    r=benchmark()
    Path(__file__).with_name("stress-results.json").write_text(json.dumps(r,indent=2))
    print({"scenes":len(r["conditions"]),"detected":sum(x["detected"] for x in r["conditions"]),"negative_controls":r["negative_controls"]})

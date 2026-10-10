import random,math
def fit(points):
    if len(points)<2:raise ValueError('At least two points required')
    my=sum(p[1] for p in points)/len(points);mx=sum(p[0] for p in points)/len(points)
    denominator=sum((y-my)**2 for x,y in points)
    if denominator==0:raise ValueError('Distinct y coordinates required')
    a=sum((y-my)*(x-mx) for x,y in points)/denominator;b=mx-a*my
    return a,b
def robust_fit(points):
    a,b=fit(points);residuals=sorted(abs(x-a*y-b) for x,y in points);median=residuals[len(residuals)//2]
    kept=[(x,y) for x,y in points if abs(x-a*y-b)<=max(4,3*median)]
    a,b=fit(kept)
    return {'slope':a,'intercept':b,'rmse':math.sqrt(sum((x-a*y-b)**2 for x,y in kept)/len(kept)),'inliers':len(kept),'points':kept}
def run(p):
    noise=float(p.get('noise',4))
    if not 0<=noise<=30:raise ValueError('Noise must be between 0 and 30')
    rng=random.Random(int(p.get('seed',42)));left=[];right=[]
    for y in range(80,241,5):
        left.append((160-.35*y+rng.gauss(0,noise),y));right.append((160+.35*y+rng.gauss(0,noise),y))
    # Add synthetic outliers; fit x=a*y+b independently for each side.
    left += [(rng.uniform(10,150),rng.uniform(80,240)) for _ in range(4)]
    right += [(rng.uniform(170,310),rng.uniform(80,240)) for _ in range(4)]
    l=robust_fit(left);r=robust_fit(right)
    return {'left':l,'right':r,'width_bottom':(r['slope']*240+r['intercept'])-(l['slope']*240+l['intercept']),'note':'Fits synthetic lane points. No camera-image detection, object recognition, vehicle control, or Tesla affiliation.'}

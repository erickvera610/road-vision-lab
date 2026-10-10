function randomGenerator(seed=42) {
    let state=seed>>>0;
    return ()=> {
        state=(1664525*state+1013904223)>>>0;
        return state/4294967296;
    }
    ;
}
function normal(random) {
    return Math.sqrt(-2*Math.log(Math.max(random(),1e-10)))*Math.cos(2*Math.PI*random());
}
function syntheticImage(seed=42,noise=4) {
    const random=randomGenerator(seed),w=256,h=144,image=Array.from( {
        length:h
    }
    ,()=>Array.from( {
        length:w
    }
    ,()=>Math.max(0,Math.min(255,20+noise*normal(random)))));
    for(let y=Math.floor(h*.4);y<h;y++)for(const x of [Math.round(w/2-.35*y),Math.round(w/2+.35*y)])for(let dx=-2;dx<=2;dx++)image[y][x+dx]=230;
    for(let y=70;y<82;y++)for(let x=110;x<140;x++)image[y][x]=210;
    return image;
}
function fitLine(points) {
    const n=points.length,my=points.reduce((s,p)=>s+p[1],0)/n,mx=points.reduce((s,p)=>s+p[0],0)/n,den=points.reduce((s,p)=>s+(p[1]-my)**2,0);
    if(!den)throw Error('Degenerate line');
    const slope=points.reduce((s,p)=>s+(p[1]-my)*(p[0]-mx),0)/den;
    return [slope,mx-slope*my];
}
function fitRansac(points,seed,sign) {
    if(points.length<8)return null;
    const random=randomGenerator(seed);
    let best=[];
    for(let i=0;i<120;i++) {
        const p=points[Math.floor(random()*points.length)],q=points[Math.floor(random()*points.length)];
        if(Math.abs(p[1]-q[1])<10)continue;
        const a=(p[0]-q[0])/(p[1]-q[1]),b=p[0]-a*p[1];
        if(!(sign*a>.05&&sign*a<1.5))continue;
        const kept=points.filter(([x,y])=>Math.abs(x-a*y-b)<=3);
        if(kept.length>best.length)best=kept;
    }
    if(best.length<8)return null;
    const [slope,intercept]=fitLine(best);
    return  {
        slope,intercept,inliers:best.length,candidate_count:points.length,inlier_ratio:best.length/points.length,rmse:Math.sqrt(best.reduce((s,[x,y])=>s+(x-slope*y-intercept)**2,0)/best.length),points:best
    }
    ;
}
function runEnhanced(p= {
}
) {
    const noise=Number(p.noise??4),seed=p.seed??42;
    if(!Number.isFinite(noise)||noise<0||noise>30)throw Error('Noise 0–30 required');
    const uploaded=Boolean(p.image),image=p.image??syntheticImage(seed,noise),h=image.length,w=image[0]?.length;
    if(h<24||h>360||w<32||w>640||image.some(row=>row.length!==w||row.some(v=>!Number.isFinite(v)||v<0||v>255)))throw Error('Rectangular grayscale image required');
    const l=[],r=[];
    for(let y=Math.floor(h*.4);y<h-1;y++)for(let x=1;x<w-1;x++) {
        const gx=[-1,0,1].reduce((s,j)=>s+image[y+j][x+1]-image[y+j][x-1],0);
        if(image[y][x]>150&&Math.abs(gx)>160)(x<w/2?l:r).push([x,y]);
    }
    const left=fitRansac(l,seed,-1),right=fitRansac(r,seed+1,1),width=left&&right?(right.slope-left.slope)*(h-1)+right.intercept-left.intercept:null;
    return  {
        image,width:w,height:h,left,right,width_bottom:width,detected:Boolean(left&&right),synthetic_width_error_px:width!==null&&!uploaded?Math.abs(width-.7*(h-1)):null,data_kind:uploaded?'uploaded image':'synthetic image',note:'Straight bright-lane pixel prototype. Uploads have no ground truth; unsuitable for driving.'
    }
    ;
}
if(typeof module!=='undefined')module.exports= {
    runEnhanced,syntheticImage
}
;

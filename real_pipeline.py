"""Classical color/edge lane prototype. No learned detector or driving control."""
import base64
import time
import cv2
import numpy as np
from pipeline import ransac

MAX_BYTES = 5_000_000

def png(image):
    ok, encoded = cv2.imencode('.png', image)
    if not ok:
        raise ValueError('Could not encode output')
    return 'data:image/png;base64,' + base64.b64encode(encoded).decode('ascii')

def decode(data):
    if not data or len(data) > MAX_BYTES:
        raise ValueError('Image must be 1 byte to 5 MB')
    # Inspect PNG/JPEG dimensions before OpenCV allocates a full decoded buffer.
    from image_header import dimensions
    width, height = dimensions(data)
    if not 32 <= width <= 8000 or not 24 <= height <= 8000 or width * height > 16_000_000:
        raise ValueError('Image dimensions out of bounds (maximum 16 megapixels)')
    image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError('Invalid PNG/JPEG image')
    return image

def detect(image, lighting="adaptive"):
    if lighting not in ["fixed", "adaptive"]:
        raise ValueError("Lighting must be fixed or adaptive")
    start = time.perf_counter()
    original_h, original_w = image.shape[:2]
    factor = min(1, 640 / original_w, 360 / original_h)
    w, h = round(original_w * factor), round(original_h * factor)
    image = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Normalize illumination only for detection; preserve the original display image.
    processing = image
    if lighting == 'adaptive':
        value = hsv[:, :, 2].astype(np.float32)
        region = value[int(h*.60):, int(w*.08):int(w*.95)]
        lo, hi = np.percentile(region, [2, 98])
        if hi - lo > 5:
            hsv[:, :, 2] = np.clip((value - lo) * (230.0/(hi - lo)), 0, 255).astype(np.uint8)
            processing = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    white = cv2.inRange(hsv, np.array([0,0,170]), np.array([179,85,255]))
    yellow = cv2.inRange(hsv, np.array([15,65,80]), np.array([40,255,255]))
    color = cv2.bitwise_or(white,yellow)
    gray = cv2.cvtColor(processing, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(cv2.GaussianBlur(gray,(5,5),0),50,150)
    edges = cv2.bitwise_and(edges, cv2.dilate(color,np.ones((3,3),np.uint8)))
    roi = np.array([[(int(w*.08),h-1),(int(w*.44),int(h*.60)),(int(w*.57),int(h*.60)),(int(w*.95),h-1)]],np.int32)
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask,roi,255)
    edges = cv2.bitwise_and(edges, mask)
    segments = cv2.HoughLinesP(edges,1,np.pi/180,20,minLineLength=20,maxLineGap=30)
    sides = [[],[]]
    count = 0
    if segments is not None:
        for x1,y1,x2,y2 in segments[:,0]:
            if abs(int(y2)-int(y1)) < 8:
                continue
            a = (int(x2)-int(x1))/(int(y2)-int(y1))
            if not .15 < abs(a) < 3.0:
                continue
            midpoint=(x1+x2)/2
            side=0 if a < 0 and midpoint < w*.55 else 1 if a > 0 and midpoint > w*.45 else None
            if side is None:
                continue
            count += 1
            for t in np.linspace(0,1,12):
                sides[side].append((float(x1+t*(x2-x1)),float(y1+t*(y2-y1))))
    left = ransac(sides[0],42,-1,tolerance=5,max_slope=3.0)
    right = ransac(sides[1],43,1,tolerance=5,max_slope=3.0)
    rejection=None
    top=int(h*.60)
    bottom=h-1
    if left and right:
        lx=lambda y:left['slope']*y+left['intercept']
        rx=lambda y:right['slope']*y+right['intercept']
        if not (0 <= lx(bottom) < rx(bottom) < w and 0 < rx(top)-lx(top) < rx(bottom)-lx(bottom)):
            rejection='Pair rejected: crossing, outside image, or non-widening geometry'
    accepted=bool(left and right and rejection is None)
    overlay=image.copy()
    cv2.polylines(overlay,roi,True,(255,180,0),1)
    for line,col in [(left,(180,220,30)),(right,(0,200,255))]:
        if line and rejection is None:
            cv2.line(overlay,(round(line['slope']*top+line['intercept']),top),(round(line['slope']*bottom+line['intercept']),bottom),col,3)
    reason=rejection or ('Two candidate lines; inspect overlay for correctness' if accepted else 'Insufficient support for a two-line pair')
    clean=lambda line: {k:v for k,v in line.items() if k!='points'} if line else None
    return {'detected':accepted,'reason':reason,'width':w,'height':h,'original_width':original_w,'original_height':original_h,
            'left':clean(left),'right':clean(right),'accepted_segments':count,
            'width_bottom_px':float((right['slope']-left['slope'])*bottom+right['intercept']-left['intercept']) if accepted else None,
            'lighting_mode':lighting,
            'elapsed_ms':round((time.perf_counter()-start)*1000,2),
            'images':{'original':png(image),'overlay':png(overlay),'edges':png(edges),'color_mask':png(color)},
            'method':'Optional ROI percentile illumination normalization → HSV white/yellow mask → blur/Canny → trapezoid ROI → Hough segments → seeded RANSAC → geometry check',
            'limitations':'Straight-line approximation, daylight bias. Detected is geometric support, not verified correctness or calibrated confidence. Width is pixels, not meters.'}

def run_bytes(data, lighting="adaptive"):
    return detect(decode(data), lighting)

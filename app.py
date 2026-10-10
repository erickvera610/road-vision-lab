"""Same-origin Python demo. Uploaded bytes are processed in memory, never saved."""
import base64
import binascii
import json
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from core import run
ROOT = Path(__file__).parent
SAMPLES = {p.name:p for p in (ROOT/'data/real').glob('*.jpg')}

class Handler(BaseHTTPRequestHandler):
    def send(self,status,data,kind='application/json'):
        body=data if isinstance(data,bytes) else data.encode() if isinstance(data,str) else json.dumps(data,allow_nan=False).encode()
        self.send_response(status)
        self.send_header('Content-Type',kind)
        self.send_header('Content-Length',str(len(body)))
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Cache-Control','no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path=urlsplit(self.path).path
        if path=='/health':return self.send(200,{'status':'ok','backend':'Python'})
        if path=='/':return self.send(200,(ROOT/'index.html').read_text(),'text/html; charset=utf-8')
        if path=='/api/samples':return self.send(200,{'samples':[{'name':name,'url':'/samples/'+name} for name in sorted(SAMPLES)]})
        if path.startswith('/samples/') and path[9:] in SAMPLES:
            return self.send(200,SAMPLES[path[9:]].read_bytes(),'image/jpeg')
        self.send(404,{'error':'Not found'})

    def do_POST(self):
        if self.path not in ['/api/run','/api/detect']:
            return self.send(404,{'error':'Not found'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=7_000_000:raise ValueError('Request body must be below 7 MB')
            payload=json.loads(self.rfile.read(length))
            if not isinstance(payload,dict):raise ValueError('JSON object required')
            if self.path=='/api/run':return self.send(200,run(payload))
            from real_pipeline import run_bytes
            if 'sample' in payload:
                if not isinstance(payload['sample'],str) or payload['sample'] not in SAMPLES:
                    raise ValueError('Unknown sample')
                data=SAMPLES[payload['sample']].read_bytes()
            elif isinstance(payload.get('image_base64'),str):
                data=base64.b64decode(payload['image_base64'],validate=True)
            else:raise ValueError('Provide sample name or image_base64')
            self.send(200,run_bytes(data))
        except (ValueError,TypeError,KeyError,OverflowError,binascii.Error) as exc:
            self.send(400,{'error':str(exc)})
        except Exception:
            self.send(500,{'error':'Image processing failed; verify the file format and installed dependencies'})

if __name__=='__main__':
    host=os.environ.get('HOST','127.0.0.1')
    port=int(os.environ.get('PORT','8000'))
    print(f'Open http://{host}:{port}',flush=True)
    ThreadingHTTPServer((host,port),Handler).serve_forever()

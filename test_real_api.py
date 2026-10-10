import base64, json, struct, threading, unittest, urllib.request, urllib.error
from http.server import ThreadingHTTPServer
from app import Handler, SAMPLES
from real_pipeline import run_bytes

class RealPipelineTests(unittest.TestCase):
    def test_real_photo(self):
        r=run_bytes(SAMPLES['solidWhiteRight.jpg'].read_bytes())
        self.assertTrue(r['detected'])
        self.assertEqual((r['width'],r['height']),(640,360))
        self.assertTrue(r['images']['overlay'].startswith('data:image/png;base64,'))
        self.assertGreater(r['width_bottom_px'],0)
    def test_decoder_rejects_invalid_and_oversized(self):
        for data in [b'not an image',b'',b'\x89PNG\r\n\x1a\n'+b'\0\0\0\rIHDR'+struct.pack('>II',99999,99999),b'x'*5_000_001]:
            with self.assertRaises(ValueError):run_bytes(data)

class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.url='http://127.0.0.1:'+str(cls.server.server_port)
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def post(self,payload):
        req=urllib.request.Request(self.url+'/api/detect',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req) as response:return json.load(response)
    def test_sample_and_upload_use_same_pipeline(self):
        a=self.post({'sample':'solidWhiteRight.jpg'})
        b=self.post({'image_base64':base64.b64encode(SAMPLES['solidWhiteRight.jpg'].read_bytes()).decode()})
        self.assertEqual(a['left'],b['left']);self.assertEqual(a['images'],b['images'])
    def test_bad_requests_and_unknown_sample(self):
        for p in [{'sample':'../../app.py'},{'sample':[]},{'image_base64':'%%%bad'},[],{}]:
            with self.assertRaises(urllib.error.HTTPError) as error:self.post(p)
            self.assertEqual(error.exception.code,400)
        self.assertTrue(self.post({'sample':'solidWhiteRight.jpg'})['detected'])
    def test_health_samples_and_page(self):
        with urllib.request.urlopen(self.url+'/api/samples') as r:self.assertEqual(len(json.load(r)['samples']),6)
        with urllib.request.urlopen(self.url+'/') as r:self.assertIn(b'/api/detect',r.read())
        with urllib.request.urlopen(self.url+'/samples/solidWhiteRight.jpg') as r:self.assertEqual(r.headers['Content-Type'],'image/jpeg')
    def test_blank_png_has_no_pair(self):
        import cv2,numpy as np
        _,image=cv2.imencode('.png',np.zeros((100,160,3),dtype=np.uint8))
        self.assertFalse(self.post({'image_base64':base64.b64encode(image).decode()})['detected'])

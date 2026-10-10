"""Read supported raster dimensions before allocating a decoder buffer."""
import struct

def dimensions(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data)>=24 and data[12:16]==b'IHDR':
        return struct.unpack('>II',data[16:24])
    if data.startswith(b'\xff\xd8'):
        i=2
        while i<len(data):
            if data[i]!=255:
                raise ValueError('Malformed JPEG header')
            while i<len(data) and data[i]==255:i+=1
            if i>=len(data):break
            marker=data[i];i+=1
            if marker in [0xd9,0xda]:break
            if marker in [0x01,*range(0xd0,0xd8)]:continue
            if i+2>len(data):break
            length=int.from_bytes(data[i:i+2],'big')
            if length<2 or i+length>len(data):break
            if marker in [0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf] and length>=7:
                h,w=struct.unpack('>HH',data[i+3:i+7]);return w,h
            i+=length
    raise ValueError('A valid PNG or JPEG image is required')

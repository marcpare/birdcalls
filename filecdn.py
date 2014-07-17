"""
Downloads, stores, and resizes images on disk

Configure to a directory.
"""

import os
import os.path
import sys
import requests
import hashlib

class FileCDN(object):
    
    def __init__(self, base_dir):
        self.base_dir = base_dir
    
    def fn(self, collection, url):
        m = hashlib.md5()
        m.update(url)
        
        file_type = url.split('.')[-1]
        
        fn = m.hexdigest() + '.' + file_type
        
        return os.path.join(self.base_dir, collection, fn)
        
    def download_if_missing(self, url):
        fn = self.fn('raw', url)
        if os.path.exists(fn):
            pass
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(fn, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)
    
    # Resizes using any ImageMagick geometry string
    # http://www.imagemagick.org/script/command-line-processing.php#geometry
    def scale(self, url, resize):
        from wand.image import Image
        
        raw_fn = self.fn('raw', url)
        out_fn = self.fn(resize, url)
        
        # ensure directory for images
        try:
            os.makedirs(os.path.join(self.base_dir, resize))
        except:
            pass
        
        # transform and save
        with Image(filename=raw_fn) as img:
            img.transform(resize=resize) 
            img.save(filename= out_fn)

if __name__ == '__main__':
    
    cdn = FileCDN('cdn')
    url = 'http://www.birdweb.org/birdweb/images/PUMA_fl_gl.jpg'
    cdn.download_if_missing(url)
    
    cdn.scale(url, '100')
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
    
    def cdn_fn(self, collection, url):
        m = hashlib.md5()
        m.update(url)
        file_type = url.split('.')[-1]
        fn = m.hexdigest() + '.' + file_type
        return os.path.join(collection, fn)
    
    def fn(self, collection, url):        
        return os.path.join(self.base_dir, self.cdn_fn(collection, url))
        
    def download_if_missing(self, url):
        cdn_fn = self.cdn_fn('raw', url)
        fn = self.fn('raw', url)
        if not os.path.exists(fn):
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(fn, 'wb') as f:
                    for chunk in r.iter_content():
                        f.write(chunk)
        return cdn_fn
    
    # Resizes using any ImageMagick geometry string
    # http://www.imagemagick.org/script/command-line-processing.php#geometry
    def scale(self, url, resize, ignore_existing=True):
        from wand.image import Image
        
        raw_fn = self.fn('raw', url)
        cdn_fn = self.cdn_fn(resize, url)
        out_fn = self.fn(resize, url)
        
        if not os.path.exists(out_fn) or not ignore_existing:    
            # ensure directory for images
            try:
                os.makedirs(os.path.join(self.base_dir, resize))
            except:
                pass
            # transform and save
            with Image(filename=raw_fn) as img:
                img.transform(resize=resize) 
                img.save(filename=out_fn)
        return cdn_fn

if __name__ == '__main__':
    
    cdn = FileCDN('cdn')
    url = 'http://www.birdweb.org/birdweb/images/PUMA_fl_gl.jpg'
    cdn.download_if_missing(url)
    
    cdn.scale(url, '100')
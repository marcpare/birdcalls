import requests
import os.path
import hashlib

DEBUG = False
CACHE_DIR = 'cache'

def cache_path(key):
    m = hashlib.md5()
    m.update(key)
    return os.path.join(CACHE_DIR, m.hexdigest())

def cache_put(key, value):
    """ Value should be a string """
    print cache_path(key)
    f = open(cache_path(key), 'w')
    f.write(value.encode('utf8'))
    f.close()

def cache_has(key):
    return os.path.isfile(cache_path(key))

def cache_get(key):
    
    if DEBUG:
        print "Retrieving %s (%s) from cache" % (key, cache_path(key))
    
    if cache_has(key):
        f = open(cache_path(key))
        return f.read().decode('utf8')
    return False

def cached_request(url):
    if not cache_has(url):
        r = requests.get(url)
        html = r.text
        cache_put(url, html)
    return cache_get(url)
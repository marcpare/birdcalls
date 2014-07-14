import os.path
import hashlib

DEBUG = False

class FileCache(object):
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def path(self, key):
        m = hashlib.md5()
        m.update(key)
        return os.path.join(self.base_dir, m.hexdigest())

    def put(self, key, value):
        """ Value should be a string """
        f = open(self.path(key), 'w')
        f.write(value.encode('utf8'))
        f.close()

    def has(self, key):
        return os.path.isfile(self.path(key))

    def get(self, key):
    
        if DEBUG:
            print "Retrieving %s (%s) from cache" % (key, cache_path(key))
    
        if self.has(key):
            f = open(self.path(key))
            return f.read().decode('utf8')
        return False
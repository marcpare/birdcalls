"""
A JSON frontend to the filesystem.

Configure to a directory.
Subdirectories are collections.
Files are items in the collection.
Store things as JSON.

"""

import os
import os.path
import sys
import json
import argparse as ap

class FileDB(object):
    
    def __init__(self, base_dir):
        self.base_dir = base_dir
    
    def fn(self, collection, name=None):
        if name:
            name += '.json'
            return os.path.join(self.base_dir, collection, name)
        else:
            return os.path.join(self.base_dir, collection)
            
    def post(self, collection, name, value):
        f = open(self.fn(collection, name), 'w')
        f.write(json.dumps(value))
        f.close()
    
    # If the item exists, only OVERWRITE collisions, don't 
    # nuke the entire entity.
    def patch(self, collection, name, value):
        existing = self.get(collection, name)
        if not existing:
            existing = {}
        existing.update(value)
        self.post(collection, name, existing)
        
    # Get a collection name to return the list
    # Get an item name to return the item
    def get(self, collection, name=None):
        if not os.path.exists(self.fn(collection, name)):
            return None
        
        if name:
            return json.loads(open(self.fn(collection, name)).read())
        else:
            return [fn[:-5] for fn in os.listdir(self.fn(collection))]

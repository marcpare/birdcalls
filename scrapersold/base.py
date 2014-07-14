from bs4 import BeautifulSoup
import os
import os.path
import sys
import json
from cache import *
import argparse as ap
from urlparse import urlparse, parse_qs

def get_soup(url):
    html = cached_request(url)
    return BeautifulSoup(html)
    
# simple file db
def db_add(collection, name, value):
    f = open(os.path.join(collection, name+'.json'), 'w')
    f.write(json.dumps(value))
    f.close()

def db_list(collection):
    # remove the trailing '.json'
    return [fn[:-5] for fn in os.listdir(collection)]
    
def db_get(collection, name):
    return json.loads(open(os.path.join(collection, name+'.json')).read())
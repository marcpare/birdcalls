from nose.tools import *
import os
import os.path
from filedb import FileDB

FN_FAKEDB = os.path.join(os.path.dirname(__file__), 'fakedb')

def test_list():
    db = FileDB(FN_FAKEDB)    
    assert_equals(db.get('foo'), ['bar', 'baz'])
    
def test_get():
    db = FileDB(FN_FAKEDB)    
    assert_equals(db.get('foo', 'bar'), {u'hi': u'there'})
    
def test_get_empty():
    db = FileDB(FN_FAKEDB)
    assert_is_none(db.get('baz'))
    assert_is_none(db.get('foo', 'zip'))

def test_post():
    db = FileDB(FN_FAKEDB)
    db.post('bar', 'zip', {'a':1})
    z = db.get('bar', 'zip')
    assert_equals(z, {'a': 1})
    
def test_patch():
    db = FileDB(FN_FAKEDB)
    db.patch('bar', 'zip', {'a':2, 'b':2})
    z = db.get('bar', 'zip')
    assert_equals(z, {'a':2, 'b': 2})
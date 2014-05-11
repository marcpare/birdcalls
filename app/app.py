from flask import Flask
from peewee import *

app = Flask(__name__)

db = MySQLDatabase('birds', user='root', passwd='root')

class MySQLModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = db

class Birds(MySQLModel):
    common_name = CharField()
 
@app.route('/')
def birds():
    return str(Birds.select().count())
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7204)
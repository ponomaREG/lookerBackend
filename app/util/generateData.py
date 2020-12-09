
import sqlite3
import os
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
UPLOAD_FOLDER = "app\\static\\img"
PLACEHOLDER_NAME = 'placeholder.jpg'
SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(50)
DATABASES_FOLDER = os.path.join(basedir,'databases')
JSON_AS_ASCII = False
DB_PATH = os.path.join(basedir,'db.db')

db = sqlite3.connect(DB_PATH,check_same_thread=False)

for i in range(300):
    ursor = db.execute("INSERT INTO online('vk_id','online') values({},{});".format(210696772,i % 2))
    ursor.close()
    db.commit()

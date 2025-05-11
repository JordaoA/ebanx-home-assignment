from flask import Flask
from config.config import DB_PATH
from tinydb import TinyDB, Query


app = Flask(__name__)

db = TinyDB(DB_PATH)

accounts = db.table('accounts')
Account = Query()

from app.controller import api
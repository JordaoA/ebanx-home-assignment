from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec
from config.config import DB_PATH
from tinydb import TinyDB, Query


app = Flask(__name__)
spec = FlaskPydanticSpec('ebanx-API')
spec.register(app)

db = TinyDB(DB_PATH)

accounts = db.table('accounts')
Account = Query()

from app.controller import api
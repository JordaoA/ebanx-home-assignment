from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec
from config.config import DB_PATH
from tinydb import TinyDB, Query


app = Flask(__name__)
spec = FlaskPydanticSpec('ebanx-API')
spec.register(app)
print("DB_PATH")
db = TinyDB(DB_PATH)
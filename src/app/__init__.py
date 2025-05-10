from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec


app = Flask(__name__)
spec = FlaskPydanticSpec('ebanx-API')
spec.register(app)
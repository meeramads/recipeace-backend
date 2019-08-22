from flask import Flask, g
from flask_cors import CORS
import models

from api.user import user

DEBUG = True
PORT = 8000

app = Flask(__name__)

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(user)

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'hi'

if __name__ == '__main__' :
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
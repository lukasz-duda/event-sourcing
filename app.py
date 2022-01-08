from flask import Flask
from flask.helpers import make_response

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def get_products():
    return make_response()
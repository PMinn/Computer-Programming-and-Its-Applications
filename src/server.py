import os
import json
# import eel
# import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_url_path="/static")
port = 8088
CORS(app)


@app.route("/", methods=["POST"])
def hello():
    data = request.json
    return data


if __name__ == "__main__":
    app.run(port=port, debug=True)

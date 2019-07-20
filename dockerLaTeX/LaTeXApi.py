#!/usr/bin/env python3.6
from flask import Flask, request, abort
from armid import *
import os


app = Flask(__name__)


@app.route('/latexApi', methods=['POST'])
def index():
    try:
        dockBookCmd = request.values.get('docBookCmd')
        os.system(dockBookCmd)
        return "Success"
    except:
        abort(500)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

#!/usr/local/bin/python
from flask import Flask, request, abort
import os

app = Flask(__name__)

allowedCommands = set(['docbook2html','docbook2rtf','dblatex','pandoc'])

@app.route('/latexApi', methods=['POST'])
def index():
  try:
    dockBookCmd = request.values.get('docBookCmd')
    if not docBookCmd:
      abort(400)
    if (docBookCmd.split(' ')[0] not in allowedCommands):
      abort(400)
    os.system(dockBookCmd)
    return "Success"
  except Exception:
    abort(500)

if __name__ == '__main__':
  app.run(host="0.0.0.0",debug=True)

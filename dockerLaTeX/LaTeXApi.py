#!/usr/local/bin/python
from flask import Flask, request, abort
import os

app = Flask(__name__)


@app.route('/latexApi', methods=['POST'])
def index():
  allowedCommands = set(['docbook2html','docbook2rtf','dblatex','pandoc'])
  try:
    dockBookCmd = request.values.get('docBookCmd')
    if not docBookCmd:
      print("No DocBook command")
      abort(400)
    cmd = docBookCmd.split(' ')[0]
    if (docBookCmd.split(' ')[0] not in allowedCommands):
      print(cmd + " is not allowed.")
      abort(400)
    os.system(dockBookCmd)
    return "Success"
  except Exception:
    abort(500)

if __name__ == '__main__':
  app.run(host="0.0.0.0",debug=True)

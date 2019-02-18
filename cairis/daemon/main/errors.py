#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

__author__ = 'Shamal Faily'

import sys
if (sys.version_info > (3,)):
  import http.client
  from http.client import CONFLICT, BAD_REQUEST, INTERNAL_SERVER_ERROR
else:
  import httplib
  from httplib import CONFLICT, BAD_REQUEST, INTERNAL_SERVER_ERROR
from cairis.daemon.CairisHTTPError import CairisHTTPError, ARMHTTPError
from cairis.core.ARM import ARMException, DatabaseProxyException
from flask import request, make_response
from cairis.daemon.main import main

@main.errorhandler(CairisHTTPError)
def handle_error(error):
  accept_header = request.headers.get('Accept', 'application/json')
  if accept_header.find('text/html') > -1:
    resp = make_response(error.handle_exception_html(), error.status_code)
    resp.headers['Content-type'] = 'text/html'
    return resp
  else:
    resp = make_response(error.handle_exception_json(), error.status_code)
    resp.headers['Content-type'] = 'application/json'
    return resp


@main.errorhandler(AssertionError)
def handle_asserterror(error):
  err = CairisHTTPError(CONFLICT, str(error), 'Unmet requirement')
  return handle_error(err)


@main.errorhandler(KeyError)
def handle_keyerror(error):
  err = CairisHTTPError(BAD_REQUEST, str(error), 'Missing attribute')
  return handle_error(err)


@main.errorhandler(ARMException)
@main.errorhandler(DatabaseProxyException)
def handle_keyerror(e):
  err = ARMHTTPError(e)
  return handle_error(err)


@main.errorhandler(500)
def handle_internalerror(e):
  return handle_exception(e)


def handle_exception(e):
  if isinstance(e, AssertionError):
    return handle_asserterror(e)
  elif isinstance(e, KeyError):
    return handle_keyerror(e)
  else:
    new_ex = CairisHTTPError(INTERNAL_SERVER_ERROR, str(e), 'Unknown error')
    return handle_error(new_ex)

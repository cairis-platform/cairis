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

import httplib
import logging

from cairis.core.ARM import DatabaseProxyException
from cairis.core.Borg import Borg
from cairis.core.MySQLDatabaseProxy import MySQLDatabaseProxy
from cairis.daemon.CairisHTTPError import MissingParameterHTTPError, CairisHTTPError, ObjectNotFoundHTTPError
from cairis.core.TemplateGenerator import TemplateGenerator
from cairis.tools.GraphicsGenerator import GraphicsGenerator

__author__ = 'Robin Quetin'


def check_required_keys(json_dict, required):
    """
    :return:
    :raise MissingParameterHTTPError:
    """
    if not all(reqKey in json_dict for reqKey in required):
        raise MissingParameterHTTPError(param_names=required)

def get_logger():
    b = Borg()
    log = logging.getLogger('cairisd')
    log.setLevel(logging.INFO)

    try:
        log = b.logger
    except AttributeError:
        b.logger = log
        try:
            log.setLevel(b.logLevel)
            b.logger.setLevel(b.logLevel)
        except AttributeError:
            b.logLevel = logging.INFO

    return log

def get_session_id(session, request):
    """
    Looks up the session ID in the HTTP session, request URL and body
    :type session: flask.session
    :type request: flask.request
    """
    session_id = None

    # Look if HTTP session is being used
    if session is not None:
        session_id = session.get('session_id', session_id)

    # Look if form data is being used
    if request.form:
        session_id = request.form.get('session_id', session_id)

    # Look if body contains session ID
    json = request.get_json(silent=True)
    if json is not False and json is not None:
        session_id = json.get('session_id', session_id)

    # Check if the session ID is provided by query parameters
    session_id = request.args.get('session_id', session_id)

    if session_id is None:
        raise MissingParameterHTTPError(param_names=['session_id'])

    return session_id

def validate_proxy(session, id, request=None, conf=None):
    """
    Validates that the DB proxy object is properly set up
    :param session: The session object of the request
    :param id: The session ID provided by the user
    :param conf: A dictionary containing configuration settings for direct authenrication
    :return: The MySQLDatabaseProxy object associated to the session
    :rtype : MySQLDatabaseProxy
    :raise CairisHTTPError: Raises a CairisHTTPError when the database could not be properly set up
    """

    if session is not None:
        session_id = session.get('session_id', -1)
    else:
        session_id = None

    if conf is not None:
        if isinstance(conf, dict):
            try:
                db_proxy = MySQLDatabaseProxy(host=conf['host'], port=conf['port'], user=conf['user'], passwd=conf['passwd'], db=conf['db'])
                if db_proxy is not None:
                    return db_proxy
                else:
                    raise CairisHTTPError(
                        status_code=httplib.CONFLICT,
                        message='The database connection could not be created.'
                    )
            except DatabaseProxyException:
                raise CairisHTTPError(
                    status_code=httplib.BAD_REQUEST,
                    message='The provided settings are invalid and cannot be used to create a database connection'
                )

    if not (session_id is None and id is None):
        if id is None:
            id = session_id
        b = Borg()
        db_proxy = b.get_dbproxy(id)

        if db_proxy is None:
            raise CairisHTTPError(
                status_code=httplib.CONFLICT,
                message='The database connection could not be created.'
            )
        elif isinstance(db_proxy, MySQLDatabaseProxy):
            return db_proxy
        else:
            raise CairisHTTPError(
                status_code=httplib.CONFLICT,
                message='The database connection was not properly set up. Please try to reset the connection.'
            )
    else:
        raise CairisHTTPError(
            status_code=httplib.BAD_REQUEST,
            message='The session is neither started or no session ID is provided with the request.'
        )

def get_fonts(session_id=None):
    """
    Validates that the fonts to output the SVG models are properly set up
    :param session_id: The session ID provided by the user
    :return: The font name, font size and AP font name
    :rtype : str,str,str
    :raise CairisHTTPError: Raises a CairisHTTPError when the database could not be properly set up
    """
    if session_id is not None:
        b = Borg()
        settings = b.get_settings(session_id)
        fontName = settings.get('fontName', None)
        fontSize = settings.get('fontSize', None)
        apFontName = settings.get('apFontSize', None)

        if fontName is None or fontSize is None or apFontName is None:
            raise CairisHTTPError(
                status_code=httplib.BAD_REQUEST,
                message='The method is not callable without setting up the project settings.'
            )
        elif isinstance(fontName, str) and isinstance(fontSize, str) and isinstance(apFontName, str):
            return fontName, fontSize, apFontName
        else:
            raise CairisHTTPError(
                status_code=httplib.BAD_REQUEST,
                message='The database connection was not properly set up. Please try to reset the connection.'
            )
    else:
        raise CairisHTTPError(
            status_code=httplib.BAD_REQUEST,
            message='The method is not callable without setting up the project settings.'
        )

def get_template_generator():
    b = Borg()
    if hasattr(b, 'template_generator'):
        template_generator = b.template_generator
        assert isinstance(template_generator, TemplateGenerator)
        return template_generator
    else:
        raise RuntimeError(
            message='The template generator is not properly initialized. Please check if all dependencies are installed correctly.'
        )

def get_model_generator():
    b = Borg()
    if hasattr(b, 'model_generator'):
        model_generator = b.model_generator
        assert isinstance(model_generator, GraphicsGenerator)
        return model_generator
    else:
        raise RuntimeError(
            message='The model generator is not properly initialized. Please check if all dependencies are installed correctly.'
        )

def check_environment(environment_name, session, session_id):
    db_proxy = validate_proxy(session, session_id)

    environment_names = db_proxy.getEnvironmentNames()
    if not environment_name in environment_names:
        raise ObjectNotFoundHTTPError('The specified environment')

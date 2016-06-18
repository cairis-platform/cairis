import httplib
import logging
from flask.ext.restful_swagger import swagger
from flask import request, make_response, session
from flask.ext.restful import Resource
from jsonpickle import encode

from cairis.core.Borg import Borg
from cairis.daemon.CairisHTTPError import MissingParameterHTTPError, MalformedJSONHTTPError
from cairis.tools.ModelDefinitions import UserConfigModel
from cairis.tools.SessionValidator import validate_proxy, get_logger


__author__ = 'Robin Quetin'


def set_dbproxy(conf):
    b = Borg()
    db_proxy = validate_proxy(None, -1, conf=conf)
    pSettings = db_proxy.getProjectSettings()

    id = b.init_settings()
    db_proxy.close()
    session['session_id'] = id
    b.settings[id]['dbProxy'] = db_proxy
    b.settings[id]['dbUser'] = conf['user']
    b.settings[id]['dbPasswd'] = conf['passwd']
    b.settings[id]['dbHost'] = conf['host']
    b.settings[id]['dbPort'] = conf['port']
    b.settings[id]['dbName'] = conf['db']
    b.settings[id]['fontSize'] = pSettings['Font Size']
    b.settings[id]['apFontSize'] = pSettings['AP Font Size']
    b.settings[id]['fontName'] = pSettings['Font Name']
    b.settings[id]['jsonPrettyPrint'] = conf.get('jsonPrettyPrint', False)

    return b.settings[id]

def serve_user_config_form():
    b = Borg()
    resp = make_response(b.template_generator.serve_result('user_config', action_url=request.full_path), httplib.OK)
    resp.headers['Content-type'] = 'text/html'
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

def handle_user_config_form():
    try:
        dict_form = request.form

        conf = {
            'host': dict_form['host'],
            'port': int(dict_form['port']),
            'user': dict_form['user'],
            'passwd': dict_form['passwd'],
            'db': dict_form['db'],
            'jsonPrettyPrint': dict_form.get('jsonPrettyPrint', False) == 'on'
        }
        s = set_dbproxy(conf)
        debug = ''
        '''debug += '{0}\nSession vars:\n{1}\nQuery string:\n'.format(
            'Configuration successfully updated',
            json_serialize(s, session_id=s['session_id']))'''

        resp = make_response(debug + 'session_id={0}'.format(s['session_id']), httplib.OK)
        resp.headers['Content-type'] = 'text/plain'
        resp.headers['Access-Control-Allow-Origin'] = "*"
        return resp
    except KeyError as ex:
        return MissingParameterHTTPError(exception=ex)

class UserConfigAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Sets up the user session',
        nickname='user-config-post',
        responseClass=str.__name__,
        parameters=[
            {
                'name': 'body',
                "description": "The configuration settings for the user's session",
                "required": True,
                "allowMultiple": False,
                'type': UserConfigModel.__name__,
                'paramType': 'body'
            }
        ],
        responseMessages=[
            {
                'code': httplib.BAD_REQUEST,
                'message': 'The method is not callable without setting up a database connection'
            },
            {
                'code': httplib.BAD_REQUEST,
                'message': 'The provided parameters are invalid'
            }
        ]
    )
    # endregion
    def post(self):
        try:
            b = Borg()
            dict_form = request.get_json(silent=True)

            if dict_form is False or dict_form is None:
                raise MalformedJSONHTTPError(data=request.get_data())

            b.logger.info(dict_form)
            s = set_dbproxy(dict_form)

            resp_dict = {'session_id': s['session_id'], 'message': 'Configuration successfully applied'}
            resp = make_response(encode(resp_dict), httplib.OK)
            resp.headers['Content-type'] = 'application/json'
            return resp

        except KeyError:
            return MissingParameterHTTPError()

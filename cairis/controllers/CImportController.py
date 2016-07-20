import httplib
from os import close as fd_close
from os import remove as remove_file
from tempfile import mkstemp
from urllib import unquote

from flask import make_response, request, session
from flask.ext.restful import Resource
from flask_restful_swagger import swagger
from werkzeug.datastructures import FileStorage

from cairis.core.ARM import DatabaseProxyException, ARMException
from cairis.core.Borg import Borg
from cairis.daemon.CairisHTTPError import MalformedJSONHTTPError, CairisHTTPError, ARMHTTPError, MissingParameterHTTPError
from cairis.bin.cimport import *
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import CImportMessage
from cairis.tools.ModelDefinitions import CImportParams
from cairis.tools.SessionValidator import validate_proxy, check_required_keys, get_session_id

__author__ = 'Robin Quetin'


class CImportTextAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Imports data from XML text',
        nickname='cimport-text-post',
        parameters=[
            {
                'name':'body',
                "description": "Options to be passed to the import tool",
                "required": True,
                "allowMultiple": False,
                'type': CImportMessage.__name__,
                'paramType': 'body'
            },
            {
                "name": "session_id",
                "description": "The ID of the user's session",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                'code': httplib.BAD_REQUEST,
                'message': 'The provided file is not a valid XML file'
            },
            {
                'code': httplib.BAD_REQUEST,
                'message': '''Some parameters are missing. Be sure 'file_contents' and 'type' are defined.'''
            }
        ]
    )
    # endregion
    def post(self):
        session_id = get_session_id(session, request)
        json_dict = request.get_json(silent=True)

        if json_dict is False or json_dict is None:
            raise MalformedJSONHTTPError(data=request.get_data())

        cimport_params = json_dict.get('object', None)
        check_required_keys(cimport_params or {}, CImportParams.required)
        file_contents = cimport_params['urlenc_file_contents']
        file_contents = unquote(file_contents)
        type = cimport_params['type']
        overwrite = cimport_params.get('overwrite', None)

        if file_contents.startswith('<?xml'):
            fd, abs_path = mkstemp(suffix='.xml')
            fs_temp = open(abs_path, 'w')
            fs_temp.write(file_contents)
            fs_temp.close()
            fd_close(fd)

            try:
                result = file_import(abs_path, type, overwrite, session_id=session_id)
            except DatabaseProxyException as ex:
                raise ARMHTTPError(ex)
            except ARMException as ex:
                raise ARMHTTPError(ex)
            except Exception as ex:
                raise CairisHTTPError(
                    status_code=500,
                    message=str(ex.message),
                    status='Unknown error'
                )

            remove_file(abs_path)

            resp_dict = {'message': str(result)}
            resp = make_response(json_serialize(resp_dict, session_id=session_id), httplib.OK)
            resp.headers['Content-Type'] = 'application/json'
            return resp
        else:
            raise CairisHTTPError(
                status_code=httplib.BAD_REQUEST,
                message='The provided file is not a valid XML file',
                status='Invalid XML input'
            )


class CImportFileAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Imports data from an XML file',
        nickname='cimport-file-post',
        parameters=[
            {
                'name':'file',
                "description": "The XML file to import",
                "required": True,
                "allowMultiple": False,
                'type': 'file',
                'paramType': 'form'
            },
            {
                "name": "overwrite",
                "description": "Defines if existing data should be overwritten",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            },
            {
                "name": "overwrite",
                "description": "Defines if existing data should be overwritten",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "form"
            },
            {
                "name": "session_id",
                "description": "The ID of the user's session",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                'code': httplib.BAD_REQUEST,
                'message': 'The provided file is not a valid XML file'
            },
            {
                'code': httplib.BAD_REQUEST,
                'message': '''Some parameters are missing. Be sure 'file_contents' and 'type' are defined.'''
            }
        ]
    )
    # endregion
    def post(self, type):
        session_id = get_session_id(session, request)
        overwrite = request.form.get('overwrite', None)
        overwrite = request.args.get('overwrite', overwrite)
        try:
            if not request.files:
                raise LookupError()
            file = request.files['file']
        except LookupError:
            raise MissingParameterHTTPError(param_names=['file'])

        try:
            fd, abs_path = mkstemp(suffix='.xml')
            fs_temp = open(abs_path, 'w')
            xml_text = file.stream.read()
            fs_temp.write(xml_text)
            fs_temp.close()
            fd_close(fd)
        except IOError:
            raise CairisHTTPError(
                status_code=httplib.CONFLICT,
                status='Unable to load XML file',
                message='The XML file could not be loaded on the server.' +
                        'Please check if the application has permission to write temporary files.'
            )

        try:
            result = file_import(abs_path, type, overwrite, session_id=session_id)
        except DatabaseProxyException as ex:
            raise ARMHTTPError(ex)
        except ARMException as ex:
            raise ARMHTTPError(ex)
        except Exception as ex:
            raise CairisHTTPError(
                status_code=500,
                message=str(ex.message),
                status='Unknown error'
            )

        remove_file(abs_path)

        resp_dict = { 'message': str(result) }
        resp = make_response(json_serialize(resp_dict, session_id=session_id), httplib.OK)
        resp.headers['Content-Type'] = 'application/json'
        return resp

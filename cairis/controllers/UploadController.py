import httplib

from flask import session, make_response
from flask import request
from flask.ext.restful import Resource
from flask.ext.restful_swagger import swagger
from cairis.daemon.CairisHTTPError import MissingParameterHTTPError, CairisHTTPError
from cairis.data.UploadDAO import UploadDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Robin Quetin'


class UploadImageAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Sets up the user session',
        nickname='user-config-post',
        parameters=[
            {
                'name': 'file',
                "description": "The image file to upload (formats: "+str(UploadDAO.accepted_image_types)+")",
                "required": True,
                "allowMultiple": False,
                'type': 'file',
                'paramType': 'form'
            },
            {
                'name': 'session_id',
                'description': 'The ID of the session to use',
                'required': False,
                'allowMultiple': False,
                'type': 'string',
                'paramType': 'query'
            }
        ],
        responseMessages=[
            {
                'code': httplib.BAD_REQUEST,
                'message': 'The provided parameters are invalid'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'Unsupported file type'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'Image not found'
            }
        ]
    )
    # endregion
    def post(self):
        session_id = get_session_id(session, request)

        if session_id is None:
            raise CairisHTTPError(
                status_code=httplib.BAD_REQUEST,
                message='The session is neither started or no session ID is provided with the request.'
            )

        content_length = request.content_length
        max_length = 10*1024*1024
        if content_length > max_length:
            raise MissingParameterHTTPError(exception=RuntimeError('File exceeded maximum size (10MB)'))

        try:
            file = request.files['file']
        except LookupError as ex:
            raise MissingParameterHTTPError(param_names=['file'])
        except Exception as ex:
            raise CairisHTTPError(
                status_code=httplib.CONFLICT,
                message=str(ex.message),
                status='Unknown error'
            )

        dao = UploadDAO(session_id)
        filename = dao.upload_image(file)

        resp_dict = {'message': 'File successfully uploaded', 'filename': filename}
        resp = make_response(json_serialize(resp_dict, session_id=session_id), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

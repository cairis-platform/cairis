import httplib
from flask import session, request, make_response
from flask.ext.restful import Resource
from flask.ext.restful_swagger import swagger
from cairis.data.ProjectDAO import ProjectDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ProjectMessage
from cairis.tools.PseudoClasses import ProjectSettings
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Robin Quetin'


class ProjectCreateAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Create a new project',
        nickname='project-create-get',
        responseClass=str.__name__,
        parameters=[
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
            }
        ]
    )
    # endregion
    def post(self):
        session_id = get_session_id(session, request)

        dao = ProjectDAO(session_id)
        dao.create_new_project()

        resp_dict = {'message': 'New project successfully created'}
        resp = make_response(json_serialize(resp_dict, session_id=session_id), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

class ProjectSettingsAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get the project settings',
        nickname='project-settings-get',
        responseClass=ProjectSettings.__name__,
        parameters=[
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
            }
        ]
    )
    # endregion
    def get(self):
        session_id = get_session_id(session, request)

        dao = ProjectDAO(session_id)
        settings = dao.get_settings()

        resp = make_response(json_serialize(settings, session_id=session_id), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Update the project settings',
        nickname='project-settings-put',
        parameters=[
            {
                'name': 'session_id',
                'description': 'The ID of the session to use',
                'required': False,
                'allowMultiple': False,
                'type': 'string',
                'paramType': 'query'
            },
            {
                'name': 'body',
                'description': 'The settings to apply to the current project',
                'required': True,
                'allowMultiple': False,
                'type': ProjectMessage.__name__,
                'paramType': 'body'
            }
        ],
        responseMessages=[
            {
                'code': httplib.BAD_REQUEST,
                'message': 'The provided parameters are invalid'
            }
        ]
    )
    # endregion
    def put(self):
        session_id = get_session_id(session, request)

        dao = ProjectDAO(session_id)
        settings = dao.from_json(request)
        dao.apply_settings(settings)

        resp_dict = {'message': 'Project settings successfully updated'}
        resp = make_response(json_serialize(resp_dict, session_id=session_id), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

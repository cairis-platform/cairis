import httplib

from flask import session, request, make_response
from flask.ext.restful_swagger import swagger
from flask_restful import Resource

from cairis.data.GoalDAO import GoalDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import GoalMessage
from cairis.tools.ModelDefinitions import GoalModel as SwaggerGoalModel
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Robin Quetin'


class GoalsAPI(Resource):
    #region Swagger Doc
    @swagger.operation(
        notes='Get all goals.',
        responseClass=SwaggerGoalModel.__name__,
        nickname='goals-get',
        parameters=[
            {
                "name": "coloured",
                "description": "Defines if the goal colour needs to be retrieved",
                "required": False,
                "allowMultiple": False,
                "dataType": int.__name__,
                "paramType": "query"
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
                "code": httplib.BAD_REQUEST,
                "message": "The database connection was not properly set up"
            }
        ]
    )
    #endregion
    def get(self):
        session_id = get_session_id(session, request)
        constraint_id = request.args.get('constraint_id', -1)
        coloured = request.args.get('coloured', False)

        dao = GoalDAO(session_id)
        goals = dao.get_goals(constraint_id=constraint_id, coloured=(coloured == '1'))
        dao.close()

        resp = make_response(json_serialize(goals, session_id=session_id))
        resp.headers['Content-Type'] = "application/json"
        return resp

    #region Swagger Doc
    @swagger.operation(
        notes='Creates a new goal',
        nickname='goal-post',
        parameters=[
            {
                "name": "body",
                "description": "The serialized version of the new goal to be added",
                "required": True,
                "allowMultiple": False,
                "type": GoalMessage.__name__,
                "paramType": "body"
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
                'message': 'One or more attributes are missing'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'Some problems were found during the name check'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    #endregion
    def post(self):
        session_id = get_session_id(session, request)

        dao = GoalDAO(session_id)
        new_goal = dao.from_json(request)
        new_goal_id = dao.add_goal(new_goal)
        dao.close()

        resp_dict = {'message': 'Goal successfully added', 'goal_id': new_goal_id}
        resp = make_response(json_serialize(resp_dict, session_id=session_id), httplib.OK)
        resp.contenttype = 'application/json'
        return resp


class GoalByNameAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get a goal by name',
        responseClass=SwaggerGoalModel.__name__,
        nickname='goal-by-name-get',
        parameters=[
            {
                "name": "coloured",
                "description": "Defines if the goal colour needs to be retrieved",
                "required": False,
                "allowMultiple": False,
                "dataType": int.__name__,
                "paramType": "query"
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
                "code": httplib.BAD_REQUEST,
                "message": "The database connection was not properly set up"
            }
        ]
    )
    # endregion
    def get(self, name):
        session_id = get_session_id(session, request)
        coloured = request.args.get('coloured', False)

        dao = GoalDAO(session_id)
        found_goal = dao.get_goal_by_name(name, coloured=(coloured == '1'))
        dao.close()

        resp = make_response(json_serialize(found_goal, session_id=session_id))
        resp.headers['Content-Type'] = "application/json"
        return resp

    #region Swagger Doc
    @swagger.operation(
        notes='Updates an existing goal',
        nickname='goal-put',
        parameters=[
            {
                "name": "body",
                "description": "The serialized version of the goal to be updated",
                "required": True,
                "allowMultiple": False,
                "type": GoalMessage.__name__,
                "paramType": "body"
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
                'message': 'One or more attributes are missing'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'Some problems were found during the name check'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    #endregion
    def put(self, name):
        session_id = get_session_id(session, request)

        dao = GoalDAO(session_id)
        upd_goal = dao.from_json(request)
        dao.update_goal(upd_goal, name)
        dao.close()

        resp_dict = {'message': 'Goal successfully updated'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

    #region Swagger Doc
    @swagger.operation(
        notes='Deletes an existing goal',
        nickname='goal-by-id-delete',
        parameters=[
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
                'message': 'One or more attributes are missing'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'Some problems were found during the name check'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    #endregion
    def delete(self, name):
        session_id = get_session_id(session, request)

        dao = GoalDAO(session_id)
        dao.delete_goal(name)
        dao.close()

        resp_dict = {'message': 'Goal successfully deleted'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.contenttype = 'application/json'
        return resp


class GoalModelAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get the goal model for a specific environment',
        responseClass=SwaggerGoalModel.__name__,
        nickname='goal-by-name-get',
        parameters=[
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
                "code": httplib.BAD_REQUEST,
                "message": "The database connection was not properly set up"
            },
            {
                "code": httplib.NOT_FOUND,
                "message": "Environment not found"
            },
            {
                "code": httplib.BAD_REQUEST,
                "message": "Environment not defined"
            }
        ]
    )
    # endregion
    def get(self, environment):
        session_id = get_session_id(session, request)
        model_generator = get_model_generator()

        dao = GoalDAO(session_id)
        dot_code = dao.get_goal_model(environment)
        dao.close()

        resp = make_response(model_generator.generate(dot_code, model_type='goal'), httplib.OK)
        accept_header = request.headers.get('Accept', 'image/svg+xml')
        if accept_header.find('text/plain') > -1:
            resp.headers['Content-type'] = 'text/plain'
        else:
            resp.headers['Content-type'] = 'image/svg+xml'

        return resp

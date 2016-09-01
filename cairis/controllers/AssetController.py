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
from flask import request, session, make_response
from flask_restful_swagger import swagger
from flask.ext.restful import Resource
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError
from cairis.data.AssetDAO import AssetDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import AssetMessage, AssetEnvironmentPropertiesMessage, ValueTypeMessage
from cairis.tools.ModelDefinitions import AssetModel as SwaggerAssetModel, AssetEnvironmentPropertiesModel, ValueTypeModel
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Robin Quetin, Shamal Faily'


class AssetsAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get all assets without the asset environment properties.' +
              'To get the asset environment properties of an asset, please use /api/assets/{name}/properties',
        responseClass=SwaggerAssetModel.__name__,
        nickname='assets-get',
        parameters=[
            {
                "name": "session_id",
                "description": "The ID of the user's session",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            },
            {
                "name": "constraint_id",
                "description": "An ID used to filter the assets",
                "required": False,
                "default": -1,
                "allowMultiple": False,
                "dataType": int.__name__,
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
    def get(self):
        constraint_id = request.args.get('constraint_id', -1)
        session_id = get_session_id(session, request)

        dao = AssetDAO(session_id)
        assets = dao.get_assets(constraint_id=constraint_id)
        dao.close()

        resp = make_response(json_serialize(assets, session_id=session_id))
        resp.headers['Content-Type'] = "application/json"
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Creates a new asset',
        nickname='asset-post',
        parameters=[
            {
                "name": "body",
                "description": "The serialized version of the new asset to be added",
                "required": True,
                "allowMultiple": False,
                "type": AssetMessage.__name__,
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
    # endregion
    def post(self):
        session_id = get_session_id(session, request)

        dao = AssetDAO(session_id)
        asset = dao.from_json(request)
        new_id = dao.add_asset(asset)
        dao.close()

        resp_dict = {'asset_id': new_id}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.contenttype = 'application/json'
        return resp


class AssetByEnvironmentNamesAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get all the asset names associated with a specific environment',
        responseClass=SwaggerAssetModel.__name__,
        nickname='assets-by-environment-names-get',
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
            }
        ]
    )
    # endregion
    def get(self, environment):
        session_id = get_session_id(session, request)

        dao = AssetDAO(session_id)
        assets = dao.get_asset_names(environment=environment)
        dao.close()

        resp = make_response(json_serialize(assets, session_id=session_id))
        resp.headers['Content-Type'] = "application/json"
        return resp


class AssetByNameAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get an asset by name',
        responseClass=SwaggerAssetModel.__name__,
        nickname='asset-by-name-get',
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
            }
        ]
    )
    # endregion
    def get(self, name):
        session_id = get_session_id(session, request)

        dao = AssetDAO(session_id)
        found_asset = dao.get_asset_by_name(name)
        dao.close()

        resp = make_response(json_serialize(found_asset, session_id=session_id))
        resp.headers['Content-Type'] = "application/json"
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Updates an existing asset',
        nickname='asset-put',
        parameters=[
            {
                "name": "body",
                "description": "The session ID and the serialized version of the asset to be updated",
                "required": True,
                "allowMultiple": False,
                "type": AssetMessage.__name__,
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
                'code': httplib.NOT_FOUND,
                'message': 'The provided asset name could not be found in the database'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    # endregion
    def put(self, name):
        import pytest
        pytest.set_trace()
        session_id = get_session_id(session, request)

        dao = AssetDAO(session_id)
        asset = dao.from_json(request)
        dao.update_asset(asset, name=name)
        dao.close()

        resp_dict = {'message': 'Update successful'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Deletes an existing asset',
        nickname='asset-delete',
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
                'code': httplib.NOT_FOUND,
                'message': 'The provided asset name could not be found in the database'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    # endregion
    def delete(self, name):
        session_id = request.args.get('session_id', None)
        dao = AssetDAO(session_id)

        dao.delete_asset(name=name)
        dao.close()

        resp_dict = {'message': 'Asset successfully deleted'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

class AssetByIdAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get an asset by ID',
        responseClass=SwaggerAssetModel.__name__,
        nickname='asset-by-id-get',
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
            }
        ]
    )
    # endregion
    def get(self, id):
        session_id = get_session_id(session, request)

        dao = AssetDAO(session_id)
        asset = dao.get_asset_by_id(id)
        dao.close()
        if asset is None:
            raise ObjectNotFoundHTTPError('The asset')

        resp = make_response(json_serialize(asset, session_id=session_id))
        resp.headers['Content-Type'] = "application/json"
        return resp


class AssetNamesAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get a list of assets',
        responseClass=str.__name__,
        responseContainer="List",
        nickname='asset-names-get',
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
            }
        ]
    )
    # endregion
    def get(self):
        session_id = request.args.get('session_id', None)

        dao = AssetDAO(session_id)
        assets_names = dao.get_asset_names()
        dao.close()

        resp = make_response(json_serialize(assets_names, session_id=session_id))
        resp.headers['Content-Type'] = "application/json"
        return resp


class AssetModelAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get the asset model for a specific environment',
        nickname='asset-model-get',
        parameters=[
            {
                "name": "environment",
                "description": "The environment to be used for the asset model",
                "required": True,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            },
            {
                "name": "asset",
                "description": "The asset filter",
                "required": True,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            },
            {
                "name": "hide_concerns",
                "description": "Defines if concerns should be hidden in the model",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "enum": ['0','1'],
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
    def get(self, environment,asset):
        session_id = get_session_id(session, request)
        hide_concerns = request.args.get('hide_concerns', '1')
        if hide_concerns == '0' or hide_concerns == 0:
            hide_concerns = False
        else:
            hide_concerns = True
        if asset == 'all':
          asset = ''
        model_generator = get_model_generator()

        dao = AssetDAO(session_id)
        dot_code = dao.get_asset_model(environment, asset, hide_concerns=hide_concerns)
        dao.close()

        if not isinstance(dot_code, str):
            raise ObjectNotFoundHTTPError('The model')

        resp = make_response(model_generator.generate(dot_code,renderer='dot'), httplib.OK)
        accept_header = request.headers.get('Accept', 'image/svg+xml')
        if accept_header.find('text/plain') > -1:
            resp.headers['Content-type'] = 'text/plain'
        else:
            resp.headers['Content-type'] = 'image/svg+xml'

        return resp


class AssetEnvironmentPropertiesAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get the environment properties for a specific asset',
        nickname='asset-envprops-by-name-get',
        responseClass=AssetEnvironmentPropertiesModel.__name__,
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
            }
        ]
    )
    # endregion
    def get(self, asset_name):
        session_id = get_session_id(session, request)

        dao = AssetDAO(session_id)
        asset_props = dao.get_asset_props(name=asset_name)
        dao.close()

        resp = make_response(json_serialize(asset_props, session_id=session_id))
        resp.contenttype = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Updates the environment properties for a specific asset',
        nickname='asset-envprops-by-name-put',
        parameters=[
            {
                "name": "body",
                "required": True,
                "allowMultiple": False,
                "dataType": AssetEnvironmentPropertiesMessage.__name__,
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
                "code": httplib.BAD_REQUEST,
                "message": "The database connection was not properly set up"
            }
        ]
    )
    # endregion
    def put(self, asset_name):
        session_id = get_session_id(session, request)

        dao = AssetDAO(session_id)
        asset_prop = dao.from_json(request, to_props=True)
        dao.update_asset_properties(asset_prop, name=asset_name)
        dao.close()

        resp_dict = {'message': 'The asset properties were successfully updated.'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.contenttype = 'application/json'
        return resp


class AssetTypesAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get all asset types',
        nickname='assets-types-get',
        responseClass=ValueTypeModel.__name__,
        responseContainer='List',
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
            }
        ]
    )
    # endregion
    def get(self):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AssetDAO(session_id)
        assets = dao.get_asset_types(environment_name=environment_name)
        dao.close()

        resp = make_response(json_serialize(assets, session_id=session_id), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Creates a new asset type',
        nickname='asset-type-by-name-post',
        parameters=[
            {
                "name": "body",
                "description": "The serialized version of the new asset type to be added",
                "required": True,
                "allowMultiple": False,
                "type": ValueTypeMessage.__name__,
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
    # endregion
    def post(self):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AssetDAO(session_id)
        new_value_type = dao.type_from_json(request)
        asset_type_id = dao.add_asset_type(new_value_type, environment_name=environment_name)
        dao.close()

        resp_dict = {'message': 'Asset type successfully added', 'asset_type_id': asset_type_id}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.contenttype = 'application/json'
        return resp


class AssetTypeByNameAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get a asset type by name',
        nickname='asset-type-by-name-get',
        responseClass=ValueTypeModel.__name__,
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
            }
        ]
    )
    # endregion
    def get(self, name):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AssetDAO(session_id)
        asset_type = dao.get_asset_type_by_name(name=name, environment_name=environment_name)
        dao.close()

        resp = make_response(json_serialize(asset_type, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Docs
    @swagger.operation(
        notes='Updates a asset type',
        nickname='asset-type-by-name-put',
        parameters=[
            {
                'name': 'body',
                "description": "",
                "required": True,
                "allowMultiple": False,
                'type': ValueTypeMessage.__name__,
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
                'message': '''Some parameters are missing. Be sure 'asset' is defined.'''
            }
        ]
    )
    # endregion
    def put(self, name):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AssetDAO(session_id)
        asset_type = dao.type_from_json(request)
        dao.update_asset_type(asset_type, name=name, environment_name=environment_name)
        dao.close()

        resp_dict = {'message': 'Asset type successfully updated'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Deletes an existing asset type',
        nickname='asset-type-by-name-delete',
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
                'code': httplib.NOT_FOUND,
                'message': 'The provided asset name could not be found in the database'
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
    # endregion
    def delete(self, name):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AssetDAO(session_id)
        dao.delete_asset_type(name=name, environment_name=environment_name)
        dao.close()

        resp_dict = {'message': 'Asset type successfully deleted'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp


class AssetValuesAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get all asset values',
        nickname='assets-values-get',
        responseClass=ValueTypeModel.__name__,
        responseContainer='List',
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
            }
        ]
    )
    # endregion
    def get(self, environment_name):
        session_id = get_session_id(session, request)

        dao = AssetDAO(session_id)
        assets = dao.get_asset_values(environment_name=environment_name)
        dao.close()

        resp = make_response(json_serialize(assets, session_id=session_id), httplib.OK)
        resp.contenttype = 'application/json'
        return resp


class AssetValueByNameAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get a asset value by name',
        nickname='asset-value-by-name-get',
        responseClass=ValueTypeModel.__name__,
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
            }
        ]
    )
    # endregion
    def get(self, name, environment_name):
        session_id = get_session_id(session, request)

        dao = AssetDAO(session_id)
        asset_value = dao.get_asset_value_by_name(name=name, environment_name=environment_name)
        dao.close()

        resp = make_response(json_serialize(asset_value, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Docs
    @swagger.operation(
        notes='Updates a asset value',
        nickname='asset-value-by-name-put',
        parameters=[
            {
                'name': 'body',
                "description": "",
                "required": True,
                "allowMultiple": False,
                'type': ValueTypeMessage.__name__,
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
                'message': '''Some parameters are missing. Be sure 'asset' is defined.'''
            }
        ]
    )
    # endregion
    def put(self, name, environment_name):
        session_id = get_session_id(session, request)

        dao = AssetDAO(session_id)
        asset_value = dao.type_from_json(request)
        dao.update_asset_value(asset_value, name=name, environment_name=environment_name)
        dao.close()

        resp_dict = {'message': 'Asset type successfully updated'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

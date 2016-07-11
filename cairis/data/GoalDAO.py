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

from cairis.core.ARM import *
from cairis.core.Goal import Goal
from cairis.core.GoalEnvironmentProperties import GoalEnvironmentProperties
from cairis.core.GoalParameters import GoalParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
from cairis.misc.KaosModel import KaosModel
from cairis.core.ValueType import ValueType
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import GoalEnvironmentPropertiesModel, GoalModel
from cairis.tools.SessionValidator import check_required_keys, get_fonts

__author__ = 'Robin Quetin'

class GoalDAO(CairisDAO):
    def __init__(self, session_id):
        CairisDAO.__init__(self, session_id)

    def get_goals(self, constraint_id=-1, coloured=False, simplify=True):
        try:
            if coloured:
                goals = self.db_proxy.getColouredGoals(constraint_id)
            else:
                goals = self.db_proxy.getGoals(constraint_id)
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)

        if simplify:
            for key, value in goals.items():
                goals[key] = self.simplify(value)

        return goals

    def get_goal_by_name(self, name, coloured=False, simplify=True):
        found_goal = None
        goals = self.get_goals(coloured=coloured, simplify=False)

        if goals is not None:
            found_goal = goals.get(name)

        if found_goal is None:
            self.close()
            raise ObjectNotFoundHTTPError('The provided goal name')

        if simplify:
            found_goal = self.simplify(found_goal)

        return found_goal

    def add_goal(self, goal):
        goalParams = GoalParameters(
            goalName=goal.theName,
            goalOrig=goal.theOriginator,
            tags=goal.theTags,
            properties=goal.theEnvironmentProperties
        )

        if not self.check_existing_goal(goal.theName):
            goal_id = self.db_proxy.addGoal(goalParams)
        else:
            self.close()
            raise OverwriteNotAllowedHTTPError('The provided goal name')

        return goal_id

    def update_goal(self, goal, name):
        old_goal = self.get_goal_by_name(name, simplify=False)
        id = old_goal.theId

        params = GoalParameters(
            goalName=goal.theName,
            goalOrig=goal.theOriginator,
            tags=goal.theTags,
            properties=goal.theEnvironmentProperties
        )
        params.setId(id)

        try:
            self.db_proxy.updateGoal(params)
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)

    def delete_goal(self, name):
        found_goal = self.get_goal_by_name(name)

        try:
            self.db_proxy.deleteGoal(found_goal.theId)
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)
        except ARMException as ex:
            self.close()
            raise ARMHTTPError(ex)

    def check_existing_goal(self, name):
        try:
            self.db_proxy.nameCheck(name, 'goal')
            return False
        except ARMException as ex:
            if str(ex.value).find('already exists') > -1:
                return True
            self.close()
            raise ARMHTTPError(ex)

    def get_goal_model(self, environment_name):
        fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)

        try:
            associationDictionary = self.db_proxy.goalModel(environment_name)
            associations = KaosModel(associationDictionary.values(), environment_name, db_proxy=self.db_proxy, font_name=fontName,
                                     font_size=fontSize)
            dot_code = associations.graph()
            return dot_code
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)

    # region Goal types
    def get_goal_types(self, environment_name=''):
        try:
            goal_types = self.db_proxy.getValueTypes('goal_type', environment_name)
            return goal_types
        except DatabaseProxyException as ex:
            raise ARMHTTPError(ex)
        except ARMException as ex:
            raise ARMHTTPError(ex)

    def get_goal_type_by_name(self, name, environment_name=''):
        found_type = None
        goal_types = self.get_goal_types(environment_name=environment_name)

        if goal_types is None or len(goal_types) < 1:
            raise ObjectNotFoundHTTPError('Goal types')

        idx = 0
        while found_type is None and idx < len(goal_types):
            if goal_types[idx].theName == name:
                found_type = goal_types[idx]
            idx += 1

        if found_type is None:
            raise ObjectNotFoundHTTPError('The provided goal type name')

        return found_type

    def add_goal_type(self, goal_type, environment_name=''):
        assert isinstance(goal_type, ValueType)
        type_exists = self.check_existing_goal_type(goal_type.theName, environment_name=environment_name)

        if type_exists:
            raise OverwriteNotAllowedHTTPError(obj_name='The goal type')

        params = ValueTypeParameters(
            vtName=goal_type.theName,
            vtDesc=goal_type.theDescription,
            vType='goal_type',
            envName=environment_name,
            vtScore=goal_type.theScore,
            vtRat=goal_type.theRationale
        )

        try:
            return self.db_proxy.addValueType(params)
        except DatabaseProxyException as ex:
            raise ARMHTTPError(ex)
        except ARMException as ex:
            raise ARMHTTPError(ex)

    def update_goal_type(self, goal_type, name, environment_name=''):
        assert isinstance(goal_type, ValueType)

        found_type = self.get_goal_type_by_name(name, environment_name)

        params = ValueTypeParameters(
            vtName=goal_type.theName,
            vtDesc=goal_type.theDescription,
            vType='goal_type',
            envName=environment_name,
            vtScore=goal_type.theScore,
            vtRat=goal_type.theRationale
        )
        params.setId(found_type.theId)

        try:
            self.db_proxy.updateValueType(params)
        except DatabaseProxyException as ex:
            raise ARMHTTPError(ex)
        except ARMException as ex:
            raise ARMHTTPError(ex)

    def delete_goal_type(self, name, environment_name=''):
        found_type = self.get_goal_type_by_name(name, environment_name)

        try:
            self.db_proxy.deleteGoalType(found_type.theId)
        except DatabaseProxyException as ex:
            raise ARMHTTPError(ex)
        except ARMException as ex:
            raise ARMHTTPError(ex)

    def check_existing_goal_type(self, name, environment_name):
        try:
            self.get_goal_type_by_name(name, environment_name)
            return True
        except ObjectNotFoundHTTPError:
            return False
    # endregion

    # region Goal values
    def get_goal_values(self, environment_name=''):
        try:
            goal_values = self.db_proxy.getValueTypes('goal_value', environment_name)
            return goal_values
        except DatabaseProxyException as ex:
            raise ARMHTTPError(ex)
        except ARMException as ex:
            raise ARMHTTPError(ex)

    def get_goal_value_by_name(self, name, environment_name=''):
        found_value = None
        goal_values = self.get_goal_values(environment_name=environment_name)
        if goal_values is None or len(goal_values) < 1:
            raise ObjectNotFoundHTTPError('Goal values')
        idx = 0
        while found_value is None and idx < len(goal_values):
            if goal_values[idx].theName == name:
                found_value = goal_values[idx]
            idx += 1
        if found_value is None:
            raise ObjectNotFoundHTTPError('The provided goal value name')
        return found_value

    def update_goal_value(self, goal_value, name, environment_name=''):
        assert isinstance(goal_value, ValueType)
        found_value = self.get_goal_value_by_name(name, environment_name)
        params = ValueTypeParameters(
            vtName=goal_value.theName,
            vtDesc=goal_value.theDescription,
            vType='goal_value',
            envName=environment_name,
            vtScore=goal_value.theScore,
            vtRat=goal_value.theRationale
        )
        params.setId(found_value.theId)
        try:
            self.db_proxy.updateValueType(params)
        except DatabaseProxyException as ex:
            raise ARMHTTPError(ex)
        except ARMException as ex:
            raise ARMHTTPError(ex)

    def check_existing_goal_value(self, name, environment_name):
        try:
            self.get_goal_value_by_name(name, environment_name)
            return True
        except ObjectNotFoundHTTPError:
            return False
    # endregion

    def convert_properties(self, real_props=None, fake_props=None):
        new_props = []
        if real_props is not None:
            for real_prop in real_props:
                assert isinstance(real_prop, GoalEnvironmentProperties)

                new_concern_assocs = []
                for concern_assoc in real_prop.theConcernAssociations:
                    new_concern_assocs.append(list(concern_assoc))

                new_goal_refinements = []
                for goal_refinement in real_prop.theGoalRefinements:
                    new_goal_refinements.append(list(goal_refinement))

                new_subgoal_refinements = []
                for subgoal_refinement in real_prop.theSubGoalRefinements:
                    new_subgoal_refinements.append(list(subgoal_refinement))

                real_prop.theConcernAssociations = new_concern_assocs
                real_prop.theGoalRefinements = new_goal_refinements
                real_prop.theSubGoalRefinements = new_subgoal_refinements
                new_props.append(real_prop)
        elif fake_props is not None:
            for fake_prop in fake_props:
                check_required_keys(fake_prop, GoalEnvironmentPropertiesModel.required)

                new_concern_assocs = []
                for concern_assoc in fake_prop['theConcernAssociations']:
                    new_concern_assocs.append(tuple(concern_assoc))

                new_goal_refinements = []
                for goal_refinement in fake_prop['theGoalRefinements']:
                    new_goal_refinements.append(tuple(goal_refinement))

                new_subgoal_refinements = []
                for subgoal_refinement in fake_prop['theSubGoalRefinements']:
                    new_subgoal_refinements.append(tuple(subgoal_refinement))

                new_prop = GoalEnvironmentProperties(
                    environmentName=fake_prop['theEnvironmentName'],
                    lbl=fake_prop['theLabel'],
                    definition=fake_prop['theDefinition'],
                    category=fake_prop['theCategory'],
                    priority=fake_prop['thePriority'],
                    fitCriterion=fake_prop['theFitCriterion'],
                    issue=fake_prop['theIssue'],
                    goalRefinements=new_goal_refinements,
                    subGoalRefinements=new_subgoal_refinements,
                    concs=fake_prop['theConcerns'],
                    cas=new_concern_assocs,
                )
                new_props.append(new_prop)
        else:
            self.close()
            raise MissingParameterHTTPError(param_names=['real_props', 'fake_props'])

        return new_props

    def from_json(self, request):
        self.logger.debug('Request data: %s', request.data)
        json = request.get_json(silent=True)
        if json is False or json is None:
            self.close()
            raise MalformedJSONHTTPError(data=request.get_data())

        json_dict = json['object']
        check_required_keys(json_dict, GoalModel.required)
        json_dict['__python_obj__'] = Goal.__module__+'.'+Goal.__name__
        props_list = json_dict.pop('theEnvironmentProperties', [])
        json_dict.pop('theEnvironmentDictionary', None)
        real_props = self.convert_properties(fake_props=props_list)

        new_json_goal = json_serialize(json_dict)
        new_json_goal = json_deserialize(new_json_goal)
        new_json_goal.theEnvironmentProperties = real_props

        if not isinstance(new_json_goal, Goal):
            self.close()
            raise MalformedJSONHTTPError(data=request.get_data())
        else:
            return new_json_goal

    def simplify(self, goal):
        """
        Simplifies the Goal object by removing the environment properties
        :param goal: The Goal to simplify
        :type goal: Goal
        :return: The simplified Goal
        :rtype: Goal
        """
        goal.theEnvironmentProperties = self.convert_properties(real_props=goal.theEnvironmentProperties)
        assert isinstance(goal, Goal)
        goal.theEnvironmentDictionary = {}

        delattr(goal, 'theEnvironmentDictionary')
        return goal

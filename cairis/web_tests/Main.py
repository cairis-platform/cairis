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

import unittest
import sys
from AssetTests import AssetTests
from CImportTests import CImportTests
from DependencyTests import DependencyTests
from EnvironmentTests import EnvironmentTests
from GoalTests import GoalTests
from MisuseCaseTests import MisuseCaseTests
from ProjectTests import ProjectTests
from RequirementTests import RequirementTests
from ResponseTests import ResponseTests
from RiskTests import RiskTests
from RoleTests import RoleTests
from ThreatTests import ThreatTests
from UploadTests import UploadTests
from UserTests import UserTests
from VulnerabilityTests import VulnerabilityTests

__author__ = 'Robin Quetin'

tests_dict = {
    'asset': [0, AssetTests],
    'dependency': [0, DependencyTests],
    'environment': [0, EnvironmentTests],
    'goal': [0, GoalTests],
    'import': [0, CImportTests],
    'misusecase': [0, MisuseCaseTests],
    'project': [0, ProjectTests],
    'requirement': [0, RequirementTests],
    'response': [0, ResponseTests],
    'risk': [0, RiskTests],
    'role': [0, RoleTests],
    'threat': [0, ThreatTests],
    'upload': [0, UploadTests],
    'vulnerability': [0, VulnerabilityTests],
    'user': [0, UserTests]
}


def enable_tests(tests):
    for test in tests:
        if test in tests_dict.keys():
            tests_dict[test][0] = 1
        else:
            print('Unrecognized test: %s' % test)

if __name__ == '__main__':
    if len(sys.argv) > 0:
        test_args = '--tests='
        needs_parsing = False

        for arg in sys.argv:
            assert isinstance(arg, str)
            if arg.startswith(test_args) or needs_parsing:
                tests_str = arg[len(test_args):]
                tests = tests_str.split(',')
                enable_tests(tests)

            if arg.startswith('-t'):
                needs_parsing = True

            if arg == '--all' or arg == '-a':
                for key in tests_dict:
                    tests_dict[key][0] = 1

    suite = unittest.TestSuite()

    for value in tests_dict.values():
        if value[0] == 1:
            suite.addTest(value[1])

    suite.run(None)

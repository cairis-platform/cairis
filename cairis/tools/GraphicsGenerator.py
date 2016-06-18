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

from cairis.tools.SVGGenerator import SVGGenerator

__author__ = 'Robin Quetin'

class GraphicsGenerator(object):
    def __init__(self, output_format='svg'):
        output_format = output_format.lower()
        if output_format == 'svg':
            self.ded_generator = SVGGenerator()
        else:
            raise RuntimeError('There is no generator registered for the provided output format.')

    def generate(self, dot_code, output_path=None, model_type=None):
        if output_path is None:
            return self.ded_generator.generate(dot_code, model_type)
        else:
            self.ded_generator.generate_file(dot_code, output_path, model_type)

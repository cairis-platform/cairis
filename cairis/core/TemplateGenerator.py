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

import mako.lookup
from mako.template import Template
from Borg import Borg
from cairis.templates.NavObject import NavObject

__author__ = 'Raf'
''' Tested using Mako 1.0.1 '''


class TemplateGenerator:
    def __init__(self):
        self.templates = dict()
        self.generate_base()

    def generate_base(self):
        file = NavObject("#", "File")
        file.setIcon("fa fa-file-o")
        levellist = list()
        levellist.append(NavObject("#", "File"))
        levellist.append(NavObject("#", "Open"))
        levellist.append(NavObject('#', "Save"))
        levellist.append(NavObject('#', "Export"))
        levellist.append(NavObject('#', "Documentation"))
        file.setmultilevel(levellist)

        req = NavObject("#", "Requirement Management")
        req.setIcon("fa fa-adjust")
        levellist = list()
        levellist.append(NavObject("#", "Commit"))
        levellist.append(NavObject("#", "Add"))
        levellist.append(NavObject('#', "Delete"))
        levellist.append(NavObject('#', "Domain Properties"))
        levellist.append(NavObject('#', "Goals"))
        levellist.append(NavObject('#', "Obstacles"))
        req.setmultilevel(levellist)

        risk = NavObject("#", "Risk Management")
        risk.setIcon("fa fa-exclamation")
        levellist = list()
        levellist.append(NavObject("#", "Roles"))
        levellist.append(NavObject("#", "Assets"))
        levellist.append(NavObject('#', "Class Associations"))
        levellist.append(NavObject('#', "Attackers"))
        levellist.append(NavObject('#', "Threats"))
        levellist.append(NavObject('#', "Vulnerabilities"))
        levellist.append(NavObject('#', "Risks"))
        levellist.append(NavObject('#', "Responses"))
        levellist.append(NavObject('#', "Countermeasures"))
        levellist.append(NavObject('#', "Security Patters"))
        risk.setmultilevel(levellist)

        iris = NavObject("#", "IRIS")
        iris.setIcon("fa fa-eye")
        levellist = list()
        levellist.append(NavObject("#", "Find"))
        levellist.append(NavObject("#", "Environments"))
        levellist.append(NavObject('#', "Personas"))
        levellist.append(NavObject('#', "Tasks"))
        levellist.append(NavObject('#', "External Documents"))
        levellist.append(NavObject('#', "Document References"))
        levellist.append(NavObject('#', "Concept References"))
        levellist.append(NavObject('#', "Persona Characteristics"))
        levellist.append(NavObject('#', "Task Characteristics"))
        iris.setmultilevel(levellist)

        eu = NavObject("#", "EUSTACE")
        eu.setIcon("fa fa-codepen")
        levellist = list()
        levellist.append(NavObject("#", "Internal Documents"))
        levellist.append(NavObject("#", "Codes"))
        levellist.append(NavObject('#', "Quotations"))
        levellist.append(NavObject('#', "Code Network"))
        levellist.append(NavObject('#', "Implied Processes"))
        eu.setmultilevel(levellist)

        options = NavObject("#", "Options")
        options.setIcon("fa fa-wrench")
        levellist = list()
        levellist.append(NavObject("#", "Asset Values"))
        levellist.append(NavObject("#", "Asset Types"))
        levellist.append(NavObject('#', "Access rights"))
        levellist.append(NavObject('#', "Protocols"))
        levellist.append(NavObject('#', "Privileges"))
        levellist.append(NavObject('#', "Surface Types"))
        levellist.append(NavObject('#', "Vulnerability Types"))
        levellist.append(NavObject('#', "Vulnerability Severities"))
        levellist.append(NavObject('#', "Capabilities"))
        levellist.append(NavObject('#', "Motivations"))
        levellist.append(NavObject('#', "Threat Types"))
        levellist.append(NavObject('#', "Threat Likelihoods"))
        levellist.append(NavObject('#', "Threat values"))
        levellist.append(NavObject('#', "Risk values"))
        levellist.append(NavObject('#', "Template Assets"))
        levellist.append(NavObject('#', "Template Requirements"))
        levellist.append(NavObject('#', "Countermeasure values"))
        options.setmultilevel(levellist)

        view = NavObject("#", "View")
        view.setIcon("fa fa-square-o")
        levellist = list()
        levellist.append(NavObject("#", "Risk Analysis"))
        levellist.append(NavObject("#", "Asset Model"))
        levellist.append(NavObject('#', "Goal Model"))
        levellist.append(NavObject('#', "Obstacle Model"))
        levellist.append(NavObject('#', "Responsibility Model"))
        levellist.append(NavObject('#', "Task Model"))
        levellist.append(NavObject('#', "Assumption Model"))
        levellist.append(NavObject('#', "Assumption Task Model"))
        levellist.append(NavObject('#', "Traceability"))
        view.setmultilevel(levellist)

        grid = NavObject("#", "Grid")
        grid.setIcon("fa fa-th")
        levellist = list()
        levellist.append(NavObject("#", "Requirements"))
        levellist.append(NavObject("#", "Goals"))
        levellist.append(NavObject('#', "Obstacles"))
        levellist.append(NavObject('#', "Relabel Objects"))
        grid.setmultilevel(levellist)

        help = NavObject("#", "Help")
        help.setIcon("fa fa-question")
        levellist = list()
        levellist.append(NavObject("#", "About"))
        help.setmultilevel(levellist)

        navList = list()
        navList.append(file)
        navList.append(req)
        navList.append(risk)
        navList.append(iris)
        navList.append(eu)
        navList.append(options)
        navList.append(view)
        navList.append(grid)
        navList.append(help)

        b = Borg()
        self.lookup = mako.lookup.TemplateLookup(directories=[b.templateDir], module_directory=b.templateDir)
        self.templates['index_page'] = self.lookup.get_template("index.mako")

    def prepare_message(self, message):
        """
        Converts regular text to HTML formatted text
        :type message: str
        """
        lines = message.split('\n')
        in_list = False

        for idx in range(0, len(lines)):
            line = lines[idx]
            if line.startswith('*'):
                line = line.lstrip('*').lstrip(' ')
                if not in_list:
                    in_list = True
                    line = '<ul>\n' + line
                line = '<li>' + line + '</li>'
                if idx == len(lines):
                    line = line + '\n</ul>'
            else:
                if in_list:
                    in_list = False
                    line = '</ul>\n' + line
                line = '<p>' + line + '</p>'
            lines[idx] = line

    def serve_result(self, template_name, **kwargs):
        # index.head.html (templatename) -> index_head (template_key)
        """
        :type template_name: str
        """
        if template_name.rfind('.mako') > -1:
            template_name[:template_name.rfind('.mako')]
        template_key = template_name.replace('.', '_')

        if not template_key in self.templates:
            template_name = template_name.replace('_', '.')
            template_name = template_name.rstrip('.')
            template_name += '.mako'
            self.templates[template_key] = self.lookup.get_template(template_name)

        return self.templates[template_key].render(**kwargs)

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

import os
from re import sub as substitute
from subprocess import check_output as cmd
from tempfile import mkstemp as make_tempfile
from xml.dom import minidom

__author__ = 'Robin Quetin'


class SVGGenerator(object):
    def __init__(self):
        self.extension = 'svg'

    def generate(self, dot_code, model_type):
        if not dot_code:
            dot_code = ''
        fd, temp_abspath = make_tempfile(suffix=self.extension)
        temp_file = open(temp_abspath, 'wb')
        temp_file.write(dot_code)
        temp_file.close()
        os.close(fd)
        output = cmd(['dot', '-Tsvg', temp_abspath])
        os.remove(temp_abspath)
        output = self.process_output(str(output), model_type)
        return output

    def generate_file(self, dot_code, output_file, model_type):
        output = self.generate(dot_code, model_type)

        try:
            fs_output = open(output_file, 'rb')
            fs_output.write(output)
            fs_output.close()
        except Exception, ex:
            fs_output.close()
            raise ex

    def process_output(self, output, model_type):
        lines = output.split('\n')
        svg_start = -1
        is_node = False

        for i in range(len(lines)):
            line = lines[i]
            if svg_start == -1:
                if lines[i].find('<svg') > -1:
                    svg_start = i

            if line.find('class="node"') > -1:
                is_node = True

            line = substitute("<!--.*?-->", "", line)
            if line.find('fill="none"') > -1 and is_node:
                line = line.replace('fill="none"', 'fill="white"')
                is_node = False

            line = correctHref(line, model_type)

            lines[i] = line

        if svg_start > -1:
            lines = lines[svg_start:]

        svg_text = '\n'.join(lines)
        svg_output = prettifySVG(svg_text)

        return svg_output

def correctHref(line, model_type):
    href_exists = -1
    href_exists = line.find('<a xlink:href="', href_exists+1)
    while href_exists > -1:
        start_index = line.find('"', href_exists)
        end_index = line.find('"', start_index+1)
        bracket_index = line.find('#', start_index+1)
        is_valid = start_index < bracket_index < end_index

        if is_valid:
            old_link = line[start_index+1:end_index]
            parts = old_link.split('#')
            type = parts[0]
            if type[-1] == 'y':
                type = type[:-1]+'ie'
            object = ''.join(parts[1:])
            if (model_type == 'goal' or model_type == 'risk') and type == 'requirement':
                new_link = '/api/{0}s/shortcode/{1}'.format(type, object)
            else:
                new_link = '/api/{0}s/name/{1}'.format(type, object)
            line = line.replace(old_link, new_link)

        href_exists = line.find('<a xlink:href="', href_exists+1)

    return line

def prettifySVG(svg_text):
    svg_doc = minidom.parseString(svg_text)
    svg_text = svg_doc.toprettyxml(indent='  ')
    svg_lines = svg_text.replace('\r\n', '\n').split('\n')
    svg_filtered = list()
    for svg_line in svg_lines:
        if svg_line.strip(' ').strip('\t') != '':
            svg_filtered.append(svg_line)

    return '\n'.join(svg_filtered[1:])

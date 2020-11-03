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

import sys
if (sys.version_info > (3,)):
  from urllib.parse import quote
else:
  from urllib import quote
import os
from re import sub as substitute
import base64
from subprocess import check_output as cmd
from tempfile import mkstemp as make_tempfile
from xml.dom import minidom
from cairis.core.Borg import Borg

__author__ = 'Robin Quetin, Shamal Faily'

class SVGGenerator(object):
  def __init__(self):
    self.extension = 'svg'

  def generate(self, dot_code, model_type, renderer = 'dot'):
    if not dot_code:
      dot_code = ''
    fd, temp_abspath = make_tempfile(suffix=self.extension)
    temp_file = open(temp_abspath, 'w')
    temp_file.write(dot_code)
    temp_file.close()
    os.close(fd)
    output = cmd([renderer, '-Tsvg', temp_abspath]).decode('utf-8')
    os.remove(temp_abspath)
    output = self.process_output(str(output), model_type)
    return output

  def generate_file(self, dot_code, output_file, model_type, renderer):
    output = self.generate(dot_code, model_type, renderer).decode('utf-8')
    fs_output = open(output_file, 'w')
    try:
      fs_output.write(output)
      fs_output.close()
    except Exception as ex:
      fs_output.close()
      raise ex

  def process_output(self, output, model_type):
    lines = output.split('\n')
    svg_start = -1
    is_node = False
    b = Borg()
    for i in range(len(lines)):
      line = lines[i]
      if svg_start == -1:
        if lines[i].find('<svg') > -1:
          svg_start = i

      if line.find('class="node"') > -1:
        is_node = True

      line = substitute(b.staticDir,"",line)
      line = substitute("<!--.*?-->", "", line)
      if line.find('fill="none"') > -1 and is_node:
        is_node = False

      line = correctHref(line, model_type)
      line = embedImage(line)
      line = correctTableLabel(line)

      lines[i] = line

    if svg_start > -1:
      lines = lines[svg_start:]

    svg_text = '\n'.join(lines)
    svg_output = prettifySVG(svg_text)

    return svg_output

def embedImage(line):
  if (line.find('<image') == 0):
    linkName = ''
    if (line.find('modelActor.png') >= 0):
      linkName = "/modelActor.png"
    elif (line.find('modelAttacker.png') >= 0):
      linkName = "/modelAttacker.png"
    elif (line.find('modelConflict.png') >= 0):
      linkName = "/modelConflict.png"
    elif (line.find('modelRole.png') >= 0):
      linkName = "/modelRole.png"
    else:
      raise Exception("No relevant image link found")
    b = Borg()
    imageName = b.assetDir + linkName
    with open(imageName, "rb") as image_file:
      encoded_string = base64.b64encode(image_file.read()).decode('ascii')
      line = line.replace('/assets/' + linkName,'data:image/png;base64,' + str(encoded_string))
  return line

def correctTableLabel(line):
  idx = line.find('&lt;TABLE')
  if (idx > 0):
    urlSegment = '/api/assets/name/'
    objtName = ''
    line = line[:idx] + objtName + '">'
  return line


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
      fromName = ''
      fromType = ''
      toName = ''
      toType = ''
      if (model_type == 'dataflow' and type == 'dataflow'):
        fromName = parts[2]
        fromType = parts[3]
        toName = parts[4]
        toType = parts[5]
        environment = parts[6]
      elif (model_type == 'control_structure' and type == 'dataflow'):
        environment = ''.join(parts[2:])
      else:
        object = ''.join(parts[1:])
      object = quote(parts[1])
      new_link = '/api/{0}/name/{1}'.format(type,object)
 
      if type == 'domainproperty':
        new_link = '/api/domainproperties/shortcode/{0}'.format(object)
               
      if (model_type == 'goal' or model_type == 'risk') and type == 'requirement':
        new_link = '/api/{0}s/shortcode/{1}'.format(type, object)
      elif (model_type == 'dataflow' and type == 'dataflow'):
        new_link = '/api/{0}s/name/{1}/from_name/{2}/from_type/{3}/to_name/{4}/to_type/{5}/environment/{6}'.format(type,object,quote(fromName),quote(fromType),quote(toName),quote(toType),quote(environment))
      elif (model_type == 'control_structure' and type == 'dataflow'):
        new_link = '/api/{0}s/name/{1}/environment/{2}'.format(type,object,quote(environment))
      elif (type == 'goalassociation'):
        assocParams = parts[1].split('/')
        new_link = '/api/goalassociations/environment/' + quote(assocParams[0]) + '/goal/' + quote(assocParams[1]) + '/subgoal/' + quote(assocParams[2])
      else:
        if type == 'grounds': 
          new_link = '/api/{0}/name/{1}'.format(type, object)
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

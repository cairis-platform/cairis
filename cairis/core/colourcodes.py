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




def threatColourCode(valueId):
  if (valueId == 9): return '359 1 .5'
  elif (valueId > 9): return '359 1 .5'
  elif (valueId == 8): return '359 1 .7'
  elif (valueId == 7): return '6 .86 .44'
  elif (valueId == 6): return '10 .7 .94'
  elif (valueId == 5): return '19 .65 .99'
  elif (valueId == 4): return '27 .48 .99'
  elif (valueId == 3): return '34 .38 .99'
  elif (valueId == 2): return '36 .21 1'
  elif (valueId == 1): return '37 .07 1'
  elif (valueId < 1): return '37 .07 1'

def responseColourCode(valueId):
  if (valueId == 1): return '359 1 .5'
  elif (valueId == 2): return '359 1 .7'
  elif (valueId == 3): return '6 .86 .44'
  elif (valueId == 4): return '10 .7 .94'
  elif (valueId == 5): return '19 .65 .99'
  elif (valueId == 6): return '27 .48 .99'
  elif (valueId == 7): return '34 .38 .99'
  elif (valueId == 8): return '36 .21 1'
  elif (valueId == 9): return '37 .07 1'
  elif (valueId > 9): return '37 .07 1'

def usabilityColourCode(valueId):
  if (valueId <= 1): return '#F7FBFF'
  elif (valueId == 2): return '#DEEBF7'
  elif (valueId == 3): return '#C6DBEF'
  elif (valueId == 4): return '#9ECAE1'
  elif (valueId == 5): return '#6BAED6'
  elif (valueId == 6): return '#4292C6'
  elif (valueId == 7): return '#2171B5'
  elif (valueId == 8): return '#08519C'
  elif (valueId == 9): return '#08306B'
  elif (valueId > 9): return '#08306B'

def obstacleColourCode(valueId):
  if (valueId <= 0.2): return '1'
  elif (valueId <= 0.3): return '2'
  elif (valueId <= 0.4): return '3'
  elif (valueId <= 0.5): return '4'
  elif (valueId <= 0.6): return '5'
  elif (valueId <= 0.7): return '6'
  elif (valueId <= 0.8): return '7'
  elif (valueId <= 0.9): return '8'
  else: return '9'

def riskTextColourCode(valueId):
  if (valueId >= 7): return 'white'
  else: return 'black'

def usabilityTextColourCode(valueId):
  if (valueId >= 7): return 'white'
  else: return 'black'

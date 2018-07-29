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

__author__ = 'Shamal Faily'


class ARMException(Exception):
  def __init__(self,value): self.value = value
  def __str__(self): return repr(self.value)

class EnvironmentValidationError(ARMException):
  def __init__(self,value): ARMException.__init__(self,value)

class ObjectNotFound(ARMException):
  def __init__(self,value): ARMException.__init__(self,value)

class DatabaseProxyException(ARMException):
  def __init__(self,value): ARMException.__init__(self,value)

class IntegrityException(DatabaseProxyException):
  def __init__(self,value): ARMException.__init__(self,value)

class RequirementDoesNotExist(ARMException):
  def __init__(self,value): ARMException.__init__(self,value)

class UnknownParameterClass(ARMException):
  def __init__(self,value): ARMException.__init__(self,value)

class UnknownPanelClass(ARMException):
  def __init__(self,value): ARMException.__init__(self,value)

class UnknownNodeType(ARMException):
  def __init__(self,value): ARMException.__init__(self,value)

class UnknownDialogClass(ARMException):
  def __init__(self,value): ARMException.__init__(self,value)

class UnknownOperatingSystem(ARMException):
  def __init__(self,value): ARMException.__init__(self,value)

class ConflictingType(ARMException):
  def __init__(self,value): ARMException.__init__(self,value)

class SessionNotFound(ARMException):
  def __init__(self,value): ARMException.__init__(self,'Session not found')

class AttributeTooBig(ARMException):
  def __init__(self,value): ARMException.__init__(self,value)

class NoImpliedCharacteristic(Exception):
  def __init__(self,pName,fromCode,toCode,rtName):
    self.thePersonaName = pName
    self.theFromCode = fromCode
    self.theToCode = toCode
    self.theRTName = rtName

  def persona(self): return self.thePersonaName
  def fromCode(self): return self.theFromCode
  def toCode(self): return self.theToCode
  def rType(self): return self.theRTName
  def __str__(self):  return repr(self.thePersonaName + '/' + self.theFromCode + '/' + self.theToCode + '/' + self.theRTName)

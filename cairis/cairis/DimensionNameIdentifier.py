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


import ARM

def dimensionName(className):
  if (className == 'AttackersDialog'):  return 'attacker'
  if (className == 'AssetsDialog'): return 'asset'
  if (className == 'TemplateAssetsDialog'): return 'template_asset'
  if (className == 'TemplateRequirementsDialog'): return 'template_requirement'
  if (className == 'SecurityPatternsDialog'): return 'securitypattern'
  if (className == 'ComponentViewsDialog'): return 'component_view'
  if (className == 'ClassAssociationsDialog'): return 'classassociation'
  if (className == 'GoalAssociationsDialog'): return 'goalassociation'
  if (className == 'GoalsDialog'): return 'goal'
  if (className == 'ObstaclesDialog'): return 'obstacle'
  if (className == 'ThreatsDialog'): return 'threat'
  if (className == 'VulnerabilitiesDialog'): return 'vulnerability'
  if (className == 'RisksDialog'): return 'risk'
  if (className == 'ResponsesDialog'): return 'response'
  if (className == 'CountermeasuresDialog'): return 'countermeasure'
  if (className == 'TracesDialog'): return 'trace'
  if (className == 'TasksDialog'): return 'task'
  if (className == 'UseCasesDialog'): return 'usecase'
  if (className == 'PersonasDialog'): return 'persona'
  if (className == 'EnvironmentsDialog'): return 'environment'
  if (className == 'RolesDialog'): return 'role'
  if (className == 'ResponsibilitiesDialog'): return 'responsibility'
  if (className == 'DomainPropertiesDialog'): return 'domainproperty'
  if (className == 'DomainsDialog'): return 'domain'
  if (className == 'ValueTypesDialog'): return 'value_type'
  if (className == 'DependenciesDialog'): return 'dependencyassociation'
  if (className == 'ExternalDocumentsDialog'): return 'external_document'
  if (className == 'InternalDocumentsDialog'): return 'internal_document'
  if (className == 'CodesDialog'): return 'code'
  if (className == 'DocumentReferencesDialog'): return 'document_reference'
  if (className == 'PersonaCharacteristicsDialog'): return 'persona_characteristic'
  if (className == 'TaskCharacteristicsDialog'): return 'task_characteristic'
  if (className == 'BehaviouralCharacteristicsDialog'): return 'persona_characteristic'
  if (className == 'ConceptReferencesDialog'): return 'concept_reference'
  raise ARM.UnknownDialogClass(className)

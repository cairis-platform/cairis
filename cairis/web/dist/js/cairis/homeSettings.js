/*  Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.

    Authors: Shamal Faily */

'use strict';

$("#homeClick").click(function () {
  refreshHomeBreadCrumb();
});

$("#homeBCClick").click(function () {
  refreshHomeBreadCrumb();
});

$('#menuBCClick').click(function() {
  refreshMenuBreadCrumb($(this).attr('dimension'));
});

function refreshHomeBreadCrumb() {
  $('#BC').hide();
  summaryTables();
}

function refreshMenuBreadCrumb(dimName) {
  $('#BC').show();
  $('#homeBCClick').show();
  $('#objtBCClick').hide();
  if (dimName == 'documentation') {
    $('#menuBCClick').text('Documentation');
    $('#menuBCClick').show();
    showDocumentationForm();
  }
  else if (dimName == 'properties') {
    $('#menuBCClick').text('Properties');
    $('#menuBCClick').show();
    showProjectSettingsForm();
  }
  else if (dimName == 'asset') {
    $('#menuBCClick').text('Assets');
    $('#menuBCClick').show();
    fillAssetTable();
  }
  else if (dimName == 'requirement') {
    $('#menuBCClick').text('Requirements');
    $('#menuBCClick').show();
    requirementsTable();
  }
  else if (dimName == 'domain_property') {
    $('#menuBCClick').text('Domain Properties');
    $('#menuBCClick').show();
    createDomainPropertiesTable();
  }
  else if (dimName == 'goal') {
    $('#menuBCClick').text('Goals');
    $('#menuBCClick').show();
    createEditGoalsTable();
  }
  else if (dimName == 'obstacle') {
    $('#menuBCClick').text('Obstacles');
    $('#menuBCClick').show();
    createEditObstaclesTable();
  }
  else if (dimName == 'use_case') {
    $('#menuBCClick').text('Use Cases');
    $('#menuBCClick').show();
    createUseCasesTable();
  }
  else if (dimName == 'dependency') {
    $('#menuBCClick').text('Dependencies');
    $('#menuBCClick').show();
    createDependenciesTable();
  }
  else if (dimName == 'dataflow') {
    $('#menuBCClick').text('Dataflows');
    $('#menuBCClick').show();
    createDataflowsTable();
  }
  else if (dimName == 'architectural_pattern') {
    $('#menuBCClick').text('Architectural Patterns');
    $('#menuBCClick').show();
    createArchitecturalPatternsTable();
  }
  else if (dimName == 'attacker') {
    $('#menuBCClick').text('Attackers');
    $('#menuBCClick').show();
    createAttackersTable();
  }
  else if (dimName == 'vulnerability') {
    $('#menuBCClick').text('Vulnerabilities');
    $('#menuBCClick').show();
    createVulnerabilityTable();
  }
  else if (dimName == 'threat') {
    $('#menuBCClick').text('Threats');
    $('#menuBCClick').show();
    createThreatsTable();
  }
  else if (dimName == 'risk') {
    $('#menuBCClick').text('Risks');
    $('#menuBCClick').show();
    createRisksTable();
  }
  else if (dimName == 'response') {
    $('#menuBCClick').text('Responses');
    $('#menuBCClick').show();
    createResponsesTable();
  }
  else if (dimName == 'countermeasure') {
    $('#menuBCClick').text('Countermeasures');
    $('#menuBCClick').show();
    createCountermeasuresTable();
  }
  else if (dimName == 'security_pattern') {
    $('#menuBCClick').text('Security Patterns');
    $('#menuBCClick').show();
    createSecurityPatternsTable();
  }
  else if (dimName == 'task') {
    $('#menuBCClick').text('Tasks');
    $('#menuBCClick').show();
    createTasksTable();
  }
  else if (dimName == 'persona') {
    $('#menuBCClick').text('Personas');
    $('#menuBCClick').show();
    createPersonasTable();
  }
  else if (dimName == 'external_document') {
    $('#menuBCClick').text('External Documents');
    $('#menuBCClick').show();
    createExternalDocumentsTable();
  }
  else if (dimName == 'document_reference') {
    $('#menuBCClick').text('Document References');
    $('#menuBCClick').show();
    createDocumentReferencesTable();
  }
  else if (dimName == 'persona_characteristic') {
    $('#menuBCClick').text('Persona Characteristics');
    $('#menuBCClick').show();
    createPersonaCharacteristicsTable();
  }
  else if (dimName == 'role') {
    $('#menuBCClick').text('Roles');
    $('#menuBCClick').show();
    fillRolesTable();
  }
  else if (dimName == 'environment') {
    $('#menuBCClick').text('Environments');
    $('#menuBCClick').show();
    createEnvironmentsTable();
  }
  else if (dimName == 'task_characteristic') {
    $('#menuBCClick').text('Task Characteristics');
    $('#menuBCClick').show();
    createTaskCharacteristicsTable();
  }
  else if (dimName == 'location') {
    $('#menuBCClick').text('Locations');
    $('#menuBCClick').show();
    createLocationsTable();
  }
  else if (dimName == 'model') {
    $('#menuBCClick').hide();
  }
}

function refreshObjectBreadCrumb(bcLabel) {
  $('#objtBCClick').text(bcLabel);
  $('#objtBCClick').show();
}

$('#summaryenvironmentsbox').change(function() {
  var envName = $(this).find('option:selected').val();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/summary/dimension/vulnerability/environment/" + encodeURIComponent(envName),
    success: function (sums) {
      nv.addGraph(function() {
        var chart = nv.models.pieChart()
          .x(function(d) { return d.theLabel })
          .y(function(d) { return d.theValue })
          .showLabels(true);
        d3.select("#vulnerabilitySummary svg")
          .datum(sums)
          .transition().duration(1200)
          .call(chart);
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/summary/dimension/threat/environment/" + encodeURIComponent(envName),
    success: function (sums) {
      nv.addGraph(function() {
        var chart = nv.models.pieChart()
          .x(function(d) { return d.theLabel })
          .y(function(d) { return d.theValue })
          .showLabels(true);
        d3.select("#threatSummary svg")
          .datum(sums)
          .transition().duration(1200)
          .call(chart);
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/summary/dimension/risk/environment/" + encodeURIComponent(envName),
    success: function (sums) {
      nv.addGraph(function() {
        var chart = nv.models.pieChart()
          .x(function(d) { return d.theLabel })
          .y(function(d) { return d.theValue })
          .showLabels(true);
        d3.select("#riskSummary svg")
          .datum(sums)
          .transition().duration(1200)
          .call(chart);
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

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

    Authors: Raf Vandelaer, Shamal Faily */

'use strict';

//  Function for adding a row to the table
$("#addReq").click(function() {
  addReq();
});

function addReq() {

  var kind  = "";

  if($( "#assetsbox").find("option:selected" ).text() == "All" && $( "#environmentsbox").find("option:selected" ).text() == "All"){
    alert("Please select an asset or an environment");
  }
  else{
    if($( "#assetsbox").find("option:selected" ).text() != ""){
      kind = "asset:" + $( "#assetsbox").find("option:selected" ).text();
    }
    else{
      kind = "environment:"+$( "#environmentsbox").find("option:selected" ).text();
    }
    var template = "";
    var num = findLabel();

    template = '<tr class="' + kind + '">' +
               '<td name="theLabel">' + num + '</td>' +
               '<td name="theName" contenteditable="true"></td>'+
               '<td name="theDescription" contenteditable="true"></td>'+
               "<td name='thePriority' class='reqCombo' contenteditable='true'><select class='form-control'><option value='1' selected>1</option><option value='2'>2</option value='3'><option>3</option></select></td>'"+
               '<td name="rationale" contenteditable="true">None</td>'+
               '<td name="fitCriterion" contenteditable="true">None</td>'+
               '<td name="originator" contenteditable="true"></td>'+
               "<td name='type' class='reqCombo' contenteditable='true'><select class='form-control'><option value='Functional' selected>Functional</option><option value='Data'>Data</option><option value='Look and Feel'>Look and Feel</option><option value='Usability'>Usability</option><option value='Performance'>Performance</option><option value='Operational'>Operational</option><option value='Operational'>Operational</option><option value='Maintainability'>Maintainability</option><option value='Portability'>Portability</option><option value='Security'>Security</option><option value='Cultural and Political'>Cultural and Political</option><option value='Legal'>Legal</option><option value='Privacy'>Privacy</option></select></td>"+
               '</tr>';
    $("#mainTable").append(template);
    $('#mainTable').find('tbody').find('tr').last().addClass(kind);
    sortTableByRow(0);
  }
}

// Removing the active tr
$("#removeReq").click(function() {
  removeReq();
});

$("#removeReqMenu").click(function() {
  removeReq();
});



function removeReq(reqName) {
  deleteObject('requirement',reqName,function(reqName) {
    var ursl = serverIP + "/api/requirements/name/" + reqName.replace(' ',"%20");
    var object = {};
    object.session_id= $.session.get('sessionID');
    var objectoutput = JSON.stringify(object);

    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      data: objectoutput,
      crossDomain: true,
      url: ursl,
      success: function (data) {
        $("tr").eq(getActiveindex()).detach();
        var refName = $('#assetsbox').val()
        if (refName != null) {
          updateAssetRequirementsTable(refName);
        }
        else {
          updateEnvironmentRequirementsTable(refName);
        }
        showPopup(true);
//        sortTableByRow(0);
      },
      error: function (xhr, textStatus, errorThrown) {
        var error = JSON.parse(xhr.responseText);
        showPopup(false, String(error.message));
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  });
}

$("#requirementsClick").click(function(){
  validateClick('requirement',function() {
    $('#menuBCClick').attr('dimension','requirement');
    refreshMenuBreadCrumb('requirement');
  });
});

//Just for debugLogger
$("#testingButton").click(function(){
   showPopup(true);
});

//For debugLogger
$("#removesessionButton").click(function() {
  $.session.remove('sessionID');
  location.reload();
});

$("#gridGoals").click(function() {
  setTableHeader("Goals");
});

$("#gridObstacles").click(function() {
  setTableHeader("Obstacles");
});


$('#assetModelClick').click(function(){
  window.theVisualModel = 'asset';
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/all/names",
    success: function (data) {
      $("#chooseEnvironmentSelect").empty();
      $.each(data, function(i, item) {
        $("#chooseEnvironmentSelect").append('<option value="' + item + '">'  + item + '</option>');
      });
      $('#chooseEnvironment').attr('data-chooseDimension',"environment");
      $('#chooseEnvironment').attr('data-applyEnvironmentSelection',"viewAssetModel");
      $('#chooseEnvironment').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
});

function viewAssetModel() {
  $('#menuBCClick').attr('dimension','model');
  refreshMenuBreadCrumb('model');
  var envName = $('#chooseEnvironment').attr('data-chosenDimension');
  refreshDimensionSelector($('#amenvironmentsbox'),'environment',undefined,function() {
    refreshDimensionSelector($('#amassetsbox'),'asset',envName,function() {
      $('#amenvironmentsbox').val(envName);
      getAssetview(envName);
    });
  });
}


$('#dataflowDiagramClick').click(function(){
  window.theVisualModel = 'dataflow';
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/all/names",
    success: function (data) {
      $("#chooseEnvironmentSelect").empty();
      $.each(data, function(i, item) {
        $("#chooseEnvironmentSelect").append('<option value="' + item + '">'  + item + '</option>');
      });
      $('#chooseEnvironment').attr('data-chooseDimension',"environment");
      $('#chooseEnvironment').attr('data-applyEnvironmentSelection',"viewDataFlowDiagram");
      $('#chooseEnvironment').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
});


function viewDataFlowDiagram() {
  $('#menuBCClick').attr('dimension','model');
  refreshMenuBreadCrumb('model');
  var envName = $('#chooseEnvironment').attr('data-chosenDimension');

  refreshDimensionSelector($('#dfdenvironmentbox'),'environment',undefined,function() {
    $('#dfdenvironmentbox').val(envName);
    refreshDimensionSelector($('#dfdfilterbox'),'dfd_filter',envName,function() {
      $('#dfdfilterbox').val('All');
      getDataFlowDiagram(envName,'None');
    });
  });
}


$('#architecturalPatternModelClick').click(function(){
  window.theVisualModel = 'architectural_pattern';
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/component_view",
    success: function (data) {
      $("#chooseEnvironmentSelect").empty();
      $("#aparchitecturalpatternsbox").empty();
      $.each(data, function(i, item) {
        $("#chooseEnvironmentSelect").append('<option value="' + item + '">'  + item + '</option>');
        $("#aparchitecturalpatternsbox").append('<option value="' + item + '">'  + item + '</option>');
      });
      $('#chooseEnvironment').attr('data-chooseDimension',"architectural pattern")
      $('#chooseEnvironment').attr('data-applyEnvironmentSelection',"getArchitecturalPatternView")
      $('#chooseEnvironment').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$('#misusabilityModelClick').click(function(){
  $('#menuBCClick').attr('dimension','model');
  refreshMenuBreadCrumb('model');
  window.theVisualModel = 'misusability';
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/misusability_case",
    success: function (data) {
      $("#chooseEnvironmentSelect").empty();
      $("#mmmisusabilitycasesbox").empty();
      $.each(data, function(i, item) {
        $("#chooseEnvironmentSelect").append('<option value="' + item + '">'  + item + '</option>');
        $("#mmmisusabilitycasesbox").append('<option value="' + item + '">'  + item + '</option>');
      });
      $('#chooseEnvironment').attr('data-chooseDimension',"misusability case")
      $('#chooseEnvironment').attr('data-applyEnvironmentSelection',"getMisusabilityView")
      $('#chooseEnvironment').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});



$('#goalModelClick').click(function(){
  window.theVisualModel = 'goal';
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/all/names",
    success: function (data) {
      $("#chooseEnvironmentSelect").empty();
      $.each(data, function(i, item) {
        $("#chooseEnvironmentSelect").append('<option value="' + item + '">'  + item + '</option>');
      });
      $('#chooseEnvironment').attr('data-chooseDimension',"environment")
      $('#chooseEnvironment').attr('data-applyEnvironmentSelection',"viewGoalModel")
      $('#chooseEnvironment').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
});

function viewGoalModel() {
  var envName = $('#chooseEnvironment').attr('data-chosenDimension');
  refreshDimensionSelector($('#gmenvironmentsbox'),'environment',undefined,function() {
    refreshDimensionSelector($('#gmgoalbox'),'goal',envName,function() {
      refreshDimensionSelector($('#gmusecasebox'),'usecase',envName,function() {
        $('#gmenvironmentsbox').val(envName);
        getGoalview(envName,'All','All');
      });
    });
  });
}

$('#responsibilityModelClick').click(function(){
  window.theVisualModel = 'responsibility';
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/all/names",
    success: function (data) {
      $("#chooseEnvironmentSelect").empty();
      $.each(data, function(i, item) {
        $("#chooseEnvironmentSelect").append('<option value="' + item + '">'  + item + '</option>');
      });
      $('#chooseEnvironment').attr('data-chooseDimension',"environment")
      $('#chooseEnvironment').attr('data-applyEnvironmentSelection',"viewResponsibilityModel")
      $('#chooseEnvironment').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

function viewResponsibilityModel() {
  var envName = $('#chooseEnvironment').attr('data-chosenDimension');
  refreshDimensionSelector($('#remenvironmentsbox'),'environment',undefined,function() {
    refreshDimensionSelector($('#remrolebox'),'role',envName,function() {
      $('#remenvironmentsbox').val(envName);
      getResponsibilityview(envName,'All');
    });
  });
}


$('#obstacleModelClick').click(function(){
  window.theVisualModel = 'obstacle';
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/all/names",
    success: function (data) {
      $("#chooseEnvironmentSelect").empty();
      $.each(data, function(i, item) {
        $("#chooseEnvironmentSelect").append('<option value="' + item + '">'  + item + '</option>');
      });
      $('#chooseEnvironment').attr('data-chooseDimension',"environment")
      $('#chooseEnvironment').attr('data-applyEnvironmentSelection',"viewObstacleModel")
      $('#chooseEnvironment').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

function viewObstacleModel() {
  var envName = $('#chooseEnvironment').attr('data-chosenDimension');
  refreshDimensionSelector($('#omenvironmentsbox'),'environment',undefined,function() {
    refreshDimensionSelector($('#omobstaclebox'),'obstacle',envName,function() {
      $('#omenvironmentsbox').val(envName);
      getObstacleview(envName,'All');
    });
  });
}

$('#riskModelClick').click(function(){
  window.theVisualModel = 'risk';
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/all/names",
    success: function (data) {
      $("#chooseEnvironmentSelect").empty();
      $.each(data, function(i, item) {
        $("#chooseEnvironmentSelect").append('<option value="' + item + '">'  + item + '</option>');
      });
      $('#chooseEnvironment').attr('data-chooseDimension',"environment")
      $('#chooseEnvironment').attr('data-applyEnvironmentSelection',"viewRiskModel")
      $('#chooseEnvironment').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

function viewRiskModel() {
  var envName = $('#chooseEnvironment').attr('data-chosenDimension');
  refreshDimensionSelector($('#rmenvironmentsbox'),'environment',undefined,function() {
    refreshSpecificSelector($('#rmobjectbox'),'/api/risks/model/environment/' + encodeURIComponent(envName) + '/names',function() {
      $('#rmenvironmentsbox').val(envName);
      getRiskview(envName,'all','all','Hierarchical');
    },['All']);
  });
}

$('#requirementModelClick').click(function(){
  window.theVisualModel = 'requirement';
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/all/names",
    success: function (data) {
      $("#chooseEnvironmentSelect").empty();
      $.each(data, function(i, item) {
        $("#chooseEnvironmentSelect").append('<option value="' + item + '">'  + item + '</option>');
      });
      $('#chooseEnvironment').attr('data-chooseDimension',"environment")
      $('#chooseEnvironment').attr('data-applyEnvironmentSelection',"viewRequirementModel")
      $('#chooseEnvironment').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

function viewRequirementModel() {
  var envName = $('#chooseEnvironment').attr('data-chosenDimension');
  refreshDimensionSelector($('#cmenvironmentsbox'),'environment',undefined,function() {
    refreshDimensionSelector($('#cmrequirementsbox'),'requirement',envName,function() {
      $('#cmenvironmentsbox').val(envName);
      getRequirementView(envName,'All');
    });
  });
}


$('#taskModelClick').click(function(){
  window.theVisualModel = 'task';
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/all/names",
    success: function (data) {
      $("#chooseEnvironmentSelect").empty();
      $.each(data, function(i, item) {
        $("#chooseEnvironmentSelect").append('<option value="' + item + '">'  + item + '</option>');
      });
      $('#chooseEnvironment').attr('data-chooseDimension',"environment")
      $('#chooseEnvironment').attr('data-applyEnvironmentSelection',"viewTaskModel")
      $('#chooseEnvironment').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

function viewTaskModel() {
  var envName = $('#chooseEnvironment').attr('data-chosenDimension');
  refreshDimensionSelector($('#tmenvironmentsbox'),'environment',undefined,function() {
    refreshDimensionSelector($('#tmtaskbox'),'task',envName,function() {
      refreshDimensionSelector($('#tmmisusecasebox'),'misusecase',envName,function() {
        $('#tmenvironmentsbox').val(envName);
        getTaskview(envName,'All','All');
      });
    });
  });
}

// When personaview is clicked
$('#personaModelClick').click(function(){
  window.theVisualModel = 'persona';
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/personas/all/names",
    success: function (data) {
      $("#chooseEnvironmentSelect").empty();
      $.each(data, function(i, item) {
        $("#chooseEnvironmentSelect").append('<option value="' + item + '">'  + item + '</option>');
      });
      $('#chooseEnvironment').attr('data-chooseDimension',"persona")
      $('#chooseEnvironment').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$('#locationsModelClick').click(function(){
  window.theVisualModel = 'locations';
  $('#chooseLocationsEnvironmentDialog').modal('show');
});

$("#chooseLocationsEnvironmentDialog").on('shown.bs.modal', function() {
  refreshDimensionSelector($('#chooseLEEnvironmentsSelector'),'environment',undefined,function() {
    refreshDimensionSelector($('#chooseLELocationsSelector'),'locations');
  });
});

$("#chooseLocationsEnvironmentDialog").on('click', '#chooseLocationEnvironmentButton',function(e) {

  var locsName = $('#chooseLELocationsSelector').val();
  var envName = $('#chooseLEEnvironmentsSelector').val();
  $('#chooseLocationsEnvironmentDialog').modal('hide');
  getLocationsView(locsName,envName);
});



$("#newClick").click(function () {
  showLoading();
  postNewProject(function () {
    refreshHomeBreadCrumb();
  });
});

//This is delegation
var mainContent = $('#objectViewer');
mainContent.on('contextmenu', '.clickable-environments', function(){
  return false;
});



$("#mainTable").on("click", "td", function() {
  $('#mainTable tr').eq(getActiveindex()).find('td:first').focus();
});


$(document).on('click', "button.deletePersonaButton",function(){
  var name = $(this).attr("value");
  $.ajax({
    type: "DELETE",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID')),
      name: name
    },
    crossDomain: true,
    url: serverIP + "/api/persona/name/" + name,
    success: function (data) {
      $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
          session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + "/api/personas",
        success: function (data) {
          setTableHeader("Personas");
          createPersonasTable(data, function(){
            newSorting(1);
          });
          activeElement("mainTable");
        },
        error: function (xhr, textStatus, errorThrown) {
          debugLogger(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

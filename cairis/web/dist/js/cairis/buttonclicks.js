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

$("#addReqMenu").click(function() {
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
    switch (window.activeTable) {
      case "Requirements":
        template = '<tr class="' + kind + '">' +
                   '<td name="theLabel">' + num + '</td>' +
                   '<td name="theName" contenteditable="true"></td>'+
                   '<td name="theDescription" contenteditable="true"></td>'+
                   '<td name="thePriority" contenteditable="true">1</td>'+
                   '<td name="theId" style="display:none;"></td>'+
                   '<td name="theVersion" style="display:none;"></td>'+
                   '<td name="rationale" contenteditable="true">None</td>'+
                   '<td name="fitCriterion" contenteditable="true">None</td>'+
                   '<td name="originator" contenteditable="true"></td>'+
                   '<td name="type" contenteditable="true">Functional</td>'+
                   '</tr>';
        break;
      case "Goals":
        template = '<tr><td name="theLabel">' + num + '</td><td name="theName" contenteditable="true" ></td><td name="theDefinition" contenteditable="true"></td><td name="theCategory" contenteditable="true">Maintain</td><td name="thePriority" contenteditable="true">Low</td><td name="theId" style="display:none;"></td><td name="fitCriterion" contenteditable="true" >None</td><td  name="theIssue" contenteditable="true">None</td><td name="originator" contenteditable="true"></td></tr>';
        break;
      case "Obstacles":
        template = '<tr><td name="theLabel">' + num + '</td><td name="theName" contenteditable="true">Name</td><td name="theDefinition" contenteditable="true">Definition</td><td name="theCategory" contenteditable="true">Category</td><td name="theId" style="display:none;"></td><td name="originator" contenteditable="true">Originator</td></tr>';
        break;
    }
    $("#reqTable").append(template);
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
    if(window.activeTable =="Requirements"){
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
          showPopup(true);
          sortTableByRow(0);
        },
        error: function (xhr, textStatus, errorThrown) {
          var error = JSON.parse(xhr.responseText);
          showPopup(false, String(error.message));
          debugLogger(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    }
  });
}

$("#requirementsClick").click(function(){
  window.activeTable = "Requirements";
  startingTable();
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
  window.activeTable = "Goals";
  setTableHeader();
});
//gridObstacles
$("#gridObstacles").click(function() {
  window.activeTable = "Obstacles";
  setTableHeader();
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
      $("#comboboxDialogSelect").empty();
      $.each(data, function(i, item) {
        $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>")
      });
      $( "#comboboxDialog" ).dialog({
        modal: true,
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
            getAssetview($( "#comboboxDialogSelect").find("option:selected" ).text());
          }
        }
      });
      $(".comboboxD").css("visibility","visible");
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
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
      $("#comboboxDialogSelect").empty();
      $.each(data, function(i, item) {
        $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>")
      });
      $( "#comboboxDialog" ).dialog({
        modal: true,
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
            getGoalview($( "#comboboxDialogSelect").find("option:selected" ).text());
          }
        }
      });
      $(".comboboxD").css("visibility","visible");
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
});

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
      $("#comboboxDialogSelect").empty();
      $.each(data, function(i, item) {
        $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>")
      });
      $( "#comboboxDialog" ).dialog({
        modal: true,
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
            getResponsibilityview($( "#comboboxDialogSelect").find("option:selected" ).text());
          }
        }
      });
      $(".comboboxD").css("visibility","visible");
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

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
      $("#comboboxDialogSelect").empty();
      $.each(data, function(i, item) {
        $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>")
      });
      $( "#comboboxDialog" ).dialog({
        modal: true,
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
            getObstacleview($( "#comboboxDialogSelect").find("option:selected" ).text());
          }
        }
      });
      $(".comboboxD").css("visibility","visible");
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

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
      $("#comboboxDialogSelect").empty();
      $.each(data, function(i, item) {
        $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>")
      });
      $( "#comboboxDialog" ).dialog({
        modal: true,
        position: {my: 'center', at: 'center', collision: 'fit'},
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
            getRiskview($( "#comboboxDialogSelect").find("option:selected" ).text());
          }
        }
      });
      $(".comboboxD").css("visibility","visible");
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});


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
      $("#comboboxDialogSelect").empty();
      $.each(data, function(i, item) {
        $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>")
      });
      $( "#comboboxDialog" ).dialog({
        modal: true,
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
            getTaskview($( "#comboboxDialogSelect").find("option:selected" ).text());
          }
        }
      });
      $(".comboboxD").css("visibility","visible");
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

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
      $("#comboboxDialogSelect").empty();
      $("#appersonasbox").empty();
      $.each(data, function(i, item) {
        $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>")
        $("#appersonasbox").append("<option value=" + item + ">"  + item + "</option>")
      });
      $( "#comboboxDialog" ).dialog({
        modal: true,
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
            var pName = $( "#comboboxDialogSelect").find("option:selected" ).text();
            appendPersonaCharacteristics(pName,'All','All');
            getPersonaView(pName,'All','All');
          }
        }
      });
      $(".comboboxD").css("visibility","visible");
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$('#locationsModelClick').click(function(){
  window.theVisualModel = 'locations';
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/locations",
    success: function (data) {
      $("#comboboxDialogSelect").empty();
      $.each(data, function(i, item) {
        $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>");
      });
      $( "#comboboxDialog" ).dialog({
        modal: true,
        buttons: {
          Ok: function() {
            var locsName = $( "#comboboxDialogSelect").find("option:selected" ).text();
            $( this ).dialog( "close" );
            $.ajax({
              type: "GET",
              dataType: "json",
              accept: "application/json",
              data: {
                session_id: String($.session.get('sessionID'))
              },
              crossDomain: true,
              url: serverIP + "/api/dimensions/table/environment",
              success: function (data) {
                $("#comboboxDialogSelect").empty();
                $.each(data, function(i, item) {
                  $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>");
                });
                $( "#comboboxDialog" ).dialog({
                  modal: true,
                  buttons: {
                    Ok: function() {
                      var envName = $( "#comboboxDialogSelect").find("option:selected" ).text();
                      $( this ).dialog( "close" );
                      getLocationsView(locsName,envName);
                    }
                  }
                });
                $(".comboboxD").css("visibility","visible");
              },
              error: function (xhr, textStatus, errorThrown) {
                debugLogger(String(this.url));
                debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
              }
            });
          }
        }
      });
      $(".comboboxD").css("visibility","visible");
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$("#newClick").click(function () {
  postNewProject(function () {
    window.activeTable = "Requirements";
    startingTable();
  });
});

//This is delegation
var mainContent = $('#objectViewer');
mainContent.on('contextmenu', '.clickable-environments', function(){
  return false;
});



$("#reqTable").on("click", "td", function() {
  if(window.activeTable == "Requirements"){
  }
  $('#reqTable tr').eq(getActiveindex()).find('td:first').focus();
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
          window.activeTable = "Personas";
          setTableHeader();
          createPersonasTable(data, function(){
            newSorting(1);
          });
          activeElement("reqTable");
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

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

$("#taskCharacteristicsClick").click(function(){
  clearLocalStorage($('#menuBCClick').attr('dimension'));
  $("#objectViewer").empty();
  $('#menuBCClick').attr('dimension','task_characteristic');
  refreshMenuBreadCrumb('task_characteristic');
});

function createTaskCharacteristicsTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/task_characteristics",
    success: function (data) {
      setTableHeader("TaskCharacteristics");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      for (var key in data) {
        var item = data[key];
        textToInsert[i++] = "<tr>";

        textToInsert[i++] = '<td class="deleteTaskCharacteristicButton"><i class="fa fa-minus" value="' + item.theTaskName + '"></i></td>';
        textToInsert[i++] = '<td class="taskcharacteristic-rows" name="theName">';
        textToInsert[i++] = item.theTaskName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="taskcharacteristic-rows" name="theCharacteristic">';
        textToInsert[i++] = item.theCharacteristic;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      }

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
      $("#mainTable").find("tbody").removeClass();

      activeElement("mainTable");
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

$(document).on('click', "td.taskcharacteristic-rows", function () {
  activeElement("objectViewer");
  var name = $(this).closest("tr").find("td:eq(2)").text();
  refreshObjectBreadCrumb(name);
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/task_characteristics/name/" + encodeURIComponent(name),
    success: function (data) {
      fillOptionMenu("fastTemplates/editTaskCharacteristicOptions.html", "#objectViewer", null, true, true, function () {
        $.ajax({
          type: "GET",
          dataType: "json",
          accept: "application/json",
          data: {
            session_id: String($.session.get('sessionID'))
          },
          crossDomain: true,
          url: serverIP + "/api/dimensions/table/task",
          success: function (tNames) {
            var taskSelect = $('#theTaskName');
            $.each(tNames, function (index,tName) {
              taskSelect.append($("<option></option>").attr("value",tName).text(tName));
            });
            $("#UpdateTaskCharacteristic").text("Update");
            $.session.set("TaskCharacteristic", JSON.stringify(data));
            taskSelect.val(data.theTaskName);
            $("#theModQual").val(data.theModQual);
            $("#theCharacteristic").val(data.theCharacteristic);
     
            $("#theGrounds").find("tbody").empty();
            $.each(data.theGrounds,function(idx,item) {
              appendTaskGWR("#theGrounds",'ground',item); 
            }); 

            $("#theWarrant").find("tbody").empty();
            $.each(data.theWarrant,function(idx,item) {
              appendTaskGWR("#theWarrant",'warrant',item); 
            });
            $("#theRebuttal").find("tbody").empty();
            $.each(data.theRebuttal,function(idx,item) {
              appendTaskGWR("#theRebuttal",'rebuttal',item); 
            });
            $("#theBacking").find("tbody").empty();
            $.each(data.theBacking,function(idx,item) {
              appendTaskBacking(item); 
            }); 
            $("#editTaskCharacteristicOptionsForm").validator('update');
          },
          error: function (xhr, textStatus, errorThrown) {
            var error = JSON.parse(xhr.responseText);
            showPopup(false, String(error.message));
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
          }
        });
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

var mainContent = $("#objectViewer");
function commitTaskCharacteristic() {
  var tc = JSON.parse($.session.get("TaskCharacteristic"));
  var oldName = tc.theCharacteristic;
  tc.theTaskName = $("#theTaskName").val();
  tc.theModQual = $("#theModQual").val();
  tc.theCharacteristic = $("#theCharacteristic").val();

  if($("#editTaskCharacteristicOptionsForm").hasClass("new")){
    postTaskCharacteristic(tc, function () {
      clearLocalStorage('task_characteristic');
      $("#editTaskCharacteristicOptionsForm").removeClass("new")
      $('#menuBCClick').attr('dimension','task_characteristic');
      refreshMenuBreadCrumb('task_characteristic');
    });
  }
  else {
    putTaskCharacteristic(tc, oldName, function () {
      clearLocalStorage('task_characteristic');
      $('#menuBCClick').attr('dimension','task_characteristic');
      refreshMenuBreadCrumb('task_characteristic');
    });
  }
}

$(document).on('click', 'td.deleteTaskCharacteristicButton', function (e) {
  e.preventDefault();
  var tName = $(this).closest('tr').find('td:eq(2)').text();
  deleteTaskCharacteristic(tName, function () {
    $('#menuBCClick').attr('dimension','task_characteristic');
    refreshMenuBreadCrumb('task_characteristic');
  });
});

$(document).on("click", "#addNewTaskCharacteristic", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editTaskCharacteristicOptions.html", "#objectViewer", null, true, true, function () {
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/dimensions/table/task",
      success: function (data) {
        var taskSelect = $('#theTaskName');
        $.each(data, function (index,tName) {
          taskSelect.append($("<option></option>").attr("value",tName).text(tName));
        });
        $("#editTaskCharacteristicOptionsForm").validator();
        $("#UpdateTaskCharacteristic").text("Create");
        $("#editTaskCharacteristicOptionsForm").addClass("new");
        $.session.set("TaskCharacteristic", JSON.stringify(jQuery.extend(true, {},taskCharacteristicDefault )));
      },
      error: function (xhr, textStatus, errorThrown) {
        var error = JSON.parse(xhr.responseText);
        showPopup(false, String(error.message));
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  });
});


function putTaskCharacteristic(tc, oldName, callback){
  var output = {};
  output.object = tc;
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);

  $.ajax({
    type: "PUT",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/task_characteristics/name/" + encodeURIComponent(oldName),
    success: function (data) {
      showPopup(true);
      if(jQuery.isFunction(callback)){
        callback();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function postTaskCharacteristic(tc, callback){
  var output = {};
  output.object = tc;
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);

  $.ajax({
    type: "POST",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/task_characteristics",
    success: function (data) {
      showPopup(true);
      if(jQuery.isFunction(callback)){
        callback();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function deleteTaskCharacteristic(name, callback){
  $.ajax({
    type: "DELETE",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    url: serverIP + "/api/task_characteristics/name/" + encodeURIComponent(name) + "?session_id=" + $.session.get('sessionID'),
    success: function (data) {
      showPopup(true);
      if(jQuery.isFunction(callback)){
        callback();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

mainContent.on('click', '#CloseTaskCharacteristic', function (e) {
  e.preventDefault();
  clearLocalStorage('task_characteristic');
  $("#objectViewer").empty();
  $('#menuBCClick').attr('dimension','task_characteristic');
  refreshMenuBreadCrumb('task_characteristic');
});

function appendTaskGWR(tableId,gwrType,item) {
  $(tableId).find("tbody").append('<tr><td class="deletetc' + gwrType + '"><i class="fa fa-minus"></i></td><td class="tc_' + gwrType + '"">'+ item.theReferenceName +'</td><td>' + item.theDimensionName + '</td><td>' + item.theReferenceDescription + '</td></tr>');
};

function appendTaskBacking(item) {
  $("#theBacking").find("tbody").append('<tr><td class="backing"">'+ item +'</td></tr>');
};

function loadTaskCharacteristicReference() {
  $('#theTCArtifactTypeDiv').show();
  var cr = $("#editTaskCharacteristicReference").data("currentcr");
  if (cr != undefined) {
    var cr = JSON.parse(cr);
    $('#theTCArtifactType').val(cr.dimension);
    refreshDimensionSelector($('#theTCReferenceName'),cr.dimension + '_reference',undefined,function() {
      $("#theTCReferenceName").val(cr.name);
      $("#theTCDescription").val(cr.description);
    });
  }
  else {
    refreshDimensionSelector($('#theTCReferenceName'),$('#theTCArtifactType').val() + '_reference',undefined,function() {
      $("#theTCDescription").val('');
    });
  }
};

$('#editTaskCharacteristicReference').on("change", "#theTCArtifactType", function(){
  var artifactType = $('#theTCArtifactType').val();
  var cr = $("#editTaskCharacteristicReference").data("currentcr");
  if (cr != undefined) {
   cr = JSON.parse(cr);
    refreshDimensionSelector($('#theTCReferenceName'),artifactType + '_reference',undefined,function() {
      $("#theTCReferenceName").val(cr.name);
      $("#theTCDescription").val(cr.description);
    });
  }
  else {
    refreshDimensionSelector($('#theTCReferenceName'),artifactType + '_reference',undefined,function() {
      $("#theTCDescription").val('');
    });
  }
});



function addTaskCharacteristicReference(e) {
  e.preventDefault();
  var cr = JSON.parse($("#editTaskCharacteristicReference").data("crtype"));
  var item = jQuery.extend(true, {},characteristicReferenceDefault );
  item.theReferenceName = $("#theTCReferenceName").val();
  item.theReferenceDescription = $("#theTCDescription").val();
  item.theDimensionName = $('#theTCArtifactType').val();
  var tc = JSON.parse($.session.get("TaskCharacteristic"));

  if (cr.tableId == '#theGrounds' && gwrItemPresent(tc.theGrounds,item.theReferenceName) == false) {
    item.theCharacteristicType = 'grounds';
    tc.theGrounds.push(item);
    appendTaskGWR(cr.tableId,cr.classId,item);
    $.session.set("TaskCharacteristic", JSON.stringify(tc));
  }
  else if (cr.tableId == '#theWarrant' && gwrItemPresent(tc.theWarrant,item.theReferenceName) == false) {
    item.theCharacteristicType = 'warrant';
    tc.theWarrant.push(item);
    appendTaskGWR(cr.tableId,cr.classId,item);
    $.session.set("TaskCharacteristic", JSON.stringify(tc));
  }
  else if (cr.tableId == '#theRebuttal' && gwrItemPresent(tc.theRebuttal,item.theReferenceName) == false) {
    item.theCharacteristicType = 'rebuttal';
    tc.theRebuttal.push(item);
    appendTaskGWR(cr.tableId,cr.classId,item);
    $.session.set("TaskCharacteristic", JSON.stringify(tc));
  }
  $("#editTaskCharacteristicReference").modal('hide');
}

function updateTaskReferenceList(e) {
  e.preventDefault();
  var cr = JSON.parse($("#editTaskCharacteristicReference").data("currentcr"));
  var item = jQuery.extend(true, {},characteristicReferenceDefault );
  item.theReferenceName = $("#theTCReferenceName").val();
  item.theDimensionName = $('#theTCArtifactType').val();
  item.theReferenceDescription = $("#theTCDescription").val();
  $(cr.tableId).find("tbody").find('tr:eq(' + cr.index + ')').find('td:eq(1)').text(item.theReferenceName);
  $(cr.tableId).find("tbody").find('tr:eq(' + cr.index + ')').find('td:eq(2)').text(item.theDimensionName);
  $(cr.tableId).find("tbody").find('tr:eq(' + cr.index + ')').find('td:eq(3)').text(item.theReferenceDescription);
  var tc = JSON.parse($.session.get("TaskCharacteristic"));

  if (cr.tableId == '#theGrounds') {
    item.theCharacteristicType = 'grounds';
    $.each(tc.theGrounds,function(idx,g) {
      if (idx == cr.index) {
        tc.theGrounds[idx] = item;
      }
    });
  }
  else if (cr.tableId == '#theWarrant') {
    item.theCharacteristicType = 'warrant';
    $.each(tc.theWarrant,function(idx,w) {
      if (idx == cr.index) {
        tc.theWarrant[idx] = item;
      }
    });
  }
  else {
    item.theCharacteristicType = 'rebuttal';
    $.each(tc.theRebuttal,function(idx,r) {
      if (idx == cr.index) {
        tc.theRebuttal[idx] = item;
      }
    });
  }
  $.session.set("TaskCharacteristic", JSON.stringify(tc));
  $("#editTaskCharacteristicReference").modal('hide');
}


mainContent.on("click", "#addTCGrounds", function(){
  var crt = {};
  crt.tableId = "#theGrounds";
  crt.classId = 'ground'; 
  $("#editTaskCharacteristicReference").data("currentcr",undefined);
  $("#editTaskCharacteristicReference").data('loadcr',loadTaskCharacteristicReference);
  $("#editTaskCharacteristicReference").data("savecr",addTaskCharacteristicReference);
  $("#editTaskCharacteristicReference").data("crtype",JSON.stringify(crt));
  $("#editTaskCharacteristicReference").modal('show');
});

mainContent.on("click", "#addTCWarrant", function(){
  var crt = {};
  crt.tableId = "#theWarrant";
  crt.classId = 'warrant'; 
  $("#editTaskCharacteristicReference").data("currentcr",undefined);
  $("#editTaskCharacteristicReference").data('loadcr',loadTaskCharacteristicReference);
  $("#editTaskCharacteristicReference").data("savecr",addTaskCharacteristicReference);
  $("#editTaskCharacteristicReference").data("crtype",JSON.stringify(crt));
  $("#editTaskCharacteristicReference").modal('show');
});

mainContent.on("click", "#addTCRebuttal", function(){
  var crt = {};
  crt.tableId = "#theRebuttal";
  crt.classId = 'rebuttal'; 
  $("#editTaskCharacteristicReference").data("currentcr",undefined);
  $("#editTaskCharacteristicReference").data('loadcr',loadTaskCharacteristicReference);
  $("#editTaskCharacteristicReference").data("savecr",addTaskCharacteristicReference);
  $("#editTaskCharacteristicReference").data("crtype",JSON.stringify(crt));
  $("#editTaskCharacteristicReference").modal('show');
});

$("#editTaskCharacteristicReference").on('shown.bs.modal', function() {
  var cmd = $("#editTaskCharacteristicReference").data("loadcr");
  cmd();
});

$("#editTaskCharacteristicReference").on('click', '#saveTaskCharacteristicReference',function(e) {
  var cmd = $("#editTaskCharacteristicReference").data("savecr");
  cmd(e);
});

mainContent.on("click",".tc_ground", function () {
  var propRow = $(this).closest("tr");
  var cr = {};
  cr.name = propRow.find("td:eq(1)").text();
  cr.dimension = propRow.find("td:eq(2)").text();
  cr.description = propRow.find("td:eq(3)").text();
  cr.index = propRow.index();
  cr.tableId = "#theGrounds";
  $("#editTaskCharacteristicReference").data("currentcr",JSON.stringify(cr));
  $("#editTaskCharacteristicReference").data('loadcr',loadTaskCharacteristicReference);
  $("#editTaskCharacteristicReference").data("savecr",updateTaskReferenceList);
  $("#editTaskCharacteristicReference").modal('show');
});
mainContent.on("click",".tc_warrant", function () {
  var propRow = $(this).closest("tr");
  var cr = {};
  cr.name = propRow.find("td:eq(1)").text();
  cr.dimension = propRow.find("td:eq(2)").text();
  cr.description = propRow.find("td:eq(3)").text();
  cr.index = propRow.index();
  cr.tableId = "#theWarrant";
  $("#editTaskCharacteristicReference").data("currentcr",JSON.stringify(cr));
  $("#editTaskCharacteristicReference").data('loadcr',loadTaskCharacteristicReference);
  $("#editTaskCharacteristicReference").data("savecr",updateTaskReferenceList);
  $("#editTaskCharacteristicReference").modal('show');
});
mainContent.on("click",".tc_rebuttal", function () {
  var propRow = $(this).closest("tr");
  var cr = {};
  cr.name = propRow.find("td:eq(1)").text();
  cr.dimension = propRow.find("td:eq(2)").text();
  cr.description = propRow.find("td:eq(3)").text();
  cr.index = propRow.index();
  cr.tableId = "#theRebuttal";
  $("#editTaskCharacteristicReference").data("currentcr",JSON.stringify(cr));
  $("#editTaskCharacteristicReference").data('loadcr',loadTaskCharacteristicReference);
  $("#editTaskCharacteristicReference").data("savecr",updateTaskReferenceList);
  $("#editTaskCharacteristicReference").modal('show');
});

mainContent.on('click','td.deletetcground',function() {
  var gRow = $(this).closest("tr");
  var rowIdx = gRow.index();
  gRow.remove();
  var tc = JSON.parse($.session.get("TaskCharacteristic"));
  tc.theGrounds.splice(rowIdx,1);
  $.session.set("TaskCharacteristic", JSON.stringify(tc));
});

mainContent.on('click','td.deletetcwarrant',function() {
  var wRow = $(this).closest("tr");
  var rowIdx = wRow.index();
  wRow.remove();
  var tc = JSON.parse($.session.get("TaskCharacteristic"));
  tc.theWarrant.splice(rowIdx,1);
  $.session.set("TaskCharacteristic", JSON.stringify(tc));
});

mainContent.on('click','td.deletetcrebuttal',function() {
  var rRow = $(this).closest("tr");
  var rowIdx = rRow.index();
  rRow.remove();
  var tc = JSON.parse($.session.get("TaskCharacteristic"));
  tc.theRebuttal.splice(rowIdx,1);
  $.session.set("TaskCharacteristic", JSON.stringify(tc));
});


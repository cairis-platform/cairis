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

      var keys = [];
      for (key in data) {
        keys.push(key);
      }
      keys.sort();

      for (var ki = 0; ki < keys.length; ki++) {
        var key = keys[ki];
        var item = data[key];
        textToInsert[i++] = "<tr>";

        textToInsert[i++] = '<td class="deleteTaskCharacteristicButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="taskcharacteristic-rows" name="theName">';
        textToInsert[i++] = item.theTaskName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theCharacteristic">';
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
            $("#editTaskCharacteristicOptionsForm").validator();
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
          },
          error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
          }
        });
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

var mainContent = $("#objectViewer");
mainContent.on('click', '#UpdateTaskCharacteristic', function (e) {
  e.preventDefault();
  var tc = JSON.parse($.session.get("TaskCharacteristic"));
  var oldName = tc.theCharacteristic;
  tc.theTaskName = $("#theTaskName").val();
  tc.theModQual = $("#theModQual").val();
  tc.theCharacteristic = $("#theCharacteristic").val();

  if($("#editTaskCharacteristicOptionsForm").hasClass("new")){
    postTaskCharacteristic(tc, function () {
      $("#editTaskCharacteristicOptionsForm").removeClass("new")
      $('#menuBCClick').attr('dimension','task_characteristic');
      refreshMenuBreadCrumb('task_characteristic');
    });
  }
  else {
    putTaskCharacteristic(tc, oldName, function () {
      $('#menuBCClick').attr('dimension','task_characteristic');
      refreshMenuBreadCrumb('task_characteristic');
    });
  }
});

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
  debugLogger(output);

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
  debugLogger(output);

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
  $('#theArtifactTypeDiv').show();
  var cr = $("#editCharacteristicReference").data("currentcr");
  if (cr != undefined) {
    $('#theArtifactType').val(cr.dimension);
    refreshDimensionSelector($('#theReferenceName'),cr.dimension + '_reference',undefined,function() {
      var cr = JSON.parse(cr);
      $("#theReferenceName").val(cr.name);
      $("#theDescription").val(cr.description);
    });
  }
  else {
    $('#theArtifactType').val('document');
    refreshDimensionSelector($('#theReferenceName'),'document_reference',undefined,function() {
      $("#theDescription").val('');
    });
  }
};

$('#editCharacteristicReference').on("change", "#theArtifactType", function(){
  var artifactType = $('#theArtifactType').val();
  var cr = JSON.parse($("#editCharacteristicReference").data("currentcr"));

  refreshDimensionSelector($('#theReferenceName'),artifactType + '_reference',undefined,function() {
    $("#theReferenceName").val(cr.name);
    $("#theDescription").val(cr.description);
  });
});



function addTaskCharacteristicReference(e) {
  e.preventDefault();
  var cr = JSON.parse($("#editCharacteristicReference").data("crtype"));
  var item = jQuery.extend(true, {},characteristicReferenceDefault );
  item.theReferenceName = $("#theReferenceName").val();
  item.theReferenceDescription = $("#theDescription").val();
  item.theDimensionName = 'document';
  var tc = JSON.parse($.session.get("TaskCharacteristic"));

  if (cr.tableId == '#theGrounds' && gwrItemPresent(tc.theGrounds,item.theReferenceName) == false) {
    item.theCharacteristicType = 'grounds';
    tc.theGrounds.push(item);
    appendTaskGWR(cr.tableId,cr.classId,item);
    $.session.set("TaskCharacteristic", JSON.stringify(tc));
  }
  else if (cr.tableId == '#theWarrant' && gwrItemPresent(pc.theWarrant,item.theReferenceName) == false) {
    item.theCharacteristicType = 'warrant';
    tc.theWarrant.push(item);
    appendTaskGWR(cr.tableId,cr.classId,item);
    $.session.set("TaskCharacteristic", JSON.stringify(tc));
  }
  else if (cr.tableId == '#theRebuttal' && gwrItemPresent(pc.theRebuttal,item.theReferenceName) == false) {
    item.theCharacteristicType = 'rebuttal';
    tc.theRebuttal.push(item);
    appendTaskGWR(cr.tableId,cr.classId,item);
    $.session.set("TaskCharacteristic", JSON.stringify(tc));
  }
  $("#editCharacteristicReference").modal('hide');
}

function updateTaskReferenceList(e) {
  e.preventDefault();
  var cr = JSON.parse($("#editCharacteristicReference").data("currentcr"));
  var item = jQuery.extend(true, {},characteristicReferenceDefault );
  item.theReferenceName = $("#theReferenceName").val();
  item.theReferenceDescription = $("#theDescription").val();
  $(cr.tableId).find("tbody").find('tr:eq(' + cr.index + ')').find('td:eq(1)').text(item.theReferenceName);
  $(cr.tableId).find("tbody").find('tr:eq(' + cr.index + ')').find('td:eq(2)').text(item.theReferenceDescription);
  item.theDimensionName = 'document';
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
  $("#editCharacteristicReference").modal('hide');
}


mainContent.on("click", "#addTCGrounds", function(){
  var crt = {};
  crt.tableId = "#theGrounds";
  crt.classId = 'ground'; 
  $("#editCharacteristicReference").data('loadcr',loadTaskCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",addTaskCharacteristicReference);
  $("#editCharacteristicReference").data("crtype",JSON.stringify(crt));
  $("#editCharacteristicReference").modal('show');
});

mainContent.on("click", "#addTCWarrant", function(){
  var crt = {};
  crt.tableId = "#theWarrant";
  crt.classId = 'warrant'; 
  $("#editCharacteristicReference").data('loadcr',loadTaskCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",addTaskCharacteristicReference);
  $("#editCharacteristicReference").data("crtype",JSON.stringify(crt));
  $("#editCharacteristicReference").modal('show');
});

mainContent.on("click", "#addTCRebuttal", function(){
  var crt = {};
  crt.tableId = "#theRebuttal";
  crt.classId = 'rebuttal'; 
  $("#editCharacteristicReference").data('loadcr',loadTaskCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",addTaskCharacteristicReference);
  $("#editCharacteristicReference").data("crtype",JSON.stringify(crt));
  $("#editCharacteristicReference").modal('show');
});

$("#editCharacteristicReference").on('shown.bs.modal', function() {
  var cmd = $("#editCharacteristicReference").data("loadcr");
  cmd();
});

$("#editCharacteristicReference").on('click', '#saveCharacteristicReference',function(e) {
  var cmd = $("#editCharacteristicReference").data("savecr");
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
  $("#editCharacteristicReference").data("currentcr",JSON.stringify(cr));
  $("#editCharacteristicReference").data('loadcr',loadTaskCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",updateTaskReferenceList);
  $("#editCharacteristicReference").modal('show');
});
mainContent.on("click",".tc_warrant", function () {
  var propRow = $(this).closest("tr");
  var cr = {};
  cr.name = propRow.find("td:eq(1)").text();
  cr.dimension = propRow.find("td:eq(2)").text();
  cr.description = propRow.find("td:eq(3)").text();
  cr.index = propRow.index();
  cr.tableId = "#theWarrant";
  $("#editCharacteristicReference").data("currentcr",JSON.stringify(cr));
  $("#editCharacteristicReference").data('loadcr',loadTaskCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",updateTaskReferenceList);
  $("#editCharacteristicReference").modal('show');
});
mainContent.on("click",".tc_rebuttal", function () {
  var propRow = $(this).closest("tr");
  var cr = {};
  cr.name = propRow.find("td:eq(1)").text();
  cr.dimension = propRow.find("td:eq(2)").text();
  cr.description = propRow.find("td:eq(3)").text();
  cr.index = propRow.index();
  cr.tableId = "#theRebuttal";
  $("#editCharacteristicReference").data("currentcr",JSON.stringify(cr));
  $("#editCharacteristicReference").data('loadcr',loadTaskCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",updateTaskReferenceList);
  $("#editCharacteristicReference").modal('show');
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
  $.session.set("TaskCharacteristic", JSON.stringify(pc));
});


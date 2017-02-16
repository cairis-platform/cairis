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
  createTaskCharacteristicsTable();
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

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";

        textToInsert[i++] = '<td class="deleteTaskCharacteristicButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="taskcharacteristic-rows" name="theName">';
        textToInsert[i++] = item.theTaskName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theCharacteristic">';
        textToInsert[i++] = item.theCharacteristic;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      });

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
      createTaskCharacteristicsTable();
      $("#editTaskCharacteristicOptionsForm").removeClass("new")
    });
  }
  else {
    putTaskCharacteristic(tc, oldName, function () {
      createTaskCharacteristicsTable();
    });
  }
});

$(document).on('click', 'td.deleteTaskCharacteristicButton', function (e) {
  e.preventDefault();
  var tName = $(this).closest('tr').find('td:eq(2)').text();
  deleteTaskCharacteristic(tName, function () {
    createTaskCharacteristicsTable();
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
  createTaskCharacteristicsTable();
});

function appendTaskGWR(tableId,gwrType,item) {
  $(tableId).find("tbody").append('<tr><td class="delete' + gwrType + '"><i class="fa fa-minus"></i></td><td class="' + gwrType + '"">'+ item.theReferenceName +'</td><td>' + item.theDimensionName + '</td><td>' + item.theReferenceDescription + '</td></tr>');
};

function appendTaskBacking(item) {
  $("#theBacking").find("tbody").append('<tr><td class="backing"">'+ item +'</td></tr>');
};

function loadTaskCharacteristicReference() {
  var cr = JSON.parse($("#editCharacteristicReference").data("currentcr"));
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/" + cr.dimension + "_reference",
    success: function (data) {
      data.sort();
      $("#theReferenceName").empty();
      $.each(data, function(key, item) {
        $("#theReferenceName").append("<option>" + item + "</option>");
      }); 
      $('#theReferenceName').val(cr.name);
      $('#theDescription').val(cr.description);
      $('#theArtifactType').val(cr.dimension);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
};

$('#editCharacteristicReference').on("change", "#theArtifactType", function(){
  var artifactType = $('#theArtifactType').val();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/" + artifactType + "_reference",
    success: function (data) {
      data.sort();
      $("#theReferenceName").empty();
      $.each(data, function(key, item) {
        $("#theReferenceName").append("<option>" + item + "</option>");
      }); 
      var cr = JSON.parse($("#editCharacteristicReference").data("currentcr"));
      $('#theReferenceName').val(cr.name);
      $('#theDescription').val(cr.description);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

function addTaskCharacteristicReference() {
  var cr = JSON.parse($("#editCharacteristicReference").data("crtype"));
  var item = jQuery.extend(true, {},characteristicReferenceDefault );
  item.theReferenceName = $("#theReferenceName").val();
  item.theReferenceDescription = $("#theDescription").val();
  appendTaskGWR(cr.tableId,cr.classId,item); 
  item.theDimensionName = 'document';
  var tc = JSON.parse($.session.get("TaskCharacteristic"));
  if (cr.tableId == '#theGrounds') {
    item.theCharacteristicType = 'grounds';
    tc.theGrounds.push(item);
  }
  else if (cr.tableId == '#theWarrant') {
    item.theCharacteristicType = 'warrant';
    tc.theWarrant.push(item);
  }
  else {
    item.theCharacteristicType = 'rebuttal';
    tc.theRebuttal.push(item);
  }
  $.session.set("TaskCharacteristic", JSON.stringify(tc));
  $("#editCharacteristicReference").modal('hide');
}

function updateTaskReferenceList() {
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


mainContent.on("click", "#addGrounds", function(){
  var crt = {};
  crt.tableId = "#theGrounds";
  crt.classId = 'ground'; 
  $("#editCharacteristicReference").data('loadcr',loadTaskCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",addTaskCharacteristicReference);
  $("#editCharacteristicReference").data("crtype",JSON.stringify(crt));
  $("#editCharacteristicReference").modal('show');
});

mainContent.on("click", "#addWarrant", function(){
  var crt = {};
  crt.tableId = "#theWarrant";
  crt.classId = 'warrant'; 
  $("#editCharacteristicReference").data('loadcr',loadTaskCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",addTaskCharacteristicReference);
  $("#editCharacteristicReference").data("crtype",JSON.stringify(crt));
  $("#editCharacteristicReference").modal('show');
});

mainContent.on("click", "#addRebuttal", function(){
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

$("#editCharacteristicReference").on('click', '#saveCharacteristicReference',function() {
  var cmd = $("#editCharacteristicReference").data("savecr");
  cmd();
});

mainContent.on("click",".ground", function () {
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
mainContent.on("click",".warrant", function () {
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
mainContent.on("click",".rebuttal", function () {
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

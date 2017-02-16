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

$("#personaCharacteristicsClick").click(function(){
  createPersonaCharacteristicsTable();
});

function createPersonaCharacteristicsTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/persona_characteristics",
    success: function (data) {
      setTableHeader("PersonaCharacteristics");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";

        textToInsert[i++] = '<td class="deletePersonaCharacteristicButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="personacharacteristic-rows" name="theName">';
        textToInsert[i++] = item.thePersonaName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theVariable">';
        textToInsert[i++] = item.theVariable;
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

$(document).on('click', "td.personacharacteristic-rows", function () {
  activeElement("objectViewer");
  var name = $(this).closest("tr").find("td:eq(3)").text();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/persona_characteristics/name/" + encodeURIComponent(name),
    success: function (data) {
      fillOptionMenu("fastTemplates/editPersonaCharacteristicOptions.html", "#objectViewer", null, true, true, function () {
        $.ajax({
          type: "GET",
          dataType: "json",
          accept: "application/json",
          data: {
            session_id: String($.session.get('sessionID'))
          },
          crossDomain: true,
          url: serverIP + "/api/dimensions/table/persona",
          success: function (pNames) {
            var personaSelect = $('#thePersonaName');
            $.each(pNames, function (index,pName) {
              personaSelect.append($("<option></option>").attr("value",pName).text(pName));
            });
            $("#editPersonaCharacteristicOptionsForm").validator();
            $("#UpdatePersonaCharacteristic").text("Update");
            $.session.set("PersonaCharacteristic", JSON.stringify(data));
            personaSelect.val(data.thePersonaName);
            $("#theVariable").val(data.theVariable);
            $("#theModQual").val(data.theModQual);
            $("#theCharacteristic").val(data.theCharacteristic);
     
            $("#theGrounds").find("tbody").empty();
            $.each(data.theGrounds,function(idx,item) {
              appendGWR("#theGrounds",'ground',item); 
            }); 

            $("#theWarrant").find("tbody").empty();
            $.each(data.theWarrant,function(idx,item) {
              appendGWR("#theWarrant",'warrant',item); 
            });
            $("#theRebuttal").find("tbody").empty();
            $.each(data.theRebuttal,function(idx,item) {
              appendGWR("#theRebuttal",'rebuttal',item); 
            });
            $("#theBacking").find("tbody").empty();
            $.each(data.theBacking,function(idx,item) {
              appendBacking(item); 
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
mainContent.on('click', '#UpdatePersonaCharacteristic', function (e) {
  e.preventDefault();
  var pc = JSON.parse($.session.get("PersonaCharacteristic"));
  var oldName = pc.theCharacteristic;
  pc.thePersonaName = $("#thePersonaName").val();
  pc.theVariable = $("#theVariable").val();
  pc.theModQual = $("#theModQual").val();
  pc.theCharacteristic = $("#theCharacteristic").val();

  if($("#editPersonaCharacteristicOptionsForm").hasClass("new")){
    postPersonaCharacteristic(pc, function () {
      createPersonaCharacteristicsTable();
      $("#editPersonaCharacteristicOptionsForm").removeClass("new")
    });
  }
  else {
    putPersonaCharacteristic(pc, oldName, function () {
      createPersonaCharacteristicsTable();
    });
  }
});

$(document).on('click', 'td.deletePersonaCharacteristicButton', function (e) {
  e.preventDefault();
  var pName = $(this).closest('tr').find('td:eq(3)').text();
  deletePersonaCharacteristic(pName, function () {
    createPersonaCharacteristicsTable();
  });
});

$(document).on("click", "#addNewPersonaCharacteristic", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editPersonaCharacteristicOptions.html", "#objectViewer", null, true, true, function () {
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/dimensions/table/persona",
      success: function (data) {
        var personaSelect = $('#thePersonaName');
        $.each(data, function (index,pName) {
          personaSelect.append($("<option></option>").attr("value",pName).text(pName));
        });
        $("#editPersonaCharacteristicOptionsForm").validator();
        $("#UpdatePersonaCharacteristic").text("Create");
        $("#editPersonaCharacteristicOptionsForm").addClass("new");
        $.session.set("PersonaCharacteristic", JSON.stringify(jQuery.extend(true, {},personaCharacteristicDefault )));
      },
      error: function (xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  });
});


function putPersonaCharacteristic(pc, oldName, callback){
  var output = {};
  output.object = pc;
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
    url: serverIP + "/api/persona_characteristics/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
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

function postPersonaCharacteristic(pc, callback){
  var output = {};
  output.object = pc;
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
    url: serverIP + "/api/persona_characteristics" + "?session_id=" + $.session.get('sessionID'),
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

function deletePersonaCharacteristic(name, callback){
  $.ajax({
    type: "DELETE",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    url: serverIP + "/api/persona_characteristics/name/" + encodeURIComponent(name) + "?session_id=" + $.session.get('sessionID'),
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

mainContent.on('click', '#ClosePersonaCharacteristic', function (e) {
  e.preventDefault();
  createPersonaCharacteristicsTable();
});

function appendGWR(tableId,gwrType,item) {
  $(tableId).find("tbody").append('<tr><td class="delete' + gwrType + '"><i class="fa fa-minus"></i></td><td class="' + gwrType + '"">'+ item.theReferenceName +'</td><td>' + item.theReferenceDescription + '</td></tr>');
};

function appendBacking(item) {
  $("#theBacking").find("tbody").append('<tr><td class="backing"">'+ item +'</td></tr>');
};

function loadCharacteristicReference() {
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/document_reference",
    success: function (data) {
      data.sort();
      $("#theReferenceName").empty();
      $.each(data, function(key, item) {
        $("#theReferenceName").append("<option>" + item + "</option>");
      }); 
      var cr = JSON.parse($("#editCharacteristicReference").data("currentcr"));
      $("#theReferenceName").val(cr.name);
      $("#theDescription").val(cr.description);
      $('#theArtifactType').prop('disabled','disabled');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
};

function addCharacteristicReference() {
  var cr = JSON.parse($("#editCharacteristicReference").data("crtype"));
  var item = jQuery.extend(true, {},characteristicReferenceDefault );
  item.theReferenceName = $("#theReferenceName").val();
  item.theReferenceDescription = $("#theDescription").val();
  appendGWR(cr.tableId,cr.classId,item); 
  item.theDimensionName = 'document';
  var pc = JSON.parse($.session.get("PersonaCharacteristic"));
  if (cr.tableId == '#theGrounds') {
    item.theCharacteristicType = 'grounds';
    pc.theGrounds.push(item);
  }
  else if (cr.tableId == '#theWarrant') {
    item.theCharacteristicType = 'warrant';
    pc.theWarrant.push(item);
  }
  else {
    item.theCharacteristicType = 'rebuttal';
    pc.theRebuttal.push(item);
  }
  $.session.set("PersonaCharacteristic", JSON.stringify(pc));
  $("#editCharacteristicReference").modal('hide');
}

function updateReferenceList() {
  var cr = JSON.parse($("#editCharacteristicReference").data("currentcr"));
  var item = jQuery.extend(true, {},characteristicReferenceDefault );
  item.theReferenceName = $("#theReferenceName").val();
  item.theReferenceDescription = $("#theDescription").val();
  $(cr.tableId).find("tbody").find('tr:eq(' + cr.index + ')').find('td:eq(1)').text(item.theReferenceName);
  $(cr.tableId).find("tbody").find('tr:eq(' + cr.index + ')').find('td:eq(2)').text(item.theReferenceDescription);
  item.theDimensionName = 'document';
  var pc = JSON.parse($.session.get("PersonaCharacteristic"));

  if (cr.tableId == '#theGrounds') {
    item.theCharacteristicType = 'grounds';
    $.each(pc.theGrounds,function(idx,g) {
      if (idx == cr.index) {
        pc.theGrounds[idx] = item;
      }
    });
  }
  else if (cr.tableId == '#theWarrant') {
    item.theCharacteristicType = 'warrant';
    $.each(pc.theWarrant,function(idx,w) {
      if (idx == cr.index) {
        pc.theWarrant[idx] = item;
      }
    });
  }
  else {
    item.theCharacteristicType = 'rebuttal';
    $.each(pc.theRebuttal,function(idx,r) {
      if (idx == cr.index) {
        pc.theRebuttal[idx] = item;
      }
    });
  }
  $.session.set("PersonaCharacteristic", JSON.stringify(pc));
  $("#editCharacteristicReference").modal('hide');
}


mainContent.on("click", "#addGrounds", function(){
  var crt = {};
  crt.tableId = "#theGrounds";
  crt.classId = 'ground'; 
  $("#editCharacteristicReference").data('loadcr',loadCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",addCharacteristicReference);
  $("#editCharacteristicReference").data("crtype",JSON.stringify(crt));
  $("#editCharacteristicReference").modal('show');
});

mainContent.on("click", "#addWarrant", function(){
  var crt = {};
  crt.tableId = "#theWarrant";
  crt.classId = 'warrant'; 
  $("#editCharacteristicReference").data('loadcr',loadCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",addCharacteristicReference);
  $("#editCharacteristicReference").data("crtype",JSON.stringify(crt));
  $("#editCharacteristicReference").modal('show');
});

mainContent.on("click", "#addRebuttal", function(){
  var crt = {};
  crt.tableId = "#theRebuttal";
  crt.classId = 'rebuttal'; 
  $("#editCharacteristicReference").data('loadcr',loadCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",addCharacteristicReference);
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
  cr.description = propRow.find("td:eq(2)").text();
  cr.index = propRow.index();
  cr.tableId = "#theGrounds";
  $("#editCharacteristicReference").data("currentcr",JSON.stringify(cr));
  $("#editCharacteristicReference").data('loadcr',loadCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",updateReferenceList);
  $("#editCharacteristicReference").modal('show');
});
mainContent.on("click",".warrant", function () {
  var propRow = $(this).closest("tr");
  var cr = {};
  cr.name = propRow.find("td:eq(1)").text();
  cr.description = propRow.find("td:eq(2)").text();
  cr.index = propRow.index();
  cr.tableId = "#theWarrant";
  $("#editCharacteristicReference").data("currentcr",JSON.stringify(cr));
  $("#editCharacteristicReference").data('loadcr',loadCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",updateReferenceList);
  $("#editCharacteristicReference").modal('show');
});
mainContent.on("click",".rebuttal", function () {
  var propRow = $(this).closest("tr");
  var cr = {};
  cr.name = propRow.find("td:eq(1)").text();
  cr.description = propRow.find("td:eq(2)").text();
  cr.index = propRow.index();
  cr.tableId = "#theRebuttal";
  $("#editCharacteristicReference").data("currentcr",JSON.stringify(cr));
  $("#editCharacteristicReference").data('loadcr',loadCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",updateReferenceList);
  $("#editCharacteristicReference").modal('show');
});

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
      window.activeTable = "PersonaCharacteristics";
      setTableHeader();
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
      $("#reqTable").find("tbody").removeClass();

      activeElement("reqTable");
      sortTableByRow(0);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
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
        $.session.set("PersonaCharacteristic", JSON.stringify(data));

        $("#theGrounds").find("tbody").empty();
        $.each(data.theGrounds,function(idx,item) {
          appendGWR("#theGrounds",'grounds',item); 
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

        $('#editPersonaCharacteristicOptionsForm').loadJSON(data, null);
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

$(document).on('click', 'td.deletePersonaCharacteristicsButton', function (e) {
  e.preventDefault();
  deletePersonaCharacteristic($(this).find('i').attr("value"), function () {
    createPersonaCharacteristicsTable();
  });
});

$(document).on("click", "#addNewPersonaCharacteristic", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editPersonaCharacteristicOptions.html", "#objectViewer", null, true, true, function () {
    $("#editPersonaCharacteristicOptionsForm").addClass("new");
    $.session.set("PersonaCharacteristic", JSON.stringify(jQuery.extend(true, {},personaCharacteristicDefault )));
  });
});


function putPersonaCharacteristic(pc, oldName, usePopup, callback){
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
      if(usePopup) {
        showPopup(true);
      }
      if(jQuery.isFunction(callback)){
        callback();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      if(usePopup) {
        var error = JSON.parse(xhr.responseText);
        showPopup(false, String(error.message));
      }
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

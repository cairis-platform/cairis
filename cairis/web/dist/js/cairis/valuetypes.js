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

$("#assetValuesClick").click(function () {
  $('#unsupportedModel').modal('show');
});

$("#assetTypesClick").click(function () {
  createValueTypesTable('asset_type');
});

$("#accessRightsClick").click(function () {
  createValueTypesTable('access_right');
});

$("#protocolsClick").click(function () {
  createValueTypesTable('protocol');
});

$("#privilegesClick").click(function () {
  createValueTypesTable('privilege');
});

$("#surfaceTypesClick").click(function () {
  createValueTypesTable('surface_type');
});

$("#vulnerabilityTypesClick").click(function () {
  createValueTypesTable('vulnerability_type');
});

$("#vulnerabilitySeveritiesClick").click(function () {
  createValueTypesTable('severity');
});

$("#capabilitiesClick").click(function () {
  createValueTypesTable('capability');
});

$("#motivationsClick").click(function () {
  createValueTypesTable('motivation');
});

$("#threatTypesClick").click(function () {
  createValueTypesTable('threat_type');
});

$("#threatLikelihoodsClick").click(function () {
  createValueTypesTable('likelihood');
});

$("#threatValuesClick").click(function () {
  createValueTypesTable('threat_value');
});

$("#riskValuesClick").click(function () {
  createValueTypesTable('risk_value');
});


function createValueTypesTable(valueType){

  $.session.set('value_type',valueType);
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/value_types/type/" + valueType + "/environment/all",
    success: function (data) {
      setTableHeader(valueType);
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";

        textToInsert[i++] = '<td class="deleteValueTypeButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';
        textToInsert[i++] = '<td class="valuetype-rows" name="theName">';
        textToInsert[i++] = item.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theDescription">';
        textToInsert[i++] = item.theDescription;
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
  })
}

$(document).on('click', "td.valuetype-rows", function () {
  activeElement("objectViewer");
  var name = $(this).text();
  var valueType = $.session.get("value_type");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/value_types/type/" + valueType + "/environment/all/name/" + encodeURIComponent(name),
    success: function (data) {
      $("#UpdateValueType").text("Update");
      var vtPage = "editValueTypeOptions.html";
      var formObjt = "#editValueTypeOptionsForm";
      if (valueType == 'access_right' || valueType == 'protocol' || valueType == 'privilege' || valueType == 'surface_type') {
        vtPage = 'editScoredValueTypeOptions.html';
        formObjt = "#editScoredValueTypeOptionsForm";
      }
      fillOptionMenu("fastTemplates/" + vtPage, "#objectViewer", null, true, true, function () {
        $.session.set("ValueType", JSON.stringify(data));
        $(formObjt).loadJSON(data, null);

      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});


var mainContent = $("#objectViewer");
mainContent.on('click', '#UpdateValueType', function (e) {
  e.preventDefault();
  var vt = JSON.parse($.session.get("ValueType"));
  var oldName = vt.theName;
  vt.theName = $("#theName").val();
  vt.theDescription = $("#theDescription").val();
  vt.theRationale = $("#theRationale").val();
  vt.theType = $.session.get("value_type");
  vt.theEnvironmentName = 'all';

  var formObjt = "#editValueTypeOptionsForm";
  if (vt.theType == 'access_right' || vt.theType == 'protocol' || vt.theType == 'privilege' || vt.theType == 'surface_type') {
    formObjt = "#editScoredValueTypeOptionsForm";
    vt.theScore = $("#theScore").val(); 
  }

  if($(formObjt).hasClass("new")){
    postValueType(vt, function () {
      createValueTypesTable(vt.theType);
      $(formObjt).removeClass("new")
    });
  } 
  else {
    putValueType(vt, oldName, function () {
      createValueTypesTable(vt.theType);
    });
  }
});

$(document).on('click', 'td.deleteValueTypeButton', function (e) {
  e.preventDefault();
  var vtName = $(this).find('i').attr("value");
  var valueType = $.session.get("value_type");
  deleteObject(valueType,vtName,function(vtName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/value_types/type/" + valueType + "/environment/all/name/" + vtName.replace(" ", "%20").replace("/","%47") + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        createValueTypesTable(valueType);
        showPopup(true);
      },
      error: function (xhr, textStatus, errorThrown) {
        var error = JSON.parse(xhr.responseText);
        showPopup(false, String(error.message));
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  });
});

$(document).on("click", "#addNewValueType", function () {
  activeElement("objectViewer");
  var valueType = $.session.get("value_type");
  var formObjt = "editValueTypeOptions";
  if (valueType == 'access_right' || valueType == 'protocol' || valueType == 'privilege' || valueType == 'surface_type') {
    formObjt = "editScoredValueTypeOptions";
  }
  fillOptionMenu("fastTemplates/" + formObjt + ".html", "#objectViewer", null, true, true, function () {
    $("#UpdateValueType").text("Create");
    $("#" + formObjt + "Form").addClass("new");
    $.session.set("ValueType", JSON.stringify(jQuery.extend(true, {},valueTypeDefault )));
  });
});

function putValueType(vt, oldName, usePopup, callback){
  var output = {};
  output.object = vt;
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);
  debugLogger(output);
  var valueType = $.session.get("value_type");

  $.ajax({
    type: "PUT",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/value_types/type/" + valueType + "/environment/all/name/" + oldName.replace(" ", "%20").replace("/","%47") + "?session_id=" + $.session.get('sessionID'),
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

function postValueType(vt, callback){
  var output = {};
  output.object = vt;
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
    url: serverIP + "/api/value_types/" + "?session_id=" + $.session.get('sessionID'),
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

mainContent.on('click', '#CloseValueType', function (e) {
  e.preventDefault();
  createValueTypesTable($.session.get("value_type"));
});

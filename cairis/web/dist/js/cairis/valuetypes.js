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
  refreshDimensionSelector($('#chooseEnvironmentSelect'),'environment', undefined, function(){
    $('#chooseEnvironment').attr('data-chooseDimension','environment');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','viewAssetValues');
    $('#chooseEnvironment').modal('show');
  },['All']);
});

function viewAssetValues() {
  var envName = $("#chooseEnvironmentSelect").val();
  $('#menuBCClick').attr('dimension','asset_value');
  refreshMenuBreadCrumb('asset_value',envName);
}

$("#assetTypesClick").click(function () {
  $('#menuBCClick').attr('dimension','asset_type');
  refreshMenuBreadCrumb('asset_type');
});

$("#accessRightsClick").click(function () {
  $('#menuBCClick').attr('dimension','access_right');
  refreshMenuBreadCrumb('access_right');
});

$("#protocolsClick").click(function () {
  $('#menuBCClick').attr('dimension','protocol');
  refreshMenuBreadCrumb('protocol');
});

$("#privilegesClick").click(function () {
  $('#menuBCClick').attr('dimension','privilege');
  refreshMenuBreadCrumb('privilege');
});

$("#surfaceTypesClick").click(function () {
  $('#menuBCClick').attr('dimension','surface_type');
  refreshMenuBreadCrumb('surface_type');
});

$("#vulnerabilityTypesClick").click(function () {
  $('#menuBCClick').attr('dimension','vulnerability_type');
  refreshMenuBreadCrumb('vulnerability_type');
});

$("#vulnerabilitySeveritiesClick").click(function () {
  $('#menuBCClick').attr('dimension','severity');
  refreshMenuBreadCrumb('severity');
});

$("#capabilitiesClick").click(function () {
  $('#menuBCClick').attr('dimension','capability');
  refreshMenuBreadCrumb('capability');
});

$("#motivationsClick").click(function () {
  $('#menuBCClick').attr('dimension','motivation');
  refreshMenuBreadCrumb('motivation');
});

$("#threatTypesClick").click(function () {
  $('#menuBCClick').attr('dimension','threat_type');
  refreshMenuBreadCrumb('threat_type');
});

$("#threatLikelihoodsClick").click(function () {
  $('#menuBCClick').attr('dimension','likelihood');
  refreshMenuBreadCrumb('likelihood');
});

$("#threatValuesClick").click(function () {
  $('#menuBCClick').attr('dimension','threat_value');
  refreshMenuBreadCrumb('threat_value');
});


function createValueTypesTable(valueType,envName){

  $.session.set('value_type',valueType);
  var vtUrl = serverIP + "/api/value_types/type/" + valueType + "/environment/";
  if (envName == undefined) {
    vtUrl += "all";
    $.session.set('environment',undefined);
  }
  else {
    vtUrl += encodeURIComponent(envName);
    $.session.set('environment',envName);
  } 
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: vtUrl,
    success: function (data) {
      setTableHeader(valueType);
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
	if (envName == undefined) {
          textToInsert[i++] = '<td class="deleteValueTypeButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';
	}
        textToInsert[i++] = '<td class="valuetype-rows" name="theName">';
        textToInsert[i++] = item.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theDescription">';
        textToInsert[i++] = item.theDescription;
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
  })
}

$(document).on('click', "td.valuetype-rows", function () {
  activeElement("objectViewer");
  var name = $(this).text();
  refreshObjectBreadCrumb(name);
  var valueType = $.session.get("value_type");
  var envName = $.session.get("environment");
  if (envName == undefined) {
    envName = 'all';
  }

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/value_types/type/" + valueType + "/environment/" + encodeURIComponent(envName) + "/name/" + encodeURIComponent(name),
    success: function (data) {
      $("#UpdateValueType").text("Update");
      $('#theRationaleLabel').hide();
      $('#theRationale').hide();
      var vtPage = "editValueTypeOptions.html";
      var formObjt = "#editValueTypeOptionsForm";
      if (valueType == 'access_right' || valueType == 'protocol' || valueType == 'privilege' || valueType == 'surface_type') {
        vtPage = 'editScoredValueTypeOptions.html';
        formObjt = "#editScoredValueTypeOptionsForm";
        $('#Rationale').attr('display','inline');
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
  vt.theType = $.session.get("value_type");
  vt.theEnvironmentName = $.session.get("environment");
  if (vt.theEnvironmentName == undefined) {
    vt.theEnvironmentName = 'all';
  }
  vt.theRationale = $("#theRationale").val();

  var formObjt = "#editValueTypeOptionsForm";
  if (vt.theType == 'access_right' || vt.theType == 'protocol' || vt.theType == 'privilege' || vt.theType == 'surface_type') {
    formObjt = "#editScoredValueTypeOptionsForm";
    vt.theScore = $("#theScore").val(); 
  }

  if($(formObjt).hasClass("new")){
    postValueType(vt, function () {
      createValueTypesTable(vt.theType);
      $(formObjt).removeClass("new")
      refreshMenuBreadCrumb(vt.theType)
    });
  } 
  else {
    putValueType(vt, oldName, function () {
      refreshMenuBreadCrumb(vt.theType,$.session.get("environment"))
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
  var valueType = $.session.get("value_type");
  var vtLabel = "Value Type";
  switch (valueType) {
    case "asset_type":
      vtLabel = "Asset Type";
      break;
    case "access_right":
      vtLabel = "Access Right";
      break;
    case "protocol":
      vtLabel = "Protocol";
      break;
    case "privilege":
      vtLabel = "Privilege";
      break;
    case "surface_type":
      vtLabel = "Surface Type";
      break;
    case "vulnerability_type":
      vtLabel = "Vulnerability Type";
      break;
    case "severity":
      vtLabel = "Severity";
      break;
    case "capability":
      vtLabel = "Capability";
      break;
    case "motivation":
      vtLabel = "Motivation";
      break;
    case "threat_type":
      vtLabel = "Threat Type";
      break;
    case "likelihood":
      vtLabel = "Likelihood";
      break;
    case "threat_value":
      vtLabel = "Threat Value";
     break;
  }
  

  refreshObjectBreadCrumb('New ' + vtLabel);
  activeElement("objectViewer");
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

function putValueType(vt, oldName, callback){
  var output = {};
  output.object = vt;
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);
  debugLogger(output);
  var valueType = $.session.get("value_type");
  var envName = $.session.get("environment");
  if (envName == undefined) {
    envName = 'all';
  }

  $.ajax({
    type: "PUT",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/value_types/type/" + valueType + "/environment/" + encodeURIComponent(envName) + "/name/" + oldName.replace(" ", "%20").replace("/","%47") + "?session_id=" + $.session.get('sessionID'),
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
  refreshMenuBreadCrumb($.session.get("value_type"),$.session.get("environment"))
});

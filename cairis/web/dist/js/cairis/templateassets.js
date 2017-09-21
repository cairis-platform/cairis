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

$("#templateAssetsClick").click(function(){
  validateClick('template_asset',function() {
    $('#menuBCClick').attr('dimension','template_asset');
    refreshMenuBreadCrumb('template_asset');
  });
});

function createTemplateAssetTable(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/template_assets",
    success: function (data) {
      setTableHeader("TemplateAssets");
      fillTemplateAssetsTable(data, function(){
        newSorting(1);
      });
      activeElement("mainTable");
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function fillTemplateAssetsTable(data, callback){
  var theTable = $(".theTable");
  var textToInsert = [];
  var i = 0;

  $.each(data, function(count, item) {
    textToInsert[i++] = '<tr>'

    textToInsert[i++] = '<td class="deleteTemplateAssetButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';

    textToInsert[i++] = '<td class="template-asset-rows" name="theName" value="' + item.theName + '">';
    textToInsert[i++] = item.theName;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '<td name="theType">';
    textToInsert[i++] = item.theType;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '<td name="theId" style="display:none;">';
    textToInsert[i++] = item.theId;
    textToInsert[i++] = '</td>';
    textToInsert[i++] = '</tr>';

  });
  theTable.append(textToInsert.join(''));
  $.contextMenu('destroy',$('.requirement-rows'));
  theTable.css("visibility","visible");
  $("#mainTable").find("tbody").removeClass();

  callback();
}

$(document).on('click', "td.template-asset-rows", function(){
  var taName = $(this).attr('value');
  refreshObjectBreadCrumb(taName);
  viewTemplateAsset(taName);
});

function viewTemplateAsset(assetName) {
  $("#UpdateTemplateAsset").text("Update");
  activeElement("objectViewer");
  $.session.set("AssetName", assetName.trim());

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/template_assets/name/" + encodeURIComponent(assetName),
    success: function (newdata) {
      fillOptionMenu("fastTemplates/editTemplateAssetOptions.html","#objectViewer",null,true,true, function(){
        refreshDimensionSelector($('#theType'),'asset_type',undefined,function(){
          $('#theType').val(newdata.theType);
          refreshDimensionSelector($('#theTemplateAssetSurfaceType'),'surface_type',undefined,function(){
            $('#theTemplateAssetSurfaceType').val(newdata.theSurfaceType);
            refreshDimensionSelector($('#theTemplateAssetAccessRight'),'access_right',undefined,function(){
              $('#theTemplateAssetAcccessRight').val(newdata.theAccessRight);
              $('#editTemplateAssetOptionsform').validator('update');
              $.session.set("TemplateAsset", JSON.stringify(newdata));
              $.each(newdata.theInterfaces,function(idx,aInt) {
                appendTemplateAssetInterface(aInt);
              });
              $.each(newdata.theProperties,function(idx,taProp) {
                if (taProp.value != 'None') {
                  appendTemplateSecurityProperty(taProp.name,taProp.value,taProp.rationale);
                }
              });
              $('#editTemplateAssetOptionsform').validator('update');
              $('#editTemplateAssetOptionsform').loadJSON(newdata,null);
            },['All']);
          },['All']);
        },['All']);
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
};

function appendTemplateAssetInterface(aInt) {
  $("#theTemplateAssetInterfaces").find("tbody").append('<tr><td class="deleteTemplateAssetInterface"><i class="fa fa-minus"></i></td><td class="template-asset-interface">'+ aInt.theInterfaceName +'</td><td>' + aInt.theInterfaceType + '</td><td>' + aInt.theAccessRight + '</td><td>' + aInt.thePrivilege + '</td></tr>');
}

mainContent.on('click','td.deleteTemplateAssetInterface',function() {
  var intRow = $(this).closest("tr");
  var rowIdx = intRow.index();
  intRow.remove();
  var ta = JSON.parse($.session.get("TemplateAsset"));
  ta.theInterfaces.splice(rowIdx,1);
  $.session.set("TemplateAsset", JSON.stringify(ta));
});

function updateTemplateAssetSecurityProperty() {
  var currentProperty = JSON.parse($("#chooseSecurityProperty").attr("data-currentproperty"));
  var propRow = undefined;

  $("#theTemplateProperties").find("tr").each(function(index, row){
    if (currentProperty.name == $(row).find("td:eq(2)").text()) {
      propRow = $(row);
    }
  });

  var updProp = {};
  updProp.name =  $("#theSecurityPropertyName").find("option:selected").text();
  updProp.value =  $("#theSecurityPropertyValue").val();
  updProp.rationale =  $("#theSecurityPropertyRationale").val();

  var ta = JSON.parse($.session.get("TemplateAsset"));

  $.each(ta.theProperties, function(idx, secProp){
    if (updProp.name == secProp.name) {
      ta.theProperties[idx] = updProp;
      $.session.set("TemplateAsset", JSON.stringify(ta));
      propRow.find("td:eq(2)").text(updProp.name);
      propRow.find("td:eq(3)").text(updProp.value);
      propRow.find("td:eq(4)").text(updProp.rationale);
      $("#chooseSecurityProperty").modal('hide');
    }
  });
}

var mainContent = $("#objectViewer");
mainContent.on('click', '.theTemplateAssetPropName', function(){
  var propRow = $(this).closest("tr");
  var selectedProp = {};
  selectedProp.name = propRow.find("td:eq(2)").text();
  selectedProp.value = propRow.find("td:eq(3)").text();
  selectedProp.rationale = propRow.find("td:eq(4)").text();

  $("#chooseSecurityProperty").attr('data-updatepropertylist',"updateTemplateAssetPropertyList");
  $("#chooseSecurityProperty").attr("data-buildproperty","updateTemplateAssetSecurityProperty");
  $("#chooseSecurityProperty").attr("data-currentproperty",JSON.stringify(selectedProp));
  $("#chooseSecurityProperty").modal('show');
});


mainContent.on("click",".deleteTemplateProperty", function(){
  var propName = $(this).closest("tr").find("td:eq(2)").text();
  $(this).closest("tr").remove();
  var ta = JSON.parse($.session.get("TemplateAsset"));
  $.each(ta.theProperties, function(idx,prop) {
    if (propName == prop.name) {
      ta.theProperties[idx] = {'name':propName,'value':'None','rationale':'None'};
      $.session.set("TemplateAsset", JSON.stringify(ta));
    }
  });
});

$(document).on('click', "#addNewTemplateAsset",function(){
  refreshObjectBreadCrumb('New Template Asset');
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editTemplateAssetOptions.html","#objectViewer",null,true,true,function(){
    $('#editTemplateAssetOptionsform').validator();
    $("#UpdateTemplateAsset").text("Create");

    refreshDimensionSelector($('#theType'),'asset_type',undefined,function(){
      refreshDimensionSelector($('#theTemplateAssetSurfaceType'),'surface_type',undefined,function(){
        refreshDimensionSelector($('#theTemplateAssetAccessRight'),'access_right',undefined,function() {
          $.session.set("TemplateAsset", JSON.stringify(jQuery.extend(true, {},templateAssetDefault )));
          $("#editTemplateAssetOptionsform").addClass("new");
        },['All']);
      },['All']);
    },['All']);
  });
});

$(document).on('click', "td.deleteTemplateAssetButton",function(e){
  var assetName = $(this).find('i').attr('value');
  e.preventDefault();
  deleteObject('template_asset',assetName, function(assetName) {

    $.ajax({
      type: "DELETE",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID')),
        name: assetName
      },
      crossDomain: true,
      url: serverIP + "/api/template_assets/name/" + encodeURIComponent(assetName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        $.ajax({
          type: "GET",
          dataType: "json",
          accept: "application/json",
          data: {
            session_id: String($.session.get('sessionID'))
          },
          crossDomain: true,
          url: serverIP + "/api/template_assets",
          success: function (data) {
            setTableHeader("TemplateAssets");
            fillTemplateAssetsTable(data, function(){
              newSorting(1);
            });
            activeElement("mainTable");
            showPopup(true);
          },
          error: function (xhr, textStatus, errorThrown) {
            var error = JSON.parse(xhr.responseText);
            showPopup(false, String(error.message));
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
          }
        });
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

function updateTemplateAssetPropertyList() {
  resetSecurityPropertyList();

  var currentProperty = $("#chooseSecurityProperty").attr('data-currentproperty');
  if (currentProperty != '') {
    currentProperty = JSON.parse(currentProperty);
  }

  $("#theTemplateProperties").find(".theTemplateAssetPropName").each(function(index, prop){
    if ((currentProperty != '') && (currentProperty.name == $(prop).text())) {
      // don't remove
    }
    else {
      $("#theSecurityPropertyName option[value='" + $(prop).text() + "']").remove();
    }
  });
  if (currentProperty != '') {
    $("#theSecurityPropertyName").val(currentProperty.name);
    $("#theSecurityPropertyValue").val(currentProperty.value);
    $("#theSecurityPropertyRationale").val(currentProperty.rationale);
  }
}

function addTemplateAssetSecurityProperty(e) {
  e.preventDefault()
  var secProp = {};
  secProp.name =  $("#theSecurityPropertyName").find("option:selected").text();
  secProp.value =  $("#theSecurityPropertyValue").val();
  secProp.rationale =  $("#theSecurityPropertyRationale").val()
  var ta = JSON.parse( $.session.get("TemplateAsset"));
  $.each(ta.theProperties, function(idx,prop) {
    if (secProp.name == prop.name) {
      ta.theProperties[idx] = secProp;
      $.session.set("TemplateAsset", JSON.stringify(ta));
      appendTemplateSecurityProperty(secProp.name,secProp.value,secProp.rationale);
      $("#chooseSecurityProperty").modal('hide');
    }
  });

}

mainContent.on("click", "#addNewTemplateProperty", function(){
  $("#chooseSecurityProperty").attr('data-updatepropertylist',"updateTemplateAssetPropertyList");
  $("#chooseSecurityProperty").attr("data-buildproperty","addTemplateAssetSecurityProperty");
  $("#chooseSecurityProperty").modal('show');
});


function appendTemplateSecurityProperty(label,value,rationale){
  $("#theTemplateProperties").find("tbody").append('<tr class="clickable-properties"><td style="display: none;">' + label + '</td><td><div class="fillparent deleteTemplateProperty"><i class="fa fa-minus"></i></div></td><td class="theTemplateAssetPropName" name="name">' + label + '</td><td name="value">'+ value +'</td><td name="rationale">'+ rationale +'</td></tr>').animate('slow');
};

mainContent.on('click', '#UpdateTemplateAsset',function(e){
  e.preventDefault();
  var ta = $.session.get("TemplateAsset");
  if($("#editTemplateAssetOptionsform").hasClass("new")){
    postTemplateAssetForm($("#editTemplateAssetOptionsform"), function(){});
  }
  else{
    putTemplateAssetForm($("#editTemplateAssetOptionsform"));
  }
  refreshMenuBreadCrumb('template_asset');
});

mainContent.on('click', '#CloseTemplateAsset', function (e) {
  e.preventDefault();
  refreshMenuBreadCrumb('template_asset');
});

function templateAssetFormToJSON(data){
  var json =  JSON.parse($.session.get("TemplateAsset"));
  json.theName = $(data).find('#theName').val();

  json["theShortCode"] = $(data).find('#theShortCode').val();
  json["theDescription"] = $(data).find('#theDescription').val();
  json["theSignificance"] = $(data).find('#theSignificance').val();
  json["theSurfaceType"] = $(data).find('#theTemplateAssetSurfaceType').val();
  json["theAccessRight"] = $(data).find('#theTemplateAssetAccessRight').val();
  json.theType =  $(data).find( "#theType option:selected" ).text().trim();


  $(data).children().each(function () {
    if(String($(this).prop("tagName")).toLowerCase() == "p"){
      $(this).children().each(function() {
        if(String($(this).prop("tagName")).toLowerCase() == "input"){
          json[$(this).prop("name")] = $(this).val();
        }

        if(String($(this).prop("tagName")).toLowerCase() == "select"){
          var id = $(this).attr('id');
          $(this).children().each(function() {
            var attr = $(this).attr('selected');
            if (typeof attr !== typeof undefined && attr !== false) {
              json[id] = $(this).val();
            }
          });
        }
      });
    }
  });
  return json
}

function putTemplateAssetForm(data){
  putTemplateAsset(templateAssetFormToJSON(data));
}

function postTemplateAssetForm(data,callback){
  var newAsset = templateAssetFormToJSON(data);
  var assetName = $(data).find('#theName').val();
  var asobject = {};
  asobject.object = newAsset
  $.session.set("AssetName",assetName);
  postTemplateAsset(asobject,callback);
}

function putTemplateAsset(json){
  var ursl = serverIP + "/api/template_assets/name/"+ encodeURIComponent(json.theName) + "?session_id=" + String($.session.get('sessionID'));
  var output = {};
  output.object = json;
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
    url: ursl,
    success: function (data) {
      showPopup(true);
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function postTemplateAsset(json,callback){
  var ursl = serverIP + "/api/template_assets?session_id=" + String($.session.get('sessionID'));
  var output = JSON.stringify(json);

  $.ajax({
    type: "POST",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: ursl,
    success: function (data) {
      showPopup(true);
      if(typeof(callback) == "function"){
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

mainContent.on('click','td.template-asset-interface',function(){
  var intRow = $(this).closest("tr");
  var selectedInt = {};
  selectedInt.theName = intRow.find("td:eq(1)").text();
  selectedInt.theType = intRow.find("td:eq(2)").text();
  selectedInt.theAccessRight = intRow.find("td:eq(3)").text();
  selectedInt.thePrivilege = intRow.find("td:eq(4)").text();

  $('#addInterfaceDialog').attr('data-selectedInterface',JSON.stringify(selectedInt));
  $('#addInterfaceDialog').attr('data-selectedIndex',intRow.index());
  $("#addInterfaceDialog").attr('data-updateinterface',"updateTemplateAssetInterface");
  $('#addInterfaceDialog').modal('show');
});


mainContent.on('click','#addTemplateAssetInterface',function() {
  $('#addInterfaceDialog').removeAttr('data-selectedInterface');
  $('#addInterfaceDialog').removeAttr('data-selectedIndex');
  $("#addInterfaceDialog").attr('data-updateinterface',"updateTemplateAssetInterface");
  $('#addInterfaceDialog').modal('show');
});

function updateTemplateAssetInterface() {
  var selectedInt = {};
  selectedInt.theInterfaceName = $('#theInterfaceName').val();
  selectedInt.theInterfaceType = $('#theInterfaceType').val();
  selectedInt.theAccessRight = $('#theAccessRight').val();
  selectedInt.thePrivilege = $('#thePrivilege').val();

  var ta = JSON.parse($.session.get("TemplateAsset"));
  var selectedIdx = $('#addInterfaceDialog').attr('data-selectedIndex');
  if (selectedIdx != undefined) {
    ta.theInterfaces[selectedIdx] = selectedInt;
    $.session.set("TemplateAsset", JSON.stringify(ta));
    $('#theTemplateAssetInterfaces').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(selectedInt.theInterfaceName);
    $('#theTemplateAssetInterfaces').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(2)').text(selectedInt.theInterfaceType);
    $('#theTemplateAssetInterfaces').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(3)').text(selectedInt.theAccessRight);
    $('#theTemplateAssetInterfaces').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(4)').text(selectedInt.thePrivilege);
  }
  else {
    ta.theInterfaces.push(selectedInt);
    $.session.set("TemplateAsset", JSON.stringify(ta));
    appendTemplateAssetInterface(selectedInt);
  }
  $('#addInterfaceDialog').modal('hide');
}


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

$("#templateRequirementsClick").click(function(){
  validateClick('template_requirement',function() {
    $('#menuBCClick').attr('dimension','template_requirement');
    refreshMenuBreadCrumb('template_requirement');
  });
});

function createTemplateRequirementsTable(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/template_requirements",
    success: function (data) {
      setTableHeader("TemplateRequirements");
      fillTemplateRequirementsTable(data, function(){
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

function fillTemplateRequirementsTable(data, callback){
  var theTable = $(".theTable");
  var textToInsert = [];
  var i = 0;

  $.each(data, function(count, item) {
    textToInsert[i++] = '<tr>'

    textToInsert[i++] = '<td class="deleteTemplateRequirementButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';

    textToInsert[i++] = '<td class="template-requirement-rows" name="theName" value="' + item.theName + '">';
    textToInsert[i++] = item.theName;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '<td name="theType">';
    textToInsert[i++] = item.theType;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '</tr>';

  });
  theTable.append(textToInsert.join(''));
  $.contextMenu('destroy',$('.requirement-rows'));
  theTable.css("visibility","visible");
  $("#mainTable").find("tbody").removeClass();

  callback();
}

$(document).on('click', "td.template-requirement-rows", function(){
  var trName = $(this).attr('value');
  refreshObjectBreadCrumb(trName);
  viewTemplateRequirement(trName);
});

function viewTemplateRequirement(trName) {
  activeElement("objectViewer");
  $.session.set("TemplateRequirementName", trName.trim());

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/template_requirements/name/" + encodeURIComponent(trName),
    success: function (data) {
      fillOptionMenu("fastTemplates/editTemplateRequirementOptions.html","#objectViewer",null,true,true, function(){
        $("#UpdateTemplateRequirement").text("Update");
        $.ajax({
          type: "GET",
          dataType: "json",
          accept: "application/json",
          data: {
            session_id: String($.session.get('sessionID'))
          },
          crossDomain: true,
          url: serverIP + "/api/dimensions/table/template_asset",
          success: function (tas) {
            $("#theTemplateAssetName option").remove();
            $.each(tas,function(idx,ta) {
              $('#theTemplateAssetName').append($("<option></option>").attr("value",ta).text(ta));
            });
          },
          error: function (xhr, textStatus, errorThrown) {
            var error = JSON.parse(xhr.responseText);
            showPopup(false, String(error.message));
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
          }
        });
        $('#editTemplateRequirementOptionsForm').validator();
        $('#theName').val(data.theName);
        $('#theTemplateAssetName').val(data.theAssetName);
        $('#theType').val(data.theType);
        $('#theDescription').val(data.theDescription);
        $('#theRationale').val(data.theRationale);
        $('#theFitCriterion').val(data.theFitCriterion);
        $.session.set("TemplateRequirement", JSON.stringify(data));
        $('#editTemplateRequirementOptionsDorm').loadJSON(data,null);
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

$(document).on('click', "#addTemplateRequirement",function(){
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editTemplateRequirementOptions.html","#objectViewer",null,true,true,function(){
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/dimensions/table/template_asset",
      success: function (tas) {
        $("#UpdateTemplateRequirement").text("Create");
        $("#theTemplateAssetName option").remove();
        $.each(tas,function(idx,ta) {
          $('#theTemplateAssetName').append($("<option></option>").attr("value",ta).text(ta));
        });
      },
      error: function (xhr, textStatus, errorThrown) {
        var error = JSON.parse(xhr.responseText);
        showPopup(false, String(error.message));
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
    $.session.set("TemplateRequirement", JSON.stringify(jQuery.extend(true, {},templateRequirementDefault )));
    $("#editTemplateRequirementOptionsForm").addClass("new");
  });
});

$(document).on('click', "td.deleteTemplateRequirementButton",function(e){
  var trName = $(this).find('i').attr('value');
  e.preventDefault();
  deleteObject('template_requirement',trName, function(trName) {

    $.ajax({
      type: "DELETE",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID')),
        name: trName
      },
      crossDomain: true,
      url: serverIP + "/api/template_requirements/name/" + encodeURIComponent(trName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        $.ajax({
          type: "GET",
          dataType: "json",
          accept: "application/json",
          data: {
            session_id: String($.session.get('sessionID'))
          },
          crossDomain: true,
          url: serverIP + "/api/template_requirements",
          success: function (data) {
            setTableHeader("TemplateRequirements");
            fillTemplateRequirementsTable(data, function(){
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

mainContent.on('click', '#UpdateTemplateRequirement',function(e){
  e.preventDefault();
  var tr = $.session.get("TemplateRequirement");
  if($("#editTemplateRequirementOptionsForm").hasClass("new")){
    postTemplateRequirementForm($("#editTemplateRequirementOptionsForm"), function(){createTemplateRequirementsTable();});
  }
  else{
    putTemplateRequirementForm($("#editTemplateRequirementOptionsForm"));
    createTemplateRequirementsTable();
  }
});

mainContent.on('click', '#CloseTemplateRequirement', function (e) {
  e.preventDefault();
  createTemplateRequirementsTable();
});

function templateRequirementFormToJSON(data){
  var json =  JSON.parse($.session.get("TemplateRequirement"));
  json.theName = $(data).find('#theName').val();

  json["theName"] = $(data).find('#theName').val();
  json["theAssetName"] = $(data).find('#theTemplateAssetName option:selected').text().trim();
  json["theType"] = $(data).find('#theType option:selected').text().trim();
  json["theDescription"] = $(data).find('#theDescription').val();
  json["theRationale"] = $(data).find('#theRationale').val();
  json["theFitCriterion"] = $(data).find('#theFitCriterion').val();
  return json
}

function putTemplateRequirementForm(data){
  putTemplateRequirement(templateRequirementFormToJSON(data));
}

function postTemplateRequirementForm(data,callback){
  var newReq = templateRequirementFormToJSON(data);
  var trName = $(data).find('#theName').val();
  var trobject = {};
  trobject.object = newReq
  $.session.set("RequirementName",newReq.theName);
  postTemplateRequirement(trobject,callback);
}

function putTemplateRequirement(json){
  var ursl = serverIP + "/api/template_requirements/name/"+ encodeURIComponent(json.theName) + "?session_id=" + String($.session.get('sessionID'));
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

function postTemplateRequirement(json,callback){
  var ursl = serverIP + "/api/template_requirements?session_id=" + String($.session.get('sessionID'));
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

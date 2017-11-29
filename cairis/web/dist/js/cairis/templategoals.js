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

$("#templateGoalsClick").click(function(){
  clearLocalStorage($('#menuBCClick').attr('dimension'));
  $('#menuBCClick').attr('dimension','template_goal');
  refreshMenuBreadCrumb('template_goal');
});

function createTemplateGoalsTable(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/template_goals",
    success: function (data) {
      setTableHeader("TemplateGoals");
      fillTemplateGoalsTable(data, function(){
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

function fillTemplateGoalsTable(data, callback){
  var theTable = $(".theTable");
  var textToInsert = [];
  var i = 0;

  $.each(data, function(count, item) {
    textToInsert[i++] = '<tr>'

    textToInsert[i++] = '<td class="deleteTemplateGoalButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';

    textToInsert[i++] = '<td class="template-goal-rows" name="theName" value="' + item.theName + '">';
    textToInsert[i++] = item.theName;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '<td name="theDefinition">';
    textToInsert[i++] = item.theDefinition;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '</tr>';

  });
  theTable.append(textToInsert.join(''));
  $.contextMenu('destroy',$('.goal-rows'));
  theTable.css("visibility","visible");
  $("#mainTable").find("tbody").removeClass();

  callback();
}

$(document).on('click', "td.template-goal-rows", function(){
  var tgName = $(this).attr('value');
  refreshObjectBreadCrumb(tgName);
  viewTemplateGoal(tgName);
});

function viewTemplateGoal(tgName) {
  activeElement("objectViewer");
  $.session.set("TemplateGoalName", tgName.trim());

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/template_goals/name/" + encodeURIComponent(tgName),
    success: function (data) {
      fillOptionMenu("fastTemplates/editTemplateGoalOptions.html","#objectViewer",null,true,true, function(){
        $('#editTemplateGoalOptionsForm').validator();
        $("#UpdateTemplateGoal").text("Update");
        $('#theName').val(data.theName);
        $('#theDefinition').val(data.theDefinition);
        $('#theRationale').val(data.theRationale);
        $.each(data.theConcerns,function(idx,concern) {
          appendTemplateGoalConcern(concern);
        });
        $.each(data.theResponsibilities,function(idx,responsibility) {
          appendTemplateGoalResponsibility(responsibility);
        });
        $.session.set("TemplateGoal", JSON.stringify(data));
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

function appendTemplateGoalConcern(concern) {
   $("#theTemplateGoalConcerns").find("tbody").append("<tr><td class='removeTemplateGoalConcern'><i class='fa fa-minus'></i></td><td class='template-goal-concern'>" + concern + "</td></tr>").animate('slow');
}

function appendTemplateGoalResponsibility(responsibility) {
   $("#theTemplateGoalResponsibilities").find("tbody").append("<tr><td class='removeTemplateGoalResponsibilities'><i class='fa fa-minus'></i></td><td class='template-goal-responsibility'>" + responsibility + "</td></tr>").animate('slow');
}

$(document).on('click', "#addTemplateGoal",function(){
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editTemplateGoalOptions.html","#objectViewer",null,true,true,function(){
    $('#editTemplateGoalOptionsForm').validator();
    $("#UpdateTemplateGoal").text("Create");
    $.session.set("TemplateGoal", JSON.stringify(jQuery.extend(true, {},templateGoalDefault )));
    $("#editTemplateGoalOptionsForm").addClass("new");
  });
});

$(document).on('click', "td.deleteTemplateGoalButton",function(e){
  var tgName = $(this).find('i').attr('value');
  e.preventDefault();
  deleteObject('template_goal',tgName, function(tgName) {

    $.ajax({
      type: "DELETE",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID')),
        name: tgName
      },
      crossDomain: true,
      url: serverIP + "/api/template_goals/name/" + encodeURIComponent(tgName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        $.ajax({
          type: "GET",
          dataType: "json",
          accept: "application/json",
          data: {
            session_id: String($.session.get('sessionID'))
          },
          crossDomain: true,
          url: serverIP + "/api/template_goals",
          success: function (data) {
            setTableHeader("TemplateGoals");
            fillTemplateGoalsTable(data, function(){
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

var mainContent = $("#objectViewer");

function commitTemplateGoal(){
  var tg = $.session.get("TemplateGoal");
  if($("#editTemplateGoalOptionsForm").hasClass("new")){
    postTemplateGoalForm($("#editTemplateGoalOptionsForm"), function(){createTemplateGoalsTable();});
    $("#editTemplateGoalOptionsForm").removeClass("new");
  }
  else{
    putTemplateGoalForm($("#editTemplateGoalOptionsForm"));
    createTemplateGoalsTable();
  }
}

mainContent.on('click', '#CloseTemplateGoal', function (e) {
  e.preventDefault();
  clearLocalStorage('template_goal');
  createTemplateGoalsTable();
});

function templateGoalFormToJSON(data){
  var json =  JSON.parse($.session.get("TemplateGoal"));
  json.theName = $(data).find('#theName').val();
  json.theDefinition = $(data).find('#theDefinition').val();
  json.theRationale = $(data).find('#theRationale').val();
  return json
}

function putTemplateGoalForm(data){
  putTemplateGoal(templateGoalFormToJSON(data));
}

function postTemplateGoalForm(data,callback){
  var newGoal = templateGoalFormToJSON(data);
  var tgName = $(data).find('#theName').val();
  var tgobject = {};
  tgobject.object = newGoal
  $.session.set("GoalName",newGoal.theName);
  postTemplateGoal(tgobject,callback);
}

function putTemplateGoal(json){
  var ursl = serverIP + "/api/template_goals/name/"+ encodeURIComponent(json.theName) + "?session_id=" + String($.session.get('sessionID'));
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
      clearLocalStorage('template_goal');
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

function postTemplateGoal(json,callback){
  var ursl = serverIP + "/api/template_goals?session_id=" + String($.session.get('sessionID'));
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
      clearLocalStorage('template_goal');
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

mainContent.on("click", "#addTemplateGoalConcern", function(){
  $("#addTemplateGoalConcernDialog").modal('show');
});

mainContent.on('click','td.template-goal-concern',function(){
  var concernRow = $(this).closest("tr");
  selectedConcern = concernRow.find("td:eq(1)").text();
  $('#addTemplateGoalConcernDialog').attr('data-selectedConcern',selectedConcern);
  $('#addTemplateGoalConcernDialog').attr('data-selectedIndex',concernRow.index());
  $('#addTemplateGoalConcernDialog').modal('show');
});



$(document).on('shown.bs.modal','#addTemplateGoalConcernDialog',function() {
  var selectedConcern = $('#addTemplateGoalConcernDialog').attr('data-selectedConcern');
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/template_asset",
    success: function (concerns) {
      $("#theTemplateGoalConcern option").remove();
      $.each(concerns,function(idx,concern) {
        $('#theTemplateGoalConcern').append($("<option></option>").attr("value",concern).text(concern));
      });
      if (selectedConcern != undefined) {
        $('#theTemplateGoalConcern').val(selectedConcern);
      }
      else {
        $('#theTemplateGoalConcern').val('');
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

mainContent.on('click','#AddTemplateGoalConcern',function() {
  var selectedConcern = $('#theTemplateGoalConcern').val();
  var tg = JSON.parse($.session.get("TemplateGoal"));
  var selectedIdx = $('#addTemplateGoalConcernDialog').attr('data-selectedIndex');
  if (selectedIdx != undefined) {
    tg.theConcerns[selectedIdx] = selectedConcern;
    $.session.set("TemplateGoal", JSON.stringify(tg));
    $('#theTemplateGoalConcerns').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(selectedConcern);
  }
  else {
    tg.theConcerns.push(selectedConcern);
    $.session.set("TemplateGoal", JSON.stringify(tg));
    appendTemplateGoalConcern(selectedConcern);
  }
  $('#addTemplateGoalConcernDialog').modal('hide');
});

mainContent.on('click','td.removeTemplateGoalConcern',function() {
  var concRow = $(this).closest("tr");
  var rowIdx = concRow.index();
  concRow.remove();
  var tg = JSON.parse($.session.get("TemplateGoal"));
  tg.theConcerns.splice(rowIdx,1);
  $.session.set("TemplateGoal", JSON.stringify(tg));
});


mainContent.on("click", "#addTemplateGoalResponsibility", function(){
  $("#addTemplateGoalResponsibilityDialog").modal('show');
});

mainContent.on('click','td.template-goal-responsibility',function(){
  var respRow = $(this).closest("tr");
  selectedResp = respRow.find("td:eq(1)").text();
  $('#addTemplateGoalResponsibilityDialog').attr('data-selectedResponsibility',selectedResponsibility);
  $('#addTemplateGoalResponsibilityDialog').attr('data-selectedIndex',respRow.index());
  $('#addTemplateGoalResponsibilityDialog').modal('show');
});

$(document).on('shown.bs.modal','#addTemplateGoalResponsibilityDialog',function() {
  var selectedResponsibility = $('#addTemplateGoalResponsibilityDialog').attr('data-selectedResponsibility');
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/role",
    success: function (responsibilities) {
      $("#theTemplateGoalResponsibility option").remove();
      $.each(responsibilities,function(idx,responsibility) {
        $('#theTemplateGoalResponsibility').append($("<option></option>").attr("value",responsibility).text(responsibility));
      });
      if (selectedResponsibility != undefined) {
        $('#theTemplateGoalResponsibility').val(selectedResponsibility);
      }
      else {
        $('#theTemplateGoalResponsibility').val('');
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

mainContent.on('click','#AddTemplateGoalResponsibility',function() {
  var selectedResp = $('#theTemplateGoalResponsibility').val();
  var tg = JSON.parse($.session.get("TemplateGoal"));
  var selectedIdx = $('#addTemplateGoalResponsibilityDialog').attr('data-selectedIndex');
  if (selectedIdx != undefined) {
    tg.theResponsibilities[selectedIdx] = selectedResp;
    $.session.set("TemplateGoal", JSON.stringify(tg));
    $('#theTemplateGoalResponsibilities').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(selectedResp);
  }
  else {
    tg.theResponsibilities.push(selectedResp);
    $.session.set("TemplateGoal", JSON.stringify(tg));
    appendTemplateGoalResponsibility(selectedResp);
  }
  $('#addTemplateGoalResponsibilityDialog').modal('hide');
});

mainContent.on('click','td.removeTemplateGoalResponsibility',function() {
  var respRow = $(this).closest("tr");
  var rowIdx = respRow.index();
  respRow.remove();
  var tg = JSON.parse($.session.get("TemplateGoal"));
  tg.theResponsibilities.splice(rowIdx,1);
  $.session.set("TemplateGoal", JSON.stringify(tg));
});

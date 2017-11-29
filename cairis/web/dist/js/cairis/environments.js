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


$(document).on('click', "td.environment-rows",function(){
  activeElement("objectViewer");
  var name = $(this).text();
  refreshObjectBreadCrumb(name);
  $.session.set("EnvironmentName", name);

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/name/" + encodeURIComponent(name),
    success: function (data) {
      fillOptionMenu("fastTemplates/editEnvironmentOptions.html", "#objectViewer", null, true, true, function () {
        $("#UpdateEnvironment").text("Update");
        $.session.set("Environment", JSON.stringify(data));
        $('#editEnvironmentOptionsform').loadJSON(data, null);
        $.each(data.theTensions, function (index, tension) {
          setTimeout(function () {
            var comboID = "#" + tension.attr_id + "-" + tension.base_attr_id;
            $(comboID).val(String(tension.value));
            $(comboID).attr("rationale", tension.rationale);
          }, 10);
        });
        $.each(data.theEnvironments, function (index, env) {
          $("#envToEnvTable").append("<tr><td><i class='fa fa-minus'></i></td><td>" + env + "</td></tr>");
          $("#overrideCombobox").append($("<option />").text(env));
        });
        switch (data.theDuplicateProperty) {
          case "Maximise":
            $("#MaximiseID").prop('checked', true);
            break;
          case "Override":
            $("#OverrideID").prop('checked', true);
            $("#overrideCombobox").prop("disabled", false);
            break;
          case "None":
            $("#overrideCombobox").prop("disabled", false);
            $("#OverrideID").prop('checked', false);
            $("#MaximiseID").prop('checked', false);
            break;
        }
        $("#editEnvironmentOptionsform").validator('update');
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

$(document).on('click', "td.deleteEnvironmentButton",function(e){
  e.preventDefault();
  var envName = $(this).find('i').attr("value");
  deleteObject('environment',envName,function(envName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/environments/name/" + encodeURIComponent(envName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        showPopup(true);
        $('#menuBCClick').attr('dimension','environment');
        refreshMenuBreadCrumb('environment');
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


$("#environmentsClick").click(function () {
  clearLocalStorage($('#menuBCClick').attr('dimension'));
  $('#menuBCClick').attr('dimension','environment');
  refreshMenuBreadCrumb('environment');
});

$("#environmentMenuClick").click(function () {
  clearLocalStorage($('#menuBCClick').attr('dimension'));
  $('#menuBCClick').attr('dimension','environment');
  refreshMenuBreadCrumb('environment');
});

var mainContent = $("#objectViewer");
mainContent.on('change', "#OverrideID", function () {
  if($("#OverrideID").prop("checked")){
    $("#overrideCombobox").prop("disabled",false);
  }
});

mainContent.on('change', "#MaximiseID", function () {
  if($("#MaximiseID").prop("checked")){
    $("#overrideCombobox").prop("disabled",true);
  }
});

mainContent.on('click', ".removeEnvinEnv", function () {
  var text = $(this).next().text();
  $(this).closest("tr").remove();
  $("#overrideCombobox").find("option").each(function () {
    var optionText = $(this).text();
    if(optionText == text){
      $(this).remove();
    }
  });
  if ($('#envToEnvTable').find("tbody").is(':empty')){
    $("input:radio[name='duplication']").each(function(i) {
      this.checked = false;
    });
  }
});

// For the rationale in the environments edit
mainContent.on("click", ".tensionCombobox", function () {
  mainContent.find("#rationale").val(String($(this).attr("rationale")));
  $.session.set("tensionMatrix", this.id);
});

mainContent.on("keyup", "#rationale", function () {
  $("#"+ $.session.get("tensionMatrix")).attr("rationale", $(this).val());
});

mainContent.on("click", "#addEnvtoEnv", function () {
  var filterList = [];
  $("#envToEnvTable").find(".envInEnv").each(function(index, env){
    filterList.push($(env).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'environment',undefined,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','environment');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addEnvToEnv');
    $('#chooseEnvironment').modal('show');
  },filterList);

});

function addEnvToEnv() {
  var text =  $("#chooseEnvironmentSelect").val();
  $("#envToEnvTable").append("<tr><td class='removeEnvinEnv'><i class='fa fa-minus'></i></td><td class='envInEnv'>"+ text +"</td></tr>");
  $("#overrideCombobox").append("<option value='" + text + "'>" + text + "</option>");
  $('#chooseEnvironment').modal('hide');
};


function commitEnvironment() {
    var env = JSON.parse($.session.get("Environment"));
    var oldName = env.theName;
    env =  fillupEnvironmentObject(env);
    $.session.set("Environment", env);
    if($("#editEnvironmentOptionsform").hasClass("newEnvironment")){
      $("#editEnvironmentOptionsform").removeClass("newEnvironment");
      postEnvironment(env, function () {
        clearLocalStorage('environment');
        $('#menuBCClick').attr('dimension','environment');
        refreshMenuBreadCrumb('environment');
      });
    }
    else {
      putEnvironment(env, oldName, function () {
        clearLocalStorage('environment');
        $('#menuBCClick').attr('dimension','environment');
        refreshMenuBreadCrumb('environment');
      });
    }
}


$("#mainTable").on("click", "#addNewEnvironment", function () {
  refreshObjectBreadCrumb('New Environment');
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editEnvironmentOptions.html", "#objectViewer", null, true, true, function () {
    $("#editEnvironmentOptionsform").validator();
    $("#UpdateEnvironment").text("Create");
    $("#editEnvironmentOptionsform").addClass("newEnvironment");
    $.session.set("Environment", JSON.stringify(jQuery.extend(true,{},environmentDefault)));
  });
});


function fillupEnvironmentObject(env) {
  env.theName = $("#theName").val();
  env.theShortCode = $("#theShortCode").val();
  env.theDescription = $("#theDescription").val();

  env.theTensions = [];
  env.theDuplicateProperty = "";

  var tensions = [];
  $("#tensionsTable").find("td").each(function() {
    var attr = $(this).find("select").attr('rationale');
    if(typeof attr !== typeof undefined && attr !== false) {
      var env = JSON.parse($.session.get("Environment"));
      var select = $(this).find("select");
      var tension = jQuery.extend(true, {}, tensionDefault);
      tension.rationale = select.attr("rationale");
      tension.value = parseInt(select.val());
      var ids = select.attr("id");
      var values = ids.split('-');
      tension.attr_id = parseInt(values[0]);
      tension.base_attr_id = parseInt(values[1]);
      env.theTensions.push(tension);
    }
  });

  var envInEnv = [];
  $("#envToEnvTable").find("tbody").find("tr .removeEnvinEnv").each(function () {
    envInEnv.push($(this).next("td").text());
  });
  env.theEnvironments = envInEnv;
  env.theDuplicateProperty = $("input:radio[name ='duplication']:checked").val();
  if(env.theDuplicateProperty == "" || env.theDuplicateProperty == undefined){
    env.theDuplicateProperty = "None";
    env.theOverridingEnvironment = $('#overrideCombobox').val();
  }

  var theEnvinEnvArray = [];
  $("#overrideCombobox").find("option").each(function (index, option) {
    theEnvinEnvArray.push($(option).text());
  });
  env.theEnvironments = theEnvinEnvArray;
  return env;
}

function createEnvironmentsTable(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments",
    success: function (data) {
      setTableHeader("Environment");
      fillEnvironmentsTable(data, function(){
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

mainContent.on('click', '#CloseEnvironment', function (e) {
  e.preventDefault();
  clearLocalStorage('environment');
  $('#menuBCClick').attr('dimension','environment');
  refreshMenuBreadCrumb('environment');
});

function fillEnvironmentsTable(data, callback){
  var theTable = $("#mainTable");
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
    textToInsert[i++] = '<td class="deleteEnvironmentButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';
    textToInsert[i++] = '<td class="environment-rows" name="theName">';
    textToInsert[i++] = item.theName;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '<td name="theType">';
    textToInsert[i++] = item.theDescription;
    textToInsert[i++] = '</td></tr>';
  }
  theTable.append(textToInsert.join(''));
  $.contextMenu('destroy',$('.requirement-rows'));
  theTable.css("visibility","visible");
  $("#mainTable").find("tbody").removeClass();

  callback();
}

function putEnvironment(environment, oldName, callback){
  var output = {};
  output.object = environment;
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
    url: serverIP + "/api/environments/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
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

function postEnvironment(environment, callback){
  var output = {};
  output.object = environment;
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
    url: serverIP + "/api/environments" + "?session_id=" + $.session.get('sessionID'),
    success: function (data) {
      showPopup(true);
      if(jQuery.isFunction(callback)){
        callback();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false);
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}


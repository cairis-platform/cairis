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
  $.session.set("EnvironmentName", name);

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/name/" + name.replace(" ", "%20"),
    success: function (data) {
      fillOptionMenu("fastTemplates/editEnvironmentOptions.html", "#objectViewer", null, true, true, function () {
        $.session.set("editableEnvironment", JSON.stringify(data));
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
      });
    },
    error: function (xhr, textStatus, errorThrown) {
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
      url: serverIP + "/api/environments/name/" + envName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        createEnvironmentsTable();
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





$("#environmentsClick").click(function () {
  createEnvironmentsTable();
});

$("#environmentMenuClick").click(function () {
  createEnvironmentsTable();
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
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/all/names",
    success: function (data) {
      $("#comboboxDialogSelect").empty();
      var none = true;
      $.each(data, function(i, item) {
        var found = false;
        $("#overrideCombobox").find("option").each(function() {
          if(this.innerHTML.trim() == item){
            found = true
          }
        });
        //if not found in environments
        if(!found) {
          $("#comboboxDialogSelect").append("<option value=" + item + ">" + item + "</option>");
          none = false;
        }
      });
      if(!none) {
        $("#comboboxDialog").dialog({
          modal: true,
          buttons: {
            Ok: function () {
              var text =  $( "#comboboxDialogSelect").find("option:selected" ).text();
              $("#envToEnvTable").append("<tr><td class='removeEnvinEnv'><i class='fa fa-minus'></i></td><td>"+ text +"</td></tr>");
              $("#overrideCombobox").append("<option value='" + text + "'>" + text + "</option>");
              $(this).dialog("close");
            }
          }
        });
        $(".comboboxD").css("visibility", "visible");
      }
      else {
        alert("All environments are already added");
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

mainContent.on('click', "#updateButtonEnvironment", function (e) {

  e.preventDefault();
  var env = JSON.parse($.session.get("editableEnvironment"));
  env =  fillupEnvironmentObject(env);
  $.session.set("editableEnvironment", env);
  if($("#editEnvironmentOptionsform").hasClass("newEnvironment")){
    $("#editEnvironmentOptionsform").removeClass("newEnvironment");
    postEnvironment(env, function () {
      createEnvironmentsTable();
    });
  }
  else {
    var oldName = env.theName;
    putEnvironment(env, oldName, function () {
      createEnvironmentsTable();
    });
  }
});


$("#reqTable").on("click", "#addNewEnvironment", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editEnvironmentOptions.html", "#objectViewer", null, true, true, function () {
    $("#editEnvironmentOptionsform").addClass("newEnvironment");
    $.session.set("editableEnvironment", JSON.stringify(jQuery.extend(true,{},environmentDefault)));
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
      var env = JSON.parse($.session.get("editableEnvironment"));
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
  var theDupProp = $("input:radio[name ='duplication']:checked").val();
  if(theDupProp == "" || theDupProp == undefined){
    theDupProp = "None";
  }

  var theEnvinEnvArray = [];
  env.theOverridingEnvironment = theDupProp;
  $("#overrideCombobox").find("option").each(function (index, option) {
    //This is for adding env to env, but wait!! first need to remove them when presssed minus!
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
      window.activeTable = "Environment";
      setTableHeader();
      fillEnvironmentsTable(data, function(){
        newSorting(1);
      });
      activeElement("reqTable");
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

mainContent.on('click', '#CloseEnvironment', function (e) {
  e.preventDefault();
  createEnvironmentsTable();
});

function fillEnvironmentsTable(data, callback){
  var theTable = $("#reqTable");
  var textToInsert = [];
  var i = 0;

  $.each(data, function(count, item) {
    textToInsert[i++] = "<tr>";
    textToInsert[i++] = '<td class="deleteEnvironmentButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';
    textToInsert[i++] = '<td class="environment-rows" name="theName">';
    textToInsert[i++] = item.theName;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '<td name="theType">';
    textToInsert[i++] = item.theDescription;
    textToInsert[i++] = '</td></tr>';
  });
  theTable.append(textToInsert.join(''));
  $.contextMenu('destroy',$('.requirement-rows'));
  $("#reqTable").find("tbody").removeClass();

  callback();
}

function putEnvironment(environment, oldName, callback){
  var output = {};
  output.object = environment;
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
    url: serverIP + "/api/environments/name/" + oldName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
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

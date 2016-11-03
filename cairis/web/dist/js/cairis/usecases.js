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

$("#useCaseClick").click(function () {
  createUseCasesTable();
});

function createUseCasesTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/usecases",
    success: function (data) {
      window.activeTable = "UseCases";
      setTableHeader();
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td class="deleteUseCaseButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="usecase-rows" name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theDescription">';
        textToInsert[i++] = item.theDescription;
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

$(document).on('click', "td.usecase-rows", function () {
  activeElement("objectViewer");
  var name = $(this).text();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/usecases/name/" + name.replace(" ", "%20"),
    success: function (data) {
      fillOptionMenu("fastTemplates/editUseCaseOptions.html", "#objectViewer", null, true, true, function () {
        $.session.set("UseCase", JSON.stringify(data));
        $('#editUseCaseOptionsForm').loadJSON(data, null);
        $.each(data.theActors, function (index, actor) {
          appendUseCaseActor(actor);
        });
        $("#theEnvironments").find(".usecaseEnvironment:first").trigger('click');

        if (data.theTags.length > 0) {
          var text = "";
          $.each(data.theTags, function (index, type) {
            text += type;
            if (index < (data.theTags.length - 1)) {
              text += ", ";
            }
          });
          $("#theTags").val(text);
        }

        $.each(data.theEnvironmentProperties, function (index, env) {
          appendUseCaseEnvironment(env.theEnvironmentName);
        });
        $("#theEnvironments").find(".usecaseEnvironment:first").trigger('click');
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});


var mainContent = $("#objectViewer");
mainContent.on("click",".usecaseEnvironment", function () {
  clearUseCaseEnvInfo();
  var usecase = JSON.parse($.session.get("UseCase"));
  var theEnvName = $(this).text();
  $.session.set("usecaseEnvironmentName", theEnvName);
  $.each(usecase.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $('#thePreCond').val(env.thePreCond);
      $('#thePostCond').val(env.thePostCond);
      for (var i = 0; i < env.theSteps.length; i++) {
        appendUseCaseStep(env.theSteps[i].theStepText);
      }
    }
  });
});

function clearUseCaseEnvInfo(){
  $("#thePreCond").val('');
  $("#thePostCond").val('');
  $("#theSteps").find("tbody").empty();
}

function appendUseCaseEnvironment(environment){
  $("#theEnvironments").find("tbody").append('<tr><td class="deleteUseCaseEnv"><i class="fa fa-minus"></i></td><td class="usecaseEnvironment">'+environment+'</td></tr>');
}

function appendUseCaseStep(stepTxt) {
  $("#theSteps").find("tbody").append("<tr><td class='removeUseCaseStep'><i class='fa fa-minus'></i></td><td class='usecaseStep'>" + stepTxt + "</td></tr>").animate('slow');
}

function appendUseCaseActor(actor) {
  $("#theActors").find("tbody").append("<tr><td class='removeActor'><i class='fa fa-minus'></i></td><td class='usecaseActor'>" + actor + "</td></tr>").animate('slow');
}

mainContent.on('click', '#addActorToUseCase', function () {
  var hasActor = [];
  $("#theActors").find(".usecaseActor").each(function(index, actor){
    hasActor.push($(actor).text());
  });
  roleDialogBox(hasActor, function (text) {
    var usecase = JSON.parse($.session.get("UseCase"));
    usecase.theActors.push(text);
    $.session.set("UseCase", JSON.stringify(usecase));
    appendUseCaseActor(text);
  });
});

mainContent.on('click', '#addStepToUseCase', function () {
  stepDialogBox(function (text) {
    var usecase = JSON.parse($.session.get("UseCase"));
    var theEnvName = $.session.get("usecaseEnvironmentName");
    $.each(usecase.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        var s = {
          "theStepText" : text,
          "theSynopsis": "",
          "theActor": "",
          "theActorType" : "",
          "theTags" : []};
        env.theSteps.push(s);
        appendUseCaseStep(text);
      }
    });
    $.session.set("UseCase", JSON.stringify(usecase));
  });
});

mainContent.on('click', ".removeUseCaseActor", function () {
  var text = $(this).next(".usecaseActor").text();
  $(this).closest("tr").remove();
  var usecase = JSON.parse($.session.get("UseCase"));
  $.each(usecase.theActors, function (index2, actor) {
    if(actor == text){
      usecase.theSteps.splice( index2 ,1 );
      $.session.set("UseCase", JSON.stringify(usecase));
      return false;
    }
  });
});


mainContent.on('click', ".removeUseCaseStep", function () {
  var text = $(this).next(".usecaseStep").text();
  $(this).closest("tr").remove();
  var usecase = JSON.parse($.session.get("UseCase"));
  var theEnvName = $.session.get("usecaseEnvironmentName");
  $.each(usecase.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theSteps, function (index2, step) {
        if(step.theStepText == text){
          env.theSteps.splice( index2 ,1 );
          $.session.set("UseCase", JSON.stringify(usecase));
          return false;
        }
      });
    }
  });
});

mainContent.on('click', ".deleteUseCaseEnv", function () {
  var envi = $(this).next(".usecaseEnvironment").text();
  $(this).closest("tr").remove();
  var usecase = JSON.parse($.session.get("UseCase"));
  $.each(usecase.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == env){
      usecase.theEnvironmentProperties.splice( index ,1 );
      $.session.set("UseCase", JSON.stringify(usecase));
      clearUseCaseEnvInfo();

      var UIenv = $("#theUseCaseEnvironments").find("tbody");
      if(jQuery(UIenv).has(".usecaseEnvironment").length){
        UIenv.find(".usecaseEnvironment:first").trigger('click');
      }else{
        $("#Properties").hide("fast");
      }

      return false;
    }
  });
});

mainContent.on("click", "#addUseCaseEnv", function () {
  var hasEnv = [];
  $(".usecaseEnvironment").each(function (index, tag) {
    hasEnv.push($(tag).text());
  });
  environmentDialogBox(hasEnv, function (text) {
    appendUseCaseEnvironment(text);
    var environment =  jQuery.extend(true, {},useCaseEnvDefault );
    environment.theEnvironmentName = text;
    var usecase = JSON.parse($.session.get("UseCase"));
    usecase.theEnvironmentProperties.push(environment);
    $.session.set("UseCase", JSON.stringify(usecase));
    $(document).find(".usecaseEnvironment").each(function () {
      if($(this).text() == text){
        $(this).trigger("click");
        $("#Properties").show("fast");
      }
    });
  });
});

mainContent.on('click', '#UpdateUseCase', function (e) {
  e.preventDefault();
  var usecase = JSON.parse($.session.get("UseCase"));
  var oldName = usecase.theName;
  usecase.theName = $("#theName").val();
  usecase.theAuthor = $("#theAuthor").val();
  usecase.theObjective = $("#theObjective").val();
  var tags = $("#theTags").text().split(", ");
  if(tags[0] != ""){
    usecase.theTags = tags;
  }

  var envName = $.session.get("usecaseEnvironmentName");
  var updatedEnvProps = [];
  $.each(usecase.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      env.thePreCond = $('#thePreCond').val();
      env.thePostCond = $('#thePostCond').val();
    }
    updatedEnvProps.push(env);
  });
  usecase.theEnvironmentProperties = updatedEnvProps;


  if($("#editUseCaseOptionsForm").hasClass("new")){
    postUseCase(usecase, function () {
      createUseCasesTable();
      $("#editUseCaseOptionsForm").removeClass("new")
    });
  } 
  else {
    putUseCase(usecase, oldName, function () {
      createUseCasesTable();
    });
  }
});

$(document).on('click', 'td.deleteUseCaseButton', function (e) {
  e.preventDefault();
  var ucName = $(this).find('i').attr("value");
  deleteObject('usecase',ucName,function(ucName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/usecases/name/" + name.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        createUseCasesTable();
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

$(document).on("click", "#addNewUseCase", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editUseCaseOptions.html", "#objectViewer", null, true, true, function () {
    $("#editUseCaseOptionsForm").addClass("new");
    $("#Properties").hide();
    $.session.set("UseCase", JSON.stringify(jQuery.extend(true, {},useCaseDefault )));
  });
});

mainContent.on('click', '#CloseUseCase', function (e) {
  e.preventDefault();
  createUseCasesTable();
});

// Dialog for entering a use case step
function stepDialogBox(callback){
  var dialogwindow = $("#EnterUseCaseStep");
  var select = dialogwindow.find("select");
  dialogwindow.dialog({
    modal: true,
    buttons: {
      Ok: function () {
        var text =  select.find("option:selected" ).text();
        if(jQuery.isFunction(callback)){
          callback($("#theStep").val());
        }
        $(this).dialog("close");
      }
    }
  });
  $(".comboboxD").css("visibility", "visible");
}

function putUseCase(usecase, oldName, usePopup, callback){
  var output = {};
  output.object = usecase;
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
    url: serverIP + "/api/usecases/name/" + oldName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
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

function postUseCase(usecase, callback){
  var output = {};
  output.object = usecase;
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
    url: serverIP + "/api/usecases" + "?session_id=" + $.session.get('sessionID'),
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

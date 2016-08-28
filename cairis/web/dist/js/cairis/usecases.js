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
        textToInsert[i++] = '<td><button class="editUseCaseButton" value="' + key + '">' + 'Edit' + '</button> <button class="deleteUseCaseButton" value="' + key + '">' + 'Delete' + '</button></td>';

        textToInsert[i++] = '<td name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theDescription">';
        textToInsert[i++] = item.theDescription;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      });

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      activeElement("reqTable");
      sortTableByRow(0);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
}

$(document).on('click', ".editUseCaseButton", function () {
  var name = $(this).val();
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
      fillOptionMenu("fastTemplates/editUseCaseOptions.html", "#optionsContent", null, true, true, function () {
        $("#optionsHeaderGear").text("UseCase properties");
        forceOpenOptions();
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


var optionsContent = $("#optionsContent");
optionsContent.on("click",".usecaseEnvironment", function () {
  clearUseCaseEnvInfo();
  var usecase = JSON.parse($.session.get("UseCase"));
  var theEnvName = $(this).text();
  $.session.set("usecaseEnvironmentName", theEnvName);
  $.each(usecase.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $('#thePreCond').val(env.thePreCond);
      $('#thePostCond').val(env.thePostCond);
      for (var i = 0; i < env.theSteps.length; i++) {
        appendUseCaseSteps(env.theSteps[i].theStepText);
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

function appendUseCaseSteps(stepTxt) {
  $("#theSteps").find("tbody").append("<tr><td class='removeUseCaseStep'><i class='fa fa-minus'></i></td><td class='usecaseStep'>" + stepTxt + "</td></tr>").animate('slow');
}

function appendUseCaseActor(actor) {
  $("#theActors").find("tbody").append("<tr><td class='removeActor'><i class='fa fa-minus'></i></td><td class='usecaseActor'>" + actor + "</td></tr>").animate('slow');
}

optionsContent.on('click', '#addConcernToUseCase', function () {
  var hasConcern = [];
  $("#theConcerns").find(".usecaseConcern").each(function(index, concern){
    hasConcern.push($(concern).text());
  });
  assetsDialogBox(hasConcern, function (text) {
    var usecase = JSON.parse($.session.get("UseCase"));
    var theEnvName = $.session.get("usecaseEnvironmentName");
    $.each(usecase.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        env.theAssets.push(text);
        $.session.set("UseCase", JSON.stringify(usecase));
        appendUseCaseConcern(text);
      }
    });
  });
});

optionsContent.on('click', ".removeUseCaseStep", function () {
  var text = $(this).next(".usecaseStep").text();
  $(this).closest("tr").remove();
  var usecase = JSON.parse($.session.get("UseCase"));
  var theEnvName = $.session.get("usecaseEnvironmentName");
  $.each(usecase.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theSteps, function (index2, concern) {
        if(concern == text){
          env.theSteps.splice( index2 ,1 );
          $.session.set("UseCase", JSON.stringify(usecase));
          return false;
        }
      });
    }
  });
});

optionsContent.on('click', ".deleteUseCaseEnv", function () {
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

optionsContent.on("click", "#addUseCaseEnv", function () {
  var hasEnv = [];
  $(".usecaseEnvironment").each(function (index, tag) {
    hasEnv.push($(tag).text());
  });
  environmentDialogBox(hasEnv, function (text) {
    appendUseCaseEnvironment(text);
    var environment =  jQuery.extend(true, {},usecaseEnvDefault );
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

optionsContent.on('click', '#UpdateUseCase', function (e) {
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

$(document).on('click', '.deleteUseCaseButton', function (e) {
  e.preventDefault();
  deleteUseCase($(this).val(), function () {
    createUseCasesTable();
  });
});

$(document).on("click", "#addNewUseCase", function () {
  fillOptionMenu("fastTemplates/editUseCaseOptions.html", "#optionsContent", null, true, true, function () {
    $("#editUseCaseOptionsForm").addClass("new");
    $("#Properties").hide();
    $.session.set("UseCase", JSON.stringify(jQuery.extend(true, {},usecaseDefault )));
    $("#optionsHeaderGear").text("UseCase properties");
    forceOpenOptions();
  });
});

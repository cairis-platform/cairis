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
  validateClick('usecase',function() {
    $('#menuBCClick').attr('dimension','use_case');
    refreshMenuBreadCrumb('use_case');
  });
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
      setTableHeader("UseCases");
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
        textToInsert[i++] = '<td class="deleteUseCaseButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="usecase-row" name="theName">';
        textToInsert[i++] = key;
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

      $("#mainTable").find("tbody").addClass('usecase-rows');

      $('.usecase-rows').contextMenu({
        selector: 'td',
        items: {
          "supports": {
            name: "Supported by",
            callback: function(key, opt) {
              var ucName = $(this).closest("tr").find("td").eq(1).html();
              traceExplorer('usecase',ucName,'0');
            }
          },
          "contributes": {
            name: "Contributes to",
            callback: function(key, opt) {
              var ucName = $(this).closest("tr").find("td").eq(1).html();
              traceExplorer('usecase',ucName,'1');
            }
          },
        }
      });



      activeElement("mainTable");
      sortTableByRow(0);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
}

$(document).on('click', "td.usecase-row", function () {
  var ucName = $(this).text();
  refreshObjectBreadCrumb(ucName);
  viewUseCase(ucName); 
});

function viewUseCase(ucName) {
  activeElement("objectViewer");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/usecases/name/" + ucName.replace(" ", "%20"),
    success: function (data) {
      fillOptionMenu("fastTemplates/editUseCaseOptions.html", "#objectViewer", null, true, true, function () {
        $('#UpdateUseCase').text("Update");
        $.session.set("UseCase", JSON.stringify(data));
        $('#editUseCaseOptionsForm').loadJSON(data, null);
        $.each(data.theActors, function (index, actor) {
          appendUseCaseActor(actor);
        });

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
        $.each(data.theReferenceContributions, function (index, refCont) {
          appendUseCaseContribution(refCont);
        });

        $.each(data.theEnvironmentProperties, function (index, env) {
          appendUseCaseEnvironment(env.theEnvironmentName);
        });
        $("#theEnvironments").find(".usecaseEnvironment:first").trigger('click');
        $('#editUseCaseOptionsForm').validator('update');
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
};


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
        $("#theExceptions").find("tbody").addClass('usecaseStepException-rows');
        $('.usecaseStepException-rows').contextMenu({
          selector: 'td',
          items: {
            "generate_obstacle": {
              name: "Generate Obstacle",
              callback: function(key, opt) {
                generateObstacleFromException($(this).closest("tr").index());
              }
            }
          }
        });
        $.each(env.theSteps[i].theExceptions,function(idx,exc){
          appendUseCaseStepException(exc.theName);
        });
      }
      $("#useCaseProperties").show("fast");
    }
  });
});

function generateObstacleFromException(exceptionIdx) {
  var stepIdx = $('#theSteps').find('.active').index();
  var uc = JSON.parse($.session.get("UseCase"));
  var envName = $.session.get('usecaseEnvironmentName');
  $.each(uc.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      var stepTxt = env.theSteps[stepIdx].theStepText;
      var excTxt = env.theSteps[stepIdx].theExceptions[exceptionIdx].theName;

      var output = {};
      output.object = uc;
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
        url: serverIP + "/api/usecases/environment/" + encodeURIComponent(envName) + "/step/" + encodeURIComponent(stepTxt) + "/exception/" + encodeURIComponent(excTxt) + "/generate_obstacle?session_id=" + $.session.get('sessionID'),
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
  });
}

function clearUseCaseEnvInfo(){
  $("#thePreCond").val('');
  $("#thePostCond").val('');
  $("#theSteps").find("tbody").empty();
  $("#theExceptions").find("tbody").empty();
  $("#theExceptions").hide();
}

function appendUseCaseEnvironment(environment){
  $("#theEnvironments").find("tbody").append('<tr><td class="deleteUseCaseEnv"><i class="fa fa-minus"></i></td><td class="usecaseEnvironment">'+environment+'</td></tr>');
}

function appendUseCaseStep(stepTxt) {
  $("#theSteps").find("tbody").append('<tr class="clickable-row"><td class="removeUseCaseStep"><i class="fa fa-minus"></i></td><td class="usecaseStep">' + stepTxt + '</td></tr>').animate('slow');
}

function appendUseCaseActor(actor) {
  $("#theActors").find("tbody").append("<tr><td class='removeUseCaseActor'><i class='fa fa-minus'></i></td><td class='usecaseActor'>" + actor + "</td></tr>").animate('slow');
}

mainContent.on('click', '#addActorToUseCase', function () {
  var filterList = [];
  $("#theActors").find(".usecaseActor").each(function(index, actor){
    filterList.push($(actor).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'role', undefined, function(){
    $('#chooseEnvironment').attr('data-chooseDimension','actor');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addUseCaseActor');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addUseCaseActor() {
  var text = $("#chooseEnvironmentSelect").val();
  var usecase = JSON.parse($.session.get("UseCase"));
  usecase.theActors.push(text);
  $.session.set("UseCase", JSON.stringify(usecase));
  appendUseCaseActor(text);
};


mainContent.on('shown.bs.modal','#useCaseStepDialog',function() {
});

mainContent.on('change','#theActorType',function() {
  var envName = $.session.get("usecaseEnvironmentName");
  refreshDimensionSelector($('#theGRLActor'),$('#theActorType').val(),envName,undefined,['All']);
});

mainContent.on('click','td.usecaseStep',function() {
  $('#AddStepButton').text('Update');
  var stepIdx = $(this).closest('tr').index();
  $('#useCaseStepDialog').attr('data-selectedIndex',stepIdx);
  var uc = JSON.parse($.session.get("UseCase"));
  var envName = $.session.get('usecaseEnvironmentName');
  $.each(uc.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      var currentStep = env.theSteps[stepIdx];
      $('#theStep').val(currentStep.theStepText);
      $('#theSynopsis').val(currentStep.theSynopsis);
      if (currentStep.theActorType == '') {
        currentStep.theActorType = 'asset';
        currentStep.theActor = '';
      }
      $('#theActorType').val(currentStep.theActorType);
      refreshDimensionSelector($('#theGRLActor'),$('#theActorType').val(),envName,function(){
        $('#theGRLActor').val(currentStep.theActor);
        $('#useCaseStepDialog').modal('show');
      },['All']);
    }
  });
});

mainContent.on('click', '#addStepToUseCase', function () {
  $('#AddStepButton').text('Add');
  $('#useCaseStepDialog').attr('data-selectedIndex',undefined);
  var envName = $.session.get("usecaseEnvironmentName");
  refreshDimensionSelector($('#theGRLActor'),$('#theActorType').val(),envName,function(){
    $('#theStep').val('');
    $('#theSynopsis').val('');
    $('#useCaseStepDialog').modal('show');
  },['All']);
});



mainContent.on('click',"#AddStepButton", function() {
  var text = $('#theStep').val();
  var stepSynopsis = $('#theSynopsis').val();
  var actorType = $('#theActorType').val();
  var grlActor = $('#theGRLActor').val();
  var usecase = JSON.parse($.session.get("UseCase"));
  var theEnvName = $.session.get("usecaseEnvironmentName");
  var stepIdx = $('#useCaseStepDialog').attr('data-selectedIndex');
  $.each(usecase.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      if (stepIdx != undefined) {
        var currentStep = env.theSteps[stepIdx];
        currentStep.theStepText = text;
        currentStep.theSynopsis = stepSynopsis;
        currentStep.theActor = grlActor;
        currentStep.theActorType = actorType;
        $('#theSteps').find("tbody").find('tr:eq(' + stepIdx + ')').find('td:eq(1)').text(currentStep.theStepText);
      }
      else {
        var s = {
          "theStepText" : text,
          "theSynopsis": stepSynopsis,
          "theActor": grlActor,
          "theActorType" : actorType,
          "theTags" : [],
          "theExceptions": []};
        env.theSteps.push(s);
        appendUseCaseStep(text);
      }
      $('#useCaseStepDialog').modal('hide');
    }
  });
  $.session.set("UseCase", JSON.stringify(usecase));
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
    if(env.theEnvironmentName == envi){
      usecase.theEnvironmentProperties.splice( index ,1 );
      $.session.set("UseCase", JSON.stringify(usecase));
      clearUseCaseEnvInfo();

      var UIenv = $("#theEnvironments").find("tbody");
      if(jQuery(UIenv).has(".usecaseEnvironment").length){
        UIenv.find(".usecaseEnvironment:last").trigger('click');
      }
      else{
        $("#useCaseProperties").hide("fast");
      }
      return false;
    }
  });
});

mainContent.on("click", "#addUseCaseEnv", function () {
  var filterList = [];
  $(".usecaseEnvironment").each(function (index, tag) {
    filterList.push($(tag).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'environment',undefined,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','environment');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addUseCaseEnvironment');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addUseCaseEnvironment() {
  var text = $("#chooseEnvironmentSelect").val();
  appendUseCaseEnvironment(text);
  var environment =  jQuery.extend(true, {},useCaseEnvDefault );
  environment.theEnvironmentName = text;
  var usecase = JSON.parse($.session.get("UseCase"));
  usecase.theEnvironmentProperties.push(environment);
  $.session.set("UseCase", JSON.stringify(usecase));
  $(document).find(".usecaseEnvironment").each(function () {
    if($(this).text() == text){
      $(this).trigger("click");
      $("#useCaseProperties").show("fast");
    }
  });
};

mainContent.on('click', '#UpdateUseCase', function (e) {
  e.preventDefault();
  var usecase = JSON.parse($.session.get("UseCase"));
  if (usecase.theEnvironmentProperties.length == 0) {
    alert("Environments not defined");
  }
  else {
    var oldName = usecase.theName;
    usecase.theName = $("#theName").val();
    usecase.theCode = $("#theCode").val();
    usecase.theAuthor = $("#theAuthor").val();
    usecase.theObjective = $("#theObjective").val();
    usecase.theDescription = $("#theDescription").val();
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
        $("#editUseCaseOptionsForm").removeClass("new")
        $('#menuBCClick').attr('dimension','use_case');
        refreshMenuBreadCrumb('use_case');
      });
    } 
    else {
      putUseCase(usecase, oldName, function () {
        $('#menuBCClick').attr('dimension','use_case');
        refreshMenuBreadCrumb('use_case');
      });
    }
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
      url: serverIP + "/api/usecases/name/" + ucName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        showPopup(true);
        $('#menuBCClick').attr('dimension','use_case');
        refreshMenuBreadCrumb('use_case');
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
  refreshObjectBreadCrumb('New Use Case');
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editUseCaseOptions.html", "#objectViewer", null, true, true, function () {
    $('#editUseCaseOptionsForm').validator();
    $('#UpdateUseCase').text("Create");
    $("#editUseCaseOptionsForm").addClass("new");
    $("#useCaseProperties").hide();
    $.session.set("UseCase", JSON.stringify(jQuery.extend(true, {},useCaseDefault )));
  });
});

mainContent.on('click', '#CloseUseCase', function (e) {
  e.preventDefault();
  $('#menuBCClick').attr('dimension','use_case');
  refreshMenuBreadCrumb('use_case');
});

function putUseCase(usecase, oldName, callback){
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

mainContent.on("click",".clickable-row", function () {
  if($(this).hasClass('active')){
    $(this).removeClass('active'); 
    $("#theExceptions").hide();
  } 
  else {
    $(this).addClass('active').siblings().removeClass('active');
    $("#theExceptions").find("tbody").empty();
    var stepIdx = $('#theSteps').find('.active').index();
    var uc = JSON.parse($.session.get("UseCase"));
    var envName = $.session.get('usecaseEnvironmentName');
    $.each(uc.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        $.each(env.theSteps[stepIdx].theExceptions,function(idx,exc) {
          appendUseCaseStepException(exc.theName);
        });
        $("#theExceptions").show();
      }
    });
  }
});

mainContent.on('click','#addExceptionToStep',function() {
  $('#useCaseStepExceptionDialog').attr('data-selectedIndex',undefined);
  $('#useCaseStepExceptionDialog').modal('show');
});

mainContent.on('shown.bs.modal','#useCaseStepExceptionDialog',function() {
  var selectedIdx = $('#useCaseStepExceptionDialog').attr('data-selectedIndex');
  if (selectedIdx != undefined) {
    $('#AddStepExceptionButton').text('Edit');
    var stepIdx = $('#theSteps').find('.active').index();
    var uc = JSON.parse($.session.get("UseCase"));
    var envName = $.session.get('usecaseEnvironmentName');
    $.each(uc.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        var currentExc = env.theSteps[stepIdx].theExceptions[selectedIdx];
        $('#theExceptionName').val(currentExc.theName);
        $('#theExceptionDefinition').val(currentExc.theDescription);
        $('#theExceptionCategory').val(currentExc.theCategoryName);
        if (currentExc.theDimensionType == 'goal') {
          $($('#theExceptionTypeGoalRadioLabel').children()[0]).prop('checked','checked')
        }
        else {
          $($('#theExceptionTypeRequirementRadioLabel').children()[0]).prop('checked','checked')
        }
        refreshExceptionTypeValues(currentExc.theDimensionType,currentExc.theDimensionValue);
      }
    });
  }
  else {
    $('#AddStepExceptionButton').text('Add');
    $('#theExceptionName').val('');
    $('#theExceptionDefinition').val('');
    $('#theExceptionCategory').val('Confidentiality Threat');
    $($('#theExceptionTypeGoalRadioLabel').children()[0]).prop('checked','checked')
    refreshExceptionTypeValues('goal');
  }
});

mainContent.on('change','input:radio[name="theExceptionTypeRadio"]',function() {
  var excType = $(this).parent().text().toLowerCase();
  refreshExceptionTypeValues(excType);
});

function refreshExceptionTypeValues(excType,excTypeValue) {
  var uc = JSON.parse($.session.get("UseCase"));
  var urlPrefix = '/api/usecases/name/' + encodeURIComponent(uc.theName);
  if (excType == 'goal') {
    var envName = $.session.get('usecaseEnvironmentName');
    urlPrefix += '/environment/' + encodeURIComponent(envName) + '/goals'
  }
  else {
    urlPrefix += '/requirements'
  }
  refreshSpecificSelector($('#theExceptionTypeValues'),urlPrefix,function() {
    if (excTypeValue != undefined) {
      $('#theExceptionTypeValues').val(excTypeValue);
    }
  });
};

mainContent.on('click',"#AddStepExceptionButton", function() {
  var exc = {};
  exc.theName = $('#theExceptionName').val();
  exc.theDimensionType = $('input:radio[name="theExceptionTypeRadio"]:checked').parent().text().toLowerCase();
  exc.theDimensionValue = $('#theExceptionTypeValues').val();
  exc.theCategoryName = $('#theExceptionCategory').val();
  exc.theDescription = $('#theExceptionDefinition').val();

  var stepIdx = $('#theSteps').find('.active').index();

  var uc = JSON.parse($.session.get("UseCase"));
  var envName = $.session.get("usecaseEnvironmentName");
  $.each(uc.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      var selectedIdx = $('#useCaseStepExceptionDialog').attr('data-selectedIndex');
      if (selectedIdx != undefined) {
        env.theSteps[stepIdx].theExceptions[selectedIdx] = exc;
        $.session.set("UseCase", JSON.stringify(uc));
        $('#theExceptions').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(exc.theName);
      }
      else {
        env.theSteps[stepIdx].theExceptions.push(exc);
        $.session.set("UseCase", JSON.stringify(uc));
        appendUseCaseStepException(exc.theName);
      }
      $('#useCaseStepExceptionDialog').modal('hide');
    }
  });
});

function appendUseCaseStepException(excName) {
  $("#theExceptions").find("tbody").append('<tr class="usecaseStepException-row"><td class="deleteUseCaseStepException"><i class="fa fa-minus"></i></td><td class="usecaseStepException">'+ excName +'</td></tr>');
}

mainContent.on("click",".usecaseStepException", function () {
  var stepIdx = $('#theSteps').find('.active').index();
  var excRow = $(this).closest('tr');
  var uc = JSON.parse($.session.get("UseCase"));
  var envName = $.session.get('usecaseEnvironmentName');
  $.each(uc.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      var currentStep = env.theSteps[stepIdx];
      $('#useCaseStepExceptionDialog').attr('data-selectedIndex',excRow.index());
      $('#useCaseStepExceptionDialog').modal('show');
    }
  });
});

mainContent.on('click', ".deleteUseCaseStepException", function () {
  var stepIdx = $('#theSteps').find('.active').index();
  var excRow = $(this).closest('tr');
  var uc = JSON.parse($.session.get("UseCase"));
  var envName = $.session.get('usecaseEnvironmentName');
  $.each(uc.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      env.theSteps[stepIdx].theExceptions.splice(excRow.index(),1);
      $.session.set("UseCase", JSON.stringify(uc));
      excRow.remove();
    }
  });
});

mainContent.on('change','#theGRLUCContributionTo',function() {
  refreshDimensionSelector($('#theGRLBeneficiary'),$(this).val());
});

mainContent.on('click', '#addContributionToUseCase', function () {
  $('#useCaseContributionDialog').attr('data-selectedIndex',undefined);
  $('#theGRLUCContributionMeansEnd').val('means');
  $('#theGRLUCContribution').val('SomePositive');
  refreshDimensionSelector($('#theGRLBeneficiary'),'persona_characteristic_synopsis', undefined, function(){
    $('#useCaseContributionDialog').modal('show');
  });

});

$(document).on('click', "td.ucgrlcontribution-row", function () {
  var ucContIdx = $(this).closest('tr').index();
  $('#useCaseContributionDialog').attr('data-selectedIndex',ucContIdx);
  var uc = JSON.parse($.session.get("UseCase"));
  var refCont = uc.theReferenceContributions[ucContIdx];
  $('#theGRLUCContributionMeansEnd').val(refCont.theReferenceContribution.theMeansEnd);
  $('#theGRLUCContribution').val(refCont.theReferenceContribution.theContribution);
  refreshDimensionSelector($('#theGRLBeneficiary'),'persona_characteristic_synopsis', undefined, function(){
    $('#theGRLBeneficiary').val(refCont.theContributionTo);
    $('#useCaseContributionDialog').modal('show');
  });
});

mainContent.on('click', '#AddUCContributionButton', function () {
  var refCont = {};
  refCont.theContributionTo = $('#theGRLBeneficiary').val();
  refCont.theReferenceContribution = {};
  refCont.theReferenceContribution.theMeansEnd = $('#theGRLUCContributionMeansEnd').val();
  refCont.theReferenceContribution.theContribution = $('#theGRLUCContribution').val();

  var uc = JSON.parse($.session.get("UseCase"));

  var selectedIdx = $('#useCaseContributionDialog').attr('data-selectedIndex');

  if (selectedIdx != undefined) {
    uc.theReferenceContributions[selectedIdx] = refCont;
    $.session.set("UseCase", JSON.stringify(uc));
    $('#theUCContributions').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(refCont.theContributionTo);
    $('#theUCContributions').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(2)').text(refCont.theReferenceContribution.theMeansEnd);
    $('#theUCContributions').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(3)').text(refCont.theReferenceContribution.theContribution);
  }
  else {
    uc.theReferenceContributions.push(refCont);
    $.session.set("UseCase", JSON.stringify(uc));
    appendUseCaseContribution(refCont);
  }
  $('#useCaseContributionDialog').modal('hide');
});

function appendUseCaseContribution(refCont) {
  $("#theUCContributions").find("tbody").append("<tr><td class='removeUseCaseContribution'><i class='fa fa-minus'></i></td><td class='ucgrlcontribution-row'>" + refCont.theContributionTo + "</td><td>" + refCont.theReferenceContribution.theMeansEnd + "</td><td>" + refCont.theReferenceContribution.theContribution + "</td></tr>").animate('slow');
}

mainContent.on('click', ".removeUseCaseContribution", function () {
  var ucContRow = $(this).closest("tr");
  var rowIdx = ucContRow.index();
  ucContRow.remove();
  var uc = JSON.parse($.session.get("UseCase"));
  uc.theReferenceContributions.splice(rowIdx,1);
  $.session.set("UseCase", JSON.stringify(uc));
});

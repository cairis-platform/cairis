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
      setTableHeader("UseCases");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td class="deleteUseCaseButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="usecase-row" name="theName">';
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
        $('#editUseCaseOptionsForm').validator();
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
        $.each(env.theSteps[i].theExceptions,function(idx,exc){
          appendUseCaseStepException(exc.theName);
        });
      }
      $("#useCaseProperties").show("fast");
    }
  });
});

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
  $("#theActors").find("tbody").append("<tr><td class='removeActor'><i class='fa fa-minus'></i></td><td class='usecaseActor'>" + actor + "</td></tr>").animate('slow');
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
 $('#theStep').val('');
});

mainContent.on('click', '#addStepToUseCase', function () {
  $('#useCaseStepDialog').modal('show');
});

mainContent.on('click',"#AddStepButton", function() {
  var text = $('#theStep').val();
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
        createUseCasesTable();
        $("#editUseCaseOptionsForm").removeClass("new")
      });
    } 
    else {
      putUseCase(usecase, oldName, function () {
        createUseCasesTable();
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
    $('#editUseCaseOptionsForm').validator();
    $('#UpdateUseCase').text("Create");
    $("#editUseCaseOptionsForm").addClass("new");
    $("#useCaseProperties").hide();
    $.session.set("UseCase", JSON.stringify(jQuery.extend(true, {},useCaseDefault )));
  });
});

mainContent.on('click', '#CloseUseCase', function (e) {
  e.preventDefault();
  createUseCasesTable();
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
  $('#useCaseStepExceptionDialog').modal('show');
});

mainContent.on('change','input:radio[name="theExceptionTypeRadio"]',function() {
  var excType = $(this).parent().text().toLowerCase();
  var envName = (excType == 'goal') ? $.session.get('usecaseEnvironmentName') : undefined;
  refreshDimensionSelector($('#theExceptionTypeValues'),excType,envName,undefined,['All']);
});

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
      env.theSteps[stepIdx].theExceptions.push(exc);
      $.session.set("UseCase", JSON.stringify(uc));
      appendUseCaseStepException(exc.theName);
      $('#useCaseStepExceptionDialog').modal('hide');
    }
  });
});

function appendUseCaseStepException(excName) {
  $("#theExceptions").find("tbody").append('<tr><td class="deleteUseCaseStepException"><i class="fa fa-minus"></i></td><td class="usecaseStepException">'+ excName +'</td></tr>');
}

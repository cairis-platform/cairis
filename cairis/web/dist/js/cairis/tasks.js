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

window.durationLookup = {};
window.durationLookup['Seconds'] = 'Low';
window.durationLookup['Minutes'] = 'Medium';
window.durationLookup['Hours or Longer'] = 'High';
window.reverseDurationLookup = {};
window.reverseDurationLookup['Low'] = 'Seconds';
window.reverseDurationLookup['Medium'] = 'Minutes';
window.reverseDurationLookup['High'] = 'Hours or Longer';
window.frequencyLookup = {};
window.frequencyLookup['Hours or more'] = 'Low';
window.frequencyLookup['Daily - Weekly'] = 'Medium';
window.frequencyLookup['Monthly or less'] = 'High';
window.reverseFrequencyLookup = {};
window.reverseFrequencyLookup['Low'] = 'Hours or more';
window.reverseFrequencyLookup['Medium'] = 'Daily - Weekly';
window.reverseFrequencyLookup['High'] = 'Monthly or less';


$("#taskClick").click(function () {
  createTasksTable();
});

$("#taskMenuClick").click(function () {
  createTasksTable();
});


function createTasksTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/tasks",
    success: function (data) {
      setTableHeader("Tasks");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";

        textToInsert[i++] = '<td class="deleteTaskButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="task-row" name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theObjective">';
        textToInsert[i++] = item.theObjective;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      });

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
      $.contextMenu('destroy',$('.task-rows'));
      $("#mainTable").find("tbody").removeClass();
      $("#mainTable").find("tbody").addClass('task-rows');

      $('.task-rows').contextMenu({
        selector: 'td',
        items: {
          "supports": {
            name: "Supported by",
            callback: function(key, opt) {
              var taskName = $(this).closest("tr").find("td").eq(1).html();
              traceExplorer('task',taskName,'0');
            }
          },
          "contributes": {
            name: "Contributes to",
            callback: function(key, opt) {
              var taskName = $(this).closest("tr").find("td").eq(1).html();
              traceExplorer('task',taskName,'1');
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

$(document).on('click', "td.task-row", function () {
  var taskName = $(this).text();
  viewTask(taskName);
});

function viewTask(taskName) {
  activeElement("objectViewer");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/tasks/name/" + taskName.replace(" ", "%20"),
    success: function (data) {
      fillOptionMenu("fastTemplates/editTaskOptions.html", "#objectViewer", null, true, true, function () {
        $("#editTaskOptionsForm").validator();
        $("#UpdateTask").text("Update");
        $.session.set("Task", JSON.stringify(data));
        $('#editTaskOptionsForm').loadJSON(data, null);

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
          appendTaskEnvironment(env.theEnvironmentName);
        });
        fillTaskEnvInfo(data.theEnvironmentProperties[0]);
        $('#tasktabsID').show('fast');
        $.session.set("taskEnvironmentName", data.theEnvironmentProperties[0].theEnvironmentName);
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
};

function fillTaskEnvInfo(env) {
  clearTaskEnvInfo();
  $('#theDependencies').val(env.theDependencies);
  $('#theNarrative').val(env.theNarrative);
  $('#theConsequences').val(env.theConsequences);
  $('#theBenefits').val(env.theBenefits);
          
  $.each(env.theAssets, function(index,concern) {
    appendTaskConcern(concern);
  });

  for (var i = 0; i < env.thePersonas.length; i++) {
    appendTaskPersona(env.thePersonas[i]['thePersona'],window.reverseDurationLookup[env.thePersonas[i]['theDuration']],window.reverseFrequencyLookup[env.thePersonas[i]['theFrequency']],env.thePersonas[i]['theDemands'],env.thePersonas[i]['theGoalConflict']);
  }

  for (var i = 0; i < env.theConcernAssociations.length; i++) {
    var aCol = [];
    $.each(env.theConcernAssociations[i], function(idx,val) { aCol.push(val); });
    appendConcernAssociation(aCol[0]);
  }
}


var mainContent = $("#objectViewer");
mainContent.on("click",".taskEnvironment", function () {
  var lastEnvName = $.session.get("taskEnvironmentName");
  var task = JSON.parse($.session.get("Task"));
  var updatedEnvProps = [];
  $.each(task.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == lastEnvName){
      env.theDependencies = $('#theDependencies').val();
      env.theNarrative = $('#theNarrative').val();
      env.theConsequences = $('#theConsequences').val();
      env.theBenefits = $('#theBenefits').val();
    }
    updatedEnvProps.push(env);
  });
  task.theEnvironmentProperties = updatedEnvProps;
  $.session.set("Task", JSON.stringify(task));
  task = JSON.parse($.session.get("Task"));

  var envName = $(this).text();
  $.session.set("taskEnvironmentName", envName);
  $.each(task.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      fillTaskEnvInfo(env);
    }
  });
});

function clearTaskEnvInfo(){
  $("#theDependencies").val('');
  $("#theNarrative").val('');
  $("#theConsequences").val('');
  $("#theBenefits").val('');
  $("#theConcerns").find("tbody").empty();
  $("#thePersonas").find("tbody").empty();
  $("#theConcernAssociations").find("tbody").empty();
}

function appendTaskEnvironment(environment){
  $("#theEnvironments").find("tbody").append('<tr><td class="deleteTaskEnv"><i class="fa fa-minus"></i></td><td class="taskEnvironment">'+environment+'</td></tr>');
}

function appendTaskConcern(concern) {
  $("#theConcerns").find("tbody").append("<tr><td class='removeTaskConcern'><i class='fa fa-minus'></i></td><td class='taskConcern'>" + concern + "</td></tr>").animate('slow');

}

mainContent.on('click', '#addConcernToTask', function () {
  var hasConcern = [];
  $("#theConcerns").find(".taskConcern").each(function(index, concern){
    hasConcern.push($(concern).text());
  });
  assetsDialogBox(hasConcern, function (text) {
    var task = JSON.parse($.session.get("Task"));
    var theEnvName = $.session.get("taskEnvironmentName");
    $.each(task.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        env.theAssets.push(text);
        $.session.set("Task", JSON.stringify(task));
        appendTaskConcern(text);
      }
    });
  });
});

mainContent.on('click', ".removeTaskConcern", function () {
  var text = $(this).next(".taskConcern").text();
  $(this).closest("tr").remove();
  var task = JSON.parse($.session.get("Task"));
  var theEnvName = $.session.get("taskEnvironmentName");
  $.each(task.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theAssets, function (index2, concern) {
        if(concern == text){
          env.theAssets.splice( index2 ,1 );
          $.session.set("Task", JSON.stringify(task));
          return false;
        }
      });
    }
  });
});

function appendTaskPersona(persona,duration,frequency,demands,goalConflict) {
  $("#thePersonas").find("tbody").append("<tr><td class='removeTaskPersona'><i class='fa fa-minus'></i></td><td class='taskPersona'>" + persona + "</td><td>" + duration + "</td><td>" + frequency + "</td><td>" + demands + "</td><td>" + goalConflict +  "</td></tr>").animate('slow');
}

mainContent.on('click', '#addPersonaToTask', function () {
  var hasPersona = [];
  $("#thePersonas").find(".taskPersona").each(function(index, persona){
    hasPersona.push($(persona).text());
  });
  taskPersonaDialogBox(hasPersona, function (persona,duration,frequency,demands,goalConflict) {
    var task = JSON.parse($.session.get("Task"));
    var theEnvName = $.session.get("taskEnvironmentName");
    $.each(task.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        var ptc = {};
        ptc['thePersona'] = persona;
        ptc['theDuration'] = window.durationLookup[duration];
        ptc['theFrequency'] = window.frequencyLookup[frequency];
        ptc['theDemands'] = demands;
        ptc['theGoalConflict'] = goalConflict;
        env.thePersonas.push(ptc);
        $.session.set("Task", JSON.stringify(task));
        appendTaskPersona(persona,duration,frequency,demands,goalConflict);
      }
    });
  });
});


mainContent.on('click', ".removeTaskPersona", function () {
  var text = $(this).next(".taskPersona").text();
  $(this).closest("tr").remove();
  var task = JSON.parse($.session.get("Task"));
  var theEnvName = $.session.get("taskEnvironmentName");
  $.each(task.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.thePersonas, function (index2, persona) {
        var pName = persona.thePersona;
        if(pName == text){
          env.thePersonas.splice( index2 ,1 );
          $.session.set("Task", JSON.stringify(task));
          return false;
        }
      });
    }
  });
});

function appendConcernAssociation(assoc) {
  $("#theConcernAssociations").find("tbody").append("<tr><td class='removeConcernAssociation'><i class='fa fa-minus'></i></td><td class='concernAssociation'>" +  assoc[0] + "</td><td>" + assoc[1] + "</td><td>" + assoc[2] + "</td><td>" + assoc[3] + "</td><td>" + assoc[4] + "</td></tr>").animate('slow'); 
}



mainContent.on('click', ".deleteTaskEnv", function () {
  var envi = $(this).next(".taskEnvironment").text();
  $(this).closest("tr").remove();
  var task = JSON.parse($.session.get("Task"));
  $.each(task.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envi){
      task.theEnvironmentProperties.splice( index ,1 );
      $.session.set("Task", JSON.stringify(task));
      clearTaskEnvInfo();

      var UIenv = $("#theTaskEnvironments").find("tbody");
      if(jQuery(UIenv).has(".taskEnvironment").length){
        UIenv.find(".taskEnvironment:first").trigger('click');
      }else{
        $("#tasktabsID").hide("fast");
      }

      return false;
    }
  });
});

mainContent.on("click", "#addTaskEnv", function () {
  var hasEnv = [];
  $(".taskEnvironment").each(function (index, tag) {
    hasEnv.push($(tag).text());
  });
  environmentDialogBox(hasEnv, function (text) {
    appendTaskEnvironment(text);
    var environment =  jQuery.extend(true, {},taskEnvDefault );
    environment.theEnvironmentName = text;
    var task = JSON.parse($.session.get("Task"));
    task.theEnvironmentProperties.push(environment);
    $.session.set("Task", JSON.stringify(task));
    $(document).find(".taskEnvironment").each(function () {
      if($(this).text() == text){
        $(this).trigger("click");
        $("#tasktabsID").show("fast");
      }
    });
  });
});

mainContent.on('click', '#UpdateTask', function (e) {
  e.preventDefault();
  var task = JSON.parse($.session.get("Task"));
  if (task.theEnvironmentProperties.length == 0) {
    alert("Environments not defined");
  } 
  else {
    var oldName = task.theName;
    task.theName = $("#theName").val();
    task.theAuthor = $("#theAuthor").val();
    task.theObjective = $("#theObjective").val();
    var tags = $("#theTags").text().split(", ");
    if(tags[0] != ""){
      task.theTags = tags;
    }

    var envName = $.session.get("taskEnvironmentName");
    var updatedEnvProps = [];
    $.each(task.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        env.theDependencies = $('#theDependencies').val();
        env.theNarrative = $('#theNarrative').val();
        env.theConsequences = $('#theConsequences').val();
        env.theBenefits = $('#theBenefits').val();
      }
      updatedEnvProps.push(env);
    });
    task.theEnvironmentProperties = updatedEnvProps;

    if($("#editTaskOptionsForm").hasClass("new")){
      postTask(task, function () {
        createTasksTable();
        $("#editTaskOptionsForm").removeClass("new")
      });
    } 
    else {
      putTask(task, oldName, function () {
        createTasksTable();
      });
    }
  }
});

$(document).on('click', 'td.deleteTaskButton', function (e) {
  e.preventDefault();
  var taskName = $(this).find('i').attr("value");
  deleteObject('task', taskName, function (taskName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/tasks/name/" + taskName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        createTasksTable();
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


$(document).on("click", "#addNewTask", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editTaskOptions.html", "#objectViewer", null, true, true, function () {
    $("#editTaskOptionsForm").validator();
    $("#UpdateTask").text("Create");
    $("#editTaskOptionsForm").addClass("new");
    $.session.set("Task", JSON.stringify(jQuery.extend(true, {},taskDefault )));
    $('#tasktabsID').hide();
  });
});

mainContent.on('click', '#CloseTask', function (e) {
  e.preventDefault();
  createTasksTable();
});

function taskPersonaDialogBox(hasPersona ,callback){
  var dialogwindow = $("#ChoosePersonaForTask");
  var envName = $.session.get("taskEnvironmentName");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/persona/environment/" + envName,
    success: function (data) {
      $("#theTaskPersona").empty();
      var none = true;
      $.each(data, function(key, persona) {
        var found = false;
        $.each(hasPersona,function(index, text) {
          if(text == persona){
            found = true
          }
        });
        //if not found in personas
        if(!found) {
          $("#theTaskPersona").append("<option value=" + persona + ">" + persona + "</option>");
          none = false;
        }
      });
      if(!none) {
        //dialogwindow.show();
        dialogwindow.dialog({
          modal: true,
          buttons: {
            Ok: function () {
              var persona = $("#theTaskPersona").find("option:selected" ).text();
              var duration = $("#theTaskDuration").find("option:selected").text();
              var frequency = $("#theTaskFrequency").find("option:selected").text();
              var demands = $("#theTaskDemands").find("option:selected").text();
              var goalConflict = $("#theTaskGoalConflict").find("option:selected").text();
              if(jQuery.isFunction(callback)){
                callback(persona, duration, frequency, demands, goalConflict);
              }
              $(this).dialog("close");
            }
          }
        });
        $(".comboboxD").css("visibility", "visible");
      }  
      else {
        alert("All possible personas are already added");
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function putTask(task, oldName, callback){
  var output = {};
  output.object = task;
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
    url: serverIP + "/api/tasks/name/" + oldName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
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

function postTask(task, callback){
  var output = {};
  output.object = task;
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
    url: serverIP + "/api/tasks" + "?session_id=" + $.session.get('sessionID'),
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

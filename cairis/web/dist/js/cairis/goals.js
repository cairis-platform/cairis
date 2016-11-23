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

    Authors: Raf Vandelaer, Shamal Faily */

'use strict';

$("#goalsClick").click(function(){
  createEditGoalsTable()
});

$("#goalMenuClick").click(function(){
  createEditGoalsTable()
});

function createEditGoalsTable(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/goals",
    success: function (data) {
      window.activeTable = "EditGoals";
      setTableHeader();
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(count, item) {
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td class="deleteGoalButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';

        textToInsert[i++] = '<td class="goal-rows" name="theName">';
        textToInsert[i++] = item.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theOriginator">';
        textToInsert[i++] = item.theOriginator;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="Status">';
        if(item.theColour == 'black'){
          textToInsert[i++] = "Check";
        }
        else if(item.theColour == 'red'){
          textToInsert[i++] = "To refine";
        }
        else {
          textToInsert[i++] = "OK";
        }

        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theId"  style="display:none;">';
        textToInsert[i++] = item.theId;
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


$(document).on('click', "td.goal-rows", function(){
  var goalName = $(this).text();
  viewGoal(goalName);
});

var mainContent = $("#objectViewer");
mainContent.on('click', ".goalEnvProperties", function () {
  var goal = JSON.parse($.session.get("Goal"));
  var name = $(this).text();
  $.session.set("GoalEnvName", name);
  emptyGoalEnvTables();

  $.each(goal.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == name){
      $('#goalProperties').loadJSON(env,null);
      $("#theIssue").val(env.theIssue);
      $("#theDefinition").val(env.theDefinition);
      $("#theFitCriterion").val(env.theFitCriterion);
      //theDef fitcrit issue

      $.each(env.theGoalRefinements, function (index, goal) {
        appendGoalGoal(goal);
      });
      $.each(env.theSubGoalRefinements, function (index, subgoal) {
        appendGoalSubGoal(subgoal);
      });
      $.each(env.theConcerns, function (index, concern) {
        appendGoalConcern(concern);
      });
      $.each(env.theConcernAssociations, function (index, assoc) {
        appendGoalConcernAssoc(assoc);
      });
    }
  });
});

mainContent.on('click', '.deleteGoalEnvConcernAssoc', function () {
  var goal = JSON.parse($.session.get("Goal"));
  var envName = $.session.get("GoalEnvName");
  var theAssoc =  $(this).closest("tr").find(".assocName").text();
  $(this).closest("tr").remove();
  $.each(goal.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      $.each(env.theConcernAssociations, function (ix, assoc) {
        if(assoc[0] == theAssoc){
          env.theConcernAssociations.splice(ix,1)
        }
      });
    }
  });
  $.session.set("Goal", JSON.stringify(goal));
});

mainContent.on('click', '#updateGoalConcernAss', function () {
  var goal = JSON.parse($.session.get("Goal"));
  var envName = $.session.get("GoalEnvName");
  var arr = [];
  arr[0] = $("#theSourceSelect").val();
  arr[1] = $("#theNSelect").val();
  arr[2] = $("#theLink").val();
  arr[3] = $("#theTargetSelect").val();
  arr[4] = $("#theN2Select").val();

  if($("#editgoalConcernAssociations").hasClass("new")){
    $.each(goal.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        env.theConcernAssociations.push(arr);
      }
    });
  }
  else {
    var oldname = $.session.get("goalAssocName");
    $.each(goal.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        $.each(env.theConcernAssociations, function (index, concern) {
          if(concern[0] == oldname){
            concern[0] = $("#theSourceSelect").val();
            concern[1] = $("#theNSelect").val();
            concern[2] = $("#theLink").val();
            concern[3] = $("#theTargetSelect").val();
            concern[4] = $("#theN2Select").val();
          }
        });
      }
    });
  }
  toggleGoalWindow("#editGoalOptionsForm");
  fillGoalOptionMenu(goal);
  $.session.set("Goal", JSON.stringify(goal));
});

mainContent.on('click',".deleteGoalSubGoal", function () {
  var goal = JSON.parse($.session.get("Goal"));
  var envName = $.session.get("GoalEnvName");
  var subGoalName =  $(this).closest("tr").find(".subGoalName").text();
  $(this).closest("tr").remove();
  $.each(goal.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      $.each(env.theSubGoalRefinements, function (ix, subgoal) {
        if(subgoal[0] == subGoalName){
          env.theSubGoalRefinements.splice(ix,1)
        }
      });
    }
  });
  $.session.set("Goal", JSON.stringify(goal));
});

mainContent.on('click',"#addConcerntoGoal", function () {
  hasAsset = [];
  $("#editgoalsConcernTable").find('tbody').find('.GoalConcernName').each(function (index, td) {
     hasAsset.push($(td).text());
  });
  var envName = $.session.get("GoalEnvName");
  assetsInEnvDialogBox(envName, hasAsset, function (text) {
    var goal = JSON.parse($.session.get("Goal"));

    $.each(goal.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        env.theConcerns.push(text);
      }
    });
    appendGoalConcern(text);
    $.session.set("Goal", JSON.stringify(goal));
  });
});

mainContent.on('click',".deleteGoalGoal", function () {
  var goal = JSON.parse($.session.get("Goal"));
  var envName = $.session.get("GoalEnvName");
  var subGoalName =  $(this).closest("tr").find(".envGoalName").text();
  $(this).closest("tr").remove();
  $.each(goal.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      $.each(env.theGoalRefinements, function (ix, thegoal) {
        if(typeof thegoal != "undefined"){
          if(thegoal[0] == subGoalName){
            env.theGoalRefinements.splice(ix,1)
          }
        }
      });
    }
  });
  $.session.set("Goal", JSON.stringify(goal));
});

//deleteGoalEnvConcern
mainContent.on('click',".deleteGoalEnvConcern", function () {
  var goal = JSON.parse($.session.get("Goal"));
  var envName = $.session.get("GoalEnvName");
  var name =  $(this).closest("tr").find(".GoalConcernName").text();
  $(this).closest("tr").remove();
  $.each(goal.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      $.each(env.theConcerns, function (ix, thecon) {
        if(typeof thecon != "undefined"){
          if(thecon == name){
            env.theConcerns.splice(ix,1)
          }
        }
      });
    }
  });
  $.session.set("Goal", JSON.stringify(goal));
});

mainContent.on('click', '#addConcernAssociationstoGoal', function () {
  toggleGoalWindow("#editgoalConcernAssociations");
  $("#editgoalConcernAssociations").addClass("new");
  var envName = $.session.get("GoalEnvName");
  $("#theSourceSelect").empty();
  $("#theTargetSelect").empty();
  getAllAssetsInEnv(envName, function (data) {
    $.each(data, function (index, asset) {
      $("#theSourceSelect").append($("<option></option>")
        .attr("value",asset)
        .text(asset));
      $("#theTargetSelect").append($("<option></option>")
        .attr("value",asset)
        .text(asset));
    })
  });
});

mainContent.on('click', '#addSubGoaltoGoal', function () {
  $("#editgoalSubGoal").addClass("new");
  toggleGoalWindow("#editgoalSubGoal");
  fillGoalEditSubGoal();
});

mainContent.on('click', '#addGoaltoGoal', function () {
  $("#editGoalGoal").addClass("new");
  toggleGoalWindow("#editGoalGoal");
  fillGoalEditGoal();
});

mainContent.on("click", "#addGoalEnvironment", function () {
  var hasEnv = [];
  $(".goalEnvProperties").each(function (index, tag) {
    hasEnv.push($(tag).text());
  });
  environmentDialogBox(hasEnv, function (text) {
    appendGoalEnvironment(text);
    var environment =  jQuery.extend(true, {},goalEnvDefault );
    environment.theEnvironmentName = text;
    var goal = JSON.parse($.session.get("Goal"));
    goal.theEnvironmentProperties.push(environment);
    $("#goalProperties").show("fast");
    $.session.set("GoalEnvName", text);
    $.session.set("Goal", JSON.stringify(goal));
  });
});

mainContent.on('click', ".deleteGoalEnv", function () {
  var envi = $(this).next(".goalEnvProperties").text();
  $(this).closest("tr").remove();
  var goal = JSON.parse($.session.get("Goal"));
  $.each(goal.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envi){
      goal.theEnvironmentProperties.splice( index ,1 );
      $.session.set("Attacker", JSON.stringify(goal));
      var UIenv =  $("#theGoalEnvironments").find("tbody");
      if(jQuery(UIenv).has(".goalEnvProperties").length){
        UIenv.find(".goalEnvProperties:first").trigger('click');
      }
      else{
        $("#goalProperties").hide("fast");
      }
      return false;
    }
  });
});

mainContent.on('click', '#updateGoalSubGoal', function () {
  var goal = JSON.parse($.session.get("Goal"));
  var envName = $.session.get("GoalEnvName");
  if($("#editgoalSubGoal").hasClass("new")){
    $("#editgoalSubGoal").removeClass("new");
    $.each(goal.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        var array = [];
        array[1] = $("#theSubgoalType").val();
        array[0] = $("#theSubGoalName").val();
        array[2] = $("#theRefinementSelect").val();
        array[3] = $("#theAlternate").val();
        array[4] = $("#theGoalSubGoalRationale").val();
        env.theSubGoalRefinements.push(array);
        appendGoalSubGoal(array);
      }
    });
  } 
  else {
    var oldName = $.session.get("oldsubGoalName");
    $.each(goal.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        $.each(env.theSubGoalRefinements, function (index, arr) {
          if(arr[0] == oldName){
            arr[1] = $("#theSubgoalType").val();
            arr[0] = $("#theSubGoalName").val();
            arr[2] = $("#theRefinementSelect").val();
            arr[3] = $("#theAlternate").val();
            arr[4] = $("#theGoalSubGoalRationale").val();
          }
        });
      }
    });
  }
  $.session.set("Goal", JSON.stringify(goal));
  fillGoalOptionMenu(goal);
  toggleGoalWindow("#editGoalOptionsForm");
});

mainContent.on('change', ".goalAutoUpdater" ,function() {
  var goal = JSON.parse($.session.get("Goal"));
  var envName = $.session.get("GoalEnvName");
  var name = $(this).attr("name");
  var element = $(this);

  $.each(goal.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      if($(element).is("input")){
        env[name] = $(element).val();
      }
      else if($(element).is("textarea")){
        env[name] = $(element).val();
      }
      else {
        env[name] = $(element).find(":selected").text();
      }
      $.session.set("Goal", JSON.stringify(goal));
    }
  });
});

$(document).on('click', '#addNewGoal', function () {
  fillGoalOptionMenu(null, function () {
    $("#editGoalOptionsForm").validator();
    $("#updateGoalButton").text("Create");
    $("#editGoalOptionsForm").addClass('new');
    $("#goalProperties").hide();
    $.session.set("Goal", JSON.stringify(jQuery.extend(true, {},goalDefault )));
  });
});


mainContent.on('click', "#updateGoalButton", function (e) {
  e.preventDefault();
  var goal = JSON.parse($.session.get("Goal"));
  if (goal.theEnvironmentProperties.length == 0) {
    alert("Environments not defined");
  }
  else {
    var oldName = goal.theName;
    goal.theName = $("#theName").val();
    goal.theOriginator = $("#theOriginator").val();
    var tags = $("#theTags").text().split(", ");
    if(tags[0] != ""){
      goal.theTags = tags;
    }
    if($("#editGoalOptionsForm").hasClass("new")){
      postGoal(goal, function () {
        createEditGoalsTable();
        $("#editGoalOptionsForm").removeClass("new")
      });
    } 
    else {
      putGoal(goal, oldName, function () {
        createEditGoalsTable();
      });
    }
  }
});

mainContent.on('dblclick', '.editGoalSubGoalRow', function () {
  toggleGoalWindow("#editgoalSubGoal");
  var name = $(this).find("td").eq(1).text();
  fillGoalEditSubGoal(name);
  var type = $(this).find("td").eq(2).text();
  var refinement = $(this).find("td").eq(3).text();
  var target = $(this).find("td").eq(4).text();
  var rationale = $(this).find("td").eq(5).text();
  $.session.set("oldsubGoalName", name);

  $("#theSubgoalType").val(type);
  $("#theRefinementSelect").val(refinement);
  $("#theAlternate").val(target);
  $("#theGoalSubGoalRationale").val(rationale);
});

mainContent.on('dblclick', '.editGoalGoalRow', function () {
  toggleGoalWindow("#editGoalGoal");
  var name = $(this).find("td").eq(1).text();
  fillGoalEditGoal(name);

  var type = $(this).find("td").eq(2).text();
  var refinement = $(this).find("td").eq(3).text();
  var target = $(this).find("td").eq(4).text();
  var rationale = $(this).find("td").eq(5).text();
  $.session.set("oldGoalName", name);

  $("#theGoalType").val(type);
  $("#theGoalRefinementSelect").val(refinement);
  $("#theGoalAlternate").val(target);
  $("#theGoalGoalRationale").val(rationale);
});

//editGoalConcernAssoc
mainContent.on('dblclick', '.editGoalConcernAssoc', function () {
  var envName = $.session.get("GoalEnvName");
  var tr = $(this);
  getAllAssetsInEnv(envName, function (data) {
    $.each(data, function (index, asset) {
      $("#theSourceSelect").append($("<option></option>")
        .attr("value",asset)
        .text(asset));
      $("#theTargetSelect").append($("<option></option>")
         .attr("value",asset)
         .text(asset));
    });
    var name = $(tr).find(".assocName").text();
    $.session.set("goalAssocName",name);
    var n1 = $(tr).find(".assocN1").text();
    var link = $(tr).find(".assocLink").text();
    var n2 = $(tr).find(".assocN2").text();
    var target = $(tr).find(".assocTarget").text();

    $("#theSourceSelect").val(name);
    $("#theNSelect").val(n1);
    $("#theLink").val(link);
    $("#theTargetSelect").val(target);
    $("#theN2Select").val(n2);
    toggleGoalWindow("#editgoalConcernAssociations");
  });
});

mainContent.on('click', '.goalCancelButton', function () {
  toggleGoalWindow("#editGoalOptionsForm")
});

mainContent.on('click',"#updateGoalGoal", function () {
  var goal = JSON.parse($.session.get("Goal"));
  var envName = $.session.get("GoalEnvName");
  if($("#editGoalGoal").hasClass("new")) {
    $("#editGoalGoal").removeClass("new");
    $.each(goal.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        var array = [];
        array[1] = $("#theGoalType").val();
        array[0] = $("#theGoalName").val();
        array[2] = $("#theGoalRefinementSelect").val();
        array[3] = $("#theGoalAlternate").val();
        array[4] = $("#theGoalGoalRationale").val();
        env.theGoalRefinements.push(array);
        appendGoalGoal(array);
      }
    });
  }
  else{
    $.each(goal.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        var oldname = $.session.get("oldGoalName");
        $.each(env.theGoalRefinements, function (index, ref) {
          if(ref[0] == oldname){
            ref[1] = $("#theGoalType").val();
            ref[0] = $("#theGoalName").val();
            ref[2] = $("#theGoalRefinementSelect").val();
            ref[3] = $("#theGoalAlternate").val();
            ref[4] = $("#theGoalGoalRationale").val();
          }
        });
      }
    });
  }
  $.session.set("Goal", JSON.stringify(goal));
  fillGoalOptionMenu(goal);
  toggleGoalWindow("#editGoalOptionsForm");
});

function viewGoal(goalName){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/goals/name/" + goalName.replace(" ", "%20"),
    success: function (data) {
      fillGoalOptionMenu(data);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function fillGoalOptionMenu(data,callback){
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editGoalsOptions.html","#objectViewer",null,true,true, function(){
    $("#editGoalOptionsForm").validator();
    $("#updateGoalButton").text("Update");
    if(data != null) {
      $.session.set("Goal", JSON.stringify(data));
      $('#editGoalOptionsForm').loadJSON(data, null);

      $.each(data.theTags, function (index, tag) {
        $("#theTags").append(tag + ", ");
      });
      $.each(data.theEnvironmentProperties, function (index, prop) {
        appendGoalEnvironment(prop.theEnvironmentName);
      });
      $("#theGoalEnvironments").find(".goalEnvProperties:first").trigger('click');
    }
    else {
      var goal =  jQuery.extend(true, {},goalDefault );
      $.session.set("Goal", JSON.stringify(goal));
    }
    if (jQuery.isFunction(callback)) {
      callback();
    }
  });
}

function fillGoalEditSubGoal(theSettableValue){
  $("#theSubGoalName").empty();
  var subname = $("#theSubGoalName");
  getAllgoals(function (data) {
    $.each(data, function (key, goal) {
      subname.append($("<option></option>")
        .attr("value", key)
        .text(key));
    });
  });
  getAllRequirements(function (data) {
    $.each(data, function (key, req) {
      subname.append($("<option></option>")
        .attr("value", req.theLabel)
        .text(req.theLabel));
    });
    if (typeof theSettableValue  !== "undefined"){
      subname.val(theSettableValue);
    }
  });
}

function fillGoalEditGoal(theSettableValue) {
  var thegoalName = $("#theGoalName");
  thegoalName.empty();
  getAllgoals(function (data) {
    $.each(data, function (key, goal) {
      thegoalName.append($("<option></option>")
        .attr("value", key)
        .text(key));
    });
  });
  getAllRequirements(function (data) {
    $.each(data, function (key, req) {
      thegoalName.append($("<option></option>")
        .attr("value", req.theLabel)
        .text(req.theLabel));
    });
    if (typeof theSettableValue  !== "undefined"){
      thegoalName.val(theSettableValue);
    }
  });
}

function toggleGoalWindow(window) {
  $("#editgoalConcernAssociations").hide();
  $("#editGoalOptionsForm").hide();
  $("#editgoalSubGoal").hide();
  $("#editGoalGoal").hide();
  $(window).show();
}

function emptyGoalEnvTables(){
  $("#editgoalsGoalsTable").find("tbody").empty();
  $("#editgoalsSubgoalsTable").find("tbody").empty();
  $("#editgoalsConcernTable").find("tbody").empty();
  $("#editgoalsConcernassociationsTable").find("tbody").empty();
}

function appendGoalEnvironment(text){
  $("#theGoalEnvironments").append("<tr><td class='deleteGoalEnv'><i class='fa fa-minus'></i></td><td class='goalEnvProperties'>"+ text +"</td></tr>");
}
function appendGoalGoal(goal){
  $("#editgoalsGoalsTable").append('<tr class="editGoalGoalRow"><td class="deleteGoalGoal"><i class="fa fa-minus"></i></td><td class="envGoalName">'+goal[0]+'</td><td>'+goal[1]+'</td><td>'+goal[2]+'</td><td>'+goal[3]+'</td><td>'+goal[4]+'</td></tr>');
}
function appendGoalSubGoal(subgoal){
  $("#editgoalsSubgoalsTable").append('<tr class="editGoalSubGoalRow"><td class="deleteGoalSubGoal"><i class="fa fa-minus"></i></td><td class="subGoalName">'+subgoal[0]+'</td><td>'+subgoal[1]+'</td><td>'+subgoal[2]+'</td><td>'+subgoal[3]+'</td><td>'+subgoal[4]+'</td></tr>');
}
function appendGoalConcern(concern){
  $("#editgoalsConcernTable").append('<tr><td class="deleteGoalEnvConcern" value="'+ concern+'"><i class="fa fa-minus"></i></td><td class="GoalConcernName">'+concern+'</td></tr>');
}
function appendGoalConcernAssoc(assoc){
  $("#editgoalsConcernassociationsTable").append('<tr class="editGoalConcernAssoc"><td class="deleteGoalEnvConcernAssoc"><i class="fa fa-minus"></i></td><td class="assocName">'+assoc[0]+'</td><td class="assocN1">'+assoc[1]+'</td><td class="assocLink">'+assoc[2]+'</td><td class="assocN2">'+assoc[4]+'</td><td class="assocTarget">'+assoc[3]+'</td></tr>');
}

mainContent.on('click', '#closeGoalButton', function (e) {
  e.preventDefault();
  createEditGoalsTable();
});

function getAllgoals(callback) {
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/goals",
    success: function (data) {
      if (jQuery.isFunction(callback)) {
        callback(data);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      return null;
    }
  });
}

$(document).on('click', "td.deleteGoalButton", function (e) {
  e.preventDefault();
  var goalName = $(this).find('i').attr("value");
  deleteObject('goal',goalName,function(goalName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/goals/name/" + goalName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        createEditGoalsTable();
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

function putGoal(goal, oldName, callback){
  var output = {};
  output.object = goal;
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
    url: serverIP + "/api/goals/name/" + oldName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
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

function postGoal(goal, callback){
  var output = {};
  output.object = goal;
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
    url: serverIP + "/api/goals" + "?session_id=" + $.session.get('sessionID'),
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

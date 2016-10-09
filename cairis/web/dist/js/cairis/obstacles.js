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

$("#obstaclesClick").click(function(){
  createEditObstaclesTable();
});

$("#obstacleMenuClick").click(function(){
  createEditObstaclesTable();
});

$(document).on('click', "button.editObstaclesButton",function() {
  var name = $(this).attr("value");
  getObstacleOptions(name);
});

var optionsContent = $("#optionsContent");
optionsContent.on('click', ".obstacleEnvProperties", function () {
  var obstacle = JSON.parse($.session.get("Obstacle"));
  var name = $(this).text();
  $.session.set("ObstacleEnvName", name);
  emptyGoalEnvTables();

  $.each(obstacle.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == name){
      $('#obstacleProperties').loadJSON(env,null);
      $("#theDefinition").val(env.theDefinition);

      $.each(env.theGoalRefinements, function (index, obstacle) {
        appendObstacleEnvGoals(obstacle);
      });
      $.each(env.theSubGoalRefinements, function (index, subobstacle) {
        appendObstacleSubGoal(subobstacle);
      });
      $.each(env.theConcerns, function (index, concern) {
        appendObstacleConcern(concern);
      });
    }
  });
});

optionsContent.on('click',".obstacle_deleteGoalSubGoal", function () {
  var obstacle = JSON.parse($.session.get("Obstacle"));
  var envName = $.session.get("ObstacleEnvName");
  var subGoalName =  $(this).closest("tr").find(".subGoalName").text();
  $(this).closest("tr").remove();
  $.each(obstacle.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      $.each(env.theSubGoalRefinements, function (ix, subobstacle) {
        if(subobstacle[0] == subGoalName){
          env.theSubGoalRefinements.splice(ix,1)
        }
      });
    }
  });
  $.session.set("Obstacle", JSON.stringify(obstacle));
});

optionsContent.on('click',"#addConcerntoObstacle", function () {
  hasAsset = [];
  $("#editObstaclesConcernTable").find('tbody').find('.ObstacleConcernName').each(function (index, td) {
    hasAsset.push($(td).text());
  });
  var envName = $.session.get("ObstacleEnvName");
  assetsInEnvDialogBox(envName, hasAsset, function (text) {
    var obstacle = JSON.parse($.session.get("Obstacle"));
    $.each(obstacle.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        env.theConcerns.push(text);
      }
    });
    appendObstacleConcern(text);
    $.session.set("Obstacle", JSON.stringify(obstacle));
  });
});

optionsContent.on('click',".obstacle_deleteGoalGoal", function () {
  var obstacle = JSON.parse($.session.get("Obstacle"));
  var envName = $.session.get("ObstacleEnvName");
  var subGoalName =  $(this).closest("tr").find(".envGoalName").text();
  $(this).closest("tr").remove();
  $.each(obstacle.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      $.each(env.theGoalRefinements, function (ix, theobstacle) {
        if(typeof theobstacle != "undefined"){
          if(theobstacle[0] == subGoalName){
            env.theGoalRefinements.splice(ix,1)
          }
        }
      });
    }
  });
  $.session.set("Obstacle", JSON.stringify(obstacle));
});

optionsContent.on('click',".deleteObstacleEnvConcern", function () {
  var obstacle = JSON.parse($.session.get("Obstacle"));
  var envName = $.session.get("ObstacleEnvName");
  var name =  $(this).closest("tr").find(".ObstacleConcernName").text();
  $(this).closest("tr").remove();
  $.each(obstacle.theEnvironmentProperties, function (index, env) {
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
  $.session.set("Obstacle", JSON.stringify(obstacle));
});

optionsContent.on('click', '#obstacle_addSubGoaltoGoal', function () {
  $("#obstacle_editGoalSubGoal").addClass("new");
  toggleObstacleWindow("#obstacle_editGoalSubGoal");
  fillObstacleEditSubGoal();
});

optionsContent.on('click', '#obstacle_addGoaltoGoal', function () {
  $("#obstacle_editGoalGoal").addClass("new");
  toggleObstacleWindow("#obstacle_editGoalGoal");
  fillObstacleEditGoal();
});

optionsContent.on("click", "#addObstacleEnvironment", function () {
  var hasEnv = [];
  $(".obstacleEnvProperties").each(function (index, tag) {
    hasEnv.push($(tag).text());
  });
  environmentDialogBox(hasEnv, function (text) {
    appendObstacleEnvironment(text);
    var environment =  jQuery.extend(true, {},obstacle.nvDefault );
    environment.theEnvironmentName = text;
    var obstacle = JSON.parse($.session.get("Obstacle"));
    obstacle.theEnvironmentProperties.push(environment);
    $("#obstacleProperties").show("fast");
    $.session.set("Obstacle", JSON.stringify(obstacle));
  });
});

optionsContent.on('click', ".deleteObstacleEnv", function () {
  var envi = $(this).next(".obstacleEnvProperties").text();
  $(this).closest("tr").remove();
  var obstacle = JSON.parse($.session.get("Obstacle"));
  $.each(obstacle.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envi){
      obstacle.theEnvironmentProperties.splice( index ,1 );
      $.session.set("Obstacle", JSON.stringify(obstacle));
      var UIenv =  $("#theObstacleEnvironments").find("tbody");
      if(jQuery(UIenv).has(".obstacleEnvProperties").length){
        UIenv.find(".obstacleEnvProperties:first").trigger('click');
      }
      else {
        $("#obstacleProperties").hide("fast");
      }
      return false;
    }
  });
});

optionsContent.on('click', '#obstacle_updateGoalSubGoal', function () {
  var obstacle = JSON.parse($.session.get("Obstacle"));
  var envName = $.session.get("ObstacleEnvName");
  if($("#obstacle_editGoalSubGoal").hasClass("new")){
    $("#obstacle_editGoalSubGoal").removeClass("new");
    $.each(obstacle.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        var array = [];
        array[1] = $("#obstacle_theSubgoalType").val();
        array[0] = $("#theSubGoalName").val();
        array[2] = $("#obstacle_theRefinementSelect").val();
        array[3] = $("#obstacle_theAlternate").val();
        array[4] = $("#obstacle_theGoalSubGoalRationale").val();
        env.theSubGoalRefinements.push(array);
      }
    });
  } 
  else {
    var oldName = $.session.get("oldsubGoalName");
    $.each(obstacle.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        $.each(env.theSubGoalRefinements, function (index, arr) {
          if(arr[0] == oldName) {
            arr[1] = $("#obstacle_theSubgoalType").val();
            arr[0] = $("#theSubGoalName").val();
            arr[2] = $("#obstacle_theRefinementSelect").val();
            arr[3] = $("#obstacle_theAlternate").val();
            arr[4] = $("#obstacle_theGoalSubGoalRationale").val();
          }
        });
      }
    });
  }
  $.session.set("Obstacle", JSON.stringify(obstacle));
  fillObstacleOptionMenu(obstacle);
  toggleObstacleWindow("#editObstacleOptionsForm");
});

optionsContent.on('change', ".obstacleAutoUpdater" ,function() {
  var obstacle = JSON.parse($.session.get("Obstacle"));
  var envName = $.session.get("ObstacleEnvName");
  var name = $(this).attr("name");
  var element = $(this);

  $.each(obstacle.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      if($(element).is("input")){
        env[name] = $(element).val();
      }
      else if($(element).is("textarea")) {
        env[name] = $(element).val();
      }
      else {
        env[name] = $(element).find(":selected").text();
      }
      $.session.set("Obstacle", JSON.stringify(obstacle));
    }
  });
});

$(document).on('click', '#addNewObstacle', function () {
  fillObstacleOptionMenu(null, function () {
    $("#editObstacleOptionsForm").addClass('new');
    $("#optionsHeaderGear").text("Obstacle properties");
    forceOpenOptions();
    $("#obstacleProperties").hide();
  });
});


optionsContent.on('click', "#updateObstacleButton", function (e) {
  e.preventDefault();
  var obstacle = JSON.parse($.session.get("Obstacle"));
  var oldName = obstacle.theName;
  obstacle.theName = $("#theName").val();
  obstacle.theOriginator = $("#theOriginator").val();
  var tags = $("#theTags").text().split(", ");
  if(tags[0] != ""){
    obstacle.theTags = tags;
  }
  if($("#editObstacleOptionsForm").hasClass("new")){
    postGoal(obstacle, function () {
      createEditObstaclesTable();
      $("#editAttackerOptionsForm").removeClass("new")
    });
  } 
  else {
    putGoal(obstacle, oldName, function () {
      createEditObstaclesTable();
    });
  }
});

optionsContent.on('dblclick', '.obstacle_editGoalSubGoalRow', function () {
  toggleObstacleWindow("#obstacle_editGoalSubGoal");
  var name = $(this).find("td").eq(1).text();
  fillObstacleEditSubGoal(name);
  var type = $(this).find("td").eq(2).text();
  var refinement = $(this).find("td").eq(3).text();
  var target = $(this).find("td").eq(4).text();
  var rationale = $(this).find("td").eq(5).text();
  $.session.set("oldsubGoalName", name);

  $("#obstacle_theSubgoalType").val(type);
  $("#obstacle_theRefinementSelect").val(refinement);
  $("#obstacle_theAlternate").val(target);
  $("#obstacle_theGoalSubGoalRationale").val(rationale);
});

optionsContent.on('dblclick', '.obstacle_editGoalGoalRow', function () {
  toggleObstacleWindow("#obstacle_editGoalGoal");
  var name = $(this).find("td").eq(1).text();
  fillObstacleEditGoal(name);

  var type = $(this).find("td").eq(2).text();
  var refinement = $(this).find("td").eq(3).text();
  var target = $(this).find("td").eq(4).text();
  var rationale = $(this).find("td").eq(5).text();
  $.session.set("oldGoalName", name);

  $("#obstacle_theGoalType").val(type);
  $("#obstacle_theGoalRefinementSelect").val(refinement);
  $("#obstacle_theGoalAlternate").val(target);
  $("#obstacle_theGoalGoalRationale").val(rationale);
});

optionsContent.on('click',"#obstacle_updateGoalGoal", function () {
  var obstacle = JSON.parse($.session.get("Obstacle"));
  var envName = $.session.get("ObstacleEnvName");
  if($("#obstacle_editGoalGoal").hasClass("new")) {
    $("#obstacle_editGoalGoal").removeClass("new");
    $.each(obstacle.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        var array = [];
        array[1] = $("#obstacle_theGoalType").val();
        array[0] = $("#obstacle_theGoalName").val();
        array[2] = $("#obstacle_theGoalRefinementSelect").val();
        array[3] = $("#obstacle_theGoalAlternate").val();
        array[4] = $("#obstacle_theGoalGoalRationale").val();
        env.theGoalRefinements.push(array);
      }
    });
  }
  else {
    $.each(obstacle.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        var oldname = $.session.get("oldGoalName");
        $.each(env.theGoalRefinements, function (index, ref) {
          if(ref[0] == oldname){
            ref[1] = $("#obstacle_theGoalType").val();
            ref[0] = $("#obstacle_theGoalName").val();
            ref[2] = $("#obstacle_theGoalRefinementSelect").val();
            ref[3] = $("#obstacle_theGoalAlternate").val();
            ref[4] = $("#obstacle_theGoalGoalRationale").val();
          }
        });
      }
    });
  }
  $.session.set("Obstacle", JSON.stringify(obstacle));
  fillObstacleOptionMenu(obstacle);
  toggleObstacleWindow("#editObstacleOptionsForm");
});

function getObstacleOptions(name){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/obstacles/name/" + name.replace(" ", "%20"),
    success: function (data) {
      fillObstacleOptionMenu(data);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function fillObstacleOptionMenu(data,callback){
  fillOptionMenu("fastTemplates/editObstaclesOptions.html","#optionsContent",null,true,true, function(){
    if(data != null) {
      $.session.set("Obstacle", JSON.stringify(data));
      $('#editObstacleOptionsForm').loadJSON(data, null);

      $.each(data.theTags, function (index, tag) {
        $("#theTags").append(tag + ", ");
      });
      $.each(data.theEnvironmentProperties, function (index, prop) {
        appendObstacleEnvironment(prop.theEnvironmentName);
      });
      $("#optionsHeaderGear").text("Obstacle properties");
      forceOpenOptions();
      $("#theObstacleEnvironments").find(".obstacleEnvProperties:first").trigger('click');
    }
    else {
      var obstacle =  jQuery.extend(true, {},obstacle.efault );
      $.session.set("Obstacle", JSON.stringify(obstacle));
    }
    if (jQuery.isFunction(callback)) {
      callback();
    }
  });
}

function fillObstacleEditSubGoal(theSettableValue){
  $("#theSubGoalName").empty();
  var subname = $("#theSubGoalName");
  getAllGoals(function (data) {
    $.each(data, function (key, goals) {
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

function fillObstacleEditGoal(theSettableValue){
  var obstacle_theGoalName = $("#obstacle_theGoalName");
  obstacle_theGoalName.empty();
  getAllGoals(function (data) {
    $.each(data, function (key, goal) {
      obstacle_theGoalName.append($("<option></option>")
        .attr("value", key)
        .text(key));
    });
  });
  getAllRequirements(function (data) {
    $.each(data, function (key, req) {
      theGoal.name.append($("<option></option>")
        .attr("value", req.theLabel)
        .text(req.theLabel));
    });
    if (typeof theSettableValue  !== "undefined"){
      theobstacle.same.val(theSettableValue);
    }
  });
}

function toggleObstaclewindow(window){
  $("#editObstacleOptionsForm").hide();
  $("#obstacle_editGoalSubGoal").hide();
  $("#obstacle_editGoalGoal").hide();
  $(window).show();
}

function emptyObstacleEnvTables(){
  $("#editObstaclesGoalsTable").find("tbody").empty();
  $("#editObstaclesSubGoals.Table").find("tbody").empty();
  $("#editObstaclesConcernTable").find("tbody").empty();
}

function appendObstacleEnvironment(text){
  $("#theObstacleEnvironments").append("<tr><td class='deleteObstacleEnv'><i class='fa fa-minus'></i></td><td class='obstacleEnvProperties'>"+ text +"</td></tr>");
}
function appendObstacleEnvGoals(obstacle){
  $("#editObstaclesGoalsTable").append('<tr class="obstacle_editGoalGoalRow"><td class="obstacle_deleteGoalGoal"><i class="fa fa-minus"></i></td><td class="envGoalName">'+obstacle[0]+'</td><td>'+obstacle[1]+'</td><td>'+obstacle[2]+'</td><td>'+obstacle[3]+'</td><td>'+obstacle[4]+'</td></tr>');
}
function appendObstacleSubGoal(subobstacle){
  $("#editObstaclesSubGoalsTable").append('<tr class="obstacle_editGoalSubGoalRow"><td class="obstacle_deleteGoalSubGoal"><i class="fa fa-minus"></i></td><td class="subGoalName">'+subobstacle[0]+'</td><td>'+subobstacle[1]+'</td><td>'+subobstacle[2]+'</td><td>'+subobstacle[3]+'</td><td>'+subobstacle[4]+'</td></tr>');
}
function appendObstacleConcern(concern){
    $("#editObstaclesConcernTable").append('<tr><td class="deleteObstacleEnvConcern" value="'+ concern+'"><i class="fa fa-minus"></i></td><td class="ObstacleConcernName">'+concern+'</td></tr>');
}

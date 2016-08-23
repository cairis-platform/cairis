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

$("#countermeasuresClick").click(function () {
  createCountermeasuresTable();
});

/*
 A function for filling the table with Countermeasures
 */
function createCountermeasuresTable(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/countermeasures",
    success: function (data) {
      window.activeTable = "Countermeasures";
      setTableHeader();
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td><button class="editCountermeasuresButton" value="' + key + '">' + 'Edit' + '</button> <button class="deleteCountermeasuresButton" value="' + key + '">' + 'Delete' + '</button></td>';

        textToInsert[i++] = '<td name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theType">';
        textToInsert[i++] = item.theType;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      });

      theTable.append(textToInsert.join(''))
      theTable.css("visibility","visible");

      activeElement("reqTable");
      sortTableByRow(0);

    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}


var optionsContent = $("#optionsContent");
$(document).on('click', ".editCountermeasuresButton", function () {
  var name = $(this).val();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/countermeasures/name/" + name.replace(" ", "%20"),
    success: function (data) {
      fillOptionMenu("fastTemplates/editCountermeasureOptions.html", "#optionsContent", null, true, true, function () {
        $("#optionsHeaderGear").text("Countermeasure properties");
        forceOpenOptions();
        $("#addPropertyDiv").hide();

        $.session.set("Countermeasure", JSON.stringify(data));
        var fillerJSON = data;
        var tags = data.theTags;
        fillerJSON.theTags = [];
        var text = "";
        $.each(tags, function (index, type) {
          text += type + ", ";
        });
        $("#theTags").val(text);

        $('#editCountermeasureOptionsForm').loadJSON(fillerJSON, null);
        $.each(data.theEnvironmentProperties, function (index, env) {
          appendCountermeasureEnvironment(env.theEnvironmentName)
        });
        $("#theEnvironments").find(".countermeasureEnvironments:first").trigger('click');

      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$(document).on("click", "#addNewCountermeasure", function () {
  fillOptionMenu("fastTemplates/editCountermeasureOptions.html", "#optionsContent", null, true, true, function () {
    $("#addPropertyDiv").hide();
    $("#editCountermeasureOptionsForm").addClass("new");
    $.session.set("Countermeasure", JSON.stringify(jQuery.extend(true, {},countermeasureDefault )));
    $("#optionsHeaderGear").text("Countermeasure properties");
    forceOpenOptions();
  });
});

optionsContent.on("click", ".countermeasureEnvironments", function () {
  clearCountermeasureEnvInfo();
  var countermeasure = JSON.parse($.session.get("Countermeasure"));
  var envName = $(this).text();
  $.session.set("countermeasureEnvironmentName", envName);
  $("#theRequirements").find("tbody").empty();
  $("#theTargets").find("tbody").empty();
  $("#countermeasureProperties").find("tbody").empty();
  $("#theRoles").find("tbody").empty();
  $("#thePersonas").find("tbody").empty();
  $.each(countermeasure.theEnvironmentProperties, function (index, env) {
    if(envName == env.theEnvironmentName){
      $("#theCost").val(env.theCost);
      $.each(env.theRequirements, function (index,requirement) {
        appendCountermeasureRequirement(requirement);
      });
      $.each(env.theTargets, function (index,target) {
        appendCountermeasureTarget(target);
      });
      $.each(env.theRoles, function (index,role) {
        appendCountermeasureRole(role);
      });
      $.each(env.thePersonas, function (index,persona) {
        appendCountermeasurePersona(env.thePersonas[index]['theTask'],env.thePersonas[index]['thePersona'],env.thePersonas[index]['theDuration'],env.thePersonas[index]['theFrequency'],env.thePersonas[index]['theDemands'],env.thePersonas[index]['theGoalConflict']);
      });
      $.each(env.theProperties, function (index,prop) {
        if( prop.value != "None"){
          appendCountermeasureProperty(prop);
        }
      });
    }
  });
});


optionsContent.on('click', '#addAssettoThreat', function () {
    var hasAssets = [];
    $("#threatAssets").find(".threatAssets").each(function(index, asset){
        hasAssets.push($(asset).text());
    });
    assetsDialogBox(hasAssets, function (text) {
        var threat = JSON.parse($.session.get("Countermeasure"));
        var theEnvName = $.session.get("threatEnvironmentName");
        $.each(threat.theEnvironmentProperties, function (index, env) {
            if(env.theEnvironmentName == theEnvName){
                env.theAssets.push(text);
                $.session.set("Countermeasure", JSON.stringify(threat));
                appendThreatAsset(text);
            }
        });
    });
});
optionsContent.on('click','#addAttackertoThreat', function () {
    var hasAttackers = [];
    var theEnvName = $.session.get("threatEnvironmentName");
    $("#threatAttackers").find(".threatAttackers").each(function(index, attacker){
        hasAttackers.push($(attacker).text());
    });
    if(hasAttackers.length <= 0){
        alert("Unable to add attackers without specifying an environment.")
    }else {
        attackerDialogBox(hasAttackers, theEnvName, function (text) {
            var threat = JSON.parse($.session.get("Countermeasure"));
            $.each(threat.theEnvironmentProperties, function (index, env) {
                if (env.theEnvironmentName == theEnvName) {
                    env.theAttackers.push(text);
                    $.session.set("Countermeasure", JSON.stringify(threat));
                    appendThreatAttacker(text);
                }
            });
        });
    }
});
optionsContent.on('change', '#theLikelihood', function () {
    var threat = JSON.parse($.session.get("Countermeasure"));
    var theEnvName = $.session.get("threatEnvironmentName");
    $.each(threat.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == theEnvName){
            env.theLikelihood = $("#theLikelihood option:selected").text();
            $.session.set("Countermeasure", JSON.stringify(threat));
        }
    });
});

optionsContent.on('click', '.removeCountermeasureRequirement', function () {
  var reqText = $(this).closest(".countermeasureRequirements").text();
  $(this).closest("tr").remove();
  var countermeasure = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");
  $.each(countermeasure.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theRequirements.splice( $.inArray(reqText,env.theRequirements) ,1 );
      $.session.set("Countermeasure", JSON.stringify(countermeasure));
    }
  });
});

optionsContent.on('click', '.removeCountermeasureTarget', function () {
  var targetText = $(this).closest(".countermeasureTargets").text();
  $(this).closest("tr").remove();
  var countermeasure = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");
  $.each(countermeasure.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theTargets.splice( $.inArray(targetText,env.theTargets) ,1 );
      $.session.set("Countermeasure", JSON.stringify(countermeasure));
    }
  });
});

optionsContent.on('click', '.removeCountermeasureRole', function () {
  var roleText = $(this).closest(".countermeasureRoles").text();
  $(this).closest("tr").remove();
  var countermeasure = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");
  $.each(countermeasure.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theRoles.splice( $.inArray(roleText,env.theRoles) ,1 );
      $.session.set("Countermeasure", JSON.stringify(countermeasure));
    }
  });
});


optionsContent.on('click','#addPropertytoCountermeasure', function () {
  $("#editCountermeasureOptionsForm").hide();
  fillCountermeasurePropProperties();
  $("#addPropertyDiv").show('slow').addClass("newProp");
});

optionsContent.on('click',"#UpdateCountermeasureProperty", function () {
  var prop = {};
  var countermeasure = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");
  prop.value = $("#thePropValue option:selected").text();
  prop.name = $("#thePropName option:selected").text();
  prop.rationale = $("#thePropRationale").val();

  if($("#addPropertyDiv").hasClass("newProp")){
    appendCountermeasureProperty(prop);
    $.each(countermeasure.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        env.theProperties.push(prop);
      }
    });
    $.session.set("Countermeasure", JSON.stringify(threat));
    toggleCountermeasureOptions();
  } 
  else {
    var theRow = $(".changeAbleProp");
    var oldname = $(theRow).find("td:eq(1)").text();
    $(theRow).find("td:eq(1)").text(prop.name);
    $(theRow).find("td:eq(2)").text(prop.value);
    $(theRow).find("td:eq(3)").text(prop.rationale);
    $.each(countermeasure.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        $.each(env.theProperties, function (index, proper) {
          if(proper.name == oldname){
            proper.name = prop.name;
            proper.value = prop.value;
            proper.rationale = prop.rationale;
          }
        });
      }
    });
    $.session.set("Countermeasure", JSON.stringify(countermeasure));
    toggleCountermeasureOptions();
  }
});

optionsContent.on("dblclick",".changeProperty", function () {
  $(this).addClass("changeAbleProp");
  toggleCountermeasureOptions();
  var text =  $(this).find("td:eq(1)").text();
  fillCountermeasurePropProperties(text);
  var value = $(this).find("td:eq(2)").text();
  $("#thePropValue").val(value);
  $("#thePropRationale").val($(this).find("td:eq(3)").text());
});

optionsContent.on("click", "#addCountermeasureEnv", function () {
  var hasEnv = [];
  $(".countermeasureEnvironments").each(function (index, tag) {
    hasEnv.push($(tag).text());
  });
  environmentDialogBox(hasEnv, function (text) {
    appendCountermeasureEnvironment(text);
    var environment =  jQuery.extend(true, {},threatEnvironmentDefault );
    environment.theEnvironmentName = text;
    var countermeasure = JSON.parse($.session.get("Countermeasure"));
    countermeasure.theEnvironmentProperties.push(environment);
    $.session.set("Countermeasure", JSON.stringify(countermeasure));
    $(document).find(".countermeasuresEnvironments").each(function () {
      if($(this).text() == text) {
        $(this).trigger("click");
        $("#Properties").show("fast");
      }
    });
  });
});

optionsContent.on('click', '#UpdateCountermeasure', function (e) {
  e.preventDefault();
  var test = $.session.get("Countermeasure");
  var countermeasure = JSON.parse($.session.get("Countermeasure"));
  var oldName = countermeasure.theName;
  countermeasure.theName = $("#CountermeasureName").val();
  threat.theMethod = $("#theMethod").val();
  var tags = $("#theTags").text().split(", ");
  threat.theTags = tags;
  threat.theType = $("#theType option:selected").text();

  if($("#editCountermeasureOptionsForm").hasClass("new")){
    postCountermeasure(threat, function () {
      createCountermeasuresTable();
    });
  } 
  else {
    putCountermeasure(threat, oldName, function () {
      createCountermeasuresTable();
    });
  }
});

optionsContent.on('click', ".deleteCountermeasureEnv", function () {
  var envi = $(this).next(".countermeasuresEnvironments").text();
  $(this).closest("tr").remove();
  var countermeasure = JSON.parse($.session.get("Countermeasure"));
  $.each(countermeasure.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envi){
      countermeasure.theEnvironmentProperties.splice( index ,1 );
      $.session.set("Countermeasure", JSON.stringify(threat));

      var UIenv = $("#CountermeasureEnvironments").find("tbody");
      if(jQuery(UIenv).has(".countermeasuresEnvironments").length){
        UIenv.find(".countermeasuresEnvironments:first").trigger('click');
      }
      else {
        $("#Properties").hide("fast");
      }
      return false;
    }
  });
});

optionsContent.on('click', ".removeCountermeasureProperty", function () {
  var attacker = $(this).closest(".threatAttackers").text();
  $(this).closest("tr").remove();
  var countermeasure = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");
  $.each(countermeasure.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theAttackers.splice( $.inArray(attacker,env.theAttackers) ,1 );
      $.session.set("Countermeasure", JSON.stringify(threat));
    }
  });
});

$(document).on('click', '.deleteCountermeasuresButton', function (e) {
  e.preventDefault();
  deleteCountermeasure($(this).val(), function () {
    createCountermeasuresTable();
  });
});

function fillCountermeasurePropProperties(extra){
  var propBox = $("#thePropName");
  propBox.empty();
  var countermeasure = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");
  $.each(countermeasure.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theProperties, function (index, prop) {
        if(prop.value == "None"){
          propBox.append($("<option></option>")
            .text(prop.name));
        }
      });
    }
  });
  if(typeof extra !== undefined && extra !=""){
    propBox.append($("<option></option>")
      .text(extra).val(extra));
    propBox.val(extra);
  }
}
function toggleCountermeasureOptions(){
    $("#editCountermeasureOptionsform").toggle();
    $("#addPropertyDiv").toggle();
}
function appendCountermeasureEnvironment(environment){
    $("#theEnvironments").find("tbody").append('<tr><td class="deleteCountermeasureEnv"><i class="fa fa-minus"></i></td><td class="countermeasureEnvironments">'+environment+'</td></tr>');
}

function appendCountermeasureRequirement(requirement){
    $("#theRequirements").find("tbody").append("<tr><td class='removeCountermeasureRequirement'><i class='fa fa-minus'></i></td><td class='countermeasureRequirements'>" + requirement + "</td></tr>").animate('slow');
}

function appendCountermeasureTarget(target){
    $("#theTargets").find("tbody").append("<tr><td class='removeCountermeasureTarget'><i class='fa fa-minus'></i></td><td class='countermeasureTargets'>" + target.theName + "</td><td>" + target.theEffectiveness + "</td></tr>").animate('slow');
}

function appendCountermeasureRole(role){
    $("#theRoles").find("tbody").append("<tr><td class='removeCountermeasureRole'><i class='fa fa-minus'></i></td><td class='countermeasureRoles'>" + role + "</td></tr>").animate('slow');
}

function appendCountermeasurePersona(task,persona,duration,frequency,demands,goalConflict) {
  $("#thePersonas").find("tbody").append("<tr><td class='removeCountermeasurePersona'><i class='fa fa-minus'></i></td><td class='countermeasurePersona'>" + task + "</td><td>" + persona + "</td><td>" + duration + "</td><td>" + frequency + "</td><td>" + demands + "</td><td>" + goalConflict +  "</td></tr>").animate('slow');
}

function appendCountermeasureProperty(prop){
    $("#countermeasureProperties").find("tbody").append("<tr class='changeProperty'><td class='removeCountermeasureProperty'><i class='fa fa-minus'></i></td><td class='countermeasureProperties'>" + prop.name + "</td><td>"+ prop.value +"</td><td>"+ prop.rationale+"</td></tr>").animate('slow');;
}
function clearCountermeasureEnvInfo(){
    $("#countermeasureProperties").find("tbody").empty();
    $("#theRequirements").find("tbody").empty();
    $("#theTargets").find("tbody").empty();
    $("#theRoles").find("tbody").empty();
    $("#thePersonas").find("tbody").empty();
}

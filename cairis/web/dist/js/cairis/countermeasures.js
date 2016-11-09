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

$("#countermeasuresClick").click(function () {
  createCountermeasuresTable();
});

$("#countermeasureMenuClick").click(function () {
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

        textToInsert[i++] = '<td class="deleteCountermeasureButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="countermeasure-rows" name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theType">';
        textToInsert[i++] = item.theType;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      });

      theTable.append(textToInsert.join(''))
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
  });
}


var mainContent = $("#objectViewer");
$(document).on('click', "td.countermeasure-rows", function () {
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
    url: serverIP + "/api/countermeasures/name/" + name.replace(" ", "%20"),
    success: function (data) {
      fillOptionMenu("fastTemplates/editCountermeasureOptions.html", "#objectViewer", null, true, true, function () {
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
        $("#theEnvironments").find(".countermeasuresEnvironments:first").trigger('click');

      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$(document).on("click", "#addNewCountermeasure", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editCountermeasureOptions.html", "#objectViewer", null, true, true, function () {
    $("#addPropertyDiv").hide();
    $("#editCountermeasureOptionsForm").addClass("new");
    $.session.set("Countermeasure", JSON.stringify(jQuery.extend(true, {},countermeasureDefault )));
    $("#Properties").hide();
  });
});

mainContent.on("click", ".countermeasuresEnvironments", function () {
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
        appendCountermeasurePersona(env.thePersonas[index].theTask,env.thePersonas[index].thePersona,env.thePersonas[index].theDuration,env.thePersonas[index].theFrequency,env.thePersonas[index].theDemands,env.thePersonas[index].theGoalConflict);
      });
      $.each(env.theProperties, function (index,prop) {
        if( prop.value != "None"){
          appendCountermeasureProperty(prop);
        }
      });
    }
  });
});


mainContent.on('click', '.removeCountermeasureRequirement', function () {
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

mainContent.on('click', '.removeCountermeasureTarget', function () {
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


mainContent.on('click', '.countermeasureTargets', function () {
  var targetRow = $(this).closest("tr");
  var targetTxt = targetRow.find("td:eq(1)").text();
  var countermeasure = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");
  $.each(countermeasure.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      var targetIdx = 0;
      for (var i = 0; i < env.theTargets.length; i++) {
        if (targetTxt == env.theTargets[i].theName) {
          targetIdx = i;
          break;
        }
      }
      var hasTargets = [];
          targetIdx = i;
      $("#theTargets").find(".countermeasureTargets").each(function(index, req){
        hasTargets.push($(req).text());
      });
      countermeasureTargetsDialogBox(hasTargets,env.theTargets[targetIdx], function (target) {
        var cm = JSON.parse($.session.get("Countermeasure"));
        var envName = $.session.get("countermeasureEnvironmentName");
        $.each(cm.theEnvironmentProperties, function (index, env) {
          if(env.theEnvironmentName == envName){
            env.theTargets[targetIdx] = target;
            $.session.set("Countermeasure", JSON.stringify(cm));
            targetRow.find("td:eq(1)").text(target.theName); 
            targetRow.find("td:eq(2)").text(target.theEffectiveness); 
          }
        });
      });
    }
  });
});

mainContent.on('click', '.removeCountermeasureRole', function () {
  var roleText = $(this).closest(".countermeasureRoles").text();
  $(this).closest("tr").remove();
  var countermeasure = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");
  $.each(countermeasure.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theRoles.splice( $.inArray(roleText,env.theRoles) ,1 );
      $.session.set("Countermeasure", JSON.stringify(countermeasure));
      updateCountermeasureTasks(theEnvName,env.theRoles);
    }
  });
});

mainContent.on('click', '.removeCountermeasurePersona', function () {
  var taskText = $(this).closest(".countermeasurePersonas").text();
  $(this).closest("tr").remove();
  var countermeasure = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");
  $.each(countermeasure.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.thePersonas.splice( $.inArray(taskText,env.thePersonas) ,1 );
      $.session.set("Countermeasure", JSON.stringify(countermeasure));
    }
  });
});

mainContent.on('click', '.countermeasurePersona', function () {
  var taskRow = $(this).closest("tr");
  var taskName = taskRow.find("td:eq(0)").text();
  var personaName = taskRow.find("td:eq(1)").text();
  var cm = JSON.parse($.session.get("Countermeasure"));
  var envName = $.session.get("countermeasureEnvironmentName");

  $.each(cm.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      var taskIdx = 0;
      $.each(env.thePersonas, function (idx, currentTp) {
        if ((currentTp.theTask == taskName) && (currentTp.thePersona = personaName)) {
          countermeasureTaskDialogBox(currentTp, function(updTp) {
            cm.theEnvironmentProperties[index].thePersonas[idx] = updTp;
            $.session.set("Countermeasure", JSON.stringify(cm));
            taskRow.find("td:eq(2)").text(updTp.theDuration);
            taskRow.find("td:eq(3)").text(updTp.theFrequency);
            taskRow.find("td:eq(4)").text(updTp.theDemands);
            taskRow.find("td:eq(5)").text(updTp.theGoalConflict);
          });
        }
      });
    }
  });
});


mainContent.on('click','#addPropertytoCountermeasure', function () {
  var hasProperties = [];
  $("#countermeasureProperties").find(".countermeasureProperties").each(function(index, prop){
    hasProperties.push($(prop).text());
  });
  securityPropertyDialogBox(hasProperties, undefined, function (prop) {
    var cm = JSON.parse($.session.get("Countermeasure"));
    var theEnvName = $.session.get("countermeasureEnvironmentName");
    $.each(cm.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        $.each(env.theProperties, function(idx, cmProp){
          if (prop.name == cmProp.name) {
            cmProp.value = prop.value;
            cmProp.rationale = prop.rationale;
            cm.theEnvironmentProperties[index].theProperties[idx] = cmProp;
            $.session.set("Countermeasure", JSON.stringify(cm));
            appendCountermeasureProperty(prop);
          }
        });
      }
    });
  });
});

mainContent.on('click', '.countermeasureProperties', function() {
  var propRow = $(this).closest("tr");
  var propName = propRow.find("td:eq(1)").text();
  var cm = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");

  var currentProp = {};
  $.each(cm.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theProperties, function(idx, cmProp){
        if (propName == cmProp.name) {
          currentProp = cmProp;
          var defaultProp = {};
          defaultProp.name = propName;
          defaultProp.value = 'None';
          defaultProp.rationale = '';
          cm.theEnvironmentProperties[index].theProperties[idx] = defaultProp;
        }
      });
    }
  });

  var hasProperties = [];
  $("#countermeasureProperties").find(".countermeasureProperties").each(function(index, prop){
    hasProperties.push($(prop).text());
  });

  securityPropertyDialogBox(hasProperties, currentProp, function (updProp) {
    $.each(cm.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        $.each(env.theProperties, function(idx, cmProp){
          if (updProp.name == cmProp.name) {
            cm.theEnvironmentProperties[index].theProperties[idx] = updProp;
            $.session.set("Countermeasure", JSON.stringify(cm));
            propRow.find("td:eq(1)").text(updProp.name);
            propRow.find("td:eq(2)").text(updProp.value);
            propRow.find("td:eq(3)").text(updProp.rationale);
          }
        });
      }
    });
  });

});

mainContent.on("click", "#addCountermeasureEnv", function () {
  var hasEnv = [];
  $(".countermeasuresEnvironments").each(function (index, tag) {
    hasEnv.push($(tag).text());
  });
  environmentDialogBox(hasEnv, function (text) {
    appendCountermeasureEnvironment(text);
    var environment =  jQuery.extend(true, {},countermeasureEnvDefault );
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

mainContent.on('click', '#UpdateCountermeasure', function (e) {
  e.preventDefault();
  var cm = JSON.parse($.session.get("Countermeasure"));
  var oldName = cm.theName;
  cm.theName = $("#theName").val();
  var tags = $("#theTags").text().split(", ");
  cm.theTags = tags;
  cm.theType = $("#theType option:selected").text();

  if($("#editCountermeasureOptionsForm").hasClass("new")){
    postCountermeasure(cm, function () {
      createCountermeasuresTable();
    });
  } 
  else {
    putCountermeasure(cm, oldName, function () {
      createCountermeasuresTable();
    });
  }
});

mainContent.on('click', ".deleteCountermeasureEnv", function () {
  var envi = $(this).next(".countermeasuresEnvironments").text();
  $(this).closest("tr").remove();
  var cm = JSON.parse($.session.get("Countermeasure"));
  $.each(cm.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envi){
      cm.theEnvironmentProperties.splice( index ,1 );
      $.session.set("Countermeasure", JSON.stringify(cm));

      var UIenv = $("#theEnvironments").find("tbody");
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

mainContent.on('click', ".removeCountermeasureProperty", function () {
  var propName = $(this).closest("tr").find("td:eq(1)").text();
  $(this).closest("tr").remove();
  var countermeasure = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");
  $.each(countermeasure.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      var idxToGo = 0;
      $.each(env.theProperties, function(index,prop) {
        if (prop.name == propName) {
          idxToGo = index;
        }
      });
      env.theProperties.splice( idxToGo ,1 );
      $.session.set("Countermeasure", JSON.stringify(countermeasure));
    }
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
          propBox.append($("<option></option>").text(prop.name));
        }
      });
    }
  });
  if(typeof extra !== undefined && extra !=""){
    propBox.append($("<option></option>").text(extra).val(extra));
  }
}
function toggleCountermeasureOptions(){
  $("#editCountermeasureOptionsform").toggle();
  $("#addPropertyDiv").toggle();
}
function appendCountermeasureEnvironment(environment){
  $("#theEnvironments").find("tbody").append('<tr><td class="deleteCountermeasureEnv"><i class="fa fa-minus"></i></td><td class="countermeasuresEnvironments">'+environment+'</td></tr>');
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
  $("#thePersonas").find("tbody").append("<tr><td class='countermeasurePersona'>" + task + "</td><td>" + persona + "</td><td>" + duration + "</td><td>" + frequency + "</td><td>" + demands + "</td><td>" + goalConflict +  "</td></tr>").animate('slow');
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

mainContent.on('click', '#CloseCountermeasure', function (e) {
  e.preventDefault();
  createCountermeasuresTable();
});

$(document).on('click', 'td.deleteCountermeasureButton', function (e) {
  e.preventDefault();
  var cmName = $(this).find('i').attr("value");
  deleteObject('countermeasure', cmName, function (cmName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/countermeasures/name/" + cmName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        createCountermeasuresTable();
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

function putCountermeasure(countermeasure, oldName, callback){
  var output = {};
  output.object = countermeasure;
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
    url: serverIP + "/api/countermeasures/name/" + oldName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
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

function postCountermeasure(countermeasure, callback){
  var output = {};
  output.object = countermeasure;
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
    url: serverIP + "/api/countermeasures" + "?session_id=" + $.session.get('sessionID'),
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

$(document).on("click", "#addRequirementToCountermeasure", function () {
  var hasReqs = [];
  $("#theRequirements").find(".countermeasureRequirements").each(function(index, req){
    hasReqs.push($(req).text());
  });
  countermeasureRequirementsDialogBox(hasReqs, function (text) {
    var cm = JSON.parse($.session.get("Countermeasure"));
    var theEnvName = $.session.get("countermeasureEnvironmentName");
    $.each(cm.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        env.theRequirements.push(text);
        $.session.set("Countermeasure", JSON.stringify(cm));
        appendCountermeasureRequirement(text);
      }
    });
  });
});

$(document).on("click", "#addTargetToCountermeasure", function () {

  var hasTargets = [];
  $("#theTargets").find(".countermeasureTargets").each(function(index, req){
    hasTargets.push($(req).text());
  });
  countermeasureTargetsDialogBox(hasTargets,undefined, function (target,undefined) {
    var cm = JSON.parse($.session.get("Countermeasure"));
    var envName = $.session.get("countermeasureEnvironmentName");
    $.each(cm.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        env.theTargets.push(target);
        $.session.set("Countermeasure", JSON.stringify(cm));
        appendCountermeasureTarget(target);
      }
    });
  });


});

function countermeasureTargetsDialogBox(haveTarget,currentTarget,callback){
  var dialogwindow = $("#ChooseTargetDialog");
  var envName = $.session.get("countermeasureEnvironmentName");
  var cm = JSON.parse($.session.get("Countermeasure"));
  var reqParams = '';
  $.each(cm.theEnvironmentProperties, function(index,env) {
    if (env.theEnvironmentName = envName) {
      reqParams = encodeQueryList('requirement',env.theRequirements);
    }
  });

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/countermeasures/targets/environment/" + envName.replace(" ","%20") + '?' + reqParams,
    success: function (data) {
      $("#chooseTarget").empty();
      var none = true;
      $.each(data, function(key, object) {
        var found = false;
        $.each(haveTarget,function(index, text) {
          if(text == key){
            found = true
          }
        });
        if(!found) {
          $("#chooseTarget").append('<option value="' + object + '">' + object + '</option>');
          none = false;
        }
      });
      if(currentTarget != undefined) {
        $("#chooseTarget").val(currentTarget.theName);
        $("#chooseEffectiveness").val(currentTarget.theEffectiveness);
        $("#enterRationale").val(currentTarget.theRationale);
      }
      if(!none) {
        dialogwindow.dialog({
          modal: true,
          buttons: {
            Ok: function () {
              var target = {}
              target.theName =  $("#chooseTarget").find("option:selected" ).text();
              target.theEffectiveness =  $("#chooseEffectiveness").val();
              target.theRationale =  $("#enterRationale").val();
              if(jQuery.isFunction(callback)){
                callback(target);
              }
              $(this).dialog("close");
            }
          }
        });
        $(".comboboxD").css("visibility", "visible");
      }
      else {
        alert("All targets are already added");
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function countermeasureRequirementsDialogBox(haveReq,callback){
  var dialogwindow = $("#ChooseRequirementDialog");
  var select = dialogwindow.find("select");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/requirement",
    success: function (data) {
      select.empty();
      var none = true;
      $.each(data, function(key, object) {
        var found = false;
        $.each(haveReq,function(index, text) {
          if(text == key){
            found = true
          }
        });
        if(!found) {
          select.append("<option value=" + object + ">" + object + "</option>");
          none = false;
        }
      });
      if(!none) {
        dialogwindow.dialog({
          modal: true,
          buttons: {
            Ok: function () {
              var text =  select.find("option:selected" ).text();
              if(jQuery.isFunction(callback)){
                callback(text);
              }
              $(this).dialog("close");
            }
          }
        });
        $(".comboboxD").css("visibility", "visible");
      }
      else {
        alert("All requirements are already added");
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function countermeasureTaskDialogBox(currentTp,callback){
  var dialogwindow = $("#EditCountermeasureTaskDialog");
  $("#theTask").val(currentTp.theTask);
  $("#thePersona").val(currentTp.thePersona);
  $("#theDuration").val(currentTp.theDuration);
  $("#theFrequency").val(currentTp.theFrequency);
  $("#theDemands").val(currentTp.theDemands);
  $("#theGoalConflict").val(currentTp.theGoalConflict);

  dialogwindow.dialog({
    modal: true,
    buttons: {
      Ok: function () {
        var updTp = {};
        updTp.theTask =  $("#theTask").val();
        updTp.thePersona =  $("#thePersona").val();
        updTp.theDuration =  $("#theDuration").val();
        updTp.theFrequency =  $("#theFrequency").val();
        updTp.theDemands =  $("#theDemands").val();
        updTp.theGoalConflict =  $("#theGoalConflict").val();
        if(jQuery.isFunction(callback)){
          callback(updTp);
        }
        $(this).dialog("close");
      }
    }
  });
  $("#EditCountermeasureTaskDialog").show();
}


mainContent.on('click', '#addRoleToCountermeasure', function () {
  var hasRole = [];
  $("#theRoles").find(".personaRole").each(function(index, role){
    hasRole.push($(role).text());
  });
  roleDialogBox(hasRole, function (text) {
    var cm = JSON.parse($.session.get("Countermeasure"));
    var theEnvName = $.session.get("countermeasureEnvironmentName");
    $.each(cm.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        env.theRoles.push(text);
        $.session.set("Countermeasure", JSON.stringify(cm));
        appendCountermeasureRole(text);
        updateCountermeasureTasks(theEnvName,env.theRoles);
      }
    });
  });
});

function updateCountermeasureTasks(envName,roleList) {
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/countermeasures/tasks/environment/" + envName.replace(" ","%20") + "?" + encodeQueryList("role",roleList),
    success: function (data) {
      $("#thePersonas").find("tbody").empty(); 
      var taskList = [];
      $.each(data, function(index,task) {
        taskList.push(task);
        appendCountermeasurePersona(task.theTask,task.thePersona,task.theDuration,task.theFrequency,task.theDemands,task.theGoalConflict); 
      });
      var cm = JSON.parse($.session.get("Countermeasure"));
      $.each(cm.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == envName){
          env.thePersonas = taskList;
          $.session.set("Countermeasure", JSON.stringify(cm));
        }
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

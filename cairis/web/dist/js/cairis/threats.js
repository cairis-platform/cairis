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

$("#threatMenuClick").click(function () {
  createThreatsTable();
});

function createThreatsTable(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/threats",
    success: function (data) {
      window.activeTable = "Threats";
      setTableHeader();
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td class="deleteThreatButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="threat-rows" name="theName">';
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
  })
}


var mainContent = $("#objectViewer");
$(document).on('click', "td.threat-rows", function () {
  var name = $(this).text();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/threats/name/" + name.replace(" ", "%20"),
    success: function (data) {
      activeElement("objectViewer");
      fillOptionMenu("fastTemplates/editThreatOptions.html", "#objectViewer", null, true, true, function () {
        $("#addPropertyDiv").hide();
        getThreatTypes(function createTypes(types) {
          $.each(types, function (index, type) {
            $('#theType').append($("<option></option>").attr("value",type.theName).text(type.theName));
          });
          $("#theType").val(data.theType);
        });

        $.session.set("theThreat", JSON.stringify(data));
        var fillerJSON = data;
        var tags = data.theTags;
        fillerJSON.theTags = [];
        var text = "";
        $.each(tags, function (index, type) {
          text += type + ", ";
        });
        $("#theTags").val(text);

        $('#editThreatOptionsform').loadJSON(fillerJSON, null);
        $.each(data.theEnvironmentProperties, function (index, env) {
          appendThreatEnvironment(env.theEnvironmentName)
        });
        $("#theThreatEnvironments").find(".threatEnvironments:first").trigger('click');
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$(document).on("click", "#addNewThreat", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editThreatOptions.html", "#objectViewer", null, true, true, function () {
    $("#addPropertyDiv").hide();
    $("#editThreatOptionsform").addClass("newThreat");
    getThreatTypes(function createTypes(types) {
      $.each(types, function (index, type) {
        $('#theType').append($("<option></option>").attr("value",type.theName).text(type.theName));
      });
      $("#Properties").hide();
    });

    $.session.set("theThreat", JSON.stringify(jQuery.extend(true, {},threatDefault )));
  });
});

mainContent.on("click", ".threatEnvironments", function () {
  clearThreatEnvInfo();
  var threat = JSON.parse($.session.get("theThreat"));
  var envName = $(this).text();
  $.session.set("threatEnvironmentName", envName);
  $("#threatAssets").find("tbody").empty();
  $("#threatAttackers").find("tbody").empty();
  $("#threatProperties").find("tbody").empty();
  $.each(threat.theEnvironmentProperties, function (index, env) {
    if(envName == env.theEnvironmentName){
      $.each(env.theAssets, function (index,asset) {
        appendThreatAsset(asset);
      });
      $.each(env.theAttackers, function (index,attacker) {
        appendThreatAttacker(attacker);
      });
      $.each(env.theProperties, function (index,prop) {
        if( prop.value != "None"){
          appendThreatProperty(prop);
        }
      });
      $("#theLikelihood").val(env.theLikelihood);
    }
  });
});

mainContent.on('click', '#addAssettoThreat', function () {
  var hasAssets = [];
  $("#threatAssets").find(".threatAssets").each(function(index, asset){
    hasAssets.push($(asset).text());
  });
  assetsDialogBox(hasAssets, function (text) {
    var threat = JSON.parse($.session.get("theThreat"));
    var theEnvName = $.session.get("threatEnvironmentName");
    $.each(threat.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        env.theAssets.push(text);
        $.session.set("theThreat", JSON.stringify(threat));
        appendThreatAsset(text);
      }
    });
  });
});

mainContent.on('click','#addAttackertoThreat', function () {
  var hasAttackers = [];
  var theEnvName = $.session.get("threatEnvironmentName");
  $("#threatAttackers").find(".threatAttackers").each(function(index, attacker){
    hasAttackers.push($(attacker).text());
  });
  if(hasAttackers.length <= 0){
    alert("Unable to add attackers without specifying an environment.")
  }
  else {
    attackerDialogBox(hasAttackers, theEnvName, function (text) {
      var threat = JSON.parse($.session.get("theThreat"));
      $.each(threat.theEnvironmentProperties, function (index, env) {
        if (env.theEnvironmentName == theEnvName) {
          env.theAttackers.push(text);
          $.session.set("theThreat", JSON.stringify(threat));
          appendThreatAttacker(text);
        }
      });
    });
  }
});

mainContent.on('change', '#theLikelihood', function () {
  var threat = JSON.parse($.session.get("theThreat"));
  var theEnvName = $.session.get("threatEnvironmentName");
  $.each(threat.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theLikelihood = $("#theLikelihood option:selected").text();
      $.session.set("theThreat", JSON.stringify(threat));
    }
  });
});

mainContent.on('click', '.removeThreatAsset', function () {
  var assetText = $(this).closest(".threatAssets").text();
  $(this).closest("tr").remove();
  var threat = JSON.parse($.session.get("theThreat"));
  var theEnvName = $.session.get("threatEnvironmentName");
  $.each(threat.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theAssets.splice( $.inArray(assetText,env.theAssets) ,1 );
      $.session.set("theThreat", JSON.stringify(threat));
    }
  });
});

mainContent.on('click','.removeThreatAttacker', function () {
  var attackerName = $(this).closest(".threatAttackers").text();
  $(this).closest("tr").remove();
  var theEnvName = $.session.get("threatEnvironmentName");
  var threat = JSON.parse($.session.get("theThreat"));
  $.each(threat.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theAttackers.splice( $.inArray(attackerName,env.theAttackers) ,1 );
      $.session.set("theThreat", JSON.stringify(threat));
    }
  });
});

mainContent.on('click','#addPropertytoThreat', function () {
  $("#editThreatOptionsform").hide();
  fillThreatPropProperties();
  $("#addPropertyDiv").show('slow').addClass("newProp");
});

mainContent.on('click',"#UpdateThreatProperty", function () {
  var prop = {};
  var threat = JSON.parse($.session.get("theThreat"));
  var theEnvName = $.session.get("threatEnvironmentName");
  prop.value = $("#thePropValue option:selected").text();
  prop.name = $("#thePropName option:selected").text();
  prop.rationale = $("#thePropRationale").val();

  if($("#addPropertyDiv").hasClass("newProp")){
    appendThreatProperty(prop);
    $.each(threat.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        env.theProperties.push(prop);
      }
    });
    $.session.set("theThreat", JSON.stringify(threat));
    toggleThreatOptions();
  } 
  else {
    var theRow = $(".changeAbleProp");
    var oldname = $(theRow).find("td:eq(1)").text();
    $(theRow).find("td:eq(1)").text(prop.name);
    $(theRow).find("td:eq(2)").text(prop.value);
    $(theRow).find("td:eq(3)").text(prop.rationale);
    $.each(threat.theEnvironmentProperties, function (index, env) {
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
    $.session.set("theThreat", JSON.stringify(threat));
    toggleThreatOptions();
  }
});

mainContent.on("dblclick",".changeProperty", function () {
  $(this).addClass("changeAbleProp");
  toggleThreatOptions();
  var text =  $(this).find("td:eq(1)").text();
  fillThreatPropProperties(text);
  var value = $(this).find("td:eq(2)").text();
  $("#thePropValue").val(value);
  $("#thePropRationale").val($(this).find("td:eq(3)").text());
});

mainContent.on("click", "#addThreatEnv", function () {
  var hasEnv = [];
  $(".threatEnvironments").each(function (index, tag) {
    hasEnv.push($(tag).text());
  });
  environmentDialogBox(hasEnv, function (text) {
    appendThreatEnvironment(text);
    var environment =  jQuery.extend(true, {},threatEnvironmentDefault );
    environment.theEnvironmentName = text;
    var threat = JSON.parse($.session.get("theThreat"));
    threat.theEnvironmentProperties.push(environment);
    $.session.set("theThreat", JSON.stringify(threat));
    $(document).find(".threatEnvironments").each(function () {
      if($(this).text() == text){
        $(this).trigger("click");
        $("#Properties").show("fast");
      }
    });
  });
});

mainContent.on('click', '#UpdateThreat', function (e) {
  e.preventDefault();
  var test = $.session.get("theThreat");
  var threat = JSON.parse($.session.get("theThreat"));
  var oldName = threat.theThreatName;
  threat.theThreatName = $("#theThreatName").val();
  threat.theMethod = $("#theMethod").val();
  var tags = $("#theTags").text().split(", ");
  threat.theTags = tags;
  threat.theType = $("#theType option:selected").text();

  if($("#editThreatOptionsform").hasClass("newThreat")){
    postThreat(threat, function () {
      createThreatsTable();
    });
  } 
  else {
    putThreat(threat, oldName, function () {
      createThreatsTable();
    });
  }
});

mainContent.on('click', ".deleteThreatEnv", function () {
  var envi = $(this).next(".threatEnvironments").text();
  $(this).closest("tr").remove();
  var threat = JSON.parse($.session.get("theThreat"));
  $.each(threat.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envi){
      threat.theEnvironmentProperties.splice( index ,1 );
      $.session.set("theThreat", JSON.stringify(threat));
      var UIenv = $("#theThreatEnvironments").find("tbody");
      if(jQuery(UIenv).has(".threatEnvironments").length){
        UIenv.find(".threatEnvironments:first").trigger('click');
      }
      else {
        $("#Properties").hide("fast");
      }
      return false;
    }
  });
});

mainContent.on('click', ".removeThreatProperty", function () {
  var attacker = $(this).closest(".threatAttackers").text();
  $(this).closest("tr").remove();
  var threat = JSON.parse($.session.get("theThreat"));
  var theEnvName = $.session.get("threatEnvironmentName");
  $.each(threat.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theAttackers.splice( $.inArray(attacker,env.theAttackers) ,1 );
      $.session.set("theThreat", JSON.stringify(threat));
    }
  });
});

$(document).on('click', 'td.deleteThreatButton', function (e) {
  e.preventDefault();
  var threatName = $(this).find('i').attr("value");
  deleteObject('threat', threatName, function (threatName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/threats/name/" + threatName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        createThreatsTable();
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

function fillThreatPropProperties(extra){
  var propBox = $("#thePropName");
  propBox.empty();
  var threat = JSON.parse($.session.get("theThreat"));
  var theEnvName = $.session.get("threatEnvironmentName");
  $.each(threat.theEnvironmentProperties, function (index, env) {
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

function getThreatTypes(callback){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/threats/types",
    success: function (data) {
      if(jQuery.isFunction(callback)){
        callback(data);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function toggleThreatOptions(){
  $("#editThreatOptionsform").toggle();
  $("#addPropertyDiv").toggle();
}

function appendThreatEnvironment(environment){
  $("#theThreatEnvironments").find("tbody").append('<tr><td class="deleteThreatEnv"><i class="fa fa-minus"></i></td><td class="threatEnvironments">'+environment+'</td></tr>');
}

function appendThreatAsset(asset){
  $("#threatAssets").find("tbody").append("<tr><td class='removeThreatAsset'><i class='fa fa-minus'></i></td><td class='threatAssets'>" + asset + "</td></tr>").animate('slow');
}

function appendThreatAttacker(attacker){
  $("#threatAttackers").find("tbody").append("<tr><td class='removeThreatAttacker' ><i class='fa fa-minus'></i></td><td class='threatAttackers'>" + attacker + "</td></tr>").animate('slow');
}

function appendThreatProperty(prop){
  $("#threatProperties").find("tbody").append("<tr class='changeProperty'><td class='removeThreatProperty'><i class='fa fa-minus'></i></td><td class='threatProperties'>" + prop.name + "</td><td>"+ prop.value +"</td><td>"+ prop.rationale+"</td></tr>").animate('slow');;
}

function clearThreatEnvInfo(){
  $("#threatProperties").find("tbody").empty();
  $("#threatAttackers").find("tbody").empty();
  $("#threatAssets").find("tbody").empty();
}

mainContent.on('click', '#CloseThreat', function (e) {
  e.preventDefault();
  createThreatsTable();
});


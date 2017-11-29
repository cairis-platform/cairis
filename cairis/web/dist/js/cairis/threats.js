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
  validateClick('threat',function() {
    clearLocalStorage($('#menuBCClick').attr('dimension'));
    $('#menuBCClick').attr('dimension','threat');
    refreshMenuBreadCrumb('threat');
  });
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
      setTableHeader("Threats");
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
        textToInsert[i++] = '<td class="deleteThreatButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="threat-rows" name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theType">';
        textToInsert[i++] = item.theType;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      }

      theTable.append(textToInsert.join(''))
      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
      $("#mainTable").find("tbody").removeClass();


      activeElement("mainTable");
      sortTableByRow(0);
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
}


var mainContent = $("#objectViewer");
$(document).on('click', "td.threat-rows", function () {
  var thrName = $(this).text();
  refreshObjectBreadCrumb(thrName);
  viewThreat(thrName);
});

function viewThreat(thrName) {
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/threats/name/" + encodeURIComponent(thrName),
    success: function (data) {
      activeElement("objectViewer");
      fillOptionMenu("fastTemplates/editThreatOptions.html", "#objectViewer", null, true, true, function () {
        $("#UpdateThreat").text("Update");
        refreshDimensionSelector($('#theType'),'threat_type',undefined,function(){
          $("#theType").val(data.theType);
        },['All']);
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
        $("#editThreatOptionsform").validator('update');
        $("#theThreatEnvironments").find(".threatEnvironments:first").trigger('click');
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
};

$(document).on("click", "#addNewThreat", function () {
  refreshObjectBreadCrumb('New Threat');
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editThreatOptions.html", "#objectViewer", null, true, true, function () {
    $("#editThreatOptionsform").validator();
    $("#UpdateThreat").text("Create");
    $("#editThreatOptionsform").addClass("newThreat");
    refreshDimensionSelector($('#theType'),'threat_type',undefined,function() {
      $("#Properties").hide();
    },['All']);
    $.session.set("theThreat", JSON.stringify(jQuery.extend(true, {},threatDefault )));
  });
});

function viewIntroducedThreat(dirEntry) {
  refreshObjectBreadCrumb(dirEntry.theLabel);
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editThreatOptions.html", "#objectViewer", null, true, true, function () {
    $("#UpdateThreat").text("Create");
    $("#editThreatOptionsform").addClass("newThreat");
    refreshDimensionSelector($('#theType'),'threat_type',undefined,function() {
      $("#Properties").hide();
    },['All']);
    $.session.set("theThreat", JSON.stringify(jQuery.extend(true, {},threatDefault )));
    $('#theThreatName').val(dirEntry.theLabel);
    $('#theType').val(dirEntry.theType); 
    $('#theMethod').val(dirEntry.theName + ': ' + dirEntry.theDescription + "\nReference: " + dirEntry.theReference); 
    $("#editThreatOptionsform").validator('update');
  });
}

$(document).on("click","#introduceThreatDirectoryEntry", function() {
  showDirectoryEntries('threat');
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
  var filterList = [];
  $("#threatAssets").find(".threatAssets").each(function(index, asset){
    filterList.push($(asset).text());
  });
  var theEnvName = $.session.get("threatEnvironmentName");
  refreshDimensionSelector($('#chooseEnvironmentSelect'),'asset',theEnvName,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','asset');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addAssetToThreatEnvironment');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addAssetToThreatEnvironment() {
  var text = $("#chooseEnvironmentSelect").val();
  var threat = JSON.parse($.session.get("theThreat"));
  var theEnvName = $.session.get("threatEnvironmentName");
  $.each(threat.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theAssets.push(text);
      $.session.set("theThreat", JSON.stringify(threat));
      appendThreatAsset(text);
    }
  });
};

mainContent.on('click','#addAttackertoThreat', function () {
  var filterList = [];
  var theEnvName = $.session.get("threatEnvironmentName");
  $("#threatAttackers").find(".threatAttackers").each(function(index, attacker){
    filterList.push($(attacker).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'attacker',theEnvName,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','attacker');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addAttackerToEnvironment');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addAttackerToEnvironment() {
  var text = $("#chooseEnvironmentSelect").val();
  var theEnvName = $.session.get("threatEnvironmentName");
  var threat = JSON.parse($.session.get("theThreat"));
  $.each(threat.theEnvironmentProperties, function (index, env) {
    if (env.theEnvironmentName == theEnvName) {
      env.theAttackers.push(text);
      $.session.set("theThreat", JSON.stringify(threat));
      appendThreatAttacker(text);
    }
  });
};

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

function updateThreatPropertyList() {
  resetSecurityPropertyList();

  var currentProperty = $("#chooseSecurityProperty").attr('data-currentproperty');
  if (currentProperty != '') {
    currentProperty = JSON.parse(currentProperty);
  }

  $("#threatProperties").find(".threatProperties").each(function(index, prop){
    if ((currentProperty != '') && (currentProperty.name == $(prop).text())) {
      // don't remove
    }
    else {
      $("#theSecurityPropertyName option[value='" + $(prop).text() + "']").remove();
    }
  });
  if (currentProperty != '') {
    $("#theSecurityPropertyName").val(currentProperty.name);
    $("#theSecurityPropertyValue").val(currentProperty.value);
    $("#theSecurityPropertyRationale").val(currentProperty.rationale);
  }
}

function addThreatSecurityProperty(e) {
  e.preventDefault()
  var prop = {};
  prop.name =  $("#theSecurityPropertyName").find("option:selected").text();
  prop.value =  $("#theSecurityPropertyValue").val();
  prop.rationale =  $("#theSecurityPropertyRationale").val()

  var threat = JSON.parse($.session.get("theThreat"));
  var theEnvName = $.session.get("threatEnvironmentName");
  $.each(threat.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theProperties, function(idx, secProp){
        if (prop.name == secProp.name) {
          secProp.value = prop.value;
          secProp.rationale = prop.rationale;
          threat.theEnvironmentProperties[index].theProperties[idx] = secProp;
          $.session.set("theThreat", JSON.stringify(threat));
          appendThreatProperty(prop);
        }
      });
    }
  });
  $("#chooseSecurityProperty").modal('hide');
}




mainContent.on('click','#addPropertytoThreat', function () {
  $("#chooseSecurityProperty").attr('data-updatepropertylist',"updateThreatPropertyList");
  $("#chooseSecurityProperty").attr("data-buildproperty","addThreatSecurityProperty");
  $("#chooseSecurityProperty").modal('show');
});

function updateThreatSecurityProperty() {
  var currentProperty = JSON.parse($("#chooseSecurityProperty").attr("data-currentproperty"));
  var propRow = undefined;

  $("#threatProperties").find("tr").each(function(index, row){
    if (currentProperty.name == $(row).find("td:eq(1)").text()) {
      propRow = $(row);
    }
  });

  var updProp = {};
  updProp.name =  $("#theSecurityPropertyName").find("option:selected").text();
  updProp.value =  $("#theSecurityPropertyValue").val();
  updProp.rationale =  $("#theSecurityPropertyRationale").val();

  var threat = JSON.parse($.session.get("theThreat"));
  var theEnvName = $.session.get("threatEnvironmentName");

  $.each(threat.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theProperties, function(idx, secProp){
        if (updProp.name == secProp.name) {
          threat.theEnvironmentProperties[index].theProperties[idx] = updProp;
          $.session.set("theThreat", JSON.stringify(threat));
          propRow.find("td:eq(1)").text(updProp.name);
          propRow.find("td:eq(2)").text(updProp.value);
          propRow.find("td:eq(3)").text(updProp.rationale);
        }
      });
    }
  });
  $("#chooseSecurityProperty").modal('hide');
}



mainContent.on("click",".threatProperties", function () {
  var propRow = $(this).closest("tr");
  var selectedProp = {};
  selectedProp.name = propRow.find("td:eq(1)").text();
  selectedProp.value = propRow.find("td:eq(2)").text();
  selectedProp.rationale = propRow.find("td:eq(3)").text();

  $("#chooseSecurityProperty").attr('data-updatepropertylist',"updateThreatPropertyList");
  $("#chooseSecurityProperty").attr("data-buildproperty","updateThreatSecurityProperty");
  $("#chooseSecurityProperty").attr("data-currentproperty",JSON.stringify(selectedProp));
  $("#chooseSecurityProperty").modal('show');
});

mainContent.on("click", "#addThreatEnv", function () {
  var filterList = [];
  $(".threatEnvironments").each(function (index, tag) {
    filterList.push($(tag).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'environment',undefined,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','environment');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addThreatEnvironment');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addThreatEnvironment() {
  var text = $("#chooseEnvironmentSelect").val();
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
};

function commitThreat() {
  var threat = JSON.parse($.session.get("theThreat"));
  if (threat.theEnvironmentProperties.length == 0) {
    alert("Environments not defined");
  }
  else {
    var oldName = threat.theThreatName;
    threat.theThreatName = $("#theThreatName").val();
    threat.theMethod = $("#theMethod").val();
    var tags = $("#theTags").text().split(", ");
    if (tags[0] != "") {
      threat.theTags = tags;
    }
    threat.theType = $("#theType option:selected").text();

    if($("#editThreatOptionsform").hasClass("newThreat")){
      postThreat(threat, function () {
        clearLocalStorage('threat');
        $('#menuBCClick').attr('dimension','threat');
        refreshMenuBreadCrumb('threat');
      });
    } 
    else {
      putThreat(threat, oldName, function () {
        clearLocalStorage('threat');
        $('#menuBCClick').attr('dimension','threat');
        refreshMenuBreadCrumb('threat');
      });
    }
  }
}

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
  var propName = $(this).closest("tr").find("td:eq(1)").text();
  $(this).closest("tr").remove();
  var threat = JSON.parse($.session.get("theThreat"));
  var theEnvName = $.session.get("threatEnvironmentName");
  $.each(threat.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theProperties, function(idx,prop) {
        if (prop.name == propName) {
          threat.theEnvironmentProperties[index].theProperties[idx].value = 'None';
          threat.theEnvironmentProperties[index].theProperties[idx].rationale = 'None';
        }
      });
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
      url: serverIP + "/api/threats/name/" + encodeURIComponent(threatName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        showPopup(true);
        $('#menuBCClick').attr('dimension','threat');
        refreshMenuBreadCrumb('threat');
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
  $("#threatProperties").find("tbody").append("<tr><td class='removeThreatProperty'><i class='fa fa-minus'></i></td><td class='threatProperties'>" + prop.name + "</td><td>"+ prop.value +"</td><td>"+ prop.rationale+"</td></tr>").animate('slow');;
}

function clearThreatEnvInfo(){
  $("#threatProperties").find("tbody").empty();
  $("#threatAttackers").find("tbody").empty();
  $("#threatAssets").find("tbody").empty();
}

mainContent.on('click', '#CloseThreat', function (e) {
  e.preventDefault();
  clearLocalStorage('threat');
  $('#menuBCClick').attr('dimension','threat');
  refreshMenuBreadCrumb('threat');
});

function putThreat(threat, oldName, callback){
  var output = {};
  output.object = threat;
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
    url: serverIP + "/api/threats/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
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

function postThreat(threat, callback){
  var output = {};
  output.object = threat;
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);

  $.ajax({
    type: "POST",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/threats" + "?session_id=" + $.session.get('sessionID'),
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


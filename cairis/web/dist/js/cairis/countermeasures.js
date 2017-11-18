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
  validateClick('countermeasure',function() {
    $('#menuBCClick').attr('dimension','countermeasure');
    refreshMenuBreadCrumb('countermeasure');
  });
});

$("#countermeasureMenuClick").click(function () {
  $('#menuBCClick').attr('dimension','countermeasure');
  refreshMenuBreadCrumb('countermeasure');
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
      setTableHeader("Countermeasures");
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

        textToInsert[i++] = '<td class="deleteCountermeasureButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="countermeasure-row" name="theName">';
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
      $("#mainTable").find("tbody").addClass('countermeasure-rows');
      $('.countermeasure-rows').contextMenu({
        selector: 'td',
        items: {
          "generateAsset": {
            name: "Generate Asset",
            callback: function(key, opt) {
              generateAsset($(this).closest("tr").find("td").eq(1).html());
            }
          },
          "generateAssetFromTemplate": {
            name: "Generate Asset from Template",
            callback: function(key, opt) {
              var cmName = $(this).closest("tr").find("td").eq(1).html();
	      $('#chooseEnvironment').attr('data-cmName',cmName);
              refreshDimensionSelector($('#chooseEnvironmentSelect'),'template_asset',undefined,function() {
                $('#chooseEnvironment').attr('data-chooseDimension',"Template Asset");
		$('#chooseEnvironment').attr('data-applyEnvironmentSelection',"generateAssetFromTemplate");
		$('#chooseEnvironment').modal('show');
	      });
            }
          },
          "situateCountermeasurePattern": {
            name: "Situate Countermeasure Pattern",
            callback: function(key, opt) {
              var cmName = $(this).closest("tr").find("td").eq(1).html();
	      $('#chooseEnvironment').attr('data-cmName',cmName);
              refreshDimensionSelector($('#chooseEnvironmentSelect'),'securitypattern',undefined,function() {
                $('#chooseEnvironment').attr('data-chooseDimension',"Security Pattern");
		$('#chooseEnvironment').attr('data-applyEnvironmentSelection',"situateCountermeasurePattern");
		$('#chooseEnvironment').modal('show');
	      });
            }
          },
          "associateWithSituatedPattern": {
            name: "Associate with situated pattern",
            callback: function(key, opt) {
              var cmName = $(this).closest("tr").find("td").eq(1).html();
	      $('#chooseEnvironment').attr('data-cmName',cmName);
              refreshSpecificSelector($('#chooseEnvironmentSelect'),'/api/countermeasures/name/' + encodeURIComponent(cmName) + '/candidate_patterns',function() {
                $('#chooseEnvironment').attr('data-chooseDimension',"Security Pattern");
		$('#chooseEnvironment').attr('data-applyEnvironmentSelection',"associateWithSituatedPattern");
		$('#chooseEnvironment').modal('show');
	      },['All']);
            }
          },
          "removeCountermeasurePattern": {
            name: "Remove countermeasure pattern",
            callback: function(key, opt) {
              var cmName = $(this).closest("tr").find("td").eq(1).html();
	      $('#chooseEnvironment').attr('data-cmName',cmName);
              refreshSpecificSelector($('#chooseEnvironmentSelect'),'/api/countermeasures/name/' + encodeURIComponent(cmName) + '/patterns',function() {
                $('#chooseEnvironment').attr('data-chooseDimension',"Security Pattern");
		$('#chooseEnvironment').attr('data-applyEnvironmentSelection',"removeCountermeasurePattern");
		$('#chooseEnvironment').modal('show');
	      },['All']);
            }
          },
        }
      });
      activeElement("mainTable");
      sortTableByRow(0);
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}


var mainContent = $("#objectViewer");
$(document).on('click', "td.countermeasure-row", function () {
  var cmName = $(this).text();
  refreshObjectBreadCrumb(cmName);
  viewCountermeasure(cmName);
});

function viewCountermeasure(cmName) {
  activeElement("objectViewer");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/countermeasures/name/" + encodeURIComponent(cmName),
    success: function (data) {
      fillOptionMenu("fastTemplates/editCountermeasureOptions.html", "#objectViewer", null, true, true, function () {
        $.session.set("Countermeasure", JSON.stringify(data));
        $("#UpdateCountermeasure").text("Update");
        var tags = data.theTags;
        var text = "";
        $.each(tags, function (index, type) {
          text += type + ", ";
        });
        $("#theTags").val(text);

        $('#editCountermeasureOptionsForm').loadJSON(data, null);
        $.each(data.theEnvironmentProperties, function (index, env) {
          appendCountermeasureEnvironment(env.theEnvironmentName)
        });
        $("#editCountermeasureOptionsForm").validator('update');
        $("#theEnvironments").find(".countermeasuresEnvironments:first").trigger('click');
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

$(document).on("click", "#addNewCountermeasure", function () {
  getNoOfRisks(function(noOfRisks) {
    if (noOfRisks == 0) {
      $('#noRisksModal').modal('show');
    }
    else {
      refreshObjectBreadCrumb('New Countermeasure');
      activeElement("objectViewer");
      fillOptionMenu("fastTemplates/editCountermeasureOptions.html", "#objectViewer", null, true, true, function () {
        $("#editCountermeasureOptionsForm").validator();
        $("#UpdateCountermeasure").text("Create");
        $("#editCountermeasureOptionsForm").addClass("new");
        $.session.set("Countermeasure", JSON.stringify(jQuery.extend(true, {},countermeasureDefault )));
        $("#Properties").hide();
      });
    }
  });
});

mainContent.on("change", "#theCountermeasureCost", function() {
  var cm = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");
  $.each(cm.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      cm.theEnvironmentProperties[index].theCost = $("#theCountermeasureCost").val();
      $.session.set("Countermeasure", JSON.stringify(cm));
    }
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
      $("#theCountermeasureCost").val(env.theCost);
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

mainContent.on('shown.bs.modal','#ChooseTargetDialog',function(e) {
  e.preventDefault();
  var envName = $.session.get("countermeasureEnvironmentName");
  var reqParams = '';
  var cm = JSON.parse($.session.get("Countermeasure"));
  $.each(cm.theEnvironmentProperties, function(index,env) {
    if (env.theEnvironmentName = envName) {
      reqParams = encodeQueryList('requirement',env.theRequirements);

      $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
          session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + "/api/countermeasures/targets/environment/" + encodeURIComponent(envName) + '?' + reqParams,
        success: function (data) {
          $('#chooseCountermeasureTargetSelect').empty();
          data.sort();
          var filterList = $('#ChooseTargetDialog').attr('data-filterList');
          data = data.filter(x => filterList.indexOf(x) < 0);
          if (data.length == 0) {
            alert('No targets available to add.');
          }
          else {
            $.each(data, function () {
              $('#chooseCountermeasureTargetSelect').append($("<option />").val(this).text(this));
            });
            var unparsedTarget = $('#ChooseTargetDialog').attr('data-currentTarget');
            if (unparsedTarget != undefined) {
              var target = JSON.parse(unparsedTarget);
              $('#chooseCountermeasureTargetSelect').val(target.theName);
              $('#chooseTargetEffectivenessSelect').val(target.theEffectiveness);
              $('#enterRationale').val(target.theRationale);
            }
            else {
              $('#chooseCountermeasureTargetSelect').val('');
              $('#chooseTargetEffectivenessSelect').val('None');
              $('#enterRationale').val('');
            }
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
  });
});

mainContent.on('click', '.countermeasureTargets', function () {
  var targetRow = $(this).closest("tr");
  var target = {};
  target.theName = targetRow.find("td:eq(1)").text();
  target.theEffectiveness = targetRow.find("td:eq(2)").text();
  target.theRationale = targetRow.find("td:eq(3)").text();
  var countermeasure = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");
  $.each(countermeasure.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      var targetIdx = 0;
      for (var i = 0; i < env.theTargets.length; i++) {
        if (target.theName == env.theTargets[i].theName) {
          targetIdx = i;
          break;
        }
      }
      var filterList = [];
      var targetIdx = i;
      $("#theTargets").find(".countermeasureTargets").each(function(index, req){
        if ($(req).text() != target.theName) {
          filterList.push($(req).text());
        }
      });

      $('#ChooseTargetDialog').attr('data-filterList',filterList);
      $('#ChooseTargetDialog').attr('data-selectedIndex',targetIdx);
      $('#ChooseTargetDialog').attr('data-currentTarget',JSON.stringify(target));

      $('#ChooseTargetDialog').modal('show');
    }
  });
});

mainContent.on('click', '#chooseTargetButton', function () {

  var target = {};
  target.theName = $('#chooseCountermeasureTargetSelect').find("option:selected" ).text();
  target.theEffectiveness = $('#chooseTargetEffectivenessSelect').val();
  target.theRationale = $('#enterRationale').val();

  var cm = JSON.parse($.session.get("Countermeasure"));
  var envName = $.session.get("countermeasureEnvironmentName");
  $.each(cm.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      var selectedIdx = $('#ChooseTargetDialog').attr('data-selectedIndex');
      if (selectedIdx != undefined) {
        env.theTargets[selectedIdx] = target;
        $.session.set("Countermeasure", JSON.stringify(cm));
        $('#theTargets').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(1)").text(target.theName);
        $('#theTargets').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(2)").text(target.theEffectiveness);
        $('#theTargets').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(2)").text(target.theRationale);
        $('#ChooseTargetDialog').modal('hide');
      }
      else {
        env.theTargets.push(target);
        $.session.set("Countermeasure", JSON.stringify(cm));
        appendCountermeasureTarget(target);
        $('#ChooseTargetDialog').modal('hide');
      }
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
  $('#EditCountermeasureTaskDialog').attr('data-selectedIndex',taskRow.index());

  var taskName = taskRow.find("td:eq(0)").text();
  var personaName = taskRow.find("td:eq(1)").text();
  var cm = JSON.parse($.session.get("Countermeasure"));
  var envName = $.session.get("countermeasureEnvironmentName");

  $.each(cm.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      var taskIdx = 0;
      $.each(env.thePersonas, function (idx, currentTp) {
        if ((currentTp.theTask == taskName) && (currentTp.thePersona = personaName)) {
          $('#EditCountermeasureTaskDialog').attr('data-currentTp',JSON.stringify(currentTp));
          $('#EditCountermeasureTaskDialog').modal('show');
        }
      });
    }
  });
});

mainContent.on('shown.bs.modal','#EditCountermeasureTaskDialog',function() {
  var currentTp = JSON.parse($('#EditCountermeasureTaskDialog').attr('data-currentTp'));
  $("#theTask").val(currentTp.theTask);
  $("#thePersona").val(currentTp.thePersona);
  $("#theDuration").val(currentTp.theDuration);
  $("#theFrequency").val(currentTp.theFrequency);
  $("#theDemands").val(currentTp.theDemands);
  $("#theGoalConflict").val(currentTp.theGoalConflict);
});

mainContent.on('click','#EditImpactedTaskButton',function() {
  var updTp = {};
  updTp.theTask =  $("#theTask").val();
  updTp.thePersona =  $("#thePersona").val();
  updTp.theDuration =  $("#theDuration").val();
  updTp.theFrequency =  $("#theFrequency").val();
  updTp.theDemands =  $("#theDemands").val();
  updTp.theGoalConflict =  $("#theGoalConflict").val();


  var cm = JSON.parse($.session.get("Countermeasure"));
  var envName = $.session.get("countermeasureEnvironmentName");
  $.each(cm.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      var selectedIdx = JSON.parse($('#EditCountermeasureTaskDialog').attr('data-selectedIndex'));
      env.thePersonas[selectedIdx] = updTp;
      $.session.set("Countermeasure", JSON.stringify(cm));
      $('#thePersonas').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(2)").text(updTp.theDuration);
      $('#thePersonas').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(3)").text(updTp.theFrequency);
      $('#thePersonas').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(4)").text(updTp.theDemands);
      $('#thePersonas').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(5)").text(updTp.theGoalConflict);
      $('#EditCountermeasureTaskDialog').modal('hide');
    }
  });
});


function updateCountermeasurePropertyList() {
  resetSecurityPropertyList();

  var currentProperty = $("#chooseSecurityProperty").attr('data-currentproperty');
  if (currentProperty != '') {
    currentProperty = JSON.parse(currentProperty);
  }

  $("#countermeasureProperties").find(".countermeasureProperties").each(function(index, prop){
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

function addCountermeasureSecurityProperty(e) {
  e.preventDefault()
  var prop = {};
  prop.name =  $("#theSecurityPropertyName").find("option:selected").text();
  prop.value =  $("#theSecurityPropertyValue").val();
  prop.rationale =  $("#theSecurityPropertyRationale").val()

  var cm = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");
  $.each(cm.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theProperties, function(idx, secProp){
        if (prop.name == secProp.name) {
          secProp.value = prop.value;
          secProp.rationale = prop.rationale;
          cm.theEnvironmentProperties[index].theProperties[idx] = secProp;
          $.session.set("Countermeasure", JSON.stringify(cm));
          appendCountermeasureProperty(prop);
        }
      });
    }
  });
  $("#chooseSecurityProperty").modal('hide');
}

function updateCountermeasureSecurityProperty() {
  var currentProperty = JSON.parse($("#chooseSecurityProperty").attr("data-currentproperty"));
  var propRow = undefined;

  $("#countermeasureProperties").find("tr").each(function(index, row){
    if (currentProperty.name == $(row).find("td:eq(1)").text()) {
      propRow = $(row);
    }
  });

  var updProp = {};
  updProp.name =  $("#theSecurityPropertyName").find("option:selected").text();
  updProp.value =  $("#theSecurityPropertyValue").val();
  updProp.rationale =  $("#theSecurityPropertyRationale").val();

  var cm = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");

  $.each(cm.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theProperties, function(idx, secProp){
        if (updProp.name == secProp.name) {
          cm.theEnvironmentProperties[index].theProperties[idx] = updProp;
          $.session.set("Countermeasure", JSON.stringify(cm));
          propRow.find("td:eq(1)").text(updProp.name);
          propRow.find("td:eq(2)").text(updProp.value);
          propRow.find("td:eq(3)").text(updProp.rationale);
        }
      });
    }
  });
  $("#chooseSecurityProperty").modal('hide');
}


mainContent.on('click','#addPropertytoCountermeasure', function () {

  $("#chooseSecurityProperty").attr('data-updatepropertylist',"updateCountermeasurePropertyList");
  $("#chooseSecurityProperty").attr("data-buildproperty","addCountermeasureSecurityProperty");
  $("#chooseSecurityProperty").modal('show');
});

mainContent.on('click', '.countermeasureProperties', function() {
  var propRow = $(this).closest("tr");
  var selectedProp = {};
  selectedProp.name = propRow.find("td:eq(1)").text();
  selectedProp.value = propRow.find("td:eq(2)").text();
  selectedProp.rationale = propRow.find("td:eq(3)").text();

  $("#chooseSecurityProperty").attr('data-updatepropertylist',"updateCountermeasurePropertyList");
  $("#chooseSecurityProperty").attr("data-buildproperty","updateCountermeasureSecurityProperty");
  $("#chooseSecurityProperty").attr("data-currentproperty",JSON.stringify(selectedProp));
  $("#chooseSecurityProperty").modal('show');
});

mainContent.on("click", "#addCountermeasureEnv", function () {
  var filterList = [];
  $(".countermeasuresEnvironments").each(function (index, tag) {
    filterList.push($(tag).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'environment',$.session.get('countermeasureEnvironmentName'),function(){
    $('#chooseEnvironment').attr('data-chooseDimension','environment');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addCountermeasureEnvironment');
    $('#chooseEnvironment').modal('show');
  },filterList);

});

function addCountermeasureEnvironment() {
  var text = $("#chooseEnvironmentSelect").val();
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
      $('#chooseEnvironment').modal('hide');
    }
  });
};

function commitCountermeasure() {
  var cm = JSON.parse($.session.get("Countermeasure"));
  if (cm.theEnvironmentProperties.length == 0) {
    alert("Environments not defined");
  }
  else {
    var oldName = cm.theName;
    cm.theName = $("#theName").val();
    var tags = $("#theTags").text().split(", ");
    if(tags[0] != ""){
      cm.theTags = tags;
    }
    cm.theType = $("#theType option:selected").text();

    if($("#editCountermeasureOptionsForm").hasClass("new")){
      postCountermeasure(cm, function () {
        $("#editCountermeasureOptionsForm").removeClass("new");
        $('#menuBCClick').attr('dimension','countermeasure');
        refreshMenuBreadCrumb('countermeasure');
      });
    } 
    else {
      putCountermeasure(cm, oldName, function () {
        $('#menuBCClick').attr('dimension','countermeasure');
        refreshMenuBreadCrumb('countermeasure');
      });
    }
  }
}

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
      $.each(env.theProperties, function(idx,prop) {
        if (prop.name == propName) {
          countermeasure.theEnvironmentProperties[index].theProperties[idx].value = 'None';
          countermeasure.theEnvironmentProperties[index].theProperties[idx].rationale = 'None';
        }
      });
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
}
function appendCountermeasureEnvironment(environment){
  $("#theEnvironments").find("tbody").append('<tr><td class="deleteCountermeasureEnv"><i class="fa fa-minus"></i></td><td class="countermeasuresEnvironments">'+environment+'</td></tr>');
}

function appendCountermeasureRequirement(requirement){
  $("#theRequirements").find("tbody").append("<tr><td class='removeCountermeasureRequirement'><i class='fa fa-minus'></i></td><td class='countermeasureRequirements'>" + requirement + "</td></tr>").animate('slow');
}

function appendCountermeasureTarget(target){
  $("#theTargets").find("tbody").append("<tr><td class='removeCountermeasureTarget'><i class='fa fa-minus'></i></td><td class='countermeasureTargets'>" + target.theName + "</td><td>" + target.theEffectiveness + "</td><td>" + target.theRationale + "</td></tr>").animate('slow');
}

function appendCountermeasureRole(role){
  $("#theRoles").find("tbody").append("<tr><td class='removeCountermeasureRole'><i class='fa fa-minus'></i></td><td class='countermeasureRoles'>" + role + "</td></tr>").animate('slow');
}

function appendCountermeasurePersona(task,persona,duration,frequency,demands,goalConflict) {
  $("#thePersonas").find("tbody").append("<tr><td class='countermeasurePersona'>" + task + "</td><td>" + persona + "</td><td>" + duration + "</td><td>" + frequency + "</td><td>" + demands + "</td><td>" + goalConflict +  "</td></tr>").animate('slow');
}

function appendCountermeasureProperty(prop){
  $("#countermeasureProperties").find("tbody").append("<tr class='changeProperty'><td class='removeCountermeasureProperty'><i class='fa fa-minus'></i></td><td class='countermeasureProperties'>" + prop.name + "</td><td>"+ prop.value +"</td><td>"+ prop.rationale+"</td></tr>").animate('slow');
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
  $('#menuBCClick').attr('dimension','countermeasure');
  refreshMenuBreadCrumb('countermeasure');
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
      url: serverIP + "/api/countermeasures/name/" + encodeURIComponent(cmName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        showPopup(true);
        $('#menuBCClick').attr('dimension','countermeasure');
        refreshMenuBreadCrumb('countermeasure');
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
    url: serverIP + "/api/countermeasures/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
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
  var filterList = [];
  $("#theRequirements").find(".countermeasureRequirements").each(function(index, req){
    filterList.push($(req).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'requirement',undefined,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','requirement');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addRequirementToCountermeasure');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addRequirementToCountermeasure() {
  var text = $("#chooseEnvironmentSelect").val();
  var cm = JSON.parse($.session.get("Countermeasure"));
  var theEnvName = $.session.get("countermeasureEnvironmentName");
  $.each(cm.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theRequirements.push(text);
      $.session.set("Countermeasure", JSON.stringify(cm));
      appendCountermeasureRequirement(text);
      $('#chooseEnvironment').modal('show');
    }
  });
};

$(document).on("click", "#addTargetToCountermeasure", function (e) {
  e.preventDefault();
  var filterList = [];
  $("#theTargets").find(".countermeasureTargets").each(function(index, req){
    filterList.push($(req).text());
  });

  $('#ChooseTargetDialog').attr('data-filterList',filterList);
  $('#ChooseTargetDialog').attr('data-selectedIndex',undefined);
  $('#ChooseTargetDialog').attr('data-currentTarget',undefined);
  $('#ChooseTargetDialog').modal('show');
});

mainContent.on('click', '#addRoleToCountermeasure', function () {
  var filterList = [];
  $("#theRoles").find(".countermeasureRoles").each(function(index, role){
    filterList.push($(role).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'role',undefined,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','role');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addRoleToCountermeasure');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addRoleToCountermeasure(){
  var text = $("#chooseEnvironmentSelect").val();
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
};

function updateCountermeasureTasks(envName,roleList) {
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/countermeasures/tasks/environment/" + encodeURIComponent(envName) + "?" + encodeQueryList("role",roleList),
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
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function generateAsset(cmName) {
  var output = {};
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
    url: serverIP + "/api/countermeasures/name/" + encodeURIComponent(cmName) + "/generate_asset?session_id=" + $.session.get('sessionID'),
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



function generateAssetFromTemplate() {
  var cmName = $("#chooseEnvironment").attr('data-cmName');
  var taName = $('#chooseEnvironmentSelect').val();
  var output = {};
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
    url: serverIP + "/api/countermeasures/name/" + encodeURIComponent(cmName) + "/template_asset/" + encodeURIComponent(taName) + "/generate_asset",
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

function situateCountermeasurePattern() {
  var cmName = $("#chooseEnvironment").attr('data-cmName');
  var spName = $('#chooseEnvironmentSelect').val();
  var output = {};
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
    url: serverIP + "/api/countermeasures/name/" + encodeURIComponent(cmName) + "/security_pattern/" + encodeURIComponent(spName) + "/situate",
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


function associateWithSituatedPattern() {
  var cmName = $("#chooseEnvironment").attr('data-cmName');
  var spName = $('#chooseEnvironmentSelect').val();
  var output = {};
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
    url: serverIP + "/api/countermeasures/name/" + encodeURIComponent(cmName) + "/security_pattern/" + encodeURIComponent(spName) + "/associate_situated",
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


function removeCountermeasurePattern() {
  var cmName = $("#chooseEnvironment").attr('data-cmName');
  var spName = $('#chooseEnvironmentSelect').val();
  var output = {};
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);

  $.ajax({
    type: "DELETE",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/countermeasures/name/" + encodeURIComponent(cmName) + "/security_pattern/" + encodeURIComponent(spName) + "/remove_situated",
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


$('#countermeasureValuesClick').click(function(){
  $('#unsupportedModal').modal('show');
});

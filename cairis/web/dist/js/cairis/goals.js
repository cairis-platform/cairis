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

$("#goalMenuClick").click(function(){
  validateClick('goal',function() {
    clearLocalStorage($('#menuBCClick').attr('dimension'));
    $("#objectViewer").empty();
    $('#menuBCClick').attr('dimension','goal');
    refreshMenuBreadCrumb('goal');
  });
});

function createEditGoalsTable(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID')),
      coloured: '1'
    },
    crfossDomain: true,
    url: serverIP + "/api/goals/summary",
    success: function (data) {
      setTableHeader("EditGoals");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      for (var r = 0; r < data.length; r++) {
        var item = data[r];
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td class="deleteGoalButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';

        textToInsert[i++] = '<td class="goal-rows" name="theName">';
        textToInsert[i++] = item.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="goal-rows" name="theOriginator">';
        textToInsert[i++] = item.theOriginator;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="goal-rows" name="Status">';
        if(item.theStatus == 'black'){
          textToInsert[i++] = "Check";
        }
        else if(item.theStatus == 'red'){
          textToInsert[i++] = "To refine";
        }
        else {
          textToInsert[i++] = "OK";
        }

        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      }
      theTable.append(textToInsert.join(''));

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


$(document).on('click', "td.goal-rows", function(){
  var goalName = $(this).closest("tr").find("td:eq(1)").text();
  refreshObjectBreadCrumb(goalName);
  viewGoal(goalName);
});

var mainContent = $("#objectViewer");
mainContent.on('click', ".goalEnvProperties", function () {
  $(this).closest('tr').addClass('active').siblings().removeClass('active');
  var goal = JSON.parse($.session.get("Goal"));
  var name = $(this).text();
  $.session.set("GoalEnvName", name);
  clearGoalEnvironmentPanel();

  $.each(goal.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == name){
      $('#theCategory').val(env.theCategory);
      $('#thePriority').val(env.thePriority);
      $("#theIssue").val(env.theIssue);
      $("#theDefinition").val(env.theDefinition);
      $("#theFitCriterion").val(env.theFitCriterion);

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
          $.session.set("Goal", JSON.stringify(goal));
          return;
        }
      });
    }
  });
});

mainContent.on('click', '#AddGoalConcernAssociationButton', function () {

  var assoc = [];
  assoc[0] = $("#theSourceSelect").val();
  assoc[1] = $("#theNSelect").val();
  assoc[2] = $("#theLink").val();
  assoc[3] = $("#theTargetSelect").val();
  assoc[4] = $("#theN2Select").val();

  var goal = JSON.parse($.session.get("Goal"));
  var envName = $.session.get("GoalEnvName");
  $.each(goal.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      var selectedIdx = $('#goalConcernAssociationsDialog').attr('data-selectedIndex');
      if (selectedIdx != undefined) {
        env.theConcernAssociations[selectedIdx] = assoc;
        $.session.set("Goal", JSON.stringify(goal));
        $('#editgoalsConcernassociationsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(1)").text(assoc[0]);
        $('#editgoalsConcernassociationsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(2)").text(assoc[1]);
        $('#editgoalsConcernassociationsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(3)").text(assoc[2]);
        $('#editgoalsConcernassociationsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(4)").text(assoc[3]);
        $('#editgoalsConcernassociationsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(5)").text(assoc[4]);
      }
      else {
        env.theConcernAssociations.push(assoc);
        $.session.set("Goal", JSON.stringify(goal));
        appendGoalConcernAssoc(assoc);
      }
      $('#goalConcernAssociationsDialog').modal('hide');
    }
  });
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
          env.theSubGoalRefinements.splice(ix,1);
          $.session.set("Goal", JSON.stringify(goal));
          return;
        }
      });
    }
  });
});

mainContent.on('click',"#addConcerntoGoal", function () {
  var filterList = [];
  $("#editgoalsConcernTable").find('tbody').find('.GoalConcernName').each(function (index, td) {
     filterList.push($(td).text());
  });

  var envName = $.session.get("GoalEnvName");

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'asset',envName,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','concern');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addGoalConcern');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addGoalConcern() {
  var text = $("#chooseEnvironmentSelect").val();
  var goal = JSON.parse($.session.get("Goal"));
  var envName = $.session.get("GoalEnvName");

  $.each(goal.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      env.theConcerns.push(text);
      appendGoalConcern(text);
      $.session.set("Goal", JSON.stringify(goal));
    }
  });
};

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
            $.session.set("Goal", JSON.stringify(goal));
            return;
          }
        }
      });
    }
  });
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
            $.session.set("Goal", JSON.stringify(goal));
            return;
          }
        }
      });
    }
  });
});

mainContent.on('click', '#addConcernAssociationstoGoal', function () {
  $('#AddGoalConcernAssociationButton').text('Add');
  $('#goalConcernAssociationsDialog').attr('data-selectedIndex',undefined);
  refreshGoalConcernSelectors();
  $('#goalConcernAssociationsDialog').modal('show');
});

mainContent.on('click', '#addSubGoaltoGoal', function () {
  $("#editGoalSubGoal").attr('data-selectedIdx',undefined);
  $("#editGoalSubGoal").attr('data-currentGoal',undefined);
  $("#theSubgoalType").val("goal");
  $("#theSubGoalName").val("");
  $("#theRefinementSelect").val("and");
  $("#theAlternate").val("No");
  $("#theGoalSubGoalRationale").val("");
  $("#editGoalSubGoal").modal('show');
});

$(document).on('shown.bs.modal','#editGoalSubGoal',function() {
  var currentObject = $('#editGoalSubGoal').attr('data-currentGoal');
  if (currentObject != undefined) {
    currentObject = JSON.parse(currentObject);
    fillGoalEditSubGoal(currentObject.name,currentObject.type,currentObject.refinement,currentObject.target,currentObject.rationale);
  }
  else {
    fillGoalEditSubGoal();
  }
});

$(document).on('shown.bs.modal','#editGoalGoal',function() {
  var currentObject = $('#editGoalGoal').attr('data-currentGoal');
  if (currentObject != undefined) {
    currentObject= JSON.parse(currentObject);
    fillGoalEditGoal(currentObject.name,currentObject.type,currentObject.refinement,currentObject.target,currentObject.rationale);
  }
  else {
    fillGoalEditGoal();
  }
});



mainContent.on('click', '#addGoaltoGoal', function () {
  $("#editGoalGoal").attr('data-selectedIdx',undefined);
  $("#editGoalGoal").attr('data-currentGoal',undefined);
  $("#theGoalType").val("goal");
  $("#theGoalName").val("");
  $("#theGoalRefinementSelect").val("and");
  $("#theGoalAlternate").val("No");
  $("#theGoalGoalRationale").val("");
  $("#editGoalGoal").modal('show');
});

mainContent.on("click", "#addGoalEnvironment", function () {
  var filterList = [];
  $(".goalEnvProperties").each(function (index, tag) {
    filterList.push($(tag).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'environment',undefined,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','environment');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addGoalEnvironment');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addGoalEnvironment() {
  var text = $("#chooseEnvironmentSelect").val();
  appendGoalEnvironment(text);
  var environment =  jQuery.extend(true, {},goalEnvDefault );
  environment.theEnvironmentName = text;
  var goal = JSON.parse($.session.get("Goal"));
  goal.theEnvironmentProperties.push(environment);
  $("#goalProperties").show("fast");
  $.session.set("GoalEnvName", text);
  $.session.set("Goal", JSON.stringify(goal));
  $("#theGoalEnvironments").find("tbody").find(".goalEnvProperties:last").trigger('click');
};

mainContent.on('click', ".deleteGoalEnv", function () {
  var envi = $(this).next(".goalEnvProperties").text();
  $(this).closest("tr").remove();
  var goal = JSON.parse($.session.get("Goal"));
  $.each(goal.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envi){
      goal.theEnvironmentProperties.splice( index ,1 );
      $.session.set("Goal", JSON.stringify(goal));
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
  var selectedIdx = $("#editGoalSubGoal").attr('data-selectedIndex');
  if(selectedIdx == undefined) {
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
        $.session.set("Goal", JSON.stringify(goal));
        $("#editGoalSubGoal").modal('hide');
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
            $.session.set("Goal", JSON.stringify(goal));
            $('#editgoalsSubgoalsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(1)").text(arr[0]);
            $('#editgoalsSubgoalsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(2)").text(arr[1]);
            $('#editgoalsSubgoalsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(3)").text(arr[2]);
            $('#editgoalsSubgoalsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(4)").text(arr[3]);
            $('#editgoalsSubgoalsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(5)").text(arr[4]);
            $("#editGoalSubGoal").modal('hide');
          }
        });
      }
    });
  }
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
  refreshObjectBreadCrumb('New Goal');
  fillGoalOptionMenu(null, function () {
    $("#updateGoalButton").text("Create");
    clearGoalEnvironmentPanel();
    $("#editGoalOptionsForm").validator();
    $("#editGoalOptionsForm").addClass('new');
    $("#goalProperties").hide();
    $.session.set("Goal", JSON.stringify(jQuery.extend(true, {},goalDefault )));
  });
});


function commitGoal() {
    var goal = JSON.parse($.session.get("Goal"));
    if (goal.theEnvironmentProperties.length == 0) {
      alert("Environments not defined");
    }
    else {
      var oldName = goal.theName;
      goal.theName = $("#theName").val();
      goal.theOriginator = $("#theOriginator").val();
      goal.theTags = $('#theTags').val().split(',').map(function(t){return t.trim();});

      if($("#editGoalOptionsForm").hasClass("new")){
        postGoal(goal, function () {
          clearLocalStorage("goal");
          $("#editGoalOptionsForm").removeClass("new")
          $('#menuBCClick').attr('dimension','goal');
          refreshMenuBreadCrumb('goal');
        });
      } 
      else {
        putGoal(goal, oldName, function () {
          clearLocalStorage("goal");
          $('#menuBCClick').attr('dimension','goal');
          refreshMenuBreadCrumb('goal');
        });
      }
    }
}

mainContent.on('click', '.editGoalSubGoalRow', function () {
  var refRow = $(this).closest('tr');
  var currentGoal = {}
  currentGoal.name = refRow.find("td").eq(1).text();
  currentGoal.type = refRow.find("td").eq(2).text();
  currentGoal.refinement = refRow.find("td").eq(3).text();
  currentGoal.target = refRow.find("td").eq(4).text();
  currentGoal.rationale = refRow.find("td").eq(5).text();
  $.session.set("oldsubGoalName", currentGoal.name);
  $("#editGoalSubGoal").attr('data-currentGoal',JSON.stringify(currentGoal));
  $("#editGoalSubGoal").attr('data-selectedIndex',refRow.index());
  $("#theSubgoalType").val(currentGoal.type);
  $("#theRefinementSelect").val(currentGoal.refinement);
  $("#theAlternate").val(currentGoal.target);
  $("#theGoalSubGoalRationale").val(currentGoal.rationale);
  $("#editGoalSubGoal").modal('show');
});

mainContent.on('click', '.editGoalGoalRow', function () {
  var refRow = $(this).closest('tr');
  var currentGoal = {}
  currentGoal.name = refRow.find("td").eq(1).text();
  currentGoal.type = refRow.find("td").eq(2).text();
  currentGoal.refinement = refRow.find("td").eq(3).text();
  currentGoal.target = refRow.find("td").eq(4).text();
  currentGoal.rationale = refRow.find("td").eq(5).text();
  $.session.set("oldGoalName", currentGoal.name);
  $("#editGoalGoal").attr('data-currentGoal',JSON.stringify(currentGoal));
  $("#editGoalGoal").attr('data-selectedIndex',refRow.index());
  $("#theGoalType").val(currentGoal.type);
  $("#theGoalRefinementSelect").val(currentGoal.refinement);
  $("#theGoalAlternate").val(currentGoal.target);
  $("#theGoalGoalRationale").val(currentGoal.rationale);
  $("#editGoalGoal").modal('show');
});

function refreshGoalConcernSelectors(name,n1,link,n2,target) {
  $("#theSourceSelect").empty();
  $("#theTargetTarget").empty();
  var goal = JSON.parse($.session.get("Goal"));
  var envName = $.session.get("GoalEnvName");
  $.each(goal.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      $.each(env.theConcerns, function (idx2, conc) {
        $("#theSourceSelect").append($("<option></option>").attr('value',conc).text(conc));
        $("#theTargetSelect").append($("<option></option>").attr('value',conc).text(conc));
      });
    }
  });
  if (name != undefined) {
    $("#theSourceSelect").val(name);
    $("#theNSelect").val(n1);
    $("#theLink").val(link);
    $("#theTargetSelect").val(target);
    $("#theN2Select").val(n2);
  }
}

mainContent.on('click', '.editGoalConcernAssoc', function () {
  var caRow = $(this).closest("tr");
  $('#AddGoalConcernAssociationButton').text('Edit');
  $('#goalConcernAssociationsDialog').attr('data-selectedIndex',caRow.index());
  var name = $(caRow).find(".assocName").text();
  $.session.set("goalAssocName",name);
  var n1 = $(caRow).find(".assocN1").text();
  var link = $(caRow).find(".assocLink").text();
  var n2 = $(caRow).find(".assocN2").text();
  var target = $(caRow).find(".assocTarget").text();
  refreshGoalConcernSelectors(name,n1,link,n2,target);
  $('#goalConcernAssociationsDialog').modal('show');
});

mainContent.on('click', '#goalCancelButton', function (e) {
  clearLocalStorage("goal");
  $("#objectViewer").empty();
  e.preventDefault();
});

mainContent.on('click',"#updateGoalGoal", function () {

  var goal = JSON.parse($.session.get("Goal"));
  var envName = $.session.get("GoalEnvName");
  var selectedIdx = $("#editGoalGoal").attr('data-selectedIndex');
  if(selectedIdx == undefined) {
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
        $.session.set("Goal", JSON.stringify(goal));
        $("#editGoalGoal").modal('hide');
      }
    });
  }
  else {
    var oldName = $.session.get("oldGoalName");
    $.each(goal.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == envName){
        $.each(env.theGoalRefinements, function (index, arr) {
          if(arr[0] == oldName){
            arr[1] = $("#theGoalType").val();
            arr[0] = $("#theGoalName").val();
            arr[2] = $("#theGoalRefinementSelect").val();
            arr[3] = $("#theGoalAlternate").val();
            arr[4] = $("#theGoalGoalRationale").val();
            $.session.set("Goal", JSON.stringify(goal));
            $('#editgoalsGoalsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(1)").text(arr[0]);
            $('#editgoalsGoalsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(2)").text(arr[1]);
            $('#editgoalsGoalsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(3)").text(arr[2]);
            $('#editgoalsGoalsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(4)").text(arr[3]);
            $('#editgoalsGoalsTable').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(5)").text(arr[4]);
            $("#editGoalGoal").modal('hide');
          }
        });
      }
    });
  }
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
    url: serverIP + "/api/goals/name/" + encodeURIComponent(goalName),
    success: function (data) {
      fillGoalOptionMenu(data);
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function fillGoalOptionMenu(data,callback){
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editGoalsOptions.html","#objectViewer",null,true,true, function(){
    $("#updateGoalButton").text("Update");
    if(data != null) {
      $.session.set("Goal", JSON.stringify(data));
      $('#theTags').val(data.theTags.join(', '));
      data.theTags = [];
      $('#editGoalOptionsForm').loadJSON(data, null);

      $.each(data.theTags, function (index, tag) {
        $("#theTags").append(tag + ", ");
      });
      $.each(data.theEnvironmentProperties, function (index, prop) {
        appendGoalEnvironment(prop.theEnvironmentName);
      });
      $("#theGoalEnvironments").find(".goalEnvProperties:first").trigger('click');
      $("#editGoalOptionsForm").validator('update');
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

function fillGoalEditSubGoal(theSettableValue,theSettableType,refinement,target,rationale){
  if (theSettableType == undefined) {
    theSettableType = 'goal';
  }
  refreshDimensionSelector($('#theSubGoalName'),theSettableType,$.session.get("GoalEnvName"),function() {
    if (theSettableValue != undefined) {
      $('#theSubGoalName').val(theSettableValue);
      $("#theRefinementSelect").val(refinement);
      $("#theAlternate").val(target);
      $("#theGoalSubGoalRationale").val(rationale);
    } 
  },['All']);
}

function fillGoalEditGoal(theSettableValue,theSettableType,refinement,target,rationale) {
  if (theSettableType == undefined) {
    theSettableType = 'goal';
  }
  refreshDimensionSelector($('#theGoalName'),theSettableType,$.session.get("GoalEnvName"),function() {
    if (theSettableValue != undefined) {
      $("#theGoalName").val(theSettableValue);
      $("#theGoalRefinementSelect").val(refinement);
      $("#theGoalAlternate").val(target);
      $("#theGoalGoalRationale").val(rationale);
    }
  },['All']); 
}

function clearGoalEnvironmentPanel(){
  $("#editgoalsGoalsTable").find("tbody").empty();
  $("#editgoalsSubgoalsTable").find("tbody").empty();
  $("#editgoalsConcernTable").find("tbody").empty();
  $("#editgoalsConcernassociationsTable").find("tbody").empty();
}

function appendGoalEnvironment(text){
  $("#theGoalEnvironments").append("<tr><td class='deleteGoalEnv addRemove'><i class='fa fa-minus'></i></td><td class='goalEnvProperties'>"+ text +"</td></tr>");
}
function appendGoalGoal(goal){
  $("#editgoalsGoalsTable").append('<tr class="addRemove"><td class="deleteGoalGoal"><i class="fa fa-minus"></i></td><td class="envGoalName editGoalGoalRow">'+goal[0]+'</td><td class="editGoalGoalRow">'+goal[1]+'</td><td class="editGoalGoalRow">'+goal[2]+'</td><td class="editGoalGoalRow">'+goal[3]+'</td><td class="editGoalGoalRow">'+goal[4]+'</td></tr>');
}
function appendGoalSubGoal(subgoal){
  $("#editgoalsSubgoalsTable").append('<tr class="addRemove"><td class="deleteGoalSubGoal"><i class="fa fa-minus"></i></td><td class="subGoalName editGoalSubGoalRow">'+subgoal[0]+'</td><td class="editGoalSubGoalRow">'+subgoal[1]+'</td><td class="editGoalSubGoalRow">'+subgoal[2]+'</td><td class="editGoalSubGoalRow">'+subgoal[3]+'</td><td class="editGoalSubGoalRow">'+subgoal[4]+'</td></tr>');
}
function appendGoalConcern(concern){
  $("#editgoalsConcernTable").append('<tr><td class="deleteGoalEnvConcern addRemove" value="'+ concern+'"><i class="fa fa-minus"></i></td><td class="GoalConcernName">'+concern+'</td></tr>');
}
function appendGoalConcernAssoc(assoc){
  $("#editgoalsConcernassociationsTable").append('<tr><td class="deleteGoalEnvConcernAssoc addRemove"><i class="fa fa-minus"></i></td><td class="assocName editGoalConcernAssoc">'+assoc[0]+'</td><td class="assocN1">'+assoc[1]+'</td><td class="assocLink editGoalConcernAssoc">'+assoc[2]+'</td><td class="assocN2 editGoalConcernAssoc">'+assoc[4]+'</td><td class="assocTarget">'+assoc[3]+'</td></tr>');
}

mainContent.on('click', '#goalCancelButton', function (e) {
  e.preventDefault();
  $('#menuBCClick').attr('dimension','goal');
  refreshMenuBreadCrumb('goal');
});

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
      url: serverIP + "/api/goals/name/" + encodeURIComponent(goalName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        $('#menuBCClick').attr('dimension','goal');
        showPopup(true);
        refreshMenuBreadCrumb('goal');
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
    url: serverIP + "/api/goals/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
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

mainContent.on('click', '#theGoalType', function () {
  var dimName = $('#theGoalType').val();
  if (dimName == 'role' || dimName == 'requirement') {
    refreshDimensionSelector($('#theGoalName'),dimName,undefined,undefined,['All']);
  }
  else {
    refreshDimensionSelector($('#theGoalName'),dimName,$.session.get("GoalEnvName"),undefined,['All']);
  }
});

mainContent.on('click', '#theSubgoalType', function () {
  var dimName = $('#theSubgoalType').val();
  if (dimName == 'role' || dimName == 'requirement') {
    refreshDimensionSelector($('#theSubGoalName'),dimName,undefined,undefined,['All']);
  }
  else {
    refreshDimensionSelector($('#theSubGoalName'),dimName,$.session.get("GoalEnvName"),undefined,['All']);
    if (dimName == 'obstacle') {
      $('#theRefinementSelect').val('conflict');
    }
    else if (dimName == 'role') {
      $('#theRefinementSelect').val('responsible');
    }
  }
});

mainContent.on('keypress','#theName',filterReservedChars);

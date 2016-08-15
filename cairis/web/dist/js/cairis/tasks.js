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

$("#taskClick").click(function () {
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
      window.activeTable = "Tasks";
      setTableHeader();
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td><button class="editTaskButton" value="' + key + '">' + 'Edit' + '</button> <button class="deleteTaskButton" value="' + key + '">' + 'Delete' + '</button></td>';

        textToInsert[i++] = '<td name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theObjective">';
        textToInsert[i++] = item.theObjective;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      });

      theTable.append(textToInsert.join(''));
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

$(document).on('click', ".editTaskButton", function () {
  var name = $(this).val();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/tasks/name/" + name.replace(" ", "%20"),
    success: function (data) {
      fillOptionMenu("fastTemplates/editTaskOptions.html", "#optionsContent", null, true, true, function () {
        $("#optionsHeaderGear").text("Task properties");
        forceOpenOptions();
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
        $("#theEnvironments").find(".taskEnvironment:first").trigger('click');
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});


var optionsContent = $("#optionsContent");
optionsContent.on("click",".taskEnvironment", function () {
  clearTaskEnvInfo();
  var task = JSON.parse($.session.get("Task"));
  var theEnvName = $(this).text();
  $.session.set("taskEnvironmentName", theEnvName);
  $.each(task.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $('#theDependencies').val(env.theDependencies);
      $('#theNarrative').val(env.theNarrative);
      $('#theConsequences').val(env.theConsequences);
      $('#theBenefits').val(env.theBenefits);
          
      var listVals = [];
      $.each(env.theAssets, function(index,concern) {
        listVals.push("<tr><td>" + concern + "</td></tr>");
      });
      $("#theConcerns").find("tbody").append(listVals.join(' '));

      listVals = [];
      for (var i = 0; i < env.thePersonas.length; i++) {
        var pCol = [];
        $.each(env.thePersonas[i], function(idx,val) { pCol.push(val); });
        listVals.push("<tr><td>" + pCol[0][0] + "</td><td>" + pCol[0][1] + "</td><td>" + pCol[0][2] + "</td><td>" + pCol[0][3] + "</td><td>");
      }
      $("#thePersonas").find("tbody").append(listVals.join(' '));

      listVals = [];
      for (var i = 0; i < env.theConcernAssociations.length; i++) {
        var aCol = [];
        $.each(env.theConcernAssociations[i], function(idx,val) { aCol.push(val); });
        listVals.push("<tr><td>" + aCol[0][0] + "</td><td>" + aCol[0][1] + "</td><td>" + aCol[0][2] + "</td><td>" + aCol[0][3] + "</td><td>" + aCol[0][4] + "</td><td");
       }
      $("#theConcernAssociations").find("tbody").append(listVals.join(' '));
    }
  });
});

function appendTaskEnvironment(environment){
  $("#theEnvironments").find("tbody").append('<tr><td class="deleteTaskEnv"><i class="fa fa-minus"></i></td><td class="taskEnvironment">'+environment+'</td></tr>');
}

function clearTaskEnvInfo(){
  $("#theDependencies").val('');
  $("#theNarrative").val('');
  $("#theConsequences").val('');
  $("#theBenefits").val('');
  $("#theConcerns").find("tbody").empty();
  $("#thePersonas").find("tbody").empty();
  $("#theConcernAssociations").find("tbody").empty();
}




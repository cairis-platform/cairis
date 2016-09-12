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

$("#dependenciesClick").click(function(){
   createDependenciesTable()
});

// A function for filling the table with Dependencies
function createDependenciesTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/dependencies",
    success: function (data) {
      var dependencies = [];
      window.activeTable = "Dependency";
      setTableHeader();
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;
      var di = 0;

      $.each(data, function(count, item) {
        dependencies[di] = item;
        textToInsert[i++] = "<tr>";
        var itemKey = item.theEnvironmentName + '/' + item.theDepender + '/' + item.theDependee + '/' + item.theDependency;
        textToInsert[i++] = '<td><button class="editDependencyButton" value="' + itemKey + '">' + 'Edit' + '</button> <button class="deleteDependencyButton" value="' + item.theVulnerabilityName + '">' + 'Delete' + '</button></td>';
        textToInsert[i++] = '<td name="theEnvironmentName">';
        textToInsert[i++] = item.theEnvironmentName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theDepender">';
        textToInsert[i++] = item.theDepender;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theDependee">';
        textToInsert[i++] = item.theDependee;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theDependenyType">';
        textToInsert[i++] = item.theDependencyType;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theDependeny">';
        textToInsert[i++] = item.theDependency;
        textToInsert[i++] = '</td>';
        textToInsert[i++] = '</tr>';
        di += 1;
      });
      $.session.set("Dependencies",JSON.stringify(dependencies));
      theTable.append(textToInsert.join(''));

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

$(document).on('click', ".editDependencyButton", function (e) {
  e.preventDefault();
  var dependencies = JSON.parse($.session.get("Dependencies"));
  var dependency = dependencies[$(this).index()];

  fillOptionMenu("fastTemplates/editDependencyOptions.html","#optionsContent",null,true,true, function(){
    $('#theRationale').val(dependency.theRationale);
    var environmentSelect = $("#theEnvironmentName");
    environmentSelect.empty()
    getEnvironments(function (envs) {
      $.each(envs, function (key,objt) {
        environmentSelect.append($('<option>', { value : objt }).text(objt));
      }); 
    });
    environmentSelect.val(dependency.theEnvironmentName);
    var dependerSelect = $("#theDependerName");
    var dependeeSelect = $("#theDependeeName");
    dependerSelect.empty()
    dependeeSelect.empty()
    getRolesInEnvironment(dependency.theEnvironmentName,function (roles) {
      $.each(roles, function (key,objt) {
        dependerSelect.append('<option>' + objt + '</option>');
        dependeeSelect.append('<option>' + objt + '</option>');
      }); 
    });
    $('#theDependerName').val(dependency.theDepender);
    $('#theDependeeName').val(dependency.theDependee);
    $("#theDependencyType").val(dependency.theDependencyType);
    $("#theDependencyName").empty();
    getDimensionsInEnvironment(dependency.theDependencyType,dependency.theEnvironmentName,function (dims) {
      $.each(dims, function (key,objt) {
        $("#theDependencyName").append('<option>' + objt + '</option>');
      }); 
    });
    $("#optionsHeaderGear").text("Dependency properties");
    forceOpenOptions();
    $.session.set("Dependency", JSON.stringify(dependency));
    $('#editDependencyOptionsForm').loadJSON(dependency, null);
  });
});

optionsContent.on('click', '#UpdateDependency', function (e) {

  $("#editDependencyOptionsForm").validator();

  var dependency = JSON.parse($.session.get("Dependency"));
  var oldEnvName = dependency.theEnvironmentName;
  var oldDepender = dependency.theDepender;
  var oldDependee = dependency.theDependee;
  var oldDependency = dependency.theDependency;
  dependency.theEnvironmentName = $("#theEnvironmentName").val();
  dependency.theDepender = $("#theDependerName").val();
  dependency.theDependee = $("#theDependeeName").val();
  dependency.theDependencyType = $("#theDependencyType").val();
  dependency.theDependency = $("#theDependencyName").val();
  dependency.theRationale = $("#theRationale").val();

  if($("#editDependencyOptionsForm").hasClass("new")){
    postDependency(dependency, function () {
      createDependenciesTable();
      $("#editDependencyOptionsForm").removeClass("new")
    });
  }  
  else {
    putDependency(dependency, oldEnvName, oldDepender, oldDependee,oldDependency,  function () {
      createDependenciesTable();
    });
  }
  e.preventDefault();
});

optionsContent.on('change',"#theEnvironmentName", function() {
  var envName = $(this).find('option:selected').text();

  var dependerSelect = $("#theDependerName");
  var dependeeSelect = $("#theDependeeName");
  dependerSelect.empty();
  dependeeSelect.empty();
  getRolesInEnvironment(envName,function (roles) {
    $.each(roles, function (key,objt) {
      dependerSelect.append('<option>' + objt + '</option>');
      dependeeSelect.append('<option>' + objt + '</option>');
    }); 
  });
});


optionsContent.on('change',"#theDependencyType", function() {
  var depType = $(this).find('option:selected').text();
  var envName = $("#theEnvironmentName").val();
  $("#theDependencyName").empty();
  getDimensionsInEnvironment(depType,envName,function (dims) {
    $.each(dims, function (key,objt) {
      $("#theDependencyName").append('<option>' + objt + '</option>');
    }); 
  });
});

$(document).on("click", "#addNewDependency", function () {
  fillOptionMenu("fastTemplates/editDependencyOptions.html", "#optionsContent", null, true, true, function () {
    $("#editDependencyOptionsForm").addClass("new");
    $.session.set("Dependency", JSON.stringify(jQuery.extend(true, {},dependencyDefault )));

    var environmentSelect = $("#theEnvironmentName");
    environmentSelect.empty()
    getEnvironments(function (envs) {
      $.each(envs, function (key,objt) {
        environmentSelect.append($('<option>', { value : objt }).text(objt));
      }); 
    });

    var dependerSelect = $("#theDependerName");
    var dependeeSelect = $("#theDependeeName");
    dependerSelect.empty();
    dependeeSelect.empty();
    getRoles(function (roles) {
      $.each(roles, function (key,objt) {
        dependerSelect.append('<option>' + objt + '</option>');
        dependeeSelect.append('<option>' + objt + '</option>');
      }); 
    });

    var depType = $("#theDependencyType").val();
    var envName = $("#theEnvironmentName").val();
    $("#theDependencyName").empty();
    getDimensionsInEnvironment(depType,envName,function (dims) {
      $.each(dims, function (key,objt) {
        $("#theDependencyName").append('<option>' + objt + '</option>');
      }); 
    });


    $("#optionsHeaderGear").text("Dependency properties");
    forceOpenOptions();
  });
});

$(document).on('click', '.deleteDependencyButton', function (e) {
  e.preventDefault();
  var dependencies = JSON.parse($.session.get("Dependencies"));
  var dependency = dependencies[$(this).index()];
  deleteDependency(dependency, function () {
    createDependenciesTable();
  });
});


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

$("#dependenciesClick").click(function(){
  validateClick('dependency',function() {
    $('#menuBCClick').attr('dimension','dependency');
    refreshMenuBreadCrumb('dependency');
  });

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
      setTableHeader("Dependency");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;
      var di = 0;

      $.each(data, function(count, item) {
        dependencies[di] = item;
        textToInsert[i++] = "<tr>";
        var itemKey = item.theEnvironmentName + '/' + item.theDepender + '/' + item.theDependee + '/' + item.theDependency;
        textToInsert[i++] = '<td class="deleteDependencyButton"><i class="fa fa-minus" value="' + itemKey + '"></i></td>';

        textToInsert[i++] = '<td class="dependency-rows" name="theEnvironmentName" value="' + itemKey + '">';
        textToInsert[i++] = item.theEnvironmentName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="dependency-rows" name="theDepender" value="' + itemKey + '">';
        textToInsert[i++] = item.theDepender;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="dependency-rows" name="theDependee" value="' + itemKey + '">';
        textToInsert[i++] = item.theDependee;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="dependency-rows" name="theDependenyType" value="' + itemKey + '">';
        textToInsert[i++] = item.theDependencyType;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="dependency-rows" name="theDependeny" value="' + itemKey + '">';
        textToInsert[i++] = item.theDependency;
        textToInsert[i++] = '</td>';
        textToInsert[i++] = '</tr>';
        di += 1;
      });
      $.session.set("Dependencies",JSON.stringify(dependencies));
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
  });
}

$(document).on('click', "td.dependency-rows", function(){
  activeElement("objectViewer");
  var dependencies = JSON.parse($.session.get("Dependencies"));
  var dependency = dependencies[$(this).closest('tr').index()];

  fillOptionMenu("fastTemplates/editDependencyOptions.html","#objectViewer",null,true,true, function(){
    $('#editDependencyOptionsForm').validator();
    $('#UpdateDependency').text("Update");
    refreshDimensionSelector($('#theEnvironmentName'),'environment',undefined,function() {
      $('#theEnvironmentName').val(dependency.theEnvironmentName);
      refreshDimensionSelector($('#theDependerName'),'role',dependency.theEnvironmentName,function() {
        $('#theDependerName').val(dependency.theDepender);
        refreshDimensionSelector($('#theDependeeName'),'role',dependency.theEnvironmentName,function() {
          $('#theDependeeName').val(dependency.theDependee);
          $('#theDependencyType').val(dependency.theDependencyType);
          refreshDimensionSelector($('#theDependencyName'),dependency.theDependencyType,undefined,function() {
            $('#theRationale').val(dependency.theRationale);
            $.session.set("Dependency", JSON.stringify(dependency));
            $('#editDependencyOptionsForm').loadJSON(dependency, null);
            $('#editDependencyOptionsForm').validator('update');
          },['All']);
        },['All']);
      },['All']);
    },['All']);
  });
});

function commitDependency() {
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
      $("#editDependencyOptionsForm").removeClass("new")
      $('#menuBCClick').attr('dimension','dependency');
      refreshMenuBreadCrumb('dependency');
    });
  }
  else {
    putDependency(dependency, oldEnvName, oldDepender, oldDependee,oldDependency,  function () {
      $('#menuBCClick').attr('dimension','dependency');
      refreshMenuBreadCrumb('dependency');
    });
  }
}

var mainContent = $("#objectViewer");
mainContent.on('change',"#theEnvironmentName", function() {
  var envName = $(this).find('option:selected').text();
  var currentDepender = $('#theDependerName').val();
  var currentDependee = $('#theDependeeName').val();
  var currentDependency = $('#theDependencyName').val();

  refreshDimensionSelector($('#theDependerName'),'role',envName,function() {
    $('#theDependerName').val(currentDepender);
    refreshDimensionSelector($('#theDependeeName'),'role',envName,function() {
      $('#theDependeeName').val(currentDependee);
      refreshDimensionSelector($('#theDependencyName'),$('#theDependencyType').val(),envName,undefined,['All']);
    });
  });
});


mainContent.on('change',"#theDependencyType", function() {
  var depType = $(this).find('option:selected').text();
  var envName = $("#theEnvironmentName").val();
  refreshDimensionSelector($('#theDependencyName'),depType,envName,undefined,['All']);
});

$(document).on("click", "#addNewDependency", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editDependencyOptions.html", "#objectViewer", null, true, true, function () {
    $('#editDependencyOptionsForm').validator();
    $('#UpdateDependency').text("Create");
    $("#editDependencyOptionsForm").addClass("new");

    refreshDimensionSelector($('#theEnvironmentName'),'environment',undefined,function() {
      refreshDimensionSelector($('#theDependerName'),'role',$('#theEnvironmentName').val(),function() {
        refreshDimensionSelector($('#theDependeeName'),'role',$('#theEnvironmentName').val(),function() {
          refreshDimensionSelector($('#theDependencyName'),$('#theDependencyType').val(),undefined,function() {
            $('#theRationale').val('');
            $.session.set("Dependency", JSON.stringify(jQuery.extend(true, {},dependencyDefault )));
          },['All']);
        });
      });
    });
  });
});

$(document).on('click', 'td.deleteDependencyButton', function (e) {
  e.preventDefault();
  var dependencies = JSON.parse($.session.get("Dependencies"));

  var depRow = $(this).closest('tr');
  var rowIdx = depRow.index();
  var dependency = dependencies[rowIdx];
  deleteDependency(dependency, function () {
    $('#menuBCClick').attr('dimension','dependency');
    refreshMenuBreadCrumb('dependency');
  });
});

mainContent.on('click', '#CloseDependency', function (e) {
  e.preventDefault();
  $('#menuBCClick').attr('dimension','dependency');
  refreshMenuBreadCrumb('dependency');
});

function deleteDependency(dependency, callback){
  $.ajax({
    type: "DELETE",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    url: serverIP +  "/api/dependencies/environment/" + encodeURIComponent(dependency.theEnvironmentName) + "/depender/" + encodeURIComponent(dependency.theDepender) + "/dependee/" + dependency.theDependee + "/dependency/" + encodeURIComponent(dependency.theDependency) + "?session_id=" + $.session.get('sessionID'),
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

function putDependency(dependency, oldEnvName, oldDepender, oldDependee, oldDependency, callback){
  var output = {};
  output.object = dependency;
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
    url: serverIP +  "/api/dependencies/environment/" + encodeURIComponent(oldEnvName) + "/depender/" + encodeURIComponent(oldDepender) + "/dependee/" + oldDependee + "/dependency/" + encodeURIComponent(oldDependency) + "?session_id=" + $.session.get('sessionID'),
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

function postDependency(dependency, callback){
  var output = {};
  output.object = dependency;
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
    url: serverIP +  "/api/dependencies/environment/" + encodeURIComponent(dependency.theEnvironmentName) + "/depender/" + encodeURIComponent(dependency.theDepender) + "/dependee/" + dependency.theDependee + "/dependency/" + encodeURIComponent(dependency.theDependency) + "?session_id=" + $.session.get('sessionID'),
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

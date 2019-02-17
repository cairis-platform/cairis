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

$("#dataflowsMenuClick").click(function(){
  validateClick('dataflow',function() {
    clearLocalStorage($('#menuBCClick').attr('dimension'));
    $("#objectViewer").empty();
    $('#menuBCClick').attr('dimension','dataflow');
    refreshMenuBreadCrumb('dataflow');
  });
});

function createDataflowsTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/dataflows",
    success: function (data) {
      var dataflows = [];
      setTableHeader("Dataflows");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;
      var di = 0;

      for (var r = 0; r < data.length; r++) {
        var item = data[r];
        dataflows[di] = item;
        textToInsert[i++] = "<tr>";
        var itemKey = item.theName + '/' + item.theEnvironmentName;
        textToInsert[i++] = '<td class="deleteDataflowButton"><i class="fa fa-minus" value="' + itemKey + '"></i></td>';

        textToInsert[i++] = '<td class="dataflow-rows" name="theEnvironmentName" value="' + item.theEnvironmentName + '">';
        textToInsert[i++] = item.theEnvironmentName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="dataflow-rows" name="theName" value="' + item.theName + '">';
        textToInsert[i++] = item.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="dataflow-rows" name="theFromName" value="' + item.theFromName + '">';
        textToInsert[i++] = item.theFromName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="dataflow-rows" name="theFromType" value="' + item.theFromType + '">';
        textToInsert[i++] = item.theFromType;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="dataflow-rows" name="theToName" value="' + item.theToName + '">';
        textToInsert[i++] = item.theToName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="dataflow-rows" name="theToType" value="' + item.theToType + '">';
        textToInsert[i++] = item.theToType;
        textToInsert[i++] = '</td>';
        textToInsert[i++] = '</tr>';
        di += 1;
      }
      $.session.set("Dataflows",JSON.stringify(dataflows));
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

$(document).on('click', "td.dataflow-rows", function(){
  activeElement("objectViewer");
  var dataflows = JSON.parse($.session.get("Dataflows"));
  var dataflow = dataflows[$(this).closest('tr').index()];
  $.session.set("Dataflow", JSON.stringify(dataflow));

  fillOptionMenu("fastTemplates/editDataflowOptions.html","#objectViewer",null,true,true, function(){
    $('#UpdateDataflow').text("Update");
    refreshDimensionSelector($('#theDataflowEnvironmentName'),'environment',undefined,function() {
      $('#theDataflowEnvironmentName').val(dataflow.theEnvironmentName);
      $('#theDataflowFromType').val(dataflow.theFromType);
      $('#theDataflowToType').val(dataflow.theToType);
      $('#theDataflowName').val(dataflow.theName);
      refreshDimensionSelector($('#theDataflowFromName'),dataflow.theFromType,dataflow.theEnvironmentName,function() {
        $('#theDataflowFromName').val(dataflow.theFromName);
        refreshDimensionSelector($('#theDataflowToName'),dataflow.theToType,dataflow.theEnvironmentName,function() {
          $('#theDataflowToName').val(dataflow.theToName);
          $.each(dataflow.theAssets,function(idx,dfAsset) {
            appendDataflowAsset(dfAsset);
          });
          $('#editDataflowOptionsForm').validator('update');
        },['All']);
      },['All']);
    });
  });
});


function appendDataflowAsset(dfAsset) {
  $("#theDataflowAssets").find("tbody").append("<tr><td class='removeDataflowAsset'><i class='fa fa-minus'></i></td><td class='dataflow-asset'>" + dfAsset + "</td></tr>").animate('slow');
}

function commitDataFlow() {
  var dataflow = JSON.parse($.session.get("Dataflow"));
  var oldDfName = dataflow.theName;
  var oldEnvName = dataflow.theEnvironmentName;
  dataflow.theName = $("#theDataflowName").val();
  dataflow.theEnvironmentName = $("#theDataflowEnvironmentName").val();
  dataflow.theFromType = $("#theDataflowFromType").val();
  dataflow.theFromName = $("#theDataflowFromName").val();
  dataflow.theToType = $("#theDataflowToType").val();
  dataflow.theToName = $("#theDataflowToName").val();

  if($("#editDataflowOptionsForm").hasClass("new")){
    postDataflow(dataflow, function () {
      clearLocalStorage('dataflow');
      $("#editDataflowOptionsForm").removeClass("new")
      $('#menuBCClick').attr('dimension','dataflow');
      refreshMenuBreadCrumb('dataflow');
    });
  }
  else {
    putDataflow(dataflow, oldDfName, oldEnvName,  function () {
      clearLocalStorage('dataflow');
      $('#menuBCClick').attr('dimension','dataflow');
      refreshMenuBreadCrumb('dataflow');
    });
  }
}

var mainContent = $("#objectViewer");
mainContent.on('change',"#theDataflowEnvironmentName", function() {
  var envName = $(this).find('option:selected').text();
  var currentFromName = $('#theDataflowFromName').val();
  var currentToName = $('#theDataflowToName').val();

  refreshDimensionSelector($('#theDataflowFromName'),$('#theDataflowFromType').val(),envName,function() {
    $('#theDataflowFromName').val(currentFromName);
    refreshDimensionSelector($('#theDataflowToName'),$('#theDataflowToType').val(),envName,function() {
      $('#theDataflowToName').val(currentToName);
    },['All']);
  },['All']);
});

mainContent.on('change',"#theDataflowFromType", function() {
  var envName = $('#theDataflowEnvironmentName').val()
  var currentFromName = $('#theDataflowFromName').val();

  refreshDimensionSelector($('#theDataflowFromName'),$('#theDataflowFromType').val(),envName,function() {
    $('#theDataflowFromName').val(currentFromName);
  },['All']);
});

mainContent.on('change',"#theDataflowToType", function() {
  var envName = $('#theDataflowEnvironmentName').val()
  var currentToName = $('#theDataflowToName').val();

  refreshDimensionSelector($('#theDataflowToName'),$('#theDataflowToType').val(),envName,function() {
    $('#theDataflowToName').val(currentToName);
  },['All']);
});


$(document).on("click", "#addNewDataflow", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editDataflowOptions.html", "#objectViewer", null, true, true, function () {
    $('#editDataflowOptionsForm').validator();
    $('#UpdateDataflow').text("Create");
    $("#editDataflowOptionsForm").addClass("new");

    refreshDimensionSelector($('#theDataflowEnvironmentName'),'environment',undefined,function() {
      $('#theDataflowFromType').val('entity');
      refreshDimensionSelector($('#theDataflowFromName'),'entity',$('#theDataflowEnvironmentName').val(),function() {
        $('#theDataflowToType').val('process');
        refreshDimensionSelector($('#theDataflowToName'),'process',$('#theDataflowEnvironmentName').val(),function() {
          $('#theDataflowName').val('');
          $.session.set("Dataflow", JSON.stringify(jQuery.extend(true, {},dataflowDefault )));
          $('#editDataflowOptionsForm').loadJSON(dataflowDefault, null);
        },['All']);
      },['All']);
    },['All']);
  });
});

$(document).on('click', 'td.deleteDataflowButton', function (e) {
  e.preventDefault();
  var dataflows = JSON.parse($.session.get("Dataflows"));
  var dfRow = $(this).closest('tr');
  var dataflow = dataflows[dfRow.index()];
  deleteDataflow(dataflow, function () {
    $('#menuBCClick').attr('dimension','dataflow');
    refreshMenuBreadCrumb('dataflow');
  });
});

mainContent.on('click', '#CloseDataflow', function (e) {
  e.preventDefault();
  clearLocalStorage('dataflow');
  $("#objectViewer").empty();
  $('#menuBCClick').attr('dimension','dataflow');
  refreshMenuBreadCrumb('dataflow');
});

function deleteDataflow(dataflow, callback){
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
    url: serverIP +  "/api/dataflows/name/" + encodeURIComponent(dataflow.theName) + "/environment/" + encodeURIComponent(dataflow.theEnvironmentName),
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

function putDataflow(dataflow, oldDfName, oldEnvName, callback){
  var output = {};
  output.object = dataflow;
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
    url: serverIP +  "/api/dataflows/name/" + encodeURIComponent(oldDfName) + "/environment/" + encodeURIComponent(oldEnvName),
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

function postDataflow(dataflow, callback){
  var output = {};
  output.object = dataflow;
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
    url: serverIP +  "/api/dataflows",
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

mainContent.on('click', '#addAssetToDataflow', function () {
  var filterList = [];
  $("#theDataflowAssets").find(".dataflow-asset").each(function(index, asset){
    filterList.push($(asset).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'asset', $('#theDataflowEnvironmentName').val(), function(){
    $('#chooseEnvironment').attr('data-chooseDimension','asset');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addDataflowAsset');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addDataflowAsset() {
  var text = $("#chooseEnvironmentSelect").val();
  var dataflow = JSON.parse($.session.get("Dataflow"));
  dataflow.theAssets.push(text);
  $.session.set("Dataflow", JSON.stringify(dataflow));
  appendDataflowAsset(text);
};

mainContent.on('click', ".removeDataflowAsset", function () {
  var text = $(this).next(".dataflow-asset").text();
  $(this).closest("tr").remove();
  var dataflow = JSON.parse($.session.get("Dataflow"));
  $.each(dataflow.theAssets, function (index2, asset) {
    if(asset == text){
      dataflow.theAssets.splice( index2 ,1 );
      $.session.set("Dataflow", JSON.stringify(dataflow));
      return false;
    }
  });
});



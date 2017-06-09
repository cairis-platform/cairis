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


$("#assetAssociationMenuClick").click(function(){
  $('#menuBCClick').attr('dimension','assetassociation');
  refreshMenuBreadCrumb('assetassociation');
});

function createAssetAssociationsTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/assets/association",
    success: function (data) {
      var assocs = [];
      setTableHeader("AssetAssociation");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;
      var di = 0;

      $.each(data, function(count, item) {
        assocs[di] = item;
        textToInsert[i++] = "<tr>";
        var itemKey = item.theEnvironmentName + '/' + item.theHeadAsset + '/' + item.theTailAsset;
        textToInsert[i++] = '<td class="deleteAssetAssociationButton"><i class="fa fa-minus" value="' + itemKey + '"></i></td>';

        textToInsert[i++] = '<td class="assetassociation-rows" name="theEnvironmentName" value="' + itemKey + '">';
        textToInsert[i++] = item.theEnvironmentName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="assetassociation-rows" name="theHeadAsset" value="' + itemKey + '">';
        textToInsert[i++] = item.theHeadAsset;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="assetassociation-rows" name="theHeadNavigation" value="' + itemKey + '">';
        textToInsert[i++] = item.theHeadNavigation;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="assetassociation-rows" name="theHeadType" value="' + itemKey + '">';
        textToInsert[i++] = item.theHeadType;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="assetassociation-rows" name="theHeadMultiplicity" value="' + itemKey + '">';
        textToInsert[i++] = item.theHeadMultiplcity;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="assetassociation-rows" name="theHeadRole" value="' + itemKey + '">';
        textToInsert[i++] = item.theHeadRole;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="assetassociation-rows" name="theTailRole" value="' + itemKey + '">';
        textToInsert[i++] = item.theTailRole;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="assetassociation-rows" name="theTailMultiplicity" value="' + itemKey + '">';
        textToInsert[i++] = item.theTailMultiplicity;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="assetassociation-rows" name="theTailType" value="' + itemKey + '">';
        textToInsert[i++] = item.theTailType;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="assetassociation-rows" name="theTailNavigation" value="' + itemKey + '">';
        textToInsert[i++] = item.theTailNavigation;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="assetassociation-rows" name="theTailAsset" value="' + itemKey + '">';
        textToInsert[i++] = item.theTailAsset;
        textToInsert[i++] = '</td>';
        textToInsert[i++] = '</tr>';
        di += 1;
      });
      $.session.set("AssetAssociations",JSON.stringify(assocs));
      theTable.append(textToInsert.join(''));

      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
      $("#mainTable").find("tbody").removeClass();

      activeElement("mainTable");
      sortTableByRow(0);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

$(document).on('click', "td.assetassociation-rows", function(){
  activeElement("objectViewer");
  var assocs = JSON.parse($.session.get("AssetAssociations"));
  var assoc = assocs[$(this).closest('tr').index()];

  fillOptionMenu("fastTemplates/editAssetAssociationOptions.html","#objectViewer",null,true,true, function(){
    $('#editAssetAssociationOptionsForm').validator();
    $('#UpdateAssetAssociation').text("Update");
    refreshDimensionSelector($('#theEnvironmentName'),'environment',undefined,function() {
      $('#theEnvironmentName').val(assoc.theEnvironmentName);
      refreshDimensionSelector($('#theHeadAsset'),'asset',assoc.theEnvironmentName,function() {
        $('#theHeadAsset').val(assoc.theHeadAsset);
        refreshDimensionSelector($('#theTailAsset'),'asset',assoc.theEnvironmentName,function() {
          $('#theTailAsset').val(assoc.theTailAsset);
          $('#theHeadNavigation').val(assoc.theHeadNavigation);
          $('#theHeadType').val(assoc.theHeadType);
          $('#theHeadMultiplicity').val(assoc.theHeadMultiplicity);
          $('#theHeadRole').val(assoc.theHeadRole);
          $('#theTailRole').val(assoc.theTailRole);
          $('#theTailMultiplicity').val(assoc.theTailMultiplicity);
          $('#theTailType').val(assoc.theTailType);
          $('#theTailNavigation').val(assoc.theTailNavigation);
          $('#theRationale').val(assoc.theRationale);
          $.session.set("AssetAssociation", JSON.stringify(assoc));
          $('#editAssetAssociationOptionsForm').loadJSON(assoc, null);
        },['All']);
      },['All']);
    },['All']);
  });
});

var mainContent = $("#objectViewer");
mainContent.on('click', '#UpdateAssetAssociation', function (e) {
  e.preventDefault();
  $("#editAssetAssociationOptionsForm").validator();

  var assoc = JSON.parse($.session.get("AssetAssociation"));
  var oldEnvName = assoc.theEnvironmentName;
  var oldHeadName = assoc.theHeadAsset;
  var oldTailName = assoc.theTailAsset;
  assoc.theEnvironmentName = $("#theEnvironmentName").val();
  assoc.theHeadAsset = $("#theHeadAsset").val();
  assoc.theHeadNavigation = $("#theHeadNavigation").val();
  assoc.theHeadType = $("#theHeadType").val();
  assoc.theHeadMultiplicity = $("#theHeadMultiplicity").val();
  assoc.theHeadRole = $("#theHeadRole").val();
  assoc.theTailRole = $("#theTailRole").val();
  assoc.theTailMultiplicity = $("#theTailMultiplicity").val();
  assoc.theTailType = $("#theTailType").val();
  assoc.theTailNavigation = $("#theTailNavigation").val();
  assoc.theTailAsset = $("#theTailAsset").val();
  assoc.theRationale = $("#theRationale").val();

  if($("#editAssetAssociationOptionsForm").hasClass("new")){
    postAssetAssociation(assoc, function () {
      $("#editAssetAssociationOptionsForm").removeClass("new")
      $('#menuBCClick').attr('dimension','assetassociation');
      refreshMenuBreadCrumb('assetassociation');
    });
  }
  else {
    putAssetAssociation(assoc, oldEnvName, oldHeadName, oldTailName,  function () {
      $('#menuBCClick').attr('dimension','assetassociation');
      refreshMenuBreadCrumb('assetassociation');
    });
  }
});

mainContent.on('change',"#theEnvironmentName", function() {
  var envName = $(this).find('option:selected').text();
  var currentHeadAsset = $('#theHeadAsset').val();
  var currentTailAsset = $('#theTailAsset').val();

  refreshDimensionSelector($('#theHeadAsset'),'asset',envName,function() {
    $('#theHeadAsset').val(currentHeadAsset);
    refreshDimensionSelector($('#theTailAsset'),'asset',envName,function() {
      $('#theTailAsset').val(currentTailAsset);
    },['All']);
  },['All']);
});


$(document).on("click", "#addNewAssetAssociation", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editAssetAssociationOptions.html", "#objectViewer", null, true, true, function () {
    $('#editAssetAssociationOptionsForm').validator();
    $('#UpdateAssetAssociation').text("Create");
    $("#editAssetAssociationOptionsForm").addClass("new");

    refreshDimensionSelector($('#theEnvironmentName'),'environment',undefined,function() {
      var envName = $('#theEnvironmentName').val();
      refreshDimensionSelector($('#theHeadAsset'),'asset',envName,function() {
        refreshDimensionSelector($('#theTailAsset'),'asset',envName,function() {
          $('#theHeadNavigation').val('0');
          $('#theHeadType').val('Association');
          $('#theHeadMultiplicity').val('*');
          $('#theHeadRole').val('');
          $('#theTailRole').val('');
          $('#theTailMultiplicity').val('*');
          $('#theTailType').val('Association');
          $('#theTailNavigation').val('0');
          $('#theRationale').val('');
          $.session.set("AssetAssociation", JSON.stringify(jQuery.extend(true, {},classAssociationDefault )));
          $('#editAssetAssociationOptionsForm').loadJSON(assoc, null);
        },['All']);
      },['All']);
    },['All']);
  });
});

$(document).on('click', 'td.deleteAssetAssociationButton', function (e) {
  e.preventDefault();
  var assocs = JSON.parse($.session.get("AssetAssociations"));

  var assocRow = $(this).closest('tr');
  var rowIdx = assocRow.index();
  var assoc = assocs[rowIdx];
  deleteAssetAssociation(assoc, function () {
    $('#menuBCClick').attr('dimension','assetassociation');
    refreshMenuBreadCrumb('assetassociation');
  });
});

mainContent.on('click', '#CloseAssetAssociation', function (e) {
  e.preventDefault();
  $('#menuBCClick').attr('dimension','assetassociation');
  refreshMenuBreadCrumb('assetassociation');
});

function deleteAssetAssociation(assoc, callback){
  $.ajax({
    type: "DELETE",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    url: serverIP +  "/api/assets/association/environment/" + encodeURIComponent(assoc.theEnvironmentName) + "/head/" + encodeURIComponent(assoc.theHeadAsset) + "/tail/" + encodeURIComponent(assoc.theTailAsset) + "?session_id=" + $.session.get('sessionID'),
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

function putAssetAssociation(assoc, oldEnvName, oldHeadAsset, oldTailAsset, callback){
  var output = {};
  output.object = assoc;
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);
  debugLogger(output);

  $.ajax({
    type: "PUT",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP +  "/api/assets/association/environment/" + encodeURIComponent(oldEnvName) + "/head/" + encodeURIComponent(oldHeadAsset) + "/tail/" + encodeURIComponent(oldTailAsset) + "?session_id=" + $.session.get('sessionID'),
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

function postAssetAssociation(assoc, callback){
  var output = {};
  output.object = assoc;
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
    url: serverIP +  "/api/assets/association",
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

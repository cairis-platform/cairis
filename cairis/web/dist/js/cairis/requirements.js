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

// For the assetsbox, if filter is selected
$('#assetsbox').change(function() {
  var selection = $(this).find('option:selected').text();
  updateAssetRequirementsTable(selection);
});

function updateAssetRequirementsTable(selection) {
  if (window.theVisualModel == 'None') {
    $('#environmentsbox').prop('selectedIndex', -1);
    if (selection.toLowerCase() == "") {
      requirementsTable('asset',selection);
    }  
    else {
      $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
          session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + "/api/requirements/asset/" + encodeURIComponent(selection),
        success: function (data) {
          createRequirementsTable(data);
        },
        error: function (xhr, textStatus, errorThrown) {
          var error = JSON.parse(xhr.responseText);
          showPopup(false, String(error.message));
          debugLogger(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    }
  }
  else if (window.theVisualModel == 'asset') {
    getAssetview($('#amenvironmentsbox').val());
  }
}

$('#environmentsbox').change(function() {
  var selection = $(this).find('option:selected').text();
  updateEnvironmentRequirementsTable(selection);
});

function updateEnvironmentRequirementsTable(selection) {
  if (window.theVisualModel == 'None') {
    $('#assetsbox').prop('selectedIndex', -1);
    if (selection.toLowerCase() == "") {
      requirementsTable('environment',selection);
    }   
    else {
      $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
          session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + "/api/requirements/environment/" + encodeURIComponent(selection),
        success: function (data) {
          createRequirementsTable(data);
        },
        error: function (xhr, textStatus, errorThrown) {
          var error = JSON.parse(xhr.responseText);
          showPopup(false, String(error.message));
          debugLogger(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    }
  }
  else if (window.theVisualModel == 'asset') {
    refreshDimensionSelector($('#amassetsbox'),'asset',selection,function(){
      $('#amassetsbox').change();
    });
  }
}

// A function for filling the table with requirements
function createRequirementsTable(data){
  var tre;
  var theTable = $(".theTable");
  $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
  var  originator, rationale, fitCriterion, type = "";

  var theRows = [];
  var i = 0;
  var j = 0;
  $.each(data, function(count, item) {
    var textToInsert = [];
    textToInsert[i++] = '<tr><td name="theLabel">';
    textToInsert[i++] = item.theLabel;
    textToInsert[i++] = '<'+'/td>';

    textToInsert[i++] = '<td name="theName" contenteditable=true>';
    textToInsert[i++] = item.theName;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '<td name="theDescription" contenteditable=true>';
    textToInsert[i++] = item.theDescription;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = "<td name='thePriority' class='reqCombo'>";
    textToInsert[i++] = "<select class='form-control'>";
    textToInsert[i++] = "<option value='1'>1</option>";
    textToInsert[i++] = "<option value='2'>2</option>";
    textToInsert[i++] = "<option value='3'>3</option></select>";
    textToInsert[i++] = '</td>';

    textToInsert[i++] = "<td name='theRationale' contenteditable=true>";
    textToInsert[i++] = item.theRationale;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = "<td name='theFitCriterion' contenteditable=true>";
    textToInsert[i++] = item.theFitCriterion;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = "<td name='theOriginator' contenteditable=true>";
    textToInsert[i++] = item.theOriginator;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = "<td name='theType' class='reqCombo'>";
    textToInsert[i++] ="<select class='form-control'>";
    textToInsert[i++] = "<option value='Functional'>Functional</option>";
    textToInsert[i++] = "<option value='Data'>Data</option>";
    textToInsert[i++] = "<option value='Look and Feel'>Look and Feel</option>";
    textToInsert[i++] = "<option value='Usability'>Usability</option>";
    textToInsert[i++] = "<option value='Performance'>Performance</option>";
    textToInsert[i++] = "<option value='Operational'>Operational</option>";
    textToInsert[i++] = "<option value='Maintainability'>Maintainability</option>";
    textToInsert[i++] = "<option value='Portability'>Portability</option>";
    textToInsert[i++] = "<option value='Security'>Security</option>";
    textToInsert[i++] = "<option value='Cultural and Political'>Cultural and Political</option>";
    textToInsert[i++] = "<option value='Legal'>Legal</option>";
    textToInsert[i++] = "<option value='Privacy'>Privacy</option></select>";
    textToInsert[i++] = '</td>';
    textToInsert[i++] = '</tr>';
    theTable.append(textToInsert.join(''));
    theTable.find('tbody').find('tr').last().find('td:eq(3)').find('.form-control').val(item.thePriority);
    theTable.find('tbody').find('tr').last().find('td:eq(7)').find('.form-control').val(item.theType);
    theTable.find('tbody').find('tr').last().attr('data-name',item.theName);
  });
  theTable.css("visibility","visible");

  $("#mainTable").find("tbody").removeClass();
  $("#mainTable").find("tbody").addClass('requirement-rows');
  $('.requirement-rows').contextMenu({
    selector: 'td',
    items: {
      "add": {
        name: "Add", 
        callback: function(key, opt) {
          addReq();
        }
      },
      "remove": {
        name: "Remove", 
        callback: function(key, opt) {
          var reqName = $(this).closest("tr").find("td").eq(1).html();
          removeReq(reqName);
        }
      },
      "supports": {
        name: "Supported by", 
        callback: function(key, opt) {
          var reqName = $(this).closest("tr").find("td").eq(1).html();
          traceExplorer('requirement',reqName,'0');
        }
      },
      "contributes": {
        name: "Contributes to", 
        callback: function(key, opt) {
          var reqName = $(this).closest("tr").find("td").eq(1).html();
          traceExplorer('requirement',reqName,'1');
        }
      },
    }
  }); 
}

$("#mainTable").on('change',".reqCombo",function(e){
  e.preventDefault();
  var row = $(this).closest('tr');
  updateRequirement(row);
});

function updateRequirement(row){
  var reqName = $(row).find('td:eq(1)').text();
  if (reqName.length <= 0) {
    alert("Requirement name cannot be empty");
    return;
  }
  var clazz = $(row).attr('class');
  if (clazz != undefined) {
    $(row).removeAttr('class');
    var arr = clazz.split(':');
    var whatKind = arr[0];
    var vall = arr[1];
    postRequirementRow(row,whatKind,vall);
  }
  else{
    putRequirementRow(row,$(row).attr('data-name'));
  }
}


function reqRowtoJSON(row){
  var json = {};

  $.each(row[0].children, function (i, v) {
    name =  $(v).attr("name");
    if(name != "thePriority" && name != "theType"){
      json[name] =  v.innerHTML;
    }
    else if (name == 'thePriority') {
      json[name] = row.find('td:eq(3)').find('.form-control').val();
    }
    else if (name == 'theType') {
      json[name] = row.find('td:eq(7)').find('.form-control').val();
    }
  });
  var reqDomain = $('#assetsbox').val();
  if (reqDomain == null) {
    reqDomain = $('#environmentsbox').val();
  } 
  json['theAsset'] = reqDomain;
  return json
}

function putRequirementRow(row,oldName){
  var json = reqRowtoJSON(row);
  var object = {};
  object.object = json;
  object.session_id= $.session.get('sessionID');
  var objectoutput = JSON.stringify(object);
  $.ajax({
    type: "PUT",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    data: objectoutput,
    crossDomain: true,
    url: serverIP + "/api/requirements/name/" + encodeURIComponent(oldName),
    success: function (data) {
      $(row).attr('data-name',json['theName']);
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

function postRequirementRow(row,whatKind,value){
  var json = reqRowtoJSON(row);
  var dimName = "asset";
  var objtName = $( "#assetsbox").find("option:selected").text();
  if (objtName == "") {
    dimName = "environment";
    objtName = $( "#environmentsbox").find("option:selected").text();
  }
  var ursl = serverIP + "/api/requirements?" + dimName + "=" + encodeURIComponent(objtName);
  var object = {};
  object.object = json;
  object.session_id= $.session.get('sessionID');
  var objectoutput = JSON.stringify(object);

  $.ajax({
    type: "POST",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    data: objectoutput,
    crossDomain: true,
    url: ursl,
    success: function (data) {
      $(row).attr('data-name',json['theName']);
      showPopup(true);
      $(document).on("click","#addReqMenu",addReq);
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

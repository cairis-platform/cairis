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
    debugLogger("Selection: " + selection);
    // Clearing the environmentsbox
    $('#environmentsbox').prop('selectedIndex', -1);
    if (selection.toLowerCase() == "all") {
      requirementsTable();
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
          debugLogger(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    }
  }
  else if (window.theVisualModel == 'asset') {
    debugLogger("Selection: " + selection);
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

    if (selection.toLowerCase() == "all") {
      requirementsTable();
    }   
    else {
      //Assetsbox
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

    textToInsert[i++] = "<td name='thePriority' class='reqCombo' contenteditable=true>";
    textToInsert[i++] = "<select class='form-control'>";
    textToInsert[i++] = "<option value='1'>1</option>";
    textToInsert[i++] = "<option value='2'>2</option>";
    textToInsert[i++] = "<option value='3'>3</option></select>";
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '<td name="theId"  style="display:none;">';
    textToInsert[i++] = item.theId;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '<td name="theVersion"  style="display:none;">';
    textToInsert[i++] = item.theVersion;
    textToInsert[i++] = '</td>';

    var datas = eval(item.attrs);
    for (var key in datas) {
      if (datas.hasOwnProperty(key)) {
        // Made this so the TD's are in the right order.
        switch(key){
          case "originator":
            originator = '<td name=' + key + ' contenteditable=true >'+ datas[key] + '</td>';
            break;
          case "rationale":
            rationale = '<td name=' + key + ' contenteditable=true >'+ datas[key] + '</td>';
            break;
          case "fitCriterion":
            fitCriterion = '<td name=' + key + ' contenteditable=true >'+ datas[key] + '</td>';
            break;
          case "type":
            type = "<td name=" + key + " contenteditable=true class='reqCombo'>";
            type +="<select class='form-control'>";
            type += "<option value='Functional'>Functional</option>";
            type += "<option value='Data'>Data</option>";
            type += "<option value='Look and Feel'>Look and Feel</option>";
            type += "<option value='Usability'>Usability</option>";
            type += "<option value='Performance'>Performance</option>";
            type += "<option value='Operational'>Operational</option>";
            type += "<option value='Maintainability'>Maintainability</option>";
            type += "<option value='Portability'>Portability</option>";
            type += "<option value='Security'>Security</option>";
            type += "<option value='Cultural and Political'>Cultural and Political</option>";
            type += "<option value='Legal'>Legal</option>";
            type += "<option value='Privacy'>Privacy</option></select>";
            type += '</td>';
            break;
        }
      }
    }
    textToInsert[i++] = rationale;
    textToInsert[i++] = fitCriterion;
    textToInsert[i++] = originator;
    textToInsert[i++] = type;
    textToInsert[i++] = '</tr>';
    theTable.append(textToInsert.join(''));
    theTable.find('tbody').find('tr').last().find('td:eq(3)').find('.form-control').val(item.thePriority);
    theTable.find('tbody').find('tr').last().find('td:eq(9)').find('.form-control').val(datas['type']);
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
  if ($(row).attr('class') != undefined) {
    var clazz = $(row).attr('class');
    $(clazz).removeClass(clazz);
    var arr = clazz.split(':');
    var whatKind = arr[0];
    var vall = arr[1];
    postRequirementRow(row,whatKind,vall);
  }
  else{
    putRequirementRow(row)
  }
}


function reqRowtoJSON(row){
  var json = {};
  json.attrs = {};

  $.each(row[0].children, function (i, v) {
    name =  $(v).attr("name");
    if(name != "originator" && name != "rationale" && name != "type" && name != "fitCriterion" && name != "thePriority"){
      json[name] =  v.innerHTML;
    }
    else if (name == 'thePriority') {
      json[name] = row.find('td:eq(3)').find('.form-control').val();
    }
    else if (name == 'type') {
      json.attrs[name] = row.find('td:eq(9)').find('.form-control').val();
    }
    else{
      json.attrs[name] = v.innerHTML;
    }
  });
  return json
}

function putRequirementRow(row){
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
    url: serverIP + "/api/requirements" ,
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

function postRequirementRow(row,whatKind,value){
  var json = reqRowtoJSON(row);
  var dimName = "asset";
  var objtName = $( "#assetsbox").find("option:selected").text();
  if (objtName == "") {
    dimName = "environment";
    objtName = $( "#environmentsbox").find("option:selected").text();
  }
  var ursl = serverIP + "/api/requirements?" + dimName + "=" + objtName.replace(' ',"%20");
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

$(document).on('click',"#addReqMenu",function(){
  addReq();
});

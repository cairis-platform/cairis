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
  if (window.theVisualModel == 'None') {
    debugLogger("Selection: " + selection);
    // Clearing the environmentsbox
    $('#environmentsbox').prop('selectedIndex', -1);
    if (selection.toLowerCase() == "all") {
      startingTable();
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
});


$('#environmentsbox').change(function() {
  var selection = $(this).find('option:selected').text();
  if (window.theVisualModel == 'None') {
    $('#assetsbox').prop('selectedIndex', -1);

    if (selection.toLowerCase() == "all") {
      startingTable();
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
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID')),
      },
      crossDomain: true,
      url: serverIP + "/api/assets/environment/" + selection.replace(" ","%20") + "/names",
      success: function (data) {
        $('#amassetsbox').empty();
        $('#amassetsbox').append($('<option>', {value: 'All', text: 'All'},'</option>'));
        $.each(data, function (index, item) {
          $('#amassetsbox').append($('<option>', {value: item, text: item},'</option>'));
        });
        $('#amassetsbox').change();
      },
      error: function (xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  }
});

// A function for filling the table with requirements
function createRequirementsTable(data){
  var tre;
  var theTable = $(".theTable");
  $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
  var textToInsert = [];
  var  originator, rationale, fitCriterion, type = "";

  var theRows = [];
  var i = 0;
  var j = 0;
  $.each(data, function(count, item) {
    textToInsert[i++] = '<tr><td name="theLabel">';
    textToInsert[i++] = item.theLabel;
    textToInsert[i++] = '<'+'/td>';

    textToInsert[i++] = '<td name="theName" contenteditable=true>';
    textToInsert[i++] = item.theName;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '<td name="theDescription" contenteditable=true>';
    textToInsert[i++] = item.theDescription;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '<td name="thePriority"  contenteditable=true>';
    textToInsert[i++] = item.thePriority;
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
            type = '<td name=' + key + ' contenteditable=true >'+ datas[key] + '</td>';
            break;
        }
      }
    }
    textToInsert[i++] = rationale;
    textToInsert[i++] = fitCriterion;
    textToInsert[i++] = originator;
    textToInsert[i++] = type;
    textToInsert[i++] = '</tr>';
  });

  theTable.append(textToInsert.join(''));

  theTable.css("visibility","visible");

  $("#reqTable").find("tbody").removeClass();
  $("#reqTable").find("tbody").addClass('requirement-rows');
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
      }
    }
  }); 
}

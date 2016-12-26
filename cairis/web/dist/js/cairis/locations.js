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

$("#locationsClick").click(function(){
  createLocationsTable();
});

function createLocationsTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/locations",
    success: function (data) {
      window.activeTable = "Locations";
      setTableHeader();
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";

        textToInsert[i++] = '<td class="deleteLocationsButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="locations-rows" name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      });

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
      $("#reqTable").find("tbody").removeClass();

      activeElement("reqTable");
      sortTableByRow(0);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
}

$(document).on('click', "td.locations-rows", function () {
  activeElement("objectViewer");
  var name = $(this).text();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/locations/name/" + name.replace(" ", "%20"),
    success: function (data) {
      fillOptionMenu("fastTemplates/editLocationsOptions.html", "#objectViewer", null, true, true, function () {
        $("#editLocationsOptionsForm").validator();
        $("#UpdateLocations").text("Update");
        $.session.set("Locations", JSON.stringify(data));
        $('#editLocationsOptionsForm').loadJSON(data, null);
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

var mainContent = $("#objectViewer");
mainContent.on('click', '#UpdateLocations', function (e) {
  e.preventDefault();
  var locs = JSON.parse($.session.get("Locations"));
  var oldName = locs.theName;
  locs.theName = $("#theName").val();

  if($("#editLocationsOptionsForm").hasClass("new")){
    postLocations(locs, function () {
      createLocationsTable();
      $("#editLocationsOptionsForm").removeClass("new")
    });
  }
  else {
    putLocations(locs, oldName, function () {
      createLocationsTable();
    });
  }
});

$(document).on('click', 'td.deleteLocationsButton', function (e) {
  e.preventDefault();
  deleteLocations($(this).find('i').attr("value"), function () {
    createLocationsTable();
  });
});

$(document).on("click", "#addNewLocations", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editLocationsOptions.html", "#objectViewer", null, true, true, function () {
    $("#editLocationsOptionsForm").validator();
    $("#UpdateLocations").text("Create");
    $("#editLocationsOptionsForm").addClass("new");
    $.session.set("Locations", JSON.stringify(jQuery.extend(true, {},locationsDefault )));
  });
});


function putLocations(locs, oldName, usePopup, callback){
  var output = {};
  output.object = locs;
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
    url: serverIP + "/api/locations/name/" + oldName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
    success: function (data) {
      if(usePopup) {
        showPopup(true);
      }
      if(jQuery.isFunction(callback)){
        callback();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      if(usePopup) {
        var error = JSON.parse(xhr.responseText);
        showPopup(false, String(error.message));
      }
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function postLocations(locs, callback){
  var output = {};
  output.object = locs;
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
    url: serverIP + "/api/locations" + "?session_id=" + $.session.get('sessionID'),
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

function deleteLocations(name, callback){
  $.ajax({
    type: "DELETE",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    url: serverIP + "/api/locations/name/" + name.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
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

mainContent.on('click', '#CloseLocations', function (e) {
  e.preventDefault();
  createLocationsTable();
});


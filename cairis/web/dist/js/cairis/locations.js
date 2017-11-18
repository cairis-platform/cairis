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
  validateClick('location',function() {
    $('#menuBCClick').attr('dimension','location');
    refreshMenuBreadCrumb('location');
  });
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
      setTableHeader("Locations");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      var keys = [];
      for (key in data) {
        keys.push(key);
      }
      keys.sort();

      for (var ki = 0; ki < keys.length; ki++) {
        var key = keys[ki];
        var item = data[key];

        textToInsert[i++] = "<tr>";

        textToInsert[i++] = '<td class="deleteLocationsButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="locations-rows" name="theName">';
        textToInsert[i++] = key;
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

$(document).on('click', "td.locations-rows", function () {
  var name = $(this).text();
  refreshObjectBreadCrumb(name);
  viewLocations(name);
});

function viewLocations(locsName) {
  activeElement("objectViewer");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/locations/name/" + encodeURIComponent(locsName),
    success: function (data) {
      fillOptionMenu("fastTemplates/editLocationsOptions.html", "#objectViewer", null, true, true, function () {
        $.session.set("Locations", JSON.stringify(data));
        $("#UpdateLocations").text("Update");
        $('#theLocationsName').val(data.theName);
        $('#theLocations').find("tbody").empty();
        $.each(data.theLocations,function(idx,loc) {
          appendLocation(loc);
        });
        $("#editLocationsOptionsForm").validator('update');
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function appendLocation(loc) {
    $("#theLocations").find("tbody").append('<tr><td class="deleteLocation"><i class="fa fa-minus"></i></td><td class="location-rows">'+ loc.theName +'</td></tr>');
};

$(document).on("click", "#addNewLocations", function () {
  refreshObjectBreadCrumb('New Locations');
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editLocationsOptions.html", "#objectViewer", null, true, true, function () {
    $("#UpdateLocations").text("Create");
    $("#editLocationsOptionsForm").addClass("new");
    $('#theLocationsName').val('');
    $('#theLocations').find("tbody").empty();
    $.session.set("Locations", JSON.stringify(jQuery.extend(true, {},locationsDefault )));
  });
});


mainContent.on('click','#addLocation',function() {
   $.session.set("Location", JSON.stringify(jQuery.extend(true, {},locationDefault )));
   $('#locationDiv').addClass('new');
   $('#locationsDiv').hide();
   $('#locationDiv').show();
   $('#theLocationName').val('');
   $('#theObjects').find("tbody").empty();
   $('#thePersonas').find("tbody").empty();
   $('#theLinks').find("tbody").empty();
});


$(document).on('click', "td.location-rows", function () {
  var locRow = $(this).closest("tr");
  $('#locationsDiv').attr('data-selectedIndex',locRow.index());
  var locName = $(this).text();
  var locs = JSON.parse($.session.get("Locations"));
  $.each(locs.theLocations,function(idx,loc) {
    if (locName == loc.theName) {
      $('#locationsDiv').hide();
      $('#locationDiv').show(function() {
        $.session.set("Location", JSON.stringify(loc));
        $('#theLocationName').val(locName);
        $('#theObjects').find("tbody").empty();
        $.each(loc.theAssetInstances,function(idx,ai) {
          appendAssetInstance(ai);
        });
        $('#thePersonas').find("tbody").empty();
        $.each(loc.thePersonaInstances,function(idx,pi) {
          appendPersonaInstance(pi);
        });
        $('#theLinks').find("tbody").empty();
        $.each(loc.theLinks,function(idx,link) {
          appendLocationLink(link);
        });

      });
    }
  });
});

function appendAssetInstance(ai) {
    $("#theObjects").find("tbody").append('<tr><td class="deleteAssetInstance"><i class="fa fa-minus"></i></td><td class="asset-instance">'+ ai.theName +'</td><td>' + ai.theAsset + '</td></tr>');
}

function appendPersonaInstance(pi) {
    $("#thePersonas").find("tbody").append('<tr><td class="deletePersonaInstance"><i class="fa fa-minus"></i></td><td class="persona-instance">'+ pi.theName +'</td><td>' + pi.thePersona + '</td></tr>');
}

function appendLocationLink(link) {
    $("#theLinks").find("tbody").append('<tr><td class="deleteLocationLink"><i class="fa fa-minus"></i></td><td class="location-link">'+ link + '</td></tr>');
}

var mainContent = $("#objectViewer");
mainContent.on("click","#CloseLocation",function(e) {
  e.preventDefault();
  $("#locationDiv").hide();
  $("#locationsDiv").show();
});

mainContent.on("click","#UpdateLocation",function(e) {
  e.preventDefault();
  var loc = JSON.parse($.session.get("Location"));
  loc.theName = $('#theLocationName').val();
  var locs = JSON.parse($.session.get("Locations"));

  if ($("#locationDiv").hasClass('new')) {
    locs.theLocations.push(loc);
    $.session.set("Locations",JSON.stringify(locs));
    appendLocation(loc);
  }
  else {
    var selectedIdx = $('#locationsDiv').attr('data-selectedIndex');
    locs.theLocations[selectedIdx] = loc;
    $.session.set("Locations",JSON.stringify(locs));
    $('#theLocations').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(loc.theName);
  }
  $("#locationDiv").hide();
  $("#locationsDiv").show();
});

$(document).on('shown.bs.modal','#addAssetInstanceDialog',function() {
  var selectedInstance = $('#addAssetInstanceDialog').attr('data-selectedInstance');
  if (selectedInstance != undefined) {
    selectedInstance = JSON.parse(selectedInstance);
    $('#AddAssetInstance').text('Update');
    $('#theAssetInstanceName').val(selectedInstance.theName);
  }
  else {
    $('#theAssetInstanceName').val('');
    $('#theAssetName').val('');
    $('#AddAssetInstance').text('Add');
  }

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/asset",
    success: function (assets) {
      $("#theAssetName option").remove();
      $.each(assets,function(idx,asset) {
        $('#theAssetName').append($("<option></option>").attr("value",asset).text(asset));
      });
      if (selectedInstance != undefined) {
        $('#theAssetName').val(selectedInstance.theAsset);
      }
      else {
        $('#theAssetName').val('');
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$(document).on('shown.bs.modal','#addPersonaInstanceDialog',function() {
  var selectedInstance = $('#addPersonaInstanceDialog').attr('data-selectedInstance');
  if (selectedInstance != undefined) {
    selectedInstance = JSON.parse(selectedInstance);
    $('#AddPersonaInstance').text('Update');
    $('#thePersonaInstanceName').val(selectedInstance.theName);
  }
  else {
    $('#thePersonaInstanceName').val('');
    $('#thePersonaName').val('');
    $('#AddPersonaInstance').text('Add');
  }

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/persona",
    success: function (personas) {
      $("#thePersonaName option").remove();
      $.each(personas,function(idx,persona) {
        $('#thePersonaName').append($("<option></option>").attr("value",persona).text(persona));
      });
      if (selectedInstance != undefined) {
        $('#thePersonaName').val(selectedInstance.thePersona);
      }
      else {
        $('#thePersonaName').val('');
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$(document).on('shown.bs.modal','#addLocationLinkDialog',function() {
  var selectedLink = $('#addLocationLinkDialog').attr('data-selectedLink');
  if (selectedLink != undefined) {
    selectedLink = JSON.parse(selectedLink);
    $('#AddLocationLink').text('Update');
    $('#theLinkName').val(selectedLink);
  }
  else {
    $('#theLinkName').val('');
    $('#AddLocationLink').text('Add');
  }
  var locs = JSON.parse($.session.get("Locations"));
  var loc = JSON.parse($.session.get("Location"));
  var currentLinks = loc.theLinks
  $("#theLinkName option").remove();
  $.each(locs.theLocations,function(idx,loc) {
    if (currentLinks.indexOf(loc.theName) < 0) {
      $('#theLinkName').append($("<option></option>").attr("value",loc.theName).text(loc.theName));
    }
  });
  if (selectedLink != undefined) {
    $('#theLinkName').val(selectedLink);
  }
  else {
    $('#theLinkName').val('');
  }
});

mainContent.on('click','#addAssetInstance',function() {
  $('#addAssetInstanceDialog').removeAttr('data-selectedInstance');
  $('#addAssetInstanceDialog').removeAttr('data-selectedIndex');
  $('#addAssetInstanceDialog').modal('show');
});


mainContent.on('click','td.asset-instance',function(){
  var iRow = $(this).closest("tr");
  var selectedInstance = {};
  selectedInstance.theName = iRow.find("td:eq(1)").text();
  selectedInstance.theAsset = iRow.find("td:eq(2)").text();

  $('#addAssetInstanceDialog').attr('data-selectedInstance',JSON.stringify(selectedInstance));
  $('#addAssetInstanceDialog').attr('data-selectedIndex',intRow.index());
  $('#addAssetInstanceDialog').modal('show');
});

mainContent.on('click','#AddAssetInstance',function() {
  var selectedInstance = {};
  selectedInstance.theName = $('#theAssetInstanceName').val();
  selectedInstance.theAsset = $('#theAssetName').val();

  var loc = JSON.parse($.session.get("Location"));
  var selectedIdx = $('#addAssetInstanceDialog').attr('data-selectedIndex');
  if (selectedIdx != undefined) {
    loc.theAssetInstances[selectedIdx] = selectedInstance;
    $.session.set("Location", JSON.stringify(loc));
    $('#theAssetInstances').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(selectedInstance.theName);
    $('#theAssetInstances').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(2)').text(selectedInstance.theAsset);
  }
  else {
    loc.theAssetInstances.push(selectedInstance);
    $.session.set("Location", JSON.stringify(loc));
    appendAssetInstance(selectedInstance);
  }
  $('#addAssetInstanceDialog').modal('hide');
});

mainContent.on('click','td.deleteAssetInstance',function() {
  var iRow = $(this).closest("tr");
  var rowIdx = iRow.index();
  iRow.remove();
  var loc = JSON.parse($.session.get("Location"));
  loc.theAssetInstances.splice(rowIdx,1);
  $.session.set("Location", JSON.stringify(loc));
});

mainContent.on('click','#addPersonaInstance',function() {
  $('#addPersonaInstanceDialog').removeAttr('data-selectedInstance');
  $('#addPersonaInstanceDialog').removeAttr('data-selectedIndex');
  $('#addPersonaInstanceDialog').modal('show');
});

mainContent.on('click','td.persona-instance',function(){
  var iRow = $(this).closest("tr");
  var selectedInstance = {};
  selectedInstance.theName = iRow.find("td:eq(1)").text();
  selectedInstance.thePersona = iRow.find("td:eq(2)").text();

  $('#addPersonaInstanceDialog').attr('data-selectedInstance',JSON.stringify(selectedInstance));
  $('#addPersonaInstanceDialog').attr('data-selectedIndex',iRow.index());
  $('#addPersonaInstanceDialog').modal('show');
});

mainContent.on('click','#AddPersonaInstance',function() {
  var selectedInstance = {};
  selectedInstance.theName = $('#thePersonaInstanceName').val();
  selectedInstance.thePersona = $('#thePersonaName').val();

  var loc = JSON.parse($.session.get("Location"));
  var selectedIdx = $('#addPersonaInstanceDialog').attr('data-selectedIndex');
  if (selectedIdx != undefined) {
    loc.thePersonaInstances[selectedIdx] = selectedInstance;
    $.session.set("Location", JSON.stringify(loc));
    $('#thePersonaInstances').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(selectedInstance.theName);
    $('#thePersonaInstances').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(2)').text(selectedInstance.thePersona);
  }
  else {
    loc.thePersonaInstances.push(selectedInstance);
    $.session.set("Location", JSON.stringify(loc));
    appendPersonaInstance(selectedInstance);
  }
  $('#addPersonaInstanceDialog').modal('hide');
});

mainContent.on('click','td.deletePersonaInstance',function() {
  var iRow = $(this).closest("tr");
  var rowIdx = iRow.index();
  iRow.remove();
  var loc = JSON.parse($.session.get("Location"));
  loc.thePersonaInstances.splice(rowIdx,1);
  $.session.set("Location", JSON.stringify(loc));
});

mainContent.on('click','#addLocationLink',function() {
  $('#addLocationLinkDialog').removeAttr('data-selectedLink');
  $('#addLocationLinkDialog').removeAttr('data-selectedIndex');
  $('#addLocationLinkDialog').modal('show');
});

mainContent.on('click','td.location-link',function(){
  var iRow = $(this).closest("tr");
  selectedLink = iRow.find("td:eq(1)").text();
  $('#addLocationLinkDialog').attr('data-selectedLink',JSON.stringify(selectedLink));
  $('#addLocationLinkDialog').attr('data-selectedIndex',iRow.index());
  $('#addLocationLinkDialog').modal('show');
});

mainContent.on('click','#AddLocationLink',function() {
  var selectedLink = $('#theLinkName').val();

  var loc = JSON.parse($.session.get("Location"));
  var selectedIdx = $('#addLocationLinkDialog').attr('data-selectedIndex');
  if (selectedIdx != undefined) {
    loc.theLinks[selectedIdx] = selectedLink;
    $.session.set("Location", JSON.stringify(loc));
    $('#theLinks').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(selectedLink);
  }
  else {
    loc.theLinks.push(selectedLink);
    $.session.set("Location", JSON.stringify(loc));
    appendLocationLink(selectedLink);
  }
  $('#addLocationLinkDialog').modal('hide');
});

mainContent.on('click','td.deleteLocationLink',function() {
  var iRow = $(this).closest("tr");
  var rowIdx = iRow.index();
  iRow.remove();
  var loc = JSON.parse($.session.get("Location"));
  loc.theLinks.splice(rowIdx,1);
  $.session.set("Location", JSON.stringify(loc));
});


function commitLocations() {
  var locs = JSON.parse($.session.get("Locations"));
  var oldName = locs.theName;
  locs.theName = $("#theLocationsName").val();

  if($("#editLocationsOptionsForm").hasClass("new")){
    postLocations(locs, function () {
      $('#menuBCClick').attr('dimension','location');
      refreshMenuBreadCrumb('location');
      $("#editLocationsOptionsForm").removeClass("new")
    });
  }
  else {
    putLocations(locs, oldName, function () {
      $('#menuBCClick').attr('dimension','location');
      refreshMenuBreadCrumb('location');
    });
  }
}

$(document).on('click', 'td.deleteLocationsButton', function (e) {
  e.preventDefault();
  deleteLocations($(this).find('i').attr("value"), function () {
    $('#menuBCClick').attr('dimension','location');
    refreshMenuBreadCrumb('location');
  });
});

$(document).on("click", "#addLocations", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editLocationsOptions.html", "#objectViewer", null, true, true, function () {
    $("#editLocationsOptionsForm").validator();
    $("#UpdateLocations").text("Create");
    $("#editLocationsOptionsForm").addClass("new");
    $.session.set("Locations", JSON.stringify(jQuery.extend(true, {},locationsDefault )));
    $('#theLocationsName').val('');
    $('#theLocations').find("tbody").empty();
  });
});


function putLocations(locs, oldName, callback){
  var output = {};
  output.object = locs;
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
    url: serverIP + "/api/locations/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
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

function postLocations(locs, callback){
  var output = {};
  output.object = locs;
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
    url: serverIP + "/api/locations/name/" + encodeURIComponent(name) + "?session_id=" + $.session.get('sessionID'),
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
  $('#menuBCClick').attr('dimension','location');
  refreshMenuBreadCrumb('location');
});


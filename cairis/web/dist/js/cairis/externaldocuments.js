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

$("#externalDocumentsClick").click(function(){
  clearLocalStorage($('#menuBCClick').attr('dimension'));
  $('#menuBCClick').attr('dimension','external_document');
  refreshMenuBreadCrumb('external_document');
});

function createExternalDocumentsTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/external_documents",
    success: function (data) {
      setTableHeader("ExternalDocuments");
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

        textToInsert[i++] = '<td class="deleteExternalDocumentButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="externaldocument-rows" name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theDescription">';
        textToInsert[i++] = item.theDescription;
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
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
}

$(document).on('click', "td.externaldocument-rows", function () {
  activeElement("objectViewer");
  var name = $(this).text();
  refreshObjectBreadCrumb(name);
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/external_documents/name/" + encodeURIComponent(name),
    success: function (data) {
      fillOptionMenu("fastTemplates/editExternalDocumentOptions.html", "#objectViewer", null, true, true, function () {
        $("#UpdateExternalDocument").text("Update");
        $.session.set("ExternalDocument", JSON.stringify(data));
        $('#editExternalDocumentOptionsForm').loadJSON(data, null);
        $("#editExternalDocumentOptionsForm").validator('update');
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

var mainContent = $("#objectViewer");

function commitExternalDocument() {
  var edoc = JSON.parse($.session.get("ExternalDocument"));
  var oldName = edoc.theName;
  edoc.theName = $("#theName").val();
  edoc.theVersion = $("#theVersion").val();
  edoc.theAuthors = $("#theAuthors").val();
  edoc.thePublicationDate = $("#thePublicationDate").val();
  edoc.theDescription = $("#theDescription").val();

  if($("#editExternalDocumentOptionsForm").hasClass("new")){
    postExternalDocument(edoc, function () {
      clearLocalStorage('external_document');
      $("#editExternalDocumentOptionsForm").removeClass("new")
      $('#menuBCClick').attr('dimension','external_document');
      refreshMenuBreadCrumb('external_document');
    });
  }
  else {
    putExternalDocument(edoc, oldName, function () {
      clearLocalStorage('external_document');
      $('#menuBCClick').attr('dimension','external_document');
      refreshMenuBreadCrumb('external_document');
    });
  }
}

$(document).on('click', 'td.deleteExternalDocumentButton', function (e) {
  e.preventDefault();
  deleteExternalDocument($(this).find('i').attr("value"), function () {
    $('#menuBCClick').attr('dimension','external_document');
    refreshMenuBreadCrumb('external_document');
  });
});

$(document).on("click", "#addNewExternalDocument", function () {
  refreshObjectBreadCrumb('New External Document');
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editExternalDocumentOptions.html", "#objectViewer", null, true, true, function () {
    $("#editExternalDocumentOptionsForm").validator();
    $("#UpdateExternalDocument").text("Create");
    $("#editExternalDocumentOptionsForm").addClass("new");
    $.session.set("ExternalDocument", JSON.stringify(jQuery.extend(true, {},externalDocumentDefault )));
  });
});


function putExternalDocument(edoc, oldName, callback){
  var output = {};
  output.object = edoc;
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
    url: serverIP + "/api/external_documents/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
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

function postExternalDocument(edoc, callback){
  var output = {};
  output.object = edoc;
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
    url: serverIP + "/api/external_documents" + "?session_id=" + $.session.get('sessionID'),
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

function deleteExternalDocument(name, callback){
  $.ajax({
    type: "DELETE",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    url: serverIP + "/api/external_documents/name/" + encodeURIComponent(name) + "?session_id=" + $.session.get('sessionID'),
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

mainContent.on('click', '#CloseExternalDocument', function (e) {
  e.preventDefault();
  clearLocalStorage('external_document');
  $('#menuBCClick').attr('dimension','external_document');
  refreshMenuBreadCrumb('external_document');
});


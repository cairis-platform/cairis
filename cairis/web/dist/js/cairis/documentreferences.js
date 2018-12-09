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

$("#documentReferencesClick").click(function(){
  clearLocalStorage($('#menuBCClick').attr('dimension'));
  $("#objectViewer").empty();
  $('#menuBCClick').attr('dimension','document_reference');
  refreshMenuBreadCrumb('document_reference');
});

function createDocumentReferencesTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/document_references",
    success: function (data) {
      setTableHeader("DocumentReferences");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      for (var r = 0; r < data.length; r++) {
        var item = data[r];

        textToInsert[i++] = "<tr>";

        textToInsert[i++] = '<td class="deleteDocumentReferenceButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';
        textToInsert[i++] = '<td class="documentreference-rows" name="theName">';
        textToInsert[i++] = item.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="documentreference-rows" name="theDocName">';
        textToInsert[i++] = item.theDocName;
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

$(document).on('click', "td.documentreference-rows", function () {
  activeElement("objectViewer");
  var name = $(this).closest("tr").find("td:eq(1)").text();
  refreshObjectBreadCrumb(name);
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/document_references/name/" + encodeURIComponent(name),
    success: function (data) {
      fillOptionMenu("fastTemplates/editDocumentReferenceOptions.html", "#objectViewer", null, true, true, function () {
        $("#UpdateDocumentReference").text("Update");
        var docNameSelect = $("#theDocName");
        var docName = data.theDocName;
        getDocNames(function(data) {
          $.each(data, function(key, obj) {
            docNameSelect.append($("<option></option>").attr("value",obj).text(obj));
          });
          docNameSelect.val(docName);
        });
        $.session.set("DocumentReference", JSON.stringify(data));
        $('#editDocumentReferenceOptionsForm').loadJSON(data, null);
        $("#editDocumentReferenceOptionsForm").validator('update');
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

var mainContent = $("#objectViewer");

function commitDocumentReference() {
  var dr = JSON.parse($.session.get("DocumentReference"));
  var oldName = dr.theName;
  dr.theName = $("#theName").val();
  dr.theDocName = $("#theDocName").val();
  dr.theContributor = $("#theContributor").val();
  dr.theExcerpt = $("#theExcerpt").val();

  if($("#editDocumentReferenceOptionsForm").hasClass("new")){
    postDocumentReference(dr, function () {
      clearLocalStorage('document_reference');
      $("#editDocumentReferenceOptionsForm").removeClass("new")
      $('#menuBCClick').attr('dimension','document_reference');
      refreshMenuBreadCrumb('document_reference');
    });
  }
  else {
    putDocumentReference(dr, oldName, function () {
      clearLocalStorage('document_reference');
      $('#menuBCClick').attr('dimension','document_reference');
      refreshMenuBreadCrumb('document_reference');
    });
  }
}

$(document).on('click', 'td.deleteDocumentReferenceButton', function (e) {
  e.preventDefault();
  deleteDocumentReference($(this).find('i').attr("value"), function () {
    $('#menuBCClick').attr('dimension','document_reference');
    refreshMenuBreadCrumb('document_reference');
  });
});

$(document).on("click", "#addNewDocumentReference", function () {
  refreshObjectBreadCrumb('New Document Reference');
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editDocumentReferenceOptions.html", "#objectViewer", null, true, true, function () {
    $("#editDocumentReferenceOptionsForm").validator();
    $("#UpdateDocumentReference").text("Create");
    $("#editDocumentReferenceOptionsForm").addClass("new");
    $.session.set("DocumentReference", JSON.stringify(jQuery.extend(true, {},documentReferenceDefault )));
    var docNameSelect = $("#theDocName");
    getDocNames(function(data) {
      $.each(data, function(key, obj) {
        docNameSelect.append($("<option></option>").attr("value",obj).text(obj));
      });
    });
  });
});


function putDocumentReference(dr, oldName, callback){
  var output = {};
  output.object = dr;
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
    url: serverIP + "/api/document_references/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
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

function postDocumentReference(dr, callback){
  var output = {};
  output.object = dr;
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
    url: serverIP + "/api/document_references" + "?session_id=" + $.session.get('sessionID'),
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

function deleteDocumentReference(name, callback){
  $.ajax({
    type: "DELETE",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    url: serverIP + "/api/document_references/name/" + encodeURIComponent(name) + "?session_id=" + $.session.get('sessionID'),
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

function getDocNames(callback){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/dimensions/table/external_document",
    success: function (data) {
      if(jQuery.isFunction(callback)){
        callback(data);
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

mainContent.on('click', '#CloseDocumentReference', function (e) {
  e.preventDefault();
  clearLocalStorage('document_reference');
  $("#objectViewer").empty();
  $('#menuBCClick').attr('dimension','document_reference');
  refreshMenuBreadCrumb('document_reference');
});


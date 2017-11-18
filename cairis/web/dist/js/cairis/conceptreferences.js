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

$("#conceptReferencesClick").click(function(){
  createConceptReferencesTable();
});

function createConceptReferencesTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/concept_references",
    success: function (data) {
      setTableHeader("ConceptReferences");
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

        textToInsert[i++] = '<td class="deleteConceptReferenceButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="conceptreference-rows" name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theDimName">';
        textToInsert[i++] = item.theDimName;
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

$(document).on('click', "td.conceptreference-rows", function () {
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
    url: serverIP + "/api/concept_references/name/" + encodeURIComponent(name),
    success: function (data) {
      fillOptionMenu("fastTemplates/editConceptReferenceOptions.html", "#objectViewer", null, true, true, function () {
        refreshDimensionSelector($('#theObjtName'),$('#theDimName').val(),undefined,function() {
          $("#UpdateConceptReference").text("Update");
          $('#theDimName').val(data.theDimName);
          getObjtNames(data.theDimName,data.theObjtName);
          $.session.set("ConceptReference", JSON.stringify(data));
          $('#editConceptReferenceOptionsForm').loadJSON(data, null);
          $("#editConceptReferenceOptionsForm").validator('update');
	});
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
mainContent.on('change', '#theDimName', function (e) {
  e.preventDefault();
  getObjtNames($('#theDimName').val());
});

function commitConceptReference() {
  var cr = JSON.parse($.session.get("ConceptReference"));
  var oldName = cr.theName;
  cr.theName = $("#theName").val();
  cr.theDimName = $("#theDimName").val();
  cr.theObjtName = $("#theObjtName").val();
  cr.theDescription = $("#theDescription").val();

  if($("#editConceptReferenceOptionsForm").hasClass("new")){
    postConceptReference(cr, function () {
      createConceptReferencesTable();
      $("#editConceptReferenceOptionsForm").removeClass("new")
    });
  }
  else {
    putConceptReference(cr, oldName, function () {
      createConceptReferencesTable();
    });
  }
}

$(document).on('click', 'td.deleteConceptReferenceButton', function (e) {
  e.preventDefault();
  deleteConceptReference($(this).find('i').attr("value"), function () {
    createConceptReferencesTable();
  });
});

$(document).on("click", "#addNewConceptReference", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editConceptReferenceOptions.html", "#objectViewer", null, true, true, function () {
    refreshDimensionSelector($('#theObjtName'),$('#theDimName').val(),undefined,function() {
      $("#editConceptReferenceOptionsForm").validator();
      $("#UpdateConceptReference").text("Create");
      $("#editConceptReferenceOptionsForm").addClass("new");
      $.session.set("ConceptReference", JSON.stringify(jQuery.extend(true, {},conceptReferenceDefault )));
    });
  });
});


function putConceptReference(cr, oldName, callback){
  var output = {};
  output.object = cr;
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
    url: serverIP + "/api/concept_references/name/" + encodeURIComponent(oldName),
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

function postConceptReference(cr, callback){
  var output = {};
  output.object = cr;
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
    url: serverIP + "/api/concept_references",
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

function deleteConceptReference(name, callback){
  $.ajax({
    type: "DELETE",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    url: serverIP + "/api/concept_references/name/" + encodeURIComponent(name) + "?session_id=" + $.session.get('sessionID'),
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

function getObjtNames(dimName,currentValue){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/dimensions/table/" + dimName,
    success: function (data) {
      $('#theObjtName').empty();
      $('#theObjtName').append($('<option>', {value: 'All', text: 'All'},'</option>'));
      $.each(data, function (index, item) {
        $('#theObjtName').append($('<option>', {value: item, text: item},'</option>'));
      });
      if (currentValue != undefined) {
        $('#theObjtName').val(currentValue);
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

mainContent.on('click', '#CloseConceptReference', function (e) {
  e.preventDefault();
  createConceptReferencesTable();
});


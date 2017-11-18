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

$("#personaCharacteristicsClick").click(function(){
  $('#menuBCClick').attr('dimension','persona_characteristic');
  refreshMenuBreadCrumb('persona_characteristic');
});

function createPersonaCharacteristicsTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/persona_characteristics",
    success: function (data) {
      setTableHeader("PersonaCharacteristics");
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

        textToInsert[i++] = '<td class="deletePersonaCharacteristicButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="personacharacteristic-rows" name="theName">';
        textToInsert[i++] = item.thePersonaName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theVariable">';
        textToInsert[i++] = item.theVariable;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theCharacteristic">';
        textToInsert[i++] = item.theCharacteristic;
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
  });
}

$(document).on('click', "td.personacharacteristic-rows", function () {
  activeElement("objectViewer");
  var name = $(this).closest("tr").find("td:eq(3)").text();
  refreshObjectBreadCrumb(name);
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/persona_characteristics/name/" + encodeURIComponent(name),
    success: function (data) {
      fillOptionMenu("fastTemplates/editPersonaCharacteristicOptions.html", "#objectViewer", null, true, true, function () {
        $.ajax({
          type: "GET",
          dataType: "json",
          accept: "application/json",
          data: {
            session_id: String($.session.get('sessionID'))
          },
          crossDomain: true,
          url: serverIP + "/api/dimensions/table/persona",
          success: function (pNames) {
            var personaSelect = $('#thePersonaName');
            $.each(pNames, function (index,pName) {
              personaSelect.append($("<option></option>").attr("value",pName).text(pName));
            });
            $("#UpdatePersonaCharacteristic").text("Update");
            $.session.set("PersonaCharacteristic", JSON.stringify(data));
            personaSelect.val(data.thePersonaName);
            $("#theVariable").val(data.theVariable);
            $("#theModQual").val(data.theModQual);
            $("#theCharacteristic").val(data.theCharacteristic);
     
            $("#theGrounds").find("tbody").empty();
            $.each(data.theGrounds,function(idx,item) {
              appendGWR("#theGrounds",'ground',item); 
            }); 

            $("#theWarrant").find("tbody").empty();
            $.each(data.theWarrant,function(idx,item) {
              appendGWR("#theWarrant",'warrant',item); 
            });
            $("#theRebuttal").find("tbody").empty();
            $.each(data.theRebuttal,function(idx,item) {
              appendGWR("#theRebuttal",'rebuttal',item); 
            });
            $("#theBacking").find("tbody").empty();
            $.each(data.theBacking,function(idx,item) {
              appendBacking(item); 
            }); 

            $('#theCharacteristicSynopsis').val(data.theCharacteristicSynopsis.theSynopsis);
            $('#theCharacteristicSynopsisElementType').val(data.theCharacteristicSynopsis.theDimension);
            $("#editPersonaCharacteristicOptionsForm").validator('update');
          },
          error: function (xhr, textStatus, errorThrown) {
            var error = JSON.parse(xhr.responseText);
            showPopup(false, String(error.message));
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
          }
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
function commitPersonaCharacteristic() {
  var pc = JSON.parse($.session.get("PersonaCharacteristic"));
  var oldName = pc.theCharacteristic;
  pc.thePersonaName = $("#thePersonaName").val();
  pc.theVariable = $("#theVariable").val();
  pc.theModQual = $("#theModQual").val();
  pc.theCharacteristic = $("#theCharacteristic").val();
  pc.theCharacteristicSynopsis.theSynopsis = $('#theCharacteristicSynopsis').val();
  pc.theCharacteristicSynopsis.theDimension = $('#theCharacteristicSynopsisElementType').val();

  if($("#editPersonaCharacteristicOptionsForm").hasClass("new")){
    postPersonaCharacteristic(pc, function () {
      $("#editPersonaCharacteristicOptionsForm").removeClass("new")
      $('#menuBCClick').attr('dimension','persona_characteristic');
      refreshMenuBreadCrumb('persona_characteristic');
    });
  }
  else {
    putPersonaCharacteristic(pc, oldName, function () {
      $('#menuBCClick').attr('dimension','persona_characteristic');
      refreshMenuBreadCrumb('persona_characteristic');
    });
  }
}

$(document).on('click', 'td.deletePersonaCharacteristicButton', function (e) {
  e.preventDefault();
  var pName = $(this).closest('tr').find('td:eq(3)').text();
  deletePersonaCharacteristic(pName, function () {
    $('#menuBCClick').attr('dimension','persona_characteristic');
    refreshMenuBreadCrumb('persona_characteristic');
  });
});

$(document).on("click", "#addNewPersonaCharacteristic", function () {
  refreshObjectBreadCrumb('New Persona Characteristic');
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editPersonaCharacteristicOptions.html", "#objectViewer", null, true, true, function () {
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/dimensions/table/persona",
      success: function (data) {
        var personaSelect = $('#thePersonaName');
        $.each(data, function (index,pName) {
          personaSelect.append($("<option></option>").attr("value",pName).text(pName));
        });
        $("#editPersonaCharacteristicOptionsForm").validator();
        $("#UpdatePersonaCharacteristic").text("Create");
        $("#editPersonaCharacteristicOptionsForm").addClass("new");
        $.session.set("PersonaCharacteristic", JSON.stringify(jQuery.extend(true, {},personaCharacteristicDefault )));
      },
      error: function (xhr, textStatus, errorThrown) {
        var error = JSON.parse(xhr.responseText);
        showPopup(false, String(error.message));
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  });
});


function putPersonaCharacteristic(pc, oldName, callback){
  var output = {};
  output.object = pc;
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
    url: serverIP + "/api/persona_characteristics/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
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

function postPersonaCharacteristic(pc, callback){
  var output = {};
  output.object = pc;
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
    url: serverIP + "/api/persona_characteristics" + "?session_id=" + $.session.get('sessionID'),
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

function deletePersonaCharacteristic(name, callback){
  $.ajax({
    type: "DELETE",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    url: serverIP + "/api/persona_characteristics/name/" + encodeURIComponent(name) + "?session_id=" + $.session.get('sessionID'),
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

mainContent.on('click', '#ClosePersonaCharacteristic', function (e) {
  e.preventDefault();
  $('#menuBCClick').attr('dimension','persona_characteristic');
  refreshMenuBreadCrumb('persona_characteristic');
});

function appendGWR(tableId,gwrType,item) {
  $(tableId).find("tbody").append('<tr><td class="delete' + gwrType + '"><i class="fa fa-minus"></i></td><td class="' + gwrType + '"">'+ item.theReferenceName +'</td><td>' + item.theReferenceDescription + '</td></tr>');
};

function appendBacking(item) {
  $("#theBacking").find("tbody").append('<tr><td class="backing"">'+ item +'</td></tr>');
};

function loadCharacteristicReference() {
  $('#theArtifactTypeDiv').hide();
  refreshDimensionSelector($('#theReferenceName'),'document_reference',undefined,function() {
    $('#theArtifactType').val('document');
    var pc = JSON.parse($.session.get("PersonaCharacteristic"));
    $('#theGWRContributionCharacteristic').val($('#theCharacteristicSynopsis').val());
    var cr = $("#editCharacteristicReference").data("currentcr");
    if (cr != undefined) {
      cr = JSON.parse(cr);
      $("#theReferenceName").val(cr.name);
      $("#theDescription").val(cr.description);
      $('#theGWRSynopsis').val(cr.theSynopsis);
      $('#theGWRElementType').val(cr.theDimension);
      $('#theGWRMeansEnds').val(cr.theMeansEnd);
      $('#theGWRContribution').val(cr.theContribution);
    }
    else {
      $("#theDescription").val('');
      $('#theGWRSynopsis').val('');
      $('#theGWRElementType').val('goal');
      $('#theGWRMeansEnds').val('means');
      $('#theGWRContribution').val('Help');
    }
  });
};

function gwrItemPresent(gwrList,refName) {
  var i;
  for (i = 0; i < gwrList.length; i++) {
    if (gwrList[i].theReferenceName == refName) {
      return true;
    }
  }
  return false;
}

function addCharacteristicReference(e) {
  e.preventDefault();
  var cr = JSON.parse($("#editCharacteristicReference").data("crtype"));
  var item = jQuery.extend(true, {},characteristicReferenceDefault );
  item.theReferenceName = $("#theReferenceName").val();
  item.theReferenceDescription = $("#theDescription").val();
  item.theDimensionName = 'document';

  var pc = JSON.parse($.session.get("PersonaCharacteristic"));

  var refSyn = {};
  refSyn.theActor = pc.thePersonaName;
  refSyn.theActorType = 'persona';
  refSyn.theSynopsis = $('#theGWRSynopsis').val();
  refSyn.theDimension = $('#theGWRElementType').val();
  item.theReferenceSynopsis = refSyn;

  var refCont = {};
  refCont.theMeansEnd = $('#theGWRMeansEnds').val();
  refCont.theContribution = $('#theGWRContribution').val();
  item.theReferenceContribution = refCont;

  if (cr.tableId == '#theGrounds' && gwrItemPresent(pc.theGrounds,item.theReferenceName) == false) {
    item.theCharacteristicType = 'grounds';
    pc.theGrounds.push(item);
    appendGWR(cr.tableId,cr.classId,item); 
    $.session.set("PersonaCharacteristic", JSON.stringify(pc));
  }
  else if (cr.tableId == '#theWarrant' && gwrItemPresent(pc.theWarrant,item.theReferenceName) == false) {
    item.theCharacteristicType = 'warrant';
    pc.theWarrant.push(item);
    appendGWR(cr.tableId,cr.classId,item); 
    $.session.set("PersonaCharacteristic", JSON.stringify(pc));
  }
  else if (cr.tableId == '#theRebuttal' && gwrItemPresent(pc.theRebuttal,item.theReferenceName) == false) {
    item.theCharacteristicType = 'rebuttal';
    pc.theRebuttal.push(item);
    appendGWR(cr.tableId,cr.classId,item); 
    $.session.set("PersonaCharacteristic", JSON.stringify(pc));
  }
  $("#editCharacteristicReference").modal('hide');
}

function updateReferenceList(e) {
  e.preventDefault();
  var cr = JSON.parse($("#editCharacteristicReference").data("currentcr"));
  var item = jQuery.extend(true, {},characteristicReferenceDefault );
  item.theReferenceName = $("#theReferenceName").val();
  item.theReferenceDescription = $("#theDescription").val();
  $(cr.tableId).find("tbody").find('tr:eq(' + cr.index + ')').find('td:eq(1)').text(item.theReferenceName);
  $(cr.tableId).find("tbody").find('tr:eq(' + cr.index + ')').find('td:eq(2)').text(item.theReferenceDescription);
  item.theDimensionName = 'document';
  var pc = JSON.parse($.session.get("PersonaCharacteristic"));

  var refSyn = {};
  refSyn.theActor = pc.thePersonaName;
  refSyn.theActorType = 'persona';
  refSyn.theSynopsis = $('#theGWRSynopsis').val();
  refSyn.theDimension = $('#theGWRElementType').val();
  item.theReferenceSynopsis = refSyn;

  var refCont = {};
  refCont.theMeansEnd = $('#theGWRMeansEnds').val();
  refCont.theContribution = $('#theGWRContribution').val();
  item.theReferenceContribution = refCont;

  if (cr.tableId == '#theGrounds') {
    item.theCharacteristicType = 'grounds';
    $.each(pc.theGrounds,function(idx,g) {
      if (idx == cr.index) {
        pc.theGrounds[idx] = item;
      }
    });
  }
  else if (cr.tableId == '#theWarrant') {
    item.theCharacteristicType = 'warrant';
    $.each(pc.theWarrant,function(idx,w) {
      if (idx == cr.index) {
        pc.theWarrant[idx] = item;
      }
    });
  }
  else {
    item.theCharacteristicType = 'rebuttal';
    $.each(pc.theRebuttal,function(idx,r) {
      if (idx == cr.index) {
        pc.theRebuttal[idx] = item;
      }
    });
  }
  $.session.set("PersonaCharacteristic", JSON.stringify(pc));
  $("#editCharacteristicReference").modal('hide');
}


mainContent.on("click", "#addGrounds", function(){
  var crt = {};
  crt.tableId = "#theGrounds";
  crt.classId = 'ground'; 
  $("#editCharacteristicReference").data('loadcr',loadCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",addCharacteristicReference);
  $("#editCharacteristicReference").data("crtype",JSON.stringify(crt));
  $("#editCharacteristicReference").modal('show');
});

mainContent.on("click", "#addWarrant", function(){
  var crt = {};
  crt.tableId = "#theWarrant";
  crt.classId = 'warrant'; 
  $("#editCharacteristicReference").data('loadcr',loadCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",addCharacteristicReference);
  $("#editCharacteristicReference").data("crtype",JSON.stringify(crt));
  $("#editCharacteristicReference").modal('show');
});

mainContent.on("click", "#addRebuttal", function(){
  var crt = {};
  crt.tableId = "#theRebuttal";
  crt.classId = 'rebuttal'; 
  $("#editCharacteristicReference").data('loadcr',loadCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",addCharacteristicReference);
  $("#editCharacteristicReference").data("crtype",JSON.stringify(crt));
  $("#editCharacteristicReference").modal('show');
});

$("#editCharacteristicReference").on('shown.bs.modal', function(e) {
  e.preventDefault();
  var cmd = $("#editCharacteristicReference").data("loadcr");
  cmd(e);
});

$("#editCharacteristicReference").on('click', '#saveCharacteristicReference',function(e) {
  e.preventDefault();
  var cmd = $("#editCharacteristicReference").data("savecr");
  cmd(e);
});

mainContent.on("click",".ground", function () {
  var propRow = $(this).closest("tr");
  var pc = JSON.parse($.session.get("PersonaCharacteristic"));

  var cr = {};
  cr.index = propRow.index();
  var currentCr = pc.theGrounds[cr.index]
  cr.name = currentCr.theReferenceName
  cr.description = currentCr.theReferenceDescription;
  cr.theSynopsis = currentCr.theReferenceSynopsis.theSynopsis
  cr.theDimension = currentCr.theReferenceSynopsis.theDimension;
  cr.theMeansEnd = currentCr.theReferenceContribution.theMeansEnd;
  cr.theContribution = currentCr.theReferenceContribution.theContribution;

  cr.tableId = "#theGrounds";


  $("#editCharacteristicReference").data("currentcr",JSON.stringify(cr));
  $("#editCharacteristicReference").data('loadcr',loadCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",updateReferenceList);
  $("#editCharacteristicReference").modal('show');
});
mainContent.on("click",".warrant", function () {
  var propRow = $(this).closest("tr");
  var pc = JSON.parse($.session.get("PersonaCharacteristic"));

  var cr = {};
  cr.index = propRow.index();
  var currentCr = pc.theGrounds[cr.index]
  cr.name = currentCr.theReferenceName
  cr.description = currentCr.theReferenceDescription;
  cr.theSynopsis = currentCr.theReferenceSynopsis.theSynopsis
  cr.theDimension = currentCr.theReferenceSynopsis.theDimension;
  cr.theMeansEnd = currentCr.theReferenceContribution.theMeansEnd;
  cr.theContribution = currentCr.theReferenceContribution.theContribution;

  cr.tableId = "#theWarrant";
  $("#editCharacteristicReference").data("currentcr",JSON.stringify(cr));
  $("#editCharacteristicReference").data('loadcr',loadCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",updateReferenceList);
  $("#editCharacteristicReference").modal('show');
});
mainContent.on("click",".rebuttal", function () {
  var propRow = $(this).closest("tr");
  var pc = JSON.parse($.session.get("PersonaCharacteristic"));
  var cr = {};

  var cr = {};
  cr.index = propRow.index();
  var currentCr = pc.theGrounds[cr.index]
  cr.name = currentCr.theReferenceName
  cr.description = currentCr.theReferenceDescription;
  cr.theSynopsis = currentCr.theReferenceSynopsis.theSynopsis
  cr.theDimension = currentCr.theReferenceSynopsis.theDimension;
  cr.theMeansEnd = currentCr.theReferenceContribution.theMeansEnd;
  cr.theContribution = currentCr.theReferenceContribution.theContribution;

  cr.tableId = "#theRebuttal";
  $("#editCharacteristicReference").data("currentcr",JSON.stringify(cr));
  $("#editCharacteristicReference").data('loadcr',loadCharacteristicReference);
  $("#editCharacteristicReference").data("savecr",updateReferenceList);
  $("#editCharacteristicReference").modal('show');
});

mainContent.on('click','td.deleteground',function() {
  var gRow = $(this).closest("tr");
  var rowIdx = gRow.index();
  gRow.remove();
  var pc = JSON.parse($.session.get("PersonaCharacteristic"));
  pc.theGrounds.splice(rowIdx,1);
  $.session.set("PersonaCharacteristic", JSON.stringify(pc));
});

mainContent.on('click','td.deletewarrant',function() {
  var wRow = $(this).closest("tr");
  var rowIdx = wRow.index();
  wRow.remove();
  var pc = JSON.parse($.session.get("PersonaCharacteristic"));
  pc.theWarrant.splice(rowIdx,1);
  $.session.set("PersonaCharacteristic", JSON.stringify(pc));
});

mainContent.on('click','td.deleterebuttal',function() {
  var rRow = $(this).closest("tr");
  var rowIdx = rRow.index();
  rRow.remove();
  var pc = JSON.parse($.session.get("PersonaCharacteristic"));
  pc.theRebuttal.splice(rowIdx,1);
  $.session.set("PersonaCharacteristic", JSON.stringify(pc));
});

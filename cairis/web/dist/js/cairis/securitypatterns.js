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

$("#securityPatternsClick").click(function () {
  validateClick('template_asset',function() {
    clearLocalStorage($('#menuBCClick').attr('dimension'));
    $("#objectViewer").empty();
    $('#menuBCClick').attr('dimension','security_pattern');
    refreshMenuBreadCrumb('security_pattern');
  });
});

function createSecurityPatternsTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/security_patterns",
    success: function (data) {
      setTableHeader("SecurityPatterns");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      for (var r = 0; r < data.length; r++) {
        var item = data[r];

        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td class="deleteSecurityPatternButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';
        textToInsert[i++] = '<td class="securitypattern-rows" name="theName">';
        textToInsert[i++] = item.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      }

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
      $("#mainTable").find("tbody").removeClass();
      $("#mainTable").find("tbody").addClass('sp-rows');
      $('.sp-rows').contextMenu({
        selector: 'td',
        items: {
          "situate": {
            name: "Situate pattern",
            callback: function(key, opt) {
              var spName = $(this).closest("tr").find("td").eq(1).html();
              $('#chooseEnvironment').attr('data-spName',spName);
              refreshDimensionSelector($('#chooseEnvironmentSelect'),'environment',undefined,function() {
                $('#chooseEnvironment').attr('data-chooseDimension',"environment");
                $('#chooseEnvironment').attr('data-applyEnvironmentSelection',"situateSecurityPattern");
                $('#chooseEnvironment').modal('show');
              });
            }
          }
        }
      });

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

$(document).on('click', "td.securitypattern-rows", function () {
  var spName = $(this).closest("tr").find("td:eq(1)").text();
  refreshObjectBreadCrumb(spName);
  viewSecurityPattern(spName);
});

function viewSecurityPattern(spName) {
  activeElement("objectViewer");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/security_patterns/name/" + encodeURIComponent(spName),
    success: function (data) {
      fillOptionMenu("fastTemplates/editSecurityPatternOptions.html", "#objectViewer", null, true, true, function () {
        $("#UpdateSecurityPattern").text("Update");
        $.session.set("SecurityPattern", JSON.stringify(data));
        $("#theName").val(data.theName);
        $("#theContext").val(data.theContext);
        $("#theProblem").val(data.theProblem);
        $("#theSolution").val(data.theSolution);
        $.each(data.theRequirements,function(idx,req) {
          appendPatternRequirement(req);
        });
        $.each(data.theConcernAssociations,function(idx,ca) {
          appendPatternStructure(ca);
        });
      });
      $("#editSecurityPatternOptionsForm").validator('update');
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
};

$(document).on("click", "#addNewSecurityPattern", function () {
  refreshObjectBreadCrumb('New Security Pattern');
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editSecurityPatternOptions.html", "#objectViewer", null, true, true, function () {
    $("#editSecurityPatternOptionsForm").validator();
    $("#UpdateSecurityPattern").text("Create");
    $("#editSecurityPatternOptionsForm").addClass("new");
    $('#theName').val('');
    $('#theContext').val('');
    $('#theProblem').val('');
    $('#theSolution').val('');
    $('#theRequirements').find('tbody').empty();
    $('#theConcernAssociations').find('tbody').empty();
    $.session.set("SecurityPattern", JSON.stringify(jQuery.extend(true, {},securityPatternDefault )));
  });
});

var mainContent = $("#objectViewer");

function commitSecurityPattern() {
  var sp = JSON.parse($.session.get("SecurityPattern"));
  if ($("#editSecurityPatternOptionsForm").hasClass("new")) {
    sp.theName = $('#theName').val();
    sp.theContext = $('#theContext').val();
    sp.theProblem = $('#theProblem').val();
    sp.theSolution = $('#theSolution').val();
    postSecurityPattern(sp,function() {
      clearLocalStorage('security_pattern');
      $("#editSecurityPatternsOptionsForm").removeClass("new");
      $('#menuBCClick').attr('dimension','security_pattern');
      refreshMenuBreadCrumb('security_pattern');
    });
  }
  else {
    var oldName = sp.theName;
    sp.theName = $('#theName').val();
    sp.theContext = $('#theContext').val();
    sp.theProblem = $('#theProblem').val();
    sp.theSolution = $('#theSolution').val();
    putSecurityPattern(sp,oldName,function() {
      clearLocalStorage('security_pattern');
      $('#menuBCClick').attr('dimension','security_pattern');
      refreshMenuBreadCrumb('security_pattern');
    });
  }
}

function postSecurityPattern(sp, callback){
  var output = {};
  output.object = sp;
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
    url: serverIP + "/api/security_patterns" + "?session_id=" + $.session.get('sessionID'),
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

function putSecurityPattern(sp, oldName, callback){
  var output = {};
  output.object = sp;
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
    url: serverIP + "/api/security_patterns/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
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

$(document).on('click', 'td.deleteSecurityPatternButton', function (e) {
  e.preventDefault();
  var spName = $(this).find('i').attr("value");
  deleteObject('securitypattern',spName,function(spName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/security_patterns/name/" + encodeURIComponent(spName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        showPopup(true);
        $('#menuBCClick').attr('dimension','security_pattern');
        refreshMenuBreadCrumb('security_pattern');
      },
      error: function (xhr, textStatus, errorThrown) {
        var error = JSON.parse(xhr.responseText);
        showPopup(false, String(error.message));
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  });
});

function appendPatternStructure(pstr) {
    $("#thePatternStructure").find("tbody").append('<tr><td class="deletePatternStructure"><i class="fa fa-minus"></i></td><td class="pattern-structure">'+ pstr.theHeadAsset +'</td><td>' + pstr.theHeadAdornment + '</td><td>' + pstr.theHeadNry + '</td><td>' + pstr.theHeadRole + '</td><td>' + pstr.theTailRole + '</td><td>' + pstr.theTailNry + '</td><td>' + pstr.theTailAdornment + '</td><td>' + pstr.theTailAsset + '</td></tr>');
};

function appendPatternRequirement(preq) {
    $("#thePatternRequirements").find("tbody").append('<tr><td class="deletePatternRequirement"><i class="fa fa-minus"></i></td><td class="pattern-requirement">'+ preq.theName + '</td></tr>');
};

mainContent.on('click', '#CloseSecurityPattern', function (e) {
  e.preventDefault();
  clearLocalStorage('security_pattern');
  $("#objectViewer").empty();
  $('#menuBCClick').attr('dimension','security_pattern');
  refreshMenuBreadCrumb('security_pattern');
});

mainContent.on('click','#addPatternStructure',function() {
  $('#addPatternStructureDialog').removeAttr('data-selectedStructure');
  $('#addPatternStructureDialog').removeAttr('data-selectedIndex');
  $('#addPatternStructureDialog').modal('show');
});

mainContent.on('click','td.pattern-structure',function(){
  var strRow = $(this).closest("tr");
  var selectedStr = {};
  selectedStr.theHeadAsset = strRow.find("td:eq(1)").text();
  selectedStr.theHeadAdornment = strRow.find("td:eq(2)").text();
  selectedStr.theHeadNry = strRow.find("td:eq(3)").text();
  selectedStr.theHeadRole = strRow.find("td:eq(4)").text();
  selectedStr.theTailRole = strRow.find("td:eq(5)").text();
  selectedStr.theTailNry = strRow.find("td:eq(6)").text();
  selectedStr.theTailAdornment = strRow.find("td:eq(7)").text();
  selectedStr.theTailAsset = strRow.find("td:eq(8)").text();

  $('#addPatternStructureDialog').attr('data-selectedStructure',JSON.stringify(selectedStr));
  $('#addPatternStructureDialog').attr('data-selectedIndex',strRow.index());
  $('#addPatternStructureDialog').modal('show');
});

$(document).on('shown.bs.modal','#addPatternStructureDialog',function() {
  var selectedStr = $('#addPatternStructureDialog').attr('data-selectedStructure');
  if (selectedStr != undefined) {
    selectedStr = JSON.parse(selectedStr);
    $('#headAdorn').val(selectedStr.theHeadAdornment);
    $('#headNry').val(selectedStr.theHeadNry);
    $('#headRole').val(selectedStr.theHeadRole);
    $('#tailRole').val(selectedStr.theTailRole);
    $('#tailNry').val(selectedStr.theTailNry);
    $('#tailAdorn').val(selectedStr.theTailAdornment);
    $('#AddPatternStructure').text('Update');
  }
  else {
    $('#headAdorn').val('Association');
    $('#headNry').val('*');
    $('#headRole').val('');
    $('#tailRole').val('');
    $('#tailNry').val('*');
    $('#tailAdorn').val('Association');
    $('#AddPatternStructure').text('Add');
  }

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/template_asset",
    success: function (assets) {
      $("#headAsset option").remove();
      $("#tailAsset option").remove();
      $.each(assets,function(idx,asset) {
        $('#headAsset').append($("<option></option>").attr("value",asset).text(asset));
        $('#tailAsset').append($("<option></option>").attr("value",asset).text(asset));
      });
      if (selectedStr != undefined) {
        $('#headAsset').val(selectedStr.theHeadAsset);
        $('#tailAsset').val(selectedStr.theTailAsset);
      }
      else {
        $('#headAsset').val('');
        $('#tailAsset').val('');
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

mainContent.on('click','#AddPatternStructure',function() {
  var selectedStr = {};
  selectedStr.theHeadAsset = $('#headAsset').val();
  selectedStr.theHeadAdornment = $('#headAdorn').val();
  selectedStr.theHeadNry = $('#headNry').val();
  selectedStr.theHeadRole = $('#headRole').val();
  selectedStr.theTailRole = $('#tailRole').val();
  selectedStr.theTailNry = $('#tailNry').val();
  selectedStr.theTailAdornment = $('#tailAdorn').val();
  selectedStr.theTailAsset = $('#tailAsset').val();

  
  var sp = JSON.parse($.session.get("SecurityPattern"));
  var selectedIdx = $('#addPatternStructureDialog').attr('data-selectedIndex');
  if (selectedIdx != undefined) {
    sp.theConcernAssociations[selectedIdx] = selectedStr;
    $.session.set("SecurityPattern", JSON.stringify(sp));
    $('#thePatternStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(selectedStr.theHeadAsset);
    $('#thePatternStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(2)').text(selectedStr.theHeadAdornment);
    $('#thePatternStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(3)').text(selectedStr.theHeadNry);
    $('#thePatternStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(4)').text(selectedStr.theHeadRole);
    $('#thePatternStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(5)').text(selectedStr.theTailRole);
    $('#thePatternStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(6)').text(selectedStr.theTailNry);
    $('#thePatternStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(7)').text(selectedStr.theTailAdornment);
    $('#thePatternStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(8)').text(selectedStr.theTailAsset);
  }
  else {
    sp.theConcernAssociations.push(selectedStr);
    $.session.set("SecurityPattern", JSON.stringify(sp));
    appendPatternStructure(selectedStr);
  }
  $('#addPatternStructureDialog').modal('hide');
});

mainContent.on('click','td.deletePatternStructure',function() {
  var strRow = $(this).closest("tr");
  var rowIdx = strRow.index();
  strRow.remove();
  var sp = JSON.parse($.session.get("SecurityPattern"));
  sp.theConcernAssociations.splice(rowIdx,1);
  $.session.set("SecurityPattern", JSON.stringify(sp));
});

mainContent.on('click','#addPatternRequirement',function() {
  refreshDimensionSelector($('#thePatternRequirementAsset'),'template_asset',undefined,function() {
    $('#thePatternRequirementName').val('');
    $('#thePatternRequirementType').val('Functional');
    $('#thePatternRequirementDescription').val('');
    $('#thePatternRequirementRationale').val('');
    $('#thePatternRequirementFitCriterion').val('');
    $('#addPatternRequirementDialog').attr('data-selectedIndex',undefined);
    $('#AddPatternRequirement').text('Add');
    $('#addPatternRequirementDialog').modal('show');
  });
});

mainContent.on('click','td.pattern-requirement',function() {
  var prRow = $(this).closest("tr");
  var sp = JSON.parse($.session.get("SecurityPattern"));
  $.each(sp.theRequirements,function(idx,req) {
    if (prRow.find("td:eq(1)").text() == req.theName) {
      refreshDimensionSelector($('#thePatternRequirementAsset'),'template_asset',undefined,function() {
        $('#thePatternRequirementName').val(req.theName);
        $('#thePatternRequirementAsset').val(req.theAsset);
        $('#thePatternRequirementType').val(req.theType);
        $('#thePatternRequirementDescription').val(req.theDescription);
        $('#thePatternRequirementRationale').val(req.theRationale);
        $('#thePatternRequirementFitCriterion').val(req.theFitCriterion);
        $('#addPatternRequirementDialog').attr('data-selectedIndex',prRow.index());
        $('#AddPatternRequirement').text('Update');
        $('#addPatternRequirementDialog').modal('show');
      });
    }
  });
});

mainContent.on('click','#AddPatternRequirement',function() {
  var pr = {};
  pr.theName = $('#thePatternRequirementName').val();
  pr.theAsset = $('#thePatternRequirementAsset').val();
  pr.theType = $('#thePatternRequirementType').val();
  pr.theDescription = $('#thePatternRequirementDescription').val();
  pr.theRationale = $('#thePatternRequirementRationale').val();
  pr.theFitCriterion = $('#thePatternRequirementFitCriterion').val();

  var sp = JSON.parse($.session.get("SecurityPattern"));

  var selectedIdx = $('#addPatternRequirementDialog').attr('data-selectedIndex');
  if (selectedIdx != undefined) {
    sp.theRequirements[selectedIdx] = pr;
    $('#thePatternRequirements').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(pr.theName);
  }
  else {
    sp.theRequirements.push(pr);
    appendPatternRequirement(pr);
  }
  $.session.set("SecurityPattern", JSON.stringify(sp));
  $('#addPatternRequirementDialog').modal('hide');
});

mainContent.on('click','td.deletePatternRequirement',function() {
  var reqRow = $(this).closest("tr");
  var rowIdx = reqRow.index();
  reqRow.remove();
  var sp = JSON.parse($.session.get("SecurityPattern"));
  sp.theRequirements.splice(rowIdx,1);
  $.session.set("SecurityPattern", JSON.stringify(sp));
});

function selectSituatedPatternEnvironment() {
  refreshDimensionSelector($('#chooseEnvironmentSelect'),'environment',undefined,function() {
    $('#chooseEnvironment').attr('data-chooseDimension',"environment");
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection',"situateSecurityPattern");
    $('#chooseEnvironment').modal('show');
  });
}
function situateSecurityPattern() {
  var patternName = $("#chooseEnvironment").attr('data-spName');
  var envName = $('#chooseEnvironmentSelect').val();
  var output = {};
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
    url: serverIP + "/api/security_patterns/name/" + encodeURIComponent(patternName) + "/environment/" + encodeURIComponent(envName)  + "/situate?session_id=" + $.session.get('sessionID'),
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

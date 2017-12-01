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

$("#vulnerabilityMenuClick").click(function(){
  validateClick('vulnerability',function() {
    clearLocalStorage($('#menuBCClick').attr('dimension'));
    $("#objectViewer").empty();
    $('#menuBCClick').attr('dimension','vulnerability');
    refreshMenuBreadCrumb('vulnerability');
  });
});

function createVulnerabilityTable(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/vulnerabilities",
    success: function (data) {
      setTableHeader("Vulnerability");
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

        textToInsert[i++] = "<tr>"

        textToInsert[i++] = '<td class="deleteVulnerabilityButton"><i class="fa fa-minus" value="' + item.theVulnerabilityName + '"></i></td>';
        textToInsert[i++] = '<td class="vulnerability-rows" name="theName">';
        textToInsert[i++] = item.theVulnerabilityName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theVulnerabilityType">';
        textToInsert[i++] = item.theVulnerabilityType;
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


$(document).on('click', "td.vulnerability-rows",function(){
  var vulName = $(this).text();
  refreshObjectBreadCrumb(vulName);
  viewVulnerability(vulName);
});

function viewVulnerability(vulName) {
  activeElement("objectViewer");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/vulnerabilities/name/" + encodeURIComponent(vulName),
    success: function (newdata) {
      fillOptionMenu("fastTemplates/editVulnerabilityOptions.html", "#objectViewer", null, true, true, function () {
        refreshDimensionSelector($('#theVulnerabilityType'),'vulnerability_type',undefined,function() {
          $('#theVulnerabilityType').val(newdata.theVulnerabilityType);
        });
        $("#UpdateVulnerability").text("Update");
        $.session.set("Vulnerability", JSON.stringify(newdata));
        $.session.set("VulnerabilityName", newdata.theVulnerabilityName);
        var jsondata = $.extend(true, {}, newdata);
        jsondata.theTags = [];
        $('#editVulnerabilityOptionsform').loadJSON(jsondata, null);
        var text = "";
        $.each(newdata.theTags, function (index, tag) {
          text += tag + ", ";
        });
        $("#theTags").val(text);
        $("#editVulnerabilityOptionsform").validator('update');

        $.each(newdata.theEnvironmentProperties, function (index, envprop) {
          $("#theVulEnvironments").append("<tr class='clickable-environments'><td class='deleteVulEnv'><i class='fa fa-minus'></i></td><td class='vulEnvProperties'>" + envprop.theEnvironmentName + "</td></tr>");
        });
        $("#theVulEnvironments").find(".vulEnvProperties:first").trigger('click');
        $.session.set("VulnEnvironmentName", $("#theVulEnvironments").find(".vulEnvProperties:first").text());
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
};

$("#mainTable").on("click", "#addNewVulnerability", function () {
  refreshObjectBreadCrumb('New Vulnerability');
  activeElement("objectViewer");
  var vul = jQuery.extend(true, {}, vulnerabilityDefault);
  $.session.set("Vulnerability", JSON.stringify(vul));
  fillOptionMenu("fastTemplates/editVulnerabilityOptions.html", "#objectViewer", null, true, true, function () {
    refreshDimensionSelector($('#theVulnerabilityType'),'vulnerability_type');
    $("#editVulnerabilityOptionsform").validator();
    $("#UpdateVulnerability").text("Create");
    $("#UpdateVulnerability").addClass("newVulnerability");
    $("#vulnerabilitiestabsID").hide();
  });
});

$(document).on("click","#introduceVulnerabilityDirectoryEntry", function() {
  showDirectoryEntries('vulnerability');
});

function viewIntroducedVulnerability(dirEntry) {
  refreshObjectBreadCrumb(dirEntry.theLabel);
  activeElement("objectViewer");
  var vul = jQuery.extend(true, {}, vulnerabilityDefault);
  $.session.set("Vulnerability", JSON.stringify(vul));
  fillOptionMenu("fastTemplates/editVulnerabilityOptions.html", "#objectViewer", null, true, true, function () {
    refreshDimensionSelector($('#theVulnerabilityType'),'vulnerability_type');
    $("#UpdateVulnerability").text("Create");
    $("#UpdateVulnerability").addClass("newVulnerability");
    $("#vulnerabilitiestabsID").hide();
    $('#theVulnerabilityName').val(dirEntry.theLabel);
    $('#theVulnerabilityType').val(dirEntry.theType);
    $('#theVulnerabilityDescription').val(dirEntry.theName + ': ' + dirEntry.theDescription + "\nReference: " + dirEntry.theReference);
    $("#editVulnerabilityOptionsform").validator('update');
  });
}

var mainContent = $("#objectViewer");
mainContent.on('click', '.deleteVulEnv', function () {
  var propName = $(this).next("td").text();
  var vuln = JSON.parse($.session.get("Vulnerability"));

  $.each(vuln.theEnvironmentProperties, function (index, prop) {
    if(prop.theEnvironmentName == propName){
      vuln.theEnvironmentProperties.splice(index,1);
    }
  });
  $.session.set("Vulnerability", JSON.stringify(vuln));
  $(this).closest("tr").remove();
  var UIenv = $("#theVulEnvironments").find("tbody");
  if(jQuery(UIenv).has(".vulEnvProperties").length){
    UIenv.find(".vulEnvProperties:first").trigger('click');
  }
  else{
    $("#vulnerabilitiestabsID").hide("fast");
  }
});

mainContent.on("click", ".vulEnvProperties", function () {
  var name = $(this).text();
  $.session.set("VulnEnvironmentName", name);
  $("#vulnEnvAssets").find("tbody").empty();
  var theVul = JSON.parse($.session.get("Vulnerability"));
  $.each(theVul.theEnvironmentProperties, function (index, prop) {
    if(prop.theEnvironmentName == name){
      if(prop.theSeverity == ""){
        $("#theSeverity").val($("#theSeverity option:first").val());
      }
      else {
        $("#theSeverity").val(prop.theSeverity);
      }

      $.each(prop.theAssets, function (index, asset) {
        $("#vulnEnvAssets").find("tbody").append("<tr><td class='removeVulnEnvAsset'><i class='fa fa-minus'></i></td><td>"+ asset+"</td></tr>");
      });
    }
  })
});

mainContent.on("click", "#addAssetToEnvFromVuln", function () {
  var filterList = [];
  $(".removeVulnEnvAsset").next("td").each(function (index, tag) {
    filterList.push($(tag).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'asset',$.session.get('VulnEnvironmentName'),function(){
    $('#chooseEnvironment').attr('data-chooseDimension','asset');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addAssetToVulnerabilityEnvironment');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addAssetToVulnerabilityEnvironment() {
  var text = $("#chooseEnvironmentSelect").val();
  $("#vulnEnvAssets").find("tbody").append('<tr><td class="removeVulnEnvAsset"><i class="fa fa-minus"></i></td><td>' + text + '</td></tr>');
  var theVul = JSON.parse($.session.get("Vulnerability"));
  var EnvName = $.session.get("VulnEnvironmentName");
  $.each(theVul.theEnvironmentProperties, function (index, prop) {
    if (prop.theEnvironmentName == EnvName) {
      prop.theAssets.push(text);
    }
  });
  $.session.set("Vulnerability", JSON.stringify(theVul));
};


mainContent.on("click", ".removeVulnEnvAsset", function () {
  var name = $(this).next("td").text();
  var theVul = JSON.parse($.session.get("Vulnerability"));
  var EnvName =$.session.get("VulnEnvironmentName");
  $.each(theVul.theEnvironmentProperties, function (index, prop) {
    if(prop.theEnvironmentName == EnvName){
      $.each(prop.theAssets, function (i, key) {
        if(key == name){
          theVul.theEnvironmentProperties[index].theAssets.splice(i,1);
          $.session.set("Vulnerability", JSON.stringify(theVul));
        }
      });
    }
  });
  $(this).closest("tr").remove();
});

function commitVulnerability() {
  var theVul = JSON.parse($.session.get("Vulnerability"));
  if (theVul.theEnvironmentProperties.length == 0) {
    alert("Environments not defined");
  }
  else {
    theVul.theVulnerabilityName = $("#theVulnerabilityName").val();
    var arr = $("#theTags").val().split(", ")
    arr = $.grep(arr,function(n){ return(n) });
    theVul.TheType = arr;
    theVul.theVulnerabilityDescription = $("#theVulnerabilityDescription").val();
    theVul.theVulnerabilityType = $("#theVulnerabilityType").val();

    var name = $.session.get("VulnEnvironmentName");
    $.each(theVul.theEnvironmentProperties, function (index, key) {
      if(key.theEnvironmentName == name){
        theVul.theEnvironmentProperties[index].theSeverity= $("#theSeverity").val();
      }
    });
    if($(this).hasClass("newVulnerability")){
      postVulnerability(theVul, function () {
        clearLocalStorage('vulnerability');
        $('#menuBCClick').attr('dimension','vulnerability');
        refreshMenuBreadCrumb('vulnerability');
      });
    }
    else {
      putVulnerability(theVul, $.session.get("VulnerabilityName"), function () {
        clearLocalStorage('vulnerability');
        $('#menuBCClick').attr('dimension','vulnerability');
        refreshMenuBreadCrumb('vulnerability');
      });
    }
  }
  e.preventDefault();
}


$(document).on('click','td.deleteVulnerabilityButton', function (event) {
  event.preventDefault();
  var vulName = $(this).find('i').attr("value");
  deleteObject('vulnerability',vulName,function(vulName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/vulnerabilities/name/" + encodeURIComponent(vulName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        showPopup(true);
        $('#menuBCClick').attr('dimension','vulnerability');
        refreshMenuBreadCrumb('vulnerability');
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

mainContent.on('click', "#addVulEnv", function () {
  var filterList = [];
  $(".vulEnvProperties").each(function (index, tag) {
    filterList.push($(tag).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'environment',undefined,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','environment');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addVulnerabilityEnvironment');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addVulnerabilityEnvironment() {
  var text = $("#chooseEnvironmentSelect").val();
  $("#theVulEnvironments").find("tbody").append('<tr class="clickable-environments"><td class="deleteVulEnv"><i class="fa fa-minus"></i></td><td class="vulEnvProperties">'+text+'</td></tr>');
  var environment =  jQuery.extend(true, {},vulEnvironmentsDefault );
  environment.theEnvironmentName = text;
  var theVul = JSON.parse($.session.get("Vulnerability"));
  theVul.theEnvironmentProperties.push(environment);
  $.session.set("Vulnerability", JSON.stringify(theVul));
  $.session.set("VulnEnvironmentName",text);
  $("#vulnerabilitiestabsID").show("fast");
  $("#theVulEnvironments").find("tbody").find(".vulEnvProperties:last").trigger('click');
};

mainContent.on('click', '#CloseVulnerability', function (e) {
  e.preventDefault();
  clearLocalStorage('vulnerability');
  $("#objectViewer").empty();
  $('#menuBCClick').attr('dimension','vulnerability');
  refreshMenuBreadCrumb('vulnerability');
});

function putVulnerability(vuln, oldName, callback){
  var output = {};
  output.object = vuln;
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
    url: serverIP + "/api/vulnerabilities/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
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

function postVulnerability(vuln, callback){
  var output = {};
  output.object = vuln;
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
    url: serverIP + "/api/vulnerabilities" + "?session_id=" + $.session.get('sessionID'),
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

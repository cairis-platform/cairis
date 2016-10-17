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
   createVulnerabilityTable()
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
      window.activeTable = "Vulnerability";
      setTableHeader();
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(count, item) {
        textToInsert[i++] = "<tr>"
        textToInsert[i++] = '<td><button class="editVulnerabilityButton" value="' + item.theVulnerabilityName + '">' + 'Edit' + '</button> <button class="deleteVulnerabilityButton" value="' + item.theVulnerabilityName + '">' + 'Delete' + '</button></td>';
        textToInsert[i++] = '<td name="theVulnerabilityName">';
        textToInsert[i++] = item.theVulnerabilityName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theVulnerabilityType">';
        textToInsert[i++] = item.theVulnerabilityType;
        textToInsert[i++] = '</td>';


        textToInsert[i++] = '</tr>';
      });
      theTable.append(textToInsert.join(''));

      theTable.css("visibility","visible");
      activeElement("reqTable");
      sortTableByRow(0);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
}


$(document).on('click', "button.editVulnerabilityButton",function(){
  activeElement("objectViewer");
  if($(this).hasClass("newVulnerability")){
    var vul = jQuery.extend(true, {}, vulnerabilityDefault);
    $.session.set("Vulnerability", JSON.stringify(vul));
    fillOptionMenu("fastTemplates/editVulnerabilityOptions.html", "#objectViewer", null, true, true, function () {
      $("#UpdateVulnerability").addClass("newVulnerability");
    });
  }
  else {
    var name = $(this).attr("value");
    $.session.set("VulnerabilityName", name.trim());
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/vulnerabilities/name/" + name.replace(" ", "%20"),
      success: function (newdata) {
        fillOptionMenu("fastTemplates/editVulnerabilityOptions.html", "#objectViewer", null, true, true, function () {
          $.session.set("Vulnerability", JSON.stringify(newdata));
          var jsondata = $.extend(true, {}, newdata);
          jsondata.theTags = [];
          $('#editVulnerabilityOptionsform').loadJSON(jsondata, null);
          var text = "";
          $.each(newdata.theTags, function (index, tag) {
            text += tag + ", ";
          });
          $("#theTags").val(text);

          $.each(newdata.theEnvironmentProperties, function (index, envprop) {
            $("#theVulEnvironments").append("<tr class='clickable-environments'><td class='deleteVulEnv'><i class='fa fa-minus'></i></td><td class='vulEnvProperties'>" + envprop.theEnvironmentName + "</td></tr>");
          });
          $("#theVulEnvironments").find(".vulEnvProperties:first").trigger('click');
          $.session.set("VulnEnvironmentName", $("#theVulEnvironments").find(".vulEnvProperties:first").text());
        });
      },
      error: function (xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  }
});

$("#reqTable").on("click", "#addNewVulnerability", function () {
  activeElement("objectViewer");
  var vul = jQuery.extend(true, {}, vulnerabilityDefault);
  $.session.set("Vulnerability", JSON.stringify(vul));
  fillOptionMenu("fastTemplates/editVulnerabilityOptions.html", "#objectViewer", null, true, true, function () {
    $("#UpdateVulnerability").addClass("newVulnerability");
    $("#Properties").hide();
  });
});

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
    $("#Properties").hide("fast");
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
  if($("#theVulEnvironments").find("tbody").children().length == 0){
    alert("First you have to add an environment");
  }
  else {
    var hasAssets = [];
    $(".removeVulnEnvAsset").next("td").each(function (index, tag) {
      hasAssets.push($(tag).text());
    });
    assetsDialogBox(hasAssets, function (text) {
      $("#vulnEnvAssets").find("tbody").append('<tr><td class="removeVulnEnvAsset"><i class="fa fa-minus"></i></td><td>' + text + '</td></tr>');
      var theVul = JSON.parse($.session.get("Vulnerability"));
      var EnvName = $.session.get("VulnEnvironmentName");
      $.each(theVul.theEnvironmentProperties, function (index, prop) {
        if (prop.theEnvironmentName == EnvName) {
          prop.theAssets.push(text);
        }
      });
      debugLogger(theVul);
      $.session.set("Vulnerability", JSON.stringify(theVul));
    });
  }
});

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

mainContent.on('click', '#UpdateVulnerability', function (e) {

  $("#editVulnerabilityOptionsform").validator();

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
        createVulnerabilityTable();
      });
    }
    else {
      putVulnerability(theVul, $.session.get("VulnerabilityName"), function () {
        createVulnerabilityTable();
      });
    }
  }
  e.preventDefault();
});


$("#reqTable").on('click','.deleteVulnerabilityButton', function (event) {
  event.preventDefault();
  var name = $(this).attr("value");
  debugLogger("Delete: " + name + ".");
  deleteVulnerability( name, function () {
    createVulnerabilityTable();
  });
});

// adding an asset env to the Vulne.
mainContent.on('click', "#addVulEnv", function () {
  var hasEnv = [];
  $(".vulEnvProperties").each(function (index, tag) {
    hasEnv.push($(tag).text());
  });
  environmentDialogBox(hasEnv, function (text) {
    $("#theVulEnvironments").find("tbody").append('<tr class="clickable-environments"><td class="deleteVulEnv"><i class="fa fa-minus"></i></td><td class="vulEnvProperties">'+text+'</td></tr>');
    var environment =  jQuery.extend(true, {},vulEnvironmentsDefault );
    environment.theEnvironmentName = text;
    var theVul = JSON.parse($.session.get("Vulnerability"));
    theVul.theEnvironmentProperties.push(environment);
    $.session.set("Vulnerability", JSON.stringify(theVul));
    $.session.set("VulnEnvironmentName",text);
    $("#Properties").show("fast");
  });
});

mainContent.on('click', '#CloseVulnerability', function (e) {
  e.preventDefault();
  createVulnerabilityTable();
});


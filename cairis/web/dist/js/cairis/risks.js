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

$("#riskMenuClick").click(function () {
  validateClick('risk',function() {
    $('#menuBCClick').attr('dimension','risk');
    refreshMenuBreadCrumb('risk');
  });
});

function createRisksTable(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/risks/summary",
    success: function (data) {
      setTableHeader("Risks");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      for (var r = 0; r < data.length; r++) {
        var item = data[r];

        textToInsert[i++] = "<tr>";

        textToInsert[i++] = '<td class="deleteRiskButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';
        textToInsert[i++] = '<td class="risk-rows" name="theName">';
        textToInsert[i++] = item.theName
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theVulnerability">';
        textToInsert[i++] = item.theVulnerability;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theThreat">';
        textToInsert[i++] = item.theThreat;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      }

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
      $("#mainTable").find("tbody").removeClass();
      activeElement("mainTable");
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
}

var mainContent = $("#objectViewer");
mainContent.on('click', "#editMisusedCase", function (e) {
  e.preventDefault();
  var name = $.session.get("riskName");
  toggleRiskWindows();
  if ($("#editRisksForm").hasClass("new")) {
    var threatName = $("#theThreatNames").val();
    var vulName = $("#theVulnerabilityNames").val();
    var riskName = $("#theName").val();
    var mcName = 'Exploit ' + riskName;
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/misusecases/threat/" + encodeURIComponent(threatName) + "/vulnerability/" + encodeURIComponent(vulName),
      success: function (data) {
        data.theName = mcName;
        data.theRiskName = riskName;
        $.session.set("MisuseCase", JSON.stringify(data));
        $("#theMisuseName").val(mcName);
        $("#theMisuseRisk").val(riskName);
        $("#theMisuseEnvironments").find("tbody").empty();
        $.each(data.theEnvironmentProperties, function (idx,env) {
          appendMisuseEnvironment(env.theEnvironmentName);
        });
        $("#theMisuseEnvironments").find(".misusecaseEnvironment:first").trigger('click');
      },
      error: function (xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
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
      url: serverIP + "/api/misusecases/risk/" + name ,
      success: function (data) {
        $.session.set("MisuseCase", JSON.stringify(data));
        $("#theMisuseName").val(data.theName);
        $("#theMisuseRisk").val(data.theRiskName);
        $("#theMisuseEnvironments").find("tbody").empty();
        $.each(data.theEnvironmentProperties, function (idx,env) {
          appendMisuseEnvironment(env.theEnvironmentName);
        });
        $("#theMisuseEnvironments").find(".misusecaseEnvironment:first").trigger('click');
      },
      error: function (xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  }
});

mainContent.on('click', "#updateMisuseCase", function (e) {
  e.preventDefault();
  var risk = JSON.parse($.session.get("Risk"));
  risk.theMisuseCase = JSON.parse($.session.get("MisuseCase"));
  $.session.set("Risk",JSON.stringify(risk));
  clearMisuseCaseInfo();
  $("#theMisuseEnvironments").find("tbody").empty();
  toggleRiskWindows();
});


mainContent.on('click', "#cancelMisuseCase", function (e) {
  e.preventDefault();
  toggleRiskWindows();
});

mainContent.on("click",".misusecaseEnvironment", function () {
  clearMisuseCaseInfo();
  var misusecase = JSON.parse($.session.get("MisuseCase"));

  var theEnvName = $(this).text();
  $.session.set("misusecaseEnvironmentName", theEnvName);
  $.each(misusecase.theEnvironmentProperties, function (idx,env) {

    if (env.theEnvironmentName == theEnvName) {
      $("#theMisuseObjective").val(env.theObjective);
      $("#misuseThreat").val(misusecase.theThreatName);
      $("#misuseLikelihood").val(env.theLikelihood);
      $("#misuseVulnerability").val(misusecase.theVulnerabilityName);
      $("#misuseSeverity").val(env.theSeverity);
      $("#misuseRiskRating").val(env.theRiskRating.rating);
      $("#theMisuseNarrative").val(env.theDescription);
      $.each(env.theAssets, function (index, asset) {
        $("#assetTable tbody").append('<tr class="table-active"><td>' + asset + '</td></tr>');
      });
      $.each(env.theAttackers, function (index, attacker) {
        $("#attackerTable tbody").append('<tr class="table-active"><td>' + attacker + '</td></tr>');
      });
    }
  });
});

mainContent.on("change","#theMisuseNarrative",function() {
  var mc = JSON.parse($.session.get("MisuseCase"));
  var envName = $.session.get("misusecaseEnvironmentName");

  $.each(mc.theEnvironmentProperties, function (idx,env) {
    if (env.theEnvironmentName == envName) {
      mc.theEnvironmentProperties[idx].theDescription = $("#theMisuseNarrative").val();
      $.session.set("MisuseCase", JSON.stringify(mc));
    }
  });
});

function clearMisuseCaseInfo() {
  $("#theMisuseObjective").val("");
  $("#misuseThreat").val("");
  $("#misuseLikelihood").val("");
  $("#misuseVulnerability").val("");
  $("#misuseSeverity").val("");
  $("#misuseRiskRating").val("");
  $("#theMisuseNarrative").val("");
  $("#assetTable").find("tbody").empty();
  $("#attackerTable").find("tbody").empty();
  $("#theObjective").val("");
}

function toggleRiskWindows(){
    $("#editMisusedCaseDiv").toggle();
    $("#editRisksForm").toggle();
}

$(document).on('click', 'td.risk-rows', function () {
  activeElement("objectViewer");
  var name = $(this).text();
  refreshObjectBreadCrumb(name);
  $.session.set("riskName", name);
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/risks/name/" + encodeURIComponent(name),
    success: function (mainData) {
      $.session.set("Risk",JSON.stringify(mainData));
      fillOptionMenu("fastTemplates/editRiskOptions.html", "#objectViewer", null, true, true, function () {
        $("#UpdateRisk").text("Update");
        $("#theName").val(mainData.theName);
        $("#editRisksForm").validator('update');
        var tags = mainData.theTags;
        var text = "";
        $.each(tags, function (index, type) {
          text += type + ", ";
        });
        $("#theTags").val(text);
        var threatSelect = $("#theThreatNames");
        var vulnSelect = $("#theVulnerabilityNames");
        getThreats(function (data) {
          $.each(data, function (key, obj) {
            threatSelect.append($("<option></option>").attr("value",key).text(key));
          });
          threatSelect.val(mainData.theThreatName);
          getVulnerabilities(function (data) {
            $.each(data, function (key, obj) {
              vulnSelect.append($("<option></option>").attr("value",key).text(key));
            });
            vulnSelect.val(mainData.theVulnerabilityName);
            getRiskEnvironments();
          });
        });
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$(document).on('click','#addNewRisk', function() {
  refreshObjectBreadCrumb('New Risk');
  activeElement("objectViewer");
  $.session.set("Risk", JSON.stringify(jQuery.extend(true, {},riskDefault )));
  fillOptionMenu("fastTemplates/editRiskOptions.html", "#objectViewer", null, true, true, function () {
    $("#editRisksForm").validator();
    $("#UpdateRisk").text("Create");
    $("#editRisksForm").addClass("new");
    var threatSelect = $("#theThreatNames");
    var vulnSelect = $("#theVulnerabilityNames");
    getThreats(function (data) {
      $.each(data, function (key, obj) {
        threatSelect.append($("<option></option>").attr("value",key).text(key));
      });
      getVulnerabilities(function (data) {
        $.each(data, function (key, obj) {
          vulnSelect.append($("<option></option>").attr("value",key).text(key));
        });
        getRiskEnvironments();
      });
    });
  });
});

mainContent.on('click', '.riskEnvironment', function () {
  var env = $(this).text();
  var name = $("#theName").val();
  getRiskEnvironmentDetails(name, env);
});

mainContent.on('change', ".riskDetailsChanger", function () {
  getRiskEnvironments()
});

function getRiskEnvironments(){
  var threatName = $("#theThreatNames").val();
  var vulName = $("#theVulnerabilityNames").val();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/threat/" + threatName + "/vulnerability/"+ vulName + "/names",
    success: function (data) {
      $('#theRiskEnvironments').find('tbody').empty();
      if (data.length > 0) {
        $('#theRiskRatingDiv').show();
        $('#theRiskEnvironmentDiv').show();
        $.each(data, function (index, object) {
          appendRiskEnvironment(object);
        });
        $('#theRiskEnvironments').find('tbody').find('.riskEnvironment:first').click();
      }
      else {
        $('#theRiskRatingDiv').hide();
        $('#theRiskEnvironmentDiv').hide();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getRiskEnvironmentDetails(name, environment){
  var threatName = $("#theThreatNames").val();
  var vulName = $("#theVulnerabilityNames").val();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/risks/threat/" + threatName + "/vulnerability/"+ vulName + "/environment/" + environment,
    success: function (data) {
      $("#rating").val(data.rating);
      if (name != '') {
        $.ajax({
          type: "GET",
          dataType: "json",
          accept: "application/json",
          data: {
            session_id: String($.session.get('sessionID'))
          },
          crfossDomain: true,
          url: serverIP + "/api/risks/name/"+ name +"/threat/" + threatName + "/vulnerability/"+ vulName + "/environment/" + environment,
          success: function (data) {
            $("#theResponses").find("tbody").empty();
            if (data.length > 0) {
              $('#theRiskResponseDiv').show();
              $.each(data, function (index, object) {
                appendRiskResponse(object);
              });
            }
            else {
              $('#theRiskResponseDiv').hide();
            }
          },
          error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
          }
        });
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getThreats(callback){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/threats",
    success: function (data) {
      if(jQuery.isFunction(callback)){
        callback(data);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getVulnerabilities(callback){
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
      if(jQuery.isFunction(callback)){
        callback(data);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}
function appendRiskEnvironment(environment){
  $("#theRiskEnvironments").find("tbody").append('<tr></td><td class="riskEnvironment">'+environment+'</td></tr>');
}
function appendRiskResponse(resp){
  $("#theResponses").find("tbody").append('<tr></td><td>'+resp.responseName+'</td><td>'+ resp.unmitScore +'</td><td>'+ resp.mitScore +'</td></tr>');
}
function appendMisuseEnvironment(environment){
  $("#theMisuseEnvironments").find("tbody").append('<tr><td class="misusecaseEnvironment">'+environment+'</td></tr>');
}

function commitRisk() {
  var risk = JSON.parse($.session.get("Risk"));
  var oldName = risk.theName;
  risk.theName = $("#theName").val();
  risk.theRiskName = $("#theName").val();
  risk.theThreatName = $("#theThreatNames").val();
  risk.theVulnerabilityName = $("#theVulnerabilityNames").val();
  var tags = $("#theTags").text().split(", ");
  if(tags[0] != ""){
    risk.theTags = tags;
  }

  if($("#editRisksForm").hasClass("new")){
    postRisk(risk, function () {
      $("#editRisksForm").removeClass("new")
      $('#menuBCClick').attr('dimension','risk');
      refreshMenuBreadCrumb('risk');
    });
  }
  else {
    putRisk(risk, oldName, function () {
      $('#menuBCClick').attr('dimension','risk');
      refreshMenuBreadCrumb('risk');
    });
  }
}

mainContent.on('click', '#CloseRisk', function (e) {
  e.preventDefault();
  $('#menuBCClick').attr('dimension','risk');
  refreshMenuBreadCrumb('risk');
});
 
$(document).on('click', 'td.deleteRiskButton', function (e) {
  e.preventDefault();
  var riskName = $(this).find('i').attr("value");
  deleteObject('risk', riskName, function (riskName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/risks/name/" + encodeURIComponent(riskName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        showPopup(true);
        $('#menuBCClick').attr('dimension','risk');
        refreshMenuBreadCrumb('risk');
      }
    });
  });
});
 
$(document).on('click', 'td.deleteRiskButton', function (e) {
  e.preventDefault();
  var riskName = $(this).find('i').attr("value");
  deleteObject('risk', riskName, function (riskName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/risks/name/" + encodeURIComponent(riskName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        showPopup(true);
        $('#menuBCClick').attr('dimension','risk');
        refreshMenuBreadCrumb('risk');
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

function putRisk(risk, oldName, callback){
  var output = {};
  output.object = risk;
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
    url: serverIP + "/api/risks/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
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

function postRisk(risk, callback){
  var output = {};
  output.object = risk;
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
    url: serverIP + "/api/risks" + "?session_id=" + $.session.get('sessionID'),
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

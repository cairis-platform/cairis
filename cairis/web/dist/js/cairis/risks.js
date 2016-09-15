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

    Authors: Raf Vandelaer */

$("#risksClick").click(function () {
    createRisksTable();
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
        url: serverIP + "/api/risks",
        success: function (data) {
            window.activeTable = "Risks";
            setTableHeader();
            var theTable = $(".theTable");
            $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
            var textToInsert = [];
            var i = 0;

            $.each(data, function(key, item) {
                textToInsert[i++] = "<tr>";
                textToInsert[i++] = '<td><button class="editRiskButton" value="' + key + '">' + 'Edit' + '</button> ' +
                    '<button class="deleteRiskButton" value="' + key + '">' + 'Delete' + '</button></td>';

                textToInsert[i++] = '<td name="theName">';
                textToInsert[i++] = key;
                textToInsert[i++] = '</td>';

                textToInsert[i++] = '<td name="theVulnerability">';
                textToInsert[i++] = item.theVulnerabilityName;
                textToInsert[i++] = '</td>';

                textToInsert[i++] = '<td name="theThreat">';
                textToInsert[i++] = item.theThreatName;
                textToInsert[i++] = '</td>';

                textToInsert[i++] = '</tr>';
            });

            theTable.append(textToInsert.join(''));
            theTable.css("visibility","visible");
            activeElement("reqTable");
            sortTableByRow(1);

        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    })
}
optionsContent.on('dblclick', ".riskEnvironment", function () {

});

optionsContent.on('click', "#editMisusedCase", function (e) {
    e.preventDefault();
    var name = $.session.get("riskName");
    toggleRiskWindows();
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
            $("#theMisuseRisk").val(data.theRisk);
            $.each(data.theEnvironmentProperties, function (idx,env) {
                appendMisuseEnvironment(env.theEnvironmentName);
            });
            $("#theMisuseEnvironments").find(".misusecaseEnvironment:first").trigger('click');

        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    })
});

optionsContent.on('click', "#updateMisuseCase", function (e) {
  e.preventDefault();
  var risk = JSON.parse($.session.get("Risk"));
  risk.theMisuseCase = JSON.parse($.session.get("MisuseCase"));
  $.session.set("Risk",JSON.stringify(risk));
  clearMisuseCaseInfo();
  $("#theMisuseEnvironments").find("tbody").empty();
  toggleRiskWindows();

});

optionsContent.on("click",".misusecaseEnvironment", function () {

/*  var lastEnvName = $.session.get("misusecaseEnvironmentName");
  var misusecase = JSON.parse($.session.get("MisuseCase"));
  var updatedEnvProps = [];
  $.each(misusecase.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == lastEnvName){
      env.theDescription = $('#theMisuseNarrative').val();
    }
    updatedEnvProps.push(env);
  });
  misusecase.theEnvironmentProperties = updatedEnvProps;
  $.session.set("MisuseCase", JSON.stringify(misusecase)); 
*/
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
        $("#assetTable tbody").append("<tr><td>" + asset + "</td></tr>");
      });
      $.each(env.theAttackers, function (index, attacker) {
        $("#attackerTable tbody").append("<tr><td>" + attacker + "</td></tr>");
      });
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
  $("#misuseNarrative").val("");
  $("#assetTable").find("tbody").empty();
  $("#attackerTable").find("tbody").empty();
  $("#theObjective").val("");
}

function toggleRiskWindows(){
    $("#editMisusedCaseDiv").toggle();
    $("#editRisksForm").toggle();
}

//fillOptionMenu("fastTemplates/editAttackerOptions.html", "#optionsContent", null, true, true, function () {
$(document).on('click', '.editRiskButton', function () {
    var name = $(this).val();
    $.session.set("riskName", name);
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + "/api/risks/name/" + name.replace(" ", "%20"),
        success: function (mainData) {
            $.session.set("Risk",JSON.stringify(mainData));
            // console.log(JSON.stringify(rawData));
            fillOptionMenu("fastTemplates/editRiskOptions.html", "#optionsContent", null, true, true, function () {
                    $("#optionsHeaderGear").text("Risk properties");
                    forceOpenOptions();
                    var threatSelect = $("#theThreatNames");
                    var vulnSelect = $("#theVulnerabilityNames");
                    getThreats(function (data) {
                        $.each(data, function (key, obj) {
                            threatSelect.append($("<option></option>")
                                    .attr("value",key)
                                    .text(key));
                        });
                        threatSelect.val(mainData.theThreatName);
                    });
                    getVulnerabilities(function (data) {
                        $.each(data, function (key, obj) {
                            vulnSelect.append($("<option></option>")
                                .attr("value",key)
                                .text(key));
                        });
                        vulnSelect.val(mainData.theVulnerabilityName);
                        getRiskEnvironments();
                    });
                    $("#theName").val(mainData.theName);
                    var tags = mainData.theTags;
                    var text = "";
                    $.each(tags, function (index, type) {
                        text += type + ", ";
                    });
                    $("#theTags").val(text);
                }
            );
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });

});

optionsContent.on('click', '.riskEnvironment', function () {
    var env = $(this).text();
    var name = $("#theName").val();
    getRiskEnvironmentDetails(name, env);
});
optionsContent.on('change', ".riskDetailsChanger", function () {
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
            $.each(data, function (index, object) {
                appendRiskEnvironment(object);
            })
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
        //GET /api/risks/threat/{threat}/vulnerability/{vulnerability}/environment/{environment}
        url: serverIP + "/api/risks/threat/" + threatName + "/vulnerability/"+ vulName + "/environment/" + environment,
        success: function (data) {
            $("#rating").val(data.rating);

            $.ajax({
                type: "GET",
                dataType: "json",
                accept: "application/json",
                data: {
                    session_id: String($.session.get('sessionID'))
                },
                crfossDomain: true,
                //GET /api/risks/threat/{threat}/vulnerability/{vulnerability}/environment/{environment}
                url: serverIP + "/api/risks/name/"+ name +"/threat/" + threatName + "/vulnerability/"+ vulName + "/environment/" + environment,
                success: function (data) {
                    $("#theResponses").find("tbody").empty();
                    $.each(data, function (index, object) {
                        appendRiskResponse(object);
                    })
                },
                error: function (xhr, textStatus, errorThrown) {
                    debugLogger(String(this.url));
                    debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
                }
            });
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });
}

//TODO> to CAIRIS.js
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

optionsContent.on('click', '#UpdateRisk', function (e) {
  e.preventDefault();
  var risk = JSON.parse($.session.get("Risk"));
  var oldName = risk.theName;
  risk.theRisk = $("#theName").val();
  risk.theThreatName = $("#theThreatNames").val();
  risk.theVulnerabilityName = $("#theVulnerabilityNames").val();
  var tags = $("#theTags").text().split(", ");
  if(tags[0] != ""){
    risk.theTags = tags;
  }

  if($("#editRisksForm").hasClass("new")){
    postRisk(risk, function () {
      createRisksTable();
      $("#editRisksForm").removeClass("new")
    });
  }
  else {
    putRisk(risk, oldName, function () {
      createRisksTable();
    });
  }
});


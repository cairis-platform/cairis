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

$( document ).ajaxComplete(function() {
  $("svg > g > g .node > a ").on('click', function (event) {
    event.stopImmediatePropagation();
    event.preventDefault();
    var link = $(this).attr("xlink:href");

    if(link.indexOf("assets") > -1) {
      forceOpenOptions();
      $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
          session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + link.replace(" ", "%20"),
        success: function (data) {
        var dataArr = [];
        dataArr["#theName"] = String(data.theName);
        dataArr["#theDescription"] = String(data.theDescription);
        dataArr["#theSignificance"] = String(data.theSignificance);
        var theTableArr =[];

        $.ajax({
          type:"GET",
          dataType: "json",
          accept:"application/json",
          data: {
            session_id: String($.session.get('sessionID'))
          },
          crossDomain: true,
          url: serverIP + "/api/assets/name/"+ data.theName,
          success: function() {
            fillOptionMenu("fastTemplates/AssetOptions.html", "#optionsContent", dataArr,false,true,function(){
              $.each(data.theEnvironmentProperties, function (idx, env) {
                if (window.assetEnvironment == env.theEnvironmentName) {
                  var propValues = [];
                  for (var i = 0; i < env.theProperties.length; i++) {
                    if (env.theProperties[i].value != "None") {
                      propValues.push("<tr><td>" + env.theProperties[i].name + "</td><td>" + env.theProperties[i].value + "</td></tr>"); 
                    }
                  }
                  $("#propTable").find("tbody").append(propValues.join(' '));
                }
              });
            });
          }, 
          error: function(xhr, textStatus, errorThrown) {
            console.log(this.url);
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
          }
        });
      },
      error: function (xhr, textStatus, errorThrown) {
          console.log(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    } 
    else if(link.indexOf("personas") > -1) {

      $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
          session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + link.replace(" ", "%20"),
        success: function (data) {
          var theTableArr =[];

          $.ajax({
            type:"GET",
            dataType: "json",
            accept:"application/json",
            data: {
              session_id: String($.session.get('sessionID'))
            },
            crossDomain: true,
            url: serverIP + "/api/personas/name/"+ data.theName,
            success: function(){
              fillOptionMenu("fastTemplates/PersonaOptions.html", "#optionsContent", data,false,true,function(){
                $.session.set("Persona", JSON.stringify(data));
                $('#personasForm').loadJSON(data,null);
                forceOpenOptions();
                $.each(data.theEnvironmentProperties, function (idx, env) {
                  if (window.assetEnvironment == env.theEnvironmentName) {
                    $("#theNarrative").val(env.theNarrative);
                  }
                });

              });
            },
            error: function(xhr, textStatus, errorThrown) {
              console.log(this.url);
              debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
            }
          });
        },
        error: function (xhr, textStatus, errorThrown) {
          console.log(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    }
    else if(link.indexOf("vulnerabilities") > -1) {
      forceOpenOptions();
      $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
          session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + link.replace(" ", "%20"),
        success: function (data) {
          var theTableArr =[];

          $.ajax({
            type:"GET",
            dataType: "json",
            accept:"application/json",
            data: {
              session_id: String($.session.get('sessionID'))
            },
            crossDomain: true,
            url: serverIP + "/api/vulnerabilities/name/"+ data.theVulnerabilityName,
            success: function(){
              fillOptionMenu("fastTemplates/VulnerabilityOptions.html", "#optionsContent", data,false,true,function(){
                $.session.set("Vulnerability", JSON.stringify(data));
                $('#vulnerabilitiesForm').loadJSON(data,null);
                forceOpenOptions();
                $.each(data.theEnvironmentProperties, function (idx, env) {
                  if (window.assetEnvironment == env.theEnvironmentName) {
                    $("#theSeverity").val(env.theSeverity);
                    var assetValues = [];
                    for (var i = 0; i < env.theAssets.length; i++) {
                      assetValues.push("<tr><td>" + env.theAssets[i] + "</td></tr>"); 
                    }
                    $("#assetTable").find("tbody").append(assetValues.join(' '));
                  }
                });

              });
            },
            error: function(xhr, textStatus, errorThrown) {
              console.log(this.url);
              debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
            }
          });
        },
        error: function (xhr, textStatus, errorThrown) {
          console.log(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    }
    else if(link.indexOf("roles") > -1) {
      forceOpenOptions();
      $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
          session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + link.replace(" ", "%20"),
        success: function (data) {
          var theTableArr =[];

          $.ajax({
            type:"GET",
            dataType: "json",
            accept:"application/json",
            data: {
              session_id: String($.session.get('sessionID'))
            },
            crossDomain: true,
            url: serverIP + "/api/roles/name/"+ data.theName,
            success: function(){
              fillOptionMenu("fastTemplates/RoleOptions.html", "#optionsContent", data,false,true,function(){
                $.session.set("Role", JSON.stringify(data));
                $('#rolesForm').loadJSON(data,null);
                forceOpenOptions();
              });
            },
            error: function(xhr, textStatus, errorThrown) {
              console.log(this.url);
              debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
            }
          });
        },
        error: function (xhr, textStatus, errorThrown) {
          console.log(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    }
    else if(link.indexOf("threats") > -1) {
      forceOpenOptions();
      $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
          session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + link.replace(" ", "%20"),
        success: function (data) {
          var theTableArr =[];

          $.ajax({
            type:"GET",
            dataType: "json",
            accept:"application/json",
            data: {
              session_id: String($.session.get('sessionID'))
            },
            crossDomain: true,
            url: serverIP + "/api/threats/name/"+ data.theThreatName,
            success: function(){
              fillOptionMenu("fastTemplates/ThreatOptions.html", "#optionsContent", data,false,true,function(){
                $.session.set("Threat", JSON.stringify(data));
                $('#threatsForm').loadJSON(data,null);
                forceOpenOptions();
                $.each(data.theEnvironmentProperties, function (idx, env) {
                  if (window.assetEnvironment == env.theEnvironmentName) {
                    $("#theLikelihood").val(env.theLikelihood);
                    var dimValues = [];
                    for (var i = 0; i < env.theAssets.length; i++) {
                      dimValues.push("<tr><td>" + env.theAssets[i] + "</td></tr>"); 
                    }
                    $("#assetTable").find("tbody").append(dimValues.join(' '));
                    dimValues = [];
                    for (var i = 0; i < env.theAttackers.length; i++) {
                      dimValues.push("<tr><td>" + env.theAttackers[i] + "</td></tr>"); 
                    }
                    $("#attackerTable").find("tbody").append(dimValues.join(' '));
                    dimValues = [];
                    for (var i = 0; i < env.theProperties.length; i++) {
                      if (env.theProperties[i].value != "None") {
                        dimValues.push("<tr><td>" + env.theProperties[i].name + "</td><td>" + env.theProperties[i].value + "</td><td>" + env.theRationale[i] + "</td></tr>"); 
                      }
                    }
                    $("#propTable").find("tbody").append(dimValues.join(' '));
                  }
                });
              });
            },
            error: function(xhr, textStatus, errorThrown) {
              console.log(this.url);
              debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
            }
          });
        },
        error: function (xhr, textStatus, errorThrown) {
          console.log(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    }
    else if(link.indexOf("requirements") > -1) {
      forceOpenOptions();
      $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
          session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + link.replace(" ", "%20"),
        success: function (data) {
          var theTableArr =[];

          $.ajax({
            type:"GET",
            dataType: "json",
            accept:"application/json",
            data: {
              session_id: String($.session.get('sessionID'))
            },
            crossDomain: true,
            url: serverIP + "/api/requirements/name/"+ data.theName,
            success: function(){
              fillOptionMenu("fastTemplates/RequirementOptions.html", "#optionsContent", data,false,true,function(){
                $.session.set("Requirement", JSON.stringify(data));
                $('#requirementsForm').loadJSON(data,null);
                forceOpenOptions();
                $('#originator').val(data.attrs.originator);
                $('#rationale').val(data.attrs.rationale);
                $('#fitCriterion').val(data.attrs.fitCriterion);
                $('#type').val(data.attrs.type);
              });
            },
            error: function(xhr, textStatus, errorThrown) {
              console.log(this.url);
              debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
            }
          });
        },
        error: function (xhr, textStatus, errorThrown) {
          console.log(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    }
    else if(link.indexOf("goals") > -1) {
      forceOpenOptions();
      $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
          session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + link.replace(" ", "%20"),
        success: function (data) {
          var theTableArr =[];

          $.ajax({
            type:"GET",
            dataType: "json",
            accept:"application/json",
            data: {
              session_id: String($.session.get('sessionID'))
            },
            crossDomain: true,
            url: serverIP + "/api/goals/name/"+ data.theName,
            success: function(){
              fillOptionMenu("fastTemplates/GoalOptions.html", "#optionsContent", data,false,true,function(){
                $.session.set("Goal", JSON.stringify(data));
                $('#goalsForm').loadJSON(data,null);
                forceOpenOptions();
                $.each(data.theEnvironmentProperties, function (idx, env) {
                  if (window.assetEnvironment == env.theEnvironmentName) {
                    $("#theCategory").val(env.theCategory);
                    $("#theDefinition").val(env.theDefinition);
                    $("#theFitCriterion").val(env.theFitCriterion);
                    $("#thePriority").val(env.thePriority);
                    $("#theIssue").val(env.theIssue);
                  }
                });
              });
            },
            error: function(xhr, textStatus, errorThrown) {
              console.log(this.url);
              debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
            }
          });
        },
        error: function (xhr, textStatus, errorThrown) {
          console.log(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    }
    else if(link.indexOf("attackers") > -1) {
      forceOpenOptions();
      $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
          session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + link.replace(" ", "%20"),
        success: function (data) {
          var theTableArr =[];

          $.ajax({
            type:"GET",
            dataType: "json",
            accept:"application/json",
            data: {
              session_id: String($.session.get('sessionID'))
            },
            crossDomain: true,
            url: serverIP + "/api/attackers/name/"+ data.theName,
            success: function(){
              fillOptionMenu("fastTemplates/AttackerOptions.html", "#optionsContent", data,false,true,function(){
                $.session.set("Attacker", JSON.stringify(data));
                $('#attackersForm').loadJSON(data,null);
                forceOpenOptions();
                $.each(data.theEnvironmentProperties, function (idx, env) {
                  if (window.assetEnvironment == env.theEnvironmentName) {
                    var dimValues = [];
                    for (var i = 0; i < env.theRoles.length; i++) {
                      dimValues.push("<tr><td>" + env.theRoles[i] + "</td></tr>"); 
                    }
                    $("#rolesTable").find("tbody").append(dimValues.join(' '));
                    dimValues = [];
                    for (var i = 0; i < env.theMotives.length; i++) {
                      dimValues.push("<tr><td>" + env.theMotives[i] + "</td></tr>"); 
                    }
                    $("#motivesTable").find("tbody").append(dimValues.join(' '));
                    dimValues = [];
                    for (var i = 0; i < env.theCapabilities.length; i++) {
                      dimValues.push("<tr><td>" + env.theCapabilities[i].name + "</td><td>" + env.theCapabilities[i].value + "</td></tr>"); 
                    }
                    $("#capabilitiesTable").find("tbody").append(dimValues.join(' '));
                  }
                });
              });
            },
            error: function(xhr, textStatus, errorThrown) {
              console.log(this.url);
              debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
            }
          });
        },
        error: function (xhr, textStatus, errorThrown) {
          console.log(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    }
    else if(link.indexOf("risks") > -1) {
      forceOpenOptions();
      $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
          session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + link.replace(" ", "%20"),
        success: function (data) {
          $.ajax({
            type:"GET",
            dataType: "json",
            accept:"application/json",
            data: {
              session_id: String($.session.get('sessionID'))
            },
            crossDomain: true,
            url: serverIP + "/api/risks/name/"+ data.theName,
            success: function(){
              fillOptionMenu("fastTemplates/RiskOptions.html", "#optionsContent", data,false,true,function(){
                $.session.set("Risk", JSON.stringify(data));
                $('#risksForm').loadJSON(data,null);
                forceOpenOptions();

                var riskName = $("#theName").val();
                var threatName = $("#theThreatName").val();
                var vulName = $("#theVulnerabilityName").val();
                var envName = window.assetEnvironment;
                $.ajax({
                  type: "GET",
                  dataType: "json",
                  accept: "application/json",
                  data: {
                    session_id: String($.session.get('sessionID'))
                  },
                  crossDomain: true,
                  url: serverIP + "/api/risks/threat/" + threatName + "/vulnerability/"+ vulName + "/environment/" + envName,
                  success: function (data) {
                    $("#theRating").val(data.rating);
                    $.ajax({
                      type: "GET",
                      dataType: "json",
                      accept: "application/json",
                      data: {
                        session_id: String($.session.get('sessionID'))
                      },
                      crossDomain: true,
                      url: serverIP + "/api/risks/name/"+ riskName +"/threat/" + threatName + "/vulnerability/"+ vulName + "/environment/" + envName,
                      success: function (data) {
                        $("#theResponses").find("tbody").empty();
                        $.each(data, function (index, resp) {
                          $("#theResponses").find("tbody").append('<tr></td><td>'+resp.responseName+'</td><td>'+ resp.unmitScore +'</td><td>'+ resp.mitScore +'</td></tr>');
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
              });
            },
            error: function(xhr, textStatus, errorThrown) {
              console.log(this.url);
              debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
            }
          });
        },
        error: function (xhr, textStatus, errorThrown) {
          console.log(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    }
  });
});

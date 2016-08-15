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
    
    if (self.theVisualModel == 'asset') {
      window.assetEnvironment = $('#environmentsbox').val();
    }
    else if (self.theVisualModel == 'goal') {
      window.assetEnvironment = $('#gmenvironmentsbox').val();
    }
    else if (self.theVisualModel == 'obstacle') {
      window.assetEnvironment = $('#omenvironmentsbox').val();
    }

    else if (self.theVisualModel == 'risk') {
      window.assetEnvironment = $('#rmenvironmentsbox').val();
    }

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
              $("#optionsHeaderGear").text("Asset properties");
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
                $("#optionsHeaderGear").text("Persona properties");
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
                $("#optionsHeaderGear").text("Vulnerability properties");
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
                $("#optionsHeaderGear").text("Role properties");
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
                $("#optionsHeaderGear").text("Threat properties");
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
                $("#optionsHeaderGear").text("Requirement properties");
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
                $("#optionsHeaderGear").text("Goal properties");
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
                $("#optionsHeaderGear").text("Attacker properties");
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
                $("#optionsHeaderGear").text("Risk properties");
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
    else if(link.indexOf("tasks") > -1) {
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
            url: serverIP + "/api/tasks/name/"+ data.theName,
            success: function(){
              fillOptionMenu("fastTemplates/TaskOptions.html", "#optionsContent", data,false,true,function(){
                $.session.set("Task", JSON.stringify(data));
                $('#tasksForm').loadJSON(data,null);
                $("#optionsHeaderGear").text("Task properties");
                forceOpenOptions();
                $.each(data.theEnvironmentProperties, function (idx, env) {
                  if (window.assetEnvironment == env.theEnvironmentName) {
                    $("#theDependencies").val(env.theDependencies);
                    $("#theNarrative").val(env.theNarrative);
                    var dimValues = [];
                    for (var i = 0; i < env.theAssets.length; i++) {
                      dimValues.push("<tr><td>" + env.theAssets[i] + "</td></tr>"); 
                    }
                    $("#theAssets").find("tbody").append(dimValues.join(' '));
                    dimValues = [];
                    for (var i = 0; i < env.thePersonas.length; i++) {
                      var pCol = [];
                      $.each(env.thePersonas[i], function(idx,val) { pCol.push(val); });
                      dimValues.push("<tr><td>" + pCol[0][0] + "</td><td>" + pCol[0][1] + "</td><td>" + pCol[0][2] + "</td><td>" + pCol[0][3] + "</td><td>" + pCol[0][4] + "</td></tr>"); 
                    }
                    $("#thePersonas").find("tbody").append(dimValues.join(' '));
                    // Usability score
                    // Task Load
                    // Countermeasure Load
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
    else if(link.indexOf("responses") > -1) {
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
            url: serverIP + "/api/responses/name/"+ data.theName,
            success: function(){
              if (data.theResponseType == 'Accept') {
                fillOptionMenu("fastTemplates/AcceptOptions.html", "#optionsContent", data,false,true,function(){
                  $.session.set("Response", JSON.stringify(data));
                  $('#acceptForm').loadJSON(data,null);
                  $("#optionsHeaderGear").text("Accept Response properties");
                  forceOpenOptions();
                  $.each(data.theEnvironmentProperties, function (idx, env) {
                    if (window.assetEnvironment == env[0].theEnvironmentName) {
                      $('#theCost').val(env[0].theCost);
                      $('#theRationale').val(env[0].theRationale);
                    } 
                  });
                }); 
              }
              else if (data.theResponseType == 'Transfer') {
                fillOptionMenu("fastTemplates/TransferOptions.html", "#optionsContent", data,false,true,function(){
                  $.session.set("Response", JSON.stringify(data));
                  $('#transferForm').loadJSON(data,null);
                  $("#optionsHeaderGear").text("Transfer Response properties");
                  forceOpenOptions();
                  $.each(data.theEnvironmentProperties, function (idx, env) {
                    if (window.assetEnvironment == env[0].theEnvironmentName) {
                      var dimValues = [];
                      for (var i = 0; i < env[0].theRoles.length; i++) {
                        dimValues.push("<tr><td>" + env[0].theRoles[i].roleName + "</td><td>" + env[0].theRoles[i].cost + "</td></tr>"); 
                      }
                      $("#rolesTable").find("tbody").append(dimValues.join(' '));
                      $('#theRationale').val(env[0].theRationale);
                    } 
                  });
                }); 
              }
              else if (data.theResponseType == 'Prevent') {
                fillOptionMenu("fastTemplates/PreventOptions.html", "#optionsContent", data,false,true,function(){
                  $.session.set("Response", JSON.stringify(data));
                  $('#preventForm').loadJSON(data,null);
                  $("#optionsHeaderGear").text("Prevent Response properties");
                  forceOpenOptions();
                }); 
              }
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
    else if(link.indexOf("misusecases") > -1) {
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
            url: serverIP + "/api/misusecases/name/"+ data.theName,
            success: function(){
              fillOptionMenu("fastTemplates/MisuseCaseOptions.html", "#optionsContent", data,false,true,function(){
                $.session.set("MisuseCase", JSON.stringify(data));
                $('#misuseCaseForm').loadJSON(data,null);
                $("#optionsHeaderGear").text("Misuse Case properties");
                forceOpenOptions();
                $.each(data.theEnvironmentDictionary, function (idx, env) {
                  if (window.assetEnvironment == env.theEnvironmentName) {
                    $('#theDescription').val(env.theDescription);
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
else if(link.indexOf("obstacles") > -1) {
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
            url: serverIP + "/api/obstacles/name/"+ data.theName,
            success: function(){
              fillOptionMenu("fastTemplates/ObstacleOptions.html", "#optionsContent", data,false,true,function(){
                $.session.set("Obstacle", JSON.stringify(data));
                $('#obstaclesForm').loadJSON(data,null);
                $("#optionsHeaderGear").text("Obstacle properties");
                forceOpenOptions();
                $.each(data.theEnvironmentProperties, function (idx, env) {
                  if (window.assetEnvironment == env.theEnvironmentName) {
                    $('#theCategory').val(env.theCategory);
                    $('#theDefinition').val(env.theDefinition);
                    $('#theProbability').val(env.theProbabilty);
                    $('#theProbabilityRationale').val(env.theProbabiltyRationale);
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
    else if(link.indexOf("countermeasures") > -1) {
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
            url: serverIP + "/api/countermeasures/name/"+ data.theName,
            success: function(){
              fillOptionMenu("fastTemplates/CountermeasureOptions.html", "#optionsContent", data,false,true,function(){
                $.session.set("Countermeasure", JSON.stringify(data));
                $('#countermeasuresForm').loadJSON(data,null);
                $("#optionsHeaderGear").text("Countermeasure properties");
                forceOpenOptions();
                $.each(data.theEnvironmentProperties, function (idx, env) {
                  if (window.assetEnvironment == env.theEnvironmentName) {
                     $('#theCost').val(env.theCost)
                     var dimValues = [];
                     for (var i = 0; i < env.theRoles.length; i++) {
                       dimValues.push("<tr><td>" + env.theRoles[i] + "</td></tr>"); 
                     }
                     $("#theRoles").find("tbody").append(dimValues.join(' '));
                     dimValues = [];
                     for (var i = 0; i < env.theTargets.length; i++) {
                       dimValues.push("<tr><td>" + env.theTargets[i].theName + "</td><td>" + env.theTargets[i].theEffectiveness + "</td><td>" + env.theTargets[i].theRationale + "</td></tr>"); 
                     }
                     $("#theTargets").find("tbody").append(dimValues.join(' '));
                     dimValues = [];
                     for (var i = 0; i < env.theRequirements.length; i++) {
                       dimValues.push("<tr><td>" + env.theRequirements[i] + "</td></tr>"); 
                     }
                     $("#theRequirements").find("tbody").append(dimValues.join(' '));
                     dimValues = [];
                     for (var i = 0; i < env.theProperties.length; i++) {
                       if (env.theProperties[i].value != "None") {
                          dimValues.push("<tr><td>" + env.theProperties[i].name + "</td><td>" + env.theProperties[i].value + "</td></tr>"); 
                       }
                     }
                     $("#theProperties").find("tbody").append(dimValues.join(' '));
                     dimValues = [];
                     for (var i = 0; i < env.thePersonas.length; i++) {
                       var pCol = [];
                       $.each(env.thePersonas[i], function(idx,val) { pCol.push(val); });
                       dimValues.push("<tr><td>" + pCol[0][0] + "</td><td>" + pCol[0][1] + "</td><td>" + pCol[0][2] + "</td><td>" + pCol[0][3] + "</td><td>" + pCol[0][4] + "</td><td>" + pCol[0][5] + "</td></tr>"); 
                     }
                     $("#thePersonas").find("tbody").append(dimValues.join(' '));
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
    else if(link.indexOf("domainproperties") > -1) {
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
            url: serverIP + "/api/domainproperties/name/"+ data.theName,
            success: function(){
              fillOptionMenu("fastTemplates/DomainPropertyOptions.html", "#optionsContent", data,false,true,function(){
                $.session.set("DomainProperty", JSON.stringify(data));
                $('#domainpropertiesForm').loadJSON(data,null);
                $("#optionsHeaderGear").text("Domain Property properties");
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
  });
});

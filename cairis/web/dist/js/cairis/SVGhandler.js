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
 
  });
});

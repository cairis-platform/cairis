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

$("#FindButton").click(function(e){
  e.preventDefault();
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editSearchOptions.html","#objectViewer",null,true,true, function(){
    var searchString = $("#theSearchString").val();

    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/find/" + searchString.replace(" ", "%20"),
      success: function (data) {
        $("#theResults").find("tbody").empty();
        $.each(data, function(idx,searchRes) {
          appendResults(searchRes);
        });
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

function appendResults(searchResults){
  $("#theResults").append('<tr class="' + searchResults[1].replace(" ","").toLowerCase() + '-rows"><td>' + searchResults[0] +'</td><td>' + searchResults[1] + '</td><td>' + searchResults[2] + '</td></tr>');
}

$(document).on('click', "tr.domainproperty-rows", function () {
  var dpName = $(this).find('td:eq(2)').text();
  viewDomainProperty(dpName);
});

$(document).on('click', "tr.goal-rows", function () {
  var goalName = $(this).find('td:eq(2)').text();
  viewGoal(goalName);
});

$(document).on('click', "tr.obstacle-rows", function () {
  var obsName = $(this).find('td:eq(2)').text();
  viewObstacle(obsName);
});

$(document).on('click', "tr.persona-rows", function () {
  var personaName = $(this).find('td:eq(2)').text();
  viewPersona(personaName);
});

$(document).on('click', "tr.task-rows", function () {
  var taskName = $(this).find('td:eq(2)').text();
  viewTask(taskName);
});

$(document).on('click', "tr.role-rows", function () {
  var roleName = $(this).find('td:eq(2)').text();
  viewRole(roleName);
});

$(document).on('click', "tr.response-rows", function () {
  var respName = $(this).find('td:eq(2)').text();
  viewResponse(respName);
});

$(document).on('click', "tr.threat-rows", function () {
  var thrName = $(this).find('td:eq(2)').text();
  viewThreat(thrName);
});

$(document).on('click', "tr.vulnerability-rows", function () {
  var vulName = $(this).find('td:eq(2)').text();
  viewVulnerability(vulName);
});

$(document).on('click', "tr.attacker-rows", function () {
  var attackerName = $(this).find('td:eq(2)').text();
  viewAttacker(attackerName);
});

$(document).on('click', "tr.role-rows", function () {
  var roleName = $(this).find('td:eq(2)').text();
  viewRole(roleName);
});

$(document).on('click', "tr.asset-rows", function () {
  var assetName = $(this).find('td:eq(2)').text();
  viewAsset(assetName);
});

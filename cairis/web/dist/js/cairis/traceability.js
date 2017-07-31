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

$("#traceabilityClick").click(function(){
  validateClick('traceability',function() {
    refreshMenuBreadCrumb('traceability');
    activeElement("objectViewer");
    $('#filtercontent').hide();
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/dimensions/table/environment",
      success: function (envs) {
        fillOptionMenu("fastTemplates/editTraceabilityOptions.html", "#objectViewer", null, true, true, function () {
          refreshDimensionSelector($('#theTraceabilityEnvironmentName'),'environment',undefined,function() {
            $('#theTraceabilityEnvironmentName').val(envs[0]);
            $('#theTraceabilityEnvironmentName').trigger('change');
          },['All']);
        });
      },
      error: function (xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  });
});

var mainContent = $('#objectViewer');
mainContent.on("change",'#theTraceabilityEnvironmentName',function() {
  var envName = $('#theTraceabilityEnvironmentName').val();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/traces/environment/" + encodeURIComponent(envName),
    success: function (trs) {
      $('#theTraces').find('tbody').empty();
      $.each(trs, function(idx,t) {
        appendTrace(t);
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
});

function appendTrace(t) {
    $("#theTraces").find("tbody").append('<tr><td class="deleteTrace"><i class="fa fa-minus"></i></td><td class="trace-rows">'+ t.theFromObject + '</td><td>' + t.theFromName + '</td><td>' + t.theToObject + '</td><td>' + t.theToName +'</td></tr>');
};

mainContent.on('click','td.deleteTrace',function() {
  var tRow = $(this).closest("tr");
  var fromObjt = tRow.find("td:eq(1)").text();
  var fromName = tRow.find("td:eq(2)").text();
  var toObjt = tRow.find("td:eq(3)").text();
  var toName = tRow.find("td:eq(4)").text();

  $.ajax({
    type: "DELETE",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    url: serverIP + "/api/traces/from_type/" + encodeURIComponent(fromObjt) + "/from_name/" + encodeURIComponent(fromName) + "/to_type/" + encodeURIComponent(toObjt) + "/to_name/" + encodeURIComponent(toName) + "?session_id=" + $.session.get('sessionID'),
    success: function (data) {
      tRow.remove();
      showPopup(true);
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

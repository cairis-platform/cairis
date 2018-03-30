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

$('#validateModelClick').click(function(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/all/names",
    success: function (data) {
      $("#chooseEnvironmentSelect").empty();
      $.each(data, function(i, item) {
        $("#chooseEnvironmentSelect").append('<option value="' + item + '">'  + item + '</option>');
      });
      $('#chooseEnvironment').attr('data-chooseDimension',"environment");
      $('#chooseEnvironment').attr('data-applyEnvironmentSelection',"validateModel");
      $('#chooseEnvironment').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
});


function validateModel() {
  var envName = $('#chooseEnvironment').attr('data-chosenDimension');

  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/validationResults.html","#objectViewer",null,true,true, function(){

    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/validation/environment/" + encodeURIComponent(envName),
      success: function (data) {
        $("#theValidationResults").find("tbody").empty();
        $.each(data, function(idx,vr) {
          appendResults(vr);
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
}

function appendResults(vr){
  $("#theValidationResults").append('<tr class="mv-rows"><td>' + vr.theLabel +'</td><td>' + vr.theMessage + '</td></tr>');
}

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

$("#exportClick").click(function () {
  var exportUrl =  serverIP + "/api/export/file?filename=model.xml"; 
  showLoading();
  $.ajax({
    type: "GET",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: exportUrl,
    success: function (data) {
      window.location.assign(exportUrl);
      showPopup(true);
    },
    complete: function() {
      hideLoading();
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$("#exportArchitecturalPatternClick").click(function () {
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/component_view",
    success: function (data) {
      $("#chooseArchitecturalPatternSelect").empty();
      $.each(data, function(i, item) {
        $("#chooseArchitecturalPatternSelect").append('<option value="' + item + '">'  + item + '</option>');
      });
      $('#chooseArchitecturalPattern').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$("#chooseArchitecturalPattern").on('click', '#chooseArchitecturalPatternButton',function(e) {
  var apName = $('#chooseArchitecturalPatternSelect').val();
  $('#chooseArchitecturalPattern').modal('hide');
  var exportUrl = serverIP + "/api/export/file/architectural_pattern/" + encodeURIComponent(apName);
  $.ajax({
    type: "GET",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: exportUrl,
    success: function (data) {
      window.location.assign(exportUrl);
      showPopup(true);
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
    }
  });
});

$("#exportGRLClick").click(function () {
  refreshDimensionSelector($('#theGRLExportEnvironment'),'environment',undefined,function() {
    var initEnvName = $('#theGRLExportEnvironment').val();
    refreshDimensionSelector($('#theGRLExportTask'),'task',initEnvName,function() {
      refreshDimensionSelector($('#theGRLExportPersona'),'persona',initEnvName,function() {
        $('#chooseGRLExportParameters').modal('show');
      });
    },['All']);
  });
});

$('#chooseGRLExportParameters').on('change','#theGRLExportEnvironment',function() {
  var envName = $('#theGRLExportEnvironment').val();
  refreshDimensionSelector($('#theGRLExportTask'),'task',envName,function() {
    refreshDimensionSelector($('#theGRLExportPersona'),'persona',envName);
  },['All']);
});

$("#chooseGRLExportParameters").on('click', '#grlExportButton',function(e) {
  var taskName = $('#theGRLExportTask').val();
  var personaName = $('#theGRLExportPersona').val();
  var envName = $('#theGRLExportEnvironment').val();
  $('#chooseGRLExportParameters').modal('hide');
  var exportUrl = serverIP + "/api/export/file/grl/task/" + encodeURIComponent(taskName) + "/persona/" + encodeURIComponent(personaName) + "/environment/" + encodeURIComponent(envName);
  $.ajax({
    type: "GET",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: exportUrl,
    success: function (data) {
      window.location.assign(exportUrl);
      showPopup(true);
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
    }
  });
});

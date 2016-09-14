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

$("#genDocClick").click(function () {
  fillOptionMenu("fastTemplates/editGenDocOptions.html", "#optionsContent", null, true, true, function () {
    $("#optionsHeaderGear").text("Generate Documentation");
    forceOpenOptions();
  });
});

var optionsContent = $("#optionsContent");
optionsContent.on('change',"#theDocumentType",function(){
  var docType = $(this).find('option:selected').text();
  if (docType == 'Requirements') {
    $("#requirementsSection").addClass('show');
    $("#requirementsSection").removeClass('hidden');
    $("#personasSection").addClass('hidden');
    $("#personasSection").removeClass('show');
  }
  else {
    $("#personasSection").addClass('show');
    $("#personasSection").removeClass('hidden');
    $("#requirementsSection").addClass('hidden');
    $("#requirementsSection").removeClass('show');
  }
}); 

optionsContent.on('click',"#GenerateDocumentation", function (e) {
  e.preventDefault();
  var json = {}; 
  var docType = $("#theDocumentType").val();
  json['theDocumentType'] = docType;

  var outputType = $("#theOutputType").val();
  if (outputType == 'PDF') {
    json['theTypeFlags'] = [0,0,1];
  }
  else {
    json['theTypeFlags'] = [0,1,0];

  }
  if (docType == 'Requirements') {
    json['theSectionFlags'] = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1];
  }
  else {
    json['theSectionFlags'] = [1,1,1,1,1];
  }

  var object = {};
  object.object = json;
  object.session_id = $.session.get('sessionID');
  var objectoutput = JSON.stringify(object);

  var genDocUrl = serverIP + "/api/documentation" + "?session_id=" + $.session.get('sessionID');
  $.ajax({
    type: "POST",
    dataType: "json",
    accept: "application/octet-stream",
    processData:false,
    contentType:"application/json",
    data: objectoutput,
    crossDomain: true,
    url: genDocUrl,
    success: function (data) {
      window.location = genDocUrl;
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


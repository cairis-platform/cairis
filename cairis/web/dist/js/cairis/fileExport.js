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

$("#exportClick").click(function () {
  fileExportDialogbox(function (type) {
    $.session.set("fileType", type);
  }) 
});
$(document).on('change','#exportFile', function () {
  var fileTag = $(document).find('#exportFile');
  var fd = new FormData();
  fd.append("file", fileTag[0].files[0]);
  var fileType = $.session.get("fileType");

  $.ajax({
    type: "GET",
    dataType: "json", 
    accept: "application/json",
    data: { session_id : String($.session.get('sessionID'))},
    crossDomain: true,
    url: serverIP + "/api/export/text?session_id="+  String($.session.get('sessionID')),
    success: function (data) {
      var exportFile = new File(fileType);
      exportFile.writeln(data.theModel);
      exportFile.open("w");
      exportFile.write(data.theModel);
      exportFile.close();
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



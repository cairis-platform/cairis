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

$("#importClick").click(function () {
  fileDialogbox(function (type) {
    var fileType = $("#theImportModelType").val();
    var object = {};
    var json = {'urlenc_file_contents' : $.session.get('importModelContent'),'type': fileType};
    object.object = json;
    object.session_id = $.session.get('sessionID');
    var objectoutput = JSON.stringify(object);

    $.ajax({
      type: "POST",
      dataType: "json",
      contentType:"application/json",
      accept: "application/json",
      crossDomain: true,
      processData:false,
      origin: serverIP,
      data: objectoutput,
      url: serverIP + "/api/import/text",
      success: function (data) {
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
});

function fileDialogbox(callback){
  var dialogwindow = $("#typeOfFile");
  var select = dialogwindow.find("select");
  dialogwindow.dialog({
    modal: true,
    buttons: {
      Ok: function () {
        var text =  select.find("option:selected" ).text();
        if(jQuery.isFunction(callback)){
          callback(text);
          $("#importClick").trigger('click')
        }
        $(this).dialog("close");
      }
    }
  });
  $(".comboboxD").css("visibility", "visible");
}

var readImportFile = function(event) {
  var input = event.target;

  var reader = new FileReader();
  reader.onload = function(){
    var text = reader.result;
    $.session.set('importModelContent',text);
  };
  reader.readAsText(input.files[0]);
};


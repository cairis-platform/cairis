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

window.serverIP = "http://"+ window.location.host;

window.debug = true;

function debugLogger(info){
  if(debug){
    console.log(info);
  }
}


$(window).load(function() {

  var sessionID = $.session.get('sessionID');
  if(!sessionID){
    $.ajax({
      type: 'POST',
      url: serverIP + '/make_session',
      data: {},
      accept:"application/json",
      contentType : "application/json",
      success: function(data, status, xhr) {
        debugLogger(data);
        var sessionID = data.session_id;
        $.session.set("sessionID", sessionID);
      },
      error: function(data, status, xhr) {
        console.log(this.url);
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + status + ", thrown: " + data);
        alert("There is a problem with the server...");
      }
    });
  }

  window.document.title = Cookies.get('wTitle');
  var modelUrl;
  if (Cookies.get('model') == 'component_asset') {
    modelUrl = serverIP + "/api/architectural_patterns/component/asset/model/" + encodeURIComponent(Cookies.get('parameter'));
  }
  else {
    modelUrl = serverIP + "/api/architectural_patterns/component/goal/model/" + encodeURIComponent(Cookies.get('parameter'));
  }

  $.ajax({
    type: "GET",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: modelUrl,
    success: function (data) {
      fillSvgViewer(data);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

function fillSvgViewer(data){
  var xmlString = (new XMLSerializer()).serializeToString(data);
  var svgDiv = $("#svgViewer");
  svgDiv.show();
  svgDiv.css("height",$("#mainContent").height());
  svgDiv.css("width","100%");
  svgDiv.html(xmlString);
  $("svg").attr("id","svg-id");
  var panZoomInstance = svgPanZoom('#svg-id', {
    zoomEnabled: true,
    controlIconsEnabled: true,
    fit: true,
    center: true,
    minZoom: 0.2
  });
}

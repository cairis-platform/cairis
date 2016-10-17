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
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  });
});

function appendResults(searchResults){
  $("#theResults").append("<tr><td>" + searchResults[0] +"</td><td>" + searchResults[1] + "</td><td>" + searchResults[2] + "</td></tr>");
}


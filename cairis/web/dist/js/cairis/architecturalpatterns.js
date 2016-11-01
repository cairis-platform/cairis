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

$("#architecturalPatternsClick").click(function () {
  createArchitecturalPatternsTable();
});

function createArchitecturalPatternsTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/architectural_patterns",
    success: function (data) {
      window.activeTable = "ArchitecturalPatterns";
      setTableHeader();
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td><button class="editArchitecturalPatternButton" value="' + item.theName + '">' + 'Edit' + '</button> <button class="deleteArchitecturalPatternButton" value="' + item.theName + '">' + 'Delete' + '</button></td>';

        textToInsert[i++] = '<td name="theName">';
        textToInsert[i++] = item.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theInterfacesDER">';
        textToInsert[i++] = item.theAttackSurfaceMetric[0];
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theChannelsDER">';
        textToInsert[i++] = item.theAttackSurfaceMetric[1];
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theUntrustedSurfaceDER">';
        textToInsert[i++] = item.theAttackSurfaceMetric[2];
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      });

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
      $("#reqTable").find("tbody").removeClass();

      activeElement("reqTable");
      sortTableByRow(0);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
}

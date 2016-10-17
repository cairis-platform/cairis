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

$("#roleMenuClick").click(function () {
  fillRolesTable();
});

function fillRolesTable(){
  window.activeTable = "Roles";
  setTableHeader();
  activeElement("reqTable");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/roles",
    success: function (json) {
      $.session.set("allRoles", JSON.stringify(json));
      var i = 0;
      var textToInsert = [];
      $.each(json, function (key, value) {
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td><button class="editRoleButton" value="' + key + '">' + 'Edit' + '</button> <button class="deleteRoleButton" value="' + key + '">' + 'Delete' + '</button></td>';
        textToInsert[i++] = '<td name="theName">';
        textToInsert[i++] = value.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theShortCode">';
        textToInsert[i++] = value.theShortCode;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theType">';
        textToInsert[i++] = value.theType;
        textToInsert[i++] = '</td>';
        textToInsert[i++] = '</tr>';
      });
      $("#reqTable").append(textToInsert.join(''));
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
  sortTableByRow(1);
}

$(document).on('click', "button.editRoleButton",function() {
  activeElement("objectViewer");
  var name = $(this).val();
  if(name == undefined || name == "") {
    fillOptionMenu("fastTemplates/editRoleOptions.html", "#objectViewer", null, true, true, function () {
      $("#editRoleOptionsform").addClass("newRole");
    });
  } 
  else {
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/roles/name/" + name.replace(" ", "%20"),
      success: function (json) {
        fillOptionMenu("fastTemplates/editRoleOptions.html", "#objectViewer", null, true, true, function () {
          var form = $('#editRoleOptionsform');
          form.loadJSON(json, null);
          $.session.set("RoleObject", JSON.stringify(json));
          $.ajax({
            type: "GET",
            dataType: "json",
            accept: "application/json",
            data: {
              session_id: String($.session.get('sessionID'))
            },
            crossDomain: true,
            url: serverIP + "/api/roles/name/" + name.replace(" ", "%20") + "/properties",
            success: function (json) {
              $.each(json, function (index, value) {
                $("#theEnvironments").find("tbody").append("<tr><td class='roleEnvironmentClick'>" + value.theEnvironmentName + "</td></tr>");
              });
              $.session.set("RoleEnvironments", JSON.stringify(json))
            },
            error: function (xhr, textStatus, errorThrown) {
              var error = JSON.parse(xhr.responseText);
              showPopup(false, String(error.message));
              debugLogger(String(this.url));
              debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
            }
          });
        });
      },
      error: function (xhr, textStatus, errorThrown) {
        var error = JSON.parse(xhr.responseText);
        showPopup(false, String(error.message));
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  }
});

var mainContent = $("#objectViewer");
mainContent.on('click','#UpdateRole', function (event) {
  event.preventDefault();

  if ($("#editRoleOptionsform").hasClass("newRole")) {
    var theRoleObject = jQuery.extend(true, {},roleDefaultObject );
    theRoleObject.theName = mainContent.find("#theName").val();
    theRoleObject.theShortCode = mainContent.find("#theShortCode").val();
    theRoleObject.theDescription = mainContent.find("#theDescription").val();
    theRoleObject.theType = mainContent.find("#theType option:selected").text().trim();
    if (theRoleObject.theName == "" || theRoleObject.theShortCode == "" || theRoleObject.theDescription == "" || theRoleObject.theType == "") {
      alert("The Name, Shortcode, Description and Type must have a value");
    }
    else {
      postRole(theRoleObject, function () {
        fillRolesTable();
      });
    }
  } 
  else {
    var theRoleObject = JSON.parse($.session.get("RoleObject"));
    var oldname = theRoleObject.theName;
    theRoleObject.theName = mainContent.find("#theName").val();
    theRoleObject.theShortCode = mainContent.find("#theShortCode").val();
    theRoleObject.theDescription = mainContent.find("#theDescription").val();
    theRoleObject.theType = mainContent.find("#theType option:selected").text().trim();
    if (theRoleObject.theName == "" || theRoleObject.theShortCode == "" || theRoleObject.theDescription == "" || theRoleObject.theType == "") {
      alert("The Name, Shortcode, Description and Type must have a value");
    }
    else {
      updateRole(theRoleObject, oldname, function () {
        fillRolesTable();
      });
    }
  }
});

$("#reqTable").on('click','.deleteRoleButton', function (event) {
  event.preventDefault();
  var name = $(this).attr("value");
  debugLogger("Delete: " + name + ".");
  deleteRole( name, function () {
    fillRolesTable();
  });
});

mainContent.on("click", '.roleEnvironmentClick', function () {
  $("#theCounterMeasures").find('tbody').empty();
  $("#theResponses").find('tbody').empty();
  var text =  $(this).text();
  var environments = JSON.parse($.session.get("RoleEnvironments"));
  var textForCounterMeasures = [];
  var textForResponses = [];
  var i =0;
  var j  = 0;
  $.each(environments, function (index, obj) {
    if(obj.theEnvironmentName == text){
      $.each(obj.theCountermeasures, function (index, val) {
        debugLogger("Found one" + val);
        textForCounterMeasures[i++] = "<tr><td>"+ val + "</td><tr>";
      });
      var theResp = obj.theResponses;
      $.each(theResp , function (index1, valu) {
        textForResponses[j++] = "<tr><td>"+ valu.__python_tuple__[0] +"</td><td>"+ valu.__python_tuple__[1] +"</td></tr>";
      });
      $("#theCounterMeasures").find('tbody').append(textForCounterMeasures.join(''));
      $("#theResponses").find('tbody').append(textForResponses.join(''));
    }
  })
});

$("#reqTable").on("click", "#addNewRole", function () {
  $("#reqTable").find("tbody").append('<tr><td><button class="editRoleButton" value="">Edit</button> <button class="deleteRoleButton" value="">Delete</button></td><td name="theName"></td><td name="theShortCode"></td><td name="theType"></td></tr>')
});

mainContent.on('click', '#CloseRole', function (e) {
  e.preventDefault();
  fillRolesTable();
});


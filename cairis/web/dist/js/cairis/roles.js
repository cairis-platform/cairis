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
  clearLocalStorage($('#menuBCClick').attr('dimension'));
  $("#objectViewer").empty();
  $('#menuBCClick').attr('dimension','role');
  refreshMenuBreadCrumb('role');
});

function fillRolesTable(){
  setTableHeader("Roles");
  activeElement("mainTable");
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

      var keys = [];
      for (key in json) {
        keys.push(key);
      }
      keys.sort();

      for (var ki = 0; ki < keys.length; ki++) {
        var key = keys[ki];
        var value = json[key];

        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td class="deleteRoleButton"><i class="fa fa-minus" value="' + value.theName + '"></i></td>';
        textToInsert[i++] = '<td class="role-rows" name="theName">';
        textToInsert[i++] = value.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theShortCode">';
        textToInsert[i++] = value.theShortCode;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theType">';
        textToInsert[i++] = value.theType;
        textToInsert[i++] = '</td>';
        textToInsert[i++] = '</tr>';
      }
      $("#mainTable").append(textToInsert.join(''));
      $(".theTable").css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
      $("#mainTable").find("tbody").removeClass();

    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
  sortTableByRow(1);
}

$(document).on('click', "td.role-rows", function(){
  var roleName = $(this).text();
  refreshObjectBreadCrumb(roleName);
  viewRole(roleName);
});

function viewRole(roleName) {
  activeElement("objectViewer");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/roles/name/" + encodeURIComponent(roleName),
    success: function (json) {
      fillOptionMenu("fastTemplates/editRoleOptions.html", "#objectViewer", null, true, true, function () {
        $("#UpdateRole").text("Update");
        $.session.set("RoleObject", JSON.stringify(json));
        $("#editRoleOptionsform").loadJSON(json, null);
        $("#editRoleOptionsform").validator('update');
        $.ajax({
          type: "GET",
          dataType: "json",
          accept: "application/json",
          data: {
            session_id: String($.session.get('sessionID'))
          },
          crossDomain: true,
          url: serverIP + "/api/roles/name/" + encodeURIComponent(roleName) + "/properties",
          success: function (json) {
            $.each(json, function (index, value) {
              $("#theEnvironments").find("tbody").append("<tr><td class='roleEnvironmentClick'>" + value.theEnvironmentName + "</td></tr>");
            });
            $.session.set("RoleEnvironments", JSON.stringify(json))
            $("#theEnvironments").find("tbody").find(".roleEnvironmentClick:first").trigger('click');
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
};

var mainContent = $("#objectViewer");
function commitRole() {
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
        clearLocalStorage("role");
        $('#menuBCClick').attr('dimension','role');
        refreshMenuBreadCrumb('role');
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
        clearLocalStorage("role");
        $('#menuBCClick').attr('dimension','role');
        refreshMenuBreadCrumb('role');
      });
    }
  }
}

$(document).on('click',"td.deleteRoleButton",function(event){
  event.preventDefault();
  var roleName = $(this).find('i').attr("value");
  deleteObject('role',roleName,function(roleName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      data: roleName,
      url: serverIP + "/api/roles/name/" + encodeURIComponent(roleName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        showPopup(true);
        $('#menuBCClick').attr('dimension','role');
        refreshMenuBreadCrumb('role');
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




mainContent.on("click", '.roleEnvironmentClick', function () {
  $(this).closest('tr').addClass('active').siblings().removeClass('active');
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

$(document).on('click', '#addNewRole', function () {
  refreshObjectBreadCrumb('New Role');
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editRoleOptions.html", "#objectViewer", null, true, true, function () {
    $("#editRoleOptionsform").validator();
    $("#UpdateRole").text("Create");
    $("#editRoleOptionsform").addClass("newRole");
    $.session.set("RoleObject", JSON.stringify(jQuery.extend(true, {},roleDefaultObject )));
  });
});

mainContent.on('click', '#CloseRole', function (e) {
  e.preventDefault();
  clearLocalStorage("role");
  $("#objectViewer").empty();
  $('#menuBCClick').attr('dimension','role');
  refreshMenuBreadCrumb('role');
});

function updateRole(role, oldName, callback){
  var output = {};
  output.object = role;
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);

  $.ajax({
    type: "PUT",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/roles/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
    success: function (data) {
      showPopup(true);
      if(jQuery.isFunction(callback)){
        callback();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function postRole(role, callback){

  var output = {};
  output.object = role;
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);

  $.ajax({
    type: "POST",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/roles?session_id=" + $.session.get('sessionID'),
    success: function (data) {
      showPopup(true);
      if(jQuery.isFunction(callback)){
        callback();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

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

$("#domainPropertyClick").click(function () {
  createDomainPropertiesTable();
});

$("#domainPropertyMenuClick").click(function () {
  createDomainPropertiesTable();
});


function createDomainPropertiesTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/domainproperties",
    success: function (data) {
      setTableHeader("DomainProperties");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td class="deleteDomainPropertyButton"><i class="fa fa-minus" value="' + key + '"></i></td>';

        textToInsert[i++] = '<td class="domainproperty-row" name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theType">';
        textToInsert[i++] = item.theType;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      });

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
      $.contextMenu('destroy',$('.domainproperty-rows'));
      $("#mainTable").find("tbody").removeClass();
      activeElement("mainTable");
      sortTableByRow(0);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
}

$(document).on('click', "td.domainproperty-row", function () {
  var dpName = $(this).text();
  viewDomainProperty(dpName);
});

function viewDomainProperty(dpName) {
  activeElement("objectViewer");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/domainproperties/name/" + dpName.replace(" ", "%20"),
    success: function (data) {
      fillOptionMenu("fastTemplates/editDomainPropertyOptions.html", "#objectViewer", null, true, true, function () {
        $("#UpdateDomainProperty").text("Update");
        $.session.set("DomainProperty", JSON.stringify(data));
        $('#editDomainPropertyOptionsForm').loadJSON(data, null);

        if (data.theTags.length > 0) {
          var text = "";
          $.each(data.theTags, function (index, type) {
            text += type;
            if (index < (data.theTags.length - 1)) {
              text += ", ";
            }
          });
          $("#theTags").val(text);
        }
        $("#editDomainPropertyOptionsForm").validator('update');
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
};

var mainContent = $("#objectViewer");

mainContent.on('click', '#UpdateDomainProperty', function (e) {
  e.preventDefault();
  var dp = JSON.parse($.session.get("DomainProperty"));
  var oldName = dp.theName;
  dp.theName = $("#theName").val();
  dp.theType = $("#theType").val();
  dp.theDescription = $("#theDescription").val();
  var tags = $("#theTags").text().split(", ");
  if(tags[0] != ""){
    dp.theTags = tags;
  }

  if($("#editDomainPropertyOptionsForm").hasClass("new")){
    postDomainProperty(dp, function () {
      createDomainPropertiesTable();
      $("#editDomainPropertyOptionsForm").removeClass("new")
    });
  } 
  else {
    putDomainProperty(dp, oldName, function () {
      createDomainPropertiesTable();
    });
  }
});

$(document).on('click', 'td.deleteDomainPropertyButton', function (e) {
  e.preventDefault();
  var dpName = $(this).find('i').attr("value");
  deleteObject('domainproperty',dpName,function(dpName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/domainproperties/name/" + dpName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        createDomainPropertiesTable();
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




$(document).on("click", "#addNewDomainProperty", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editDomainPropertyOptions.html", "#objectViewer", null, true, true, function () {
    $("#editDomainPropertyOptionsForm").validator();
    $("#UpdateDomainProperty").text("Create");
    $("#editDomainPropertyOptionsForm").addClass("new");
    $.session.set("DomainProperty", JSON.stringify(jQuery.extend(true, {},domainPropertyDefault )));
    $("#optionsHeaderGear").text("Domain Property properties");
  });
});

function putDomainProperty(dp, oldName, usePopup, callback){
  var output = {};
  output.object = dp;
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);
  debugLogger(output);

  $.ajax({
    type: "PUT",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/domainproperties/name/" + oldName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
    success: function (data) {
      if(usePopup) {
        showPopup(true);
      }
      if(jQuery.isFunction(callback)){
        callback();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      if(usePopup) {
        var error = JSON.parse(xhr.responseText);
        showPopup(false, String(error.message));
      }
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function postDomainProperty(dp, callback){
  var output = {};
  output.object = dp;
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);
  debugLogger(output);

  $.ajax({
    type: "POST",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/domainproperties" + "?session_id=" + $.session.get('sessionID'),
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

mainContent.on('click', '#CloseDomainProperty', function (e) {
  e.preventDefault();
  createDomainPropertiesTable();
});


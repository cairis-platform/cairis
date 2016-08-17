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

$("#domainPropertyClick").click(function () {
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
      window.activeTable = "DomainProperties";
      setTableHeader();
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td><button class="editDomainPropertyButton" value="' + key + '">' + 'Edit' + '</button> <button class="deleteDomainPropertyButton" value="' + key + '">' + 'Delete' + '</button></td>';

        textToInsert[i++] = '<td name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theType">';
        textToInsert[i++] = item.theType;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      });

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      activeElement("reqTable");
      sortTableByRow(0);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
}

$(document).on('click', ".editDomainPropertyButton", function () {
  var name = $(this).val();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/domainproperties/name/" + name.replace(" ", "%20"),
    success: function (data) {
      fillOptionMenu("fastTemplates/editDomainPropertyOptions.html", "#optionsContent", null, true, true, function () {
        $("#optionsHeaderGear").text("Domain Property properties");
        forceOpenOptions();
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
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

optionsContent.on('click', '#UpdateDomainProperty', function (e) {
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

$(document).on('click', '.deleteDomainPropertyButton', function (e) {
  e.preventDefault();
  deleteDomainProperty($(this).val(), function () {
    createDomainPropertiesTable();
  });
});

$(document).on("click", "#addNewDomainProperty", function () {
  fillOptionMenu("fastTemplates/editDomainPropertyOptions.html", "#optionsContent", null, true, true, function () {
    $("#editDomainPropertyOptionsForm").addClass("new");
    $.session.set("DomainProperty", JSON.stringify(jQuery.extend(true, {},domainPropertyDefault )));
    $("#optionsHeaderGear").text("Domain Property properties");
    forceOpenOptions();
  });
});

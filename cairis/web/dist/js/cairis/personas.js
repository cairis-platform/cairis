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

$("#personaMenuClick").click(function () {
  createPersonasTable();
});

$("#personaClick").click(function () {
  createPersonasTable();
});


function createPersonasTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/personas",
    success: function (data) {
      setTableHeader("Personas");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td class="deletePersonaButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="persona-row" name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="thePersonaType">';
        textToInsert[i++] = item.thePersonaType;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      });

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
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

$(document).on('click', "td.persona-row", function () {
  var personaName = $(this).text();
  viewPersona(personaName);
});

function viewPersona(personaName) {
  activeElement("objectViewer");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/personas/name/" + personaName.replace(" ", "%20"),
    success: function (data) {
      fillOptionMenu("fastTemplates/editPersonasOptions.html", "#objectViewer", null, true, true, function () {
        $("#editPersonasOptionsForm").validator();
        $("#UpdatePersona").text("Update");
        $.session.set("Persona", JSON.stringify(data));
        $('#editPersonasOptionsForm').loadJSON(data, null);


        getPersonaTypes(function createTypes(types) {
          $.each(types, function (pType,index) {
            $('#thePersonaType').append($("<option></option>").attr("value", pType).text(pType));
          });
          $("#thePersonaType").val(data.thePersonaType);
        });

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

        $.each(data.theEnvironmentProperties, function (index, env) {
          appendPersonaEnvironment(env.theEnvironmentName);
        });
        $("#thePersonaEnvironments").find(".personaEnvironment:first").trigger('click');
        $("#theImage").attr("src",getImagedir(data.theImage));
        rescaleImage($("#theImage"),300);

        $('#thePersonaCharacteristicList').contextMenu({
          selector: 'li.personaContextMenu',
          items: {
            "visualise": {
              name: "Visualise",
              callback: function(key, opt) {
                var pName = data.theName;
                var bvName = $(this).text();
                getTabbedPersonaView(pName,bvName,'All');
              }
            }
          }
        });
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
};


var mainContent = $("#objectViewer");
mainContent.on("click",".personaEnvironment", function () {
  clearPersonaEnvInfo();
  var persona = JSON.parse($.session.get("Persona"));
  var theEnvName = $(this).text();
  $.session.set("personaEnvironmentName", theEnvName);
  $.each(persona.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theRoles, function (index, role) {
        appendPersonaRole(role);
      });
      if (env.theDirectFlag == "True") {
        $("#theDirectFlag").prop("checked",true);
      }
      else {
        $("#theDirectFlag").prop("checked",false);
      }
      $("#theNarrative").val(env.theNarrative);
    }
  });
});

mainContent.on('click', ".removePersonaRole", function () {
  var text = $(this).next(".personaRole").text();
  $(this).closest("tr").remove();
  var persona = JSON.parse($.session.get("Persona"));
  var theEnvName = $.session.get("personaEnvironmentName");
  $.each(persona.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theRoles, function (index2, role) {
        if(role == text){
          env.theRoles.splice( index2 ,1 );
          $.session.set("Persona", JSON.stringify(persona));
          return false;
        }
      });
    }
  });
});

mainContent.on('click', ".deletePersonaEnv", function () {
  var envi = $(this).next(".personaEnvironment").text();
  $(this).closest("tr").remove();
  var persona = JSON.parse($.session.get("Persona"));
  $.each(persona.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envi){
      persona.theEnvironmentProperties.splice( index ,1 );
      $.session.set("Persona", JSON.stringify(persona));
      clearPersonaEnvInfo();

      var UIenv = $("#thePersonaEnvironments").find("tbody");
      if(jQuery(UIenv).has(".personaEnvironment").length){
        UIenv.find(".personaEnvironment:first").trigger('click');
      }else{
        $("#Properties").hide("fast");
      }

      return false;
    }
  });
});

mainContent.on("click", "#addPersonaEnv", function () {
  var hasEnv = [];
  $(".personaEnvironment").each(function (index, tag) {
    hasEnv.push($(tag).text());
  });
  environmentDialogBox(hasEnv, function (text) {
    appendPersonaEnvironment(text);
    var environment =  jQuery.extend(true, {},personaEnvDefault );
    environment.theEnvironmentName = text;
    var persona = JSON.parse($.session.get("Persona"));
    persona.theEnvironmentProperties.push(environment);
    $.session.set("Persona", JSON.stringify(persona));
    $(document).find(".personaEnvironment").each(function () {
      if($(this).text() == text){
        $(this).trigger("click");
        $("#Properties").show("fast");
      }
    });
  });
});

mainContent.on('click', '#addRoleToPersona', function () {
  var hasRole = [];
  $("#personaRole").find(".personaRole").each(function(index, role){
    hasRole.push($(role).text());
  });
  roleDialogBox(hasRole, function (text) {
    var persona = JSON.parse($.session.get("Persona"));
    var theEnvName = $.session.get("personaEnvironmentName");
    $.each(persona.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        env.theRoles.push(text);
        $.session.set("Persona", JSON.stringify(persona));
        appendPersonaRole(text);
      }
    });
  });
});

mainContent.on('click', '#UpdatePersona', function (e) {
  $("#editPersonasOptionsForm").validator('validate');
  e.preventDefault();
  var persona = JSON.parse($.session.get("Persona"));
  if (persona.theEnvironmentProperties.length == 0) {
    alert("Environments not defined");
  }
  else {
    var oldName = persona.theName;
    persona.theId = -1;
    persona.theName = $("#theName").val();
    persona.theDescription = $("#theDescription").val();
    persona.theActivities = $("#theActivities").val();
    persona.theAttitudes = $("#theAttitudes").val();
    persona.theAptitudes = $("#theAptitudes").val();
    persona.theMotivations = $("#theMotivations").val();
    persona.theSkills = $("#theSkills").val();
    persona.theIntrinsic = $("#theIntrinsic").val();
    persona.theContextual = $("#theContextual").val();
    persona.theAssumption = 0;
    persona.thePersonaType = $("#thePersonaType :selected").text();
    persona.theCodes = [];

    var tags = $("#theTags").text().split(", ");
    if(tags[0] != ""){
      persona.theTags = tags;
    }
    var theEnvName = $.session.get("personaEnvironmentName");
    $.each(persona.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        env.theNarrative = $("#theNarrative").val()
        $.session.set("Persona", JSON.stringify(persona));
      }
    });

    if($("#editPersonasOptionsForm").hasClass("new")){
      postPersona(persona, function () {
        createPersonasTable();
        $("#editPersonasOptionsForm").removeClass("new")
      });
    } 
    else {
      putPersona(persona, oldName, function () {
        createPersonasTable();
      });
    }
  }
});

$(document).on("click", "#addNewPersona", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editPersonasOptions.html", "#objectViewer", null, true, true, function () {
    $("#editPersonasOptionsForm").validator();
    $("#UpdatePersona").text("Create");
    $("#editPersonasOptionsForm").addClass("new");
    $("#Properties").hide();
    $.session.set("Persona", JSON.stringify(jQuery.extend(true, {},personaDefault )));

    getPersonaTypes(function createTypes(types) {
      $.each(types, function (pType,index) {
        $('#thePersonaType').append($("<option></option>").attr("value", pType).text(pType));
      });
    });
  });
});

//deletePersonaButton
$(document).on('click', 'td.deletePersonaButton', function (e) {
  e.preventDefault();
  deletePersona($(this).find('i').attr("value"), function () {
    createPersonasTable();
  });
});


// Image uploading functions
var uploading = false;
mainContent.on('click', '#theImage', function (e) {
  if(!uploading) {
    $('#fileupload').trigger("click");
  }
});


mainContent.on('change','#fileupload', function () {
  uploading = true;
  var test = $(document).find('#fileupload');
  var fd = new FormData();
  fd.append("file", test[0].files[0]);
  var bar = $(".progress-bar");
  var outerbar = $(".progress");
  bar.css("width", 0);
  outerbar.show("slide", { direction: "up" }, 750);

  $.ajax({
    type: "POST",
    accept: "application/json",
    processData:false,
    contentType:false,
    data: fd,
    crossDomain: true,
    url: serverIP + "/api/upload/image?session_id="+  String($.session.get('sessionID')),
    success: function (data) {
      outerbar.hide("slide", { direction: "down" }, 750);
      uploading = false;
      data = JSON.parse(data);
      updatePersonaImage(data.filename, getImagedir(data.filename));
    },
    error: function (xhr, textStatus, errorThrown) {
      uploading = false;
      outerbar.hide("slide", { direction: "down" }, 750);
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    },
    xhr: function() {
      var xhr = new window.XMLHttpRequest();
      xhr.upload.addEventListener("progress", function(evt) {
        if (evt.lengthComputable) {
          var percentComplete = evt.loaded / evt.total;
          percentComplete = (percentComplete) * outerbar.width();
          bar.css("width", percentComplete)
        }
      }, false);
      return xhr;
    }
  });
});

function updatePersonaImage(imagedir, actualDir) {
  var persona = JSON.parse($.session.get("Persona"));
  persona.theImage = imagedir;
  $("#theImage").attr("src", actualDir);
  rescaleImage($("#theImage"),300);
  $.session.set("Persona", JSON.stringify(persona));
}

function personaToggle(){
  $("#editPersonasOptionsForm").toggle();
}
function appendPersonaEnvironment(environment){
  $("#thePersonaEnvironments").find("tbody").append('<tr><td class="deletePersonaEnv"><i class="fa fa-minus"></i></td><td class="personaEnvironment">'+environment+'</td></tr>');
}
function appendPersonaRole(role){
  $("#personaRole").find("tbody").append("<tr><td class='removePersonaRole'><i class='fa fa-minus'></i></td><td class='personaRole'>" + role + "</td></tr>").animate('slow');
}
function clearPersonaEnvInfo(){
  $("#personaRole").find("tbody").empty();
  $("#theNarrative").val('');
}

function getPersonaTypes(callback){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/personas/types",
    success: function (data) {
      if(jQuery.isFunction(callback)){
        callback(data);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

mainContent.on('click', '#ClosePersona', function (e) {
  e.preventDefault();
  createPersonasTable();
});

function deletePersona(name, callback){
  $.ajax({
    type: "DELETE",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    url: serverIP + "/api/personas/name/" + name.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
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

function putPersona(persona, oldName, usePopup, callback){
  var output = {};
  output.object = persona;
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
    url: serverIP + "/api/personas/name/" + oldName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
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

function postPersona(persona, callback){
  var output = {};
  output.object = persona;
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
    url: serverIP + "/api/personas" + "?session_id=" + $.session.get('sessionID'),
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

function getTabbedPersonaView(pName,bvName,pcName){
  Cookies.set('model','persona');
  Cookies.set('pName',pName);
  Cookies.set('bvName',bvName);
  Cookies.set('pcName',pcName);
  Cookies.set('wTitle',pName + " persona characteristics");
  var viewerWindow = window.open('viewer.html');
}

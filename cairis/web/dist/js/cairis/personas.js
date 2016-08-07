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

$("#personaClick").click(function () {
  createPersonasTable();
});

/*
 A function for filling the table with Personas
 */
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
      window.activeTable = "Personas";
      setTableHeader();
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td><button class="editPersonaButton" value="' + key + '">' + 'Edit' + '</button> <button class="deletePersonaButton" value="' + key + '">' + 'Delete' + '</button></td>';

        textToInsert[i++] = '<td name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="thePersonaType">';
        textToInsert[i++] = item.thePersonaType;
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

$(document).on('click', ".editPersonaButton", function () {
  var name = $(this).val();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/personas/name/" + name.replace(" ", "%20"),
    success: function (data) {
      // console.log(JSON.stringify(rawData));
      fillOptionMenu("fastTemplates/editPersonasOptions.html", "#optionsContent", null, true, true, function () {
        forceOpenOptions();
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
        resaleImage($("#theImage"));
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

var optionsContent = $("#optionsContent");
optionsContent.on("click",".personaEnvironment", function () {
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

optionsContent.on('click', ".removePersonaRole", function () {
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

optionsContent.on('click', ".deletePersonaEnv", function () {
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

optionsContent.on("click", "#addPersonaEnv", function () {
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

optionsContent.on('click', '#addRoleToPersona', function () {
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

optionsContent.on('click', '#UpdatePersona', function (e) {
  e.preventDefault();
  var persona = JSON.parse($.session.get("Persona"));
  var oldName = persona.theName;
  persona.theName = $("#theName").val();
  persona.theDescription = $("#theDescription").val();
  var tags = $("#theTags").text().split(", ");
  if(tags[0] != ""){
    persona.theTags = tags;
  }
  //IF NEW Persona
  if($("#editPersonasOptionsForm").hasClass("new")){
    postPersona(persona, function () {
      createPersonasTable();
      $("#editPersonasOptionsForm").removeClass("new")
    });
  } else {
    putPersona(persona, oldName, function () {
      createPersonasTable();
    });
  }
});

$(document).on("click", "#addNewPersona", function () {
  fillOptionMenu("fastTemplates/editPersonasOptions.html", "#optionsContent", null, true, true, function () {
    $("#editPersonasOptionsForm").addClass("new");
    $("#Properties").hide();
    $.session.set("Persona", JSON.stringify(jQuery.extend(true, {},personaDefault )));
    forceOpenOptions();
  });
});

//deletePersonaButton
$(document).on('click', '.deletePersonaButton', function (e) {
  e.preventDefault();
  deletePersona($(this).val(), function () {
    createPersonasTable();
  });
});

/*
Image uploading functions
 */
var uploading = false;
$("#optionsContent").on('click', '#theImage', function () {
  if(!uploading) {
    $('#fileupload').trigger("click");
  }
});

$("#optionsContent").on('change','#fileupload', function () {
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

      postImage(data.filename, getImagedir(data.filename));


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

function postImage(imagedir, actualDir) {
    var persona = JSON.parse($.session.get("Persona"));

    persona.theImage = imagedir;
    $("#theImages").attr("src", actualDir);
    putPersona(persona, persona.theName, false, function () {
        $("#theImages").attr("src", actualDir);
        resaleImage($("#theImages"),200);
    });

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


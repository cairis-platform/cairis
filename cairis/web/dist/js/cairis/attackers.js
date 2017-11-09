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

'use strict';

$("#attackerMenuClick").click(function () {
  validateClick('attacker',function() {
    $('#menuBCClick').attr('dimension','attacker');
    refreshMenuBreadCrumb('attacker');
  });
});

function createAttackersTable(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/attackers",
    success: function (data) {
      setTableHeader("Attackers");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      var keys = [];
      for (key in data) {
        keys.push(key);
      }
      keys.sort();

      for (var ki = 0; ki < keys.length; ki++) {
        var key = keys[ki];
        var item = data[key];

        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td class="deleteAttackerButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';
        textToInsert[i++] = '<td class="attacker-rows" name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theType">';
        textToInsert[i++] = item.theDescription;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      }

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
      $("#mainTable").find("tbody").removeClass();

      activeElement("mainTable");
      sortTableByRow(0);

    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
}

$(document).on('click', "td.attacker-rows", function () {
  var attackerName = $(this).text();
  refreshObjectBreadCrumb(attackerName);
  viewAttacker(attackerName);
});

function viewAttacker(attackerName) {
  activeElement("objectViewer"); 
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/attackers/name/" + encodeURIComponent(attackerName),
    success: function (data) {
      fillOptionMenu("fastTemplates/editAttackerOptions.html", "#objectViewer", null, true, true, function () {
        $("#UpdateAttacker").text("Update");
        $.session.set("Attacker", JSON.stringify(data));
        $('#editAttackerOptionsForm').loadJSON(data, null);
        var tags = data.theTags;
        var text = "";
        $.each(tags, function (index, type) {
          text += type + ", ";
        });
        $("#theTags").val(text);
        $.each(data.theEnvironmentProperties, function (index, env) {
          appendAttackerEnvironment(env.theEnvironmentName);
        });
        $("#theAttackerEnvironments").find(".attackerEnvironment:first").trigger('click');
        $("#theAttackerImage").attr("src",getImagedir(data.theImage));
        rescaleImage($("#theAttackerImage"),225);
        $("#editAttackerOptionsForm").validator('update');
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
mainContent.on("click",".attackerEnvironment", function () {
  clearAttackerEnvInfo();
  var attacker = JSON.parse($.session.get("Attacker"));
  var theEnvName = $(this).text();
  $.session.set("attackerEnvironmentName", theEnvName);
  $.each(attacker.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theMotives, function (index, motive) {
        appendAttackerMotive(motive);
      });
      $.each(env.theRoles, function (index, role) {
        appendAttackerRole(role);
      });
      $.each(env.theCapabilities, function (index, cap) {
        appendAttackerCapability(cap);
      });
    }
  });
});

mainContent.on("click", "#addMotivetoAttacker", function () {
  var filterList = [];
  var theEnvName =  $.session.get("attackerEnvironmentName");
  $(".attackerMotive").each(function (index, tag) {
    filterList.push($(tag).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'motivation',undefined,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','motivation');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addMotivationToAttacker');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addMotivationToAttacker() {
  var text = $("#chooseEnvironmentSelect").val();
  var attacker = JSON.parse($.session.get("Attacker"));
  var theEnvName = $.session.get("attackerEnvironmentName");

  $.each(attacker.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theMotives.push(text);
      appendAttackerMotive(text);
      $.session.set("Attacker", JSON.stringify(attacker));
      $('#chooseEnvironment').modal('hide');
    }
  });
};

mainContent.on('click', "#addCapabilitytoAttacker", function () {

  var attacker = JSON.parse($.session.get("Attacker"));
  var theEnvName = $.session.get("attackerEnvironmentName");

  var filterList = [];
  $("#attackerCapability").find(".attackerCapability").each(function(index, asset){
    filterList.push($(asset).text());
  });

  refreshDimensionSelector($('#theCapability'),'capability',undefined,function(){
    $('#attackerCapabilityDialog').attr('data-currentCapability',undefined);
    $('#attackerCapabilityDialog').attr('data-selectedIndex',undefined);
    $('#attackerCapabilityDialog').modal('show');
  },filterList);
});

mainContent.on('shown.bs.modal',"#attackerCapabilityDialog", function() {
  var currentCap = JSON.parse($('#attackerCapabilityDialog').attr('data-currentCapability'));
  if (currentCap != undefined) {
    $('#theCapability').val(currentCap.name);
    $('#theCapabilityValue').val(currentCap.value);
    $('#AddAttackerCapabilityButton').text('Edit');
  }
  else {
    $('#theCapability').val('');
    $('#theCapabilityValue').val('');
  }
});


mainContent.on('click',"#AddAttackerCapabilityButton", function(e) {
  e.preventDefault();
  var updCap = {};
  updCap.name = $("#theCapability").val();
  updCap.value = $("#theCapabilityValue").val();
  var attacker = JSON.parse($.session.get("Attacker"));
  var theEnvName = $.session.get("attackerEnvironmentName");

  $.each(attacker.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      var selectedIdx = $('#attackerCapabilityDialog').attr('data-selectedIndex');
      if (selectedIdx == undefined) {
        attacker.theEnvironmentProperties[index].theCapabilities.push(updCap);
        $.session.set("Attacker", JSON.stringify(attacker));
        appendAttackerCapability(updCap);
        $('#attackerCapabilityDialog').modal('hide');
      }
      else {
        $.each(env.theCapabilities,function(idx,cap) {
          if (cap.name == updCap.name) {
            attacker.theEnvironmentProperties[index].theCapabilities[idx].value = updCap.value;
            $.session.set("Attacker", JSON.stringify(attacker));
            $('#attackerCapability').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(1)").text(updCap.name);
            $('#attackerCapability').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(2)").text(updCap.value);
            $('#attackerCapabilityDialog').modal('hide');
          }
        });
      }
    }
  });
});


mainContent.on('dblclick', ".changeCapability", function () {
  var capRow = $(this).closest("tr");
  var attacker = JSON.parse($.session.get("Attacker"));
  var theEnvName = $.session.get("attackerEnvironmentName");

  var filterList = [];
  $("#attackerCapability").find(".attackerCapability").each(function(index, cap){
    if ($(cap).text() != capRow.find("td:eq(1)").text()) {
      filterList.push($(cap).text());
    }
  });

  refreshDimensionSelector($('#theCapability'),'capability',undefined,function(){
    var currentCap = {};
    currentCap.name = capRow.find("td:eq(1)").text();
    currentCap.value = capRow.find("td:eq(2)").text();
    $('#attackerCapabilityDialog').attr('data-currentCapability',JSON.stringify(currentCap));
    $('#attackerCapabilityDialog').attr('data-selectedIndex',capRow.index());
    $('#attackerCapabilityDialog').modal('show');
  },filterList);
});

mainContent.on('click', ".removeAttackerMotive", function () {
  var text = $(this).next(".attackerMotive").text();
  $(this).closest("tr").remove();
  var attacker = JSON.parse($.session.get("Attacker"));
  var theEnvName = $.session.get("attackerEnvironmentName");
  $.each(attacker.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theMotives, function (index2, mot) {
        if(mot == text){
          env.theMotives.splice( index2 ,1 );
          $.session.set("Attacker", JSON.stringify(attacker));
          return false;
        }
      });
    }
  });
});

mainContent.on('click', ".removeAttackerRole", function () {
  var text = $(this).next(".attackerRole").text();
  $(this).closest("tr").remove();
  var attacker = JSON.parse($.session.get("Attacker"));
  var theEnvName = $.session.get("attackerEnvironmentName");
  $.each(attacker.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theRoles, function (index2, role) {
        if(role == text){
          env.theRoles.splice( index2 ,1 );
          $.session.set("Attacker", JSON.stringify(attacker));
          return false;
        }
      });
    }
  });
});

mainContent.on('click', ".deleteAttackerEnv", function () {
  var envi = $(this).next(".attackerEnvironment").text();
  $(this).closest("tr").remove();
  var attacker = JSON.parse($.session.get("Attacker"));
  $.each(attacker.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envi){
      attacker.theEnvironmentProperties.splice( index ,1 );
      $.session.set("Attacker", JSON.stringify(attacker));
      clearAttackerEnvInfo();

      var UIenv = $("#theAttackerEnvironments").find("tbody");
      if(jQuery(UIenv).has(".attackerEnvironment").length){
        UIenv.find(".attackerEnvironment:first").trigger('click');
      }
      else {
        $("#Properties").hide("fast");
      }
      return false;
    }
  });
});

mainContent.on("click", "#addAttackerEnv", function () {
  var filterList = [];
  $(".attackerEnvironment").each(function (index, tag) {
    filterList.push($(tag).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'environment',undefined,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','environment');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addAttackerEnvironment');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addAttackerEnvironment() {
  var text = $("#chooseEnvironmentSelect").val();
  appendAttackerEnvironment(text);
  var environment =  jQuery.extend(true, {},attackerEnvDefault );
  environment.theEnvironmentName = text;
  var attacker = JSON.parse($.session.get("Attacker"));
  attacker.theEnvironmentProperties.push(environment);
  $.session.set("Attacker", JSON.stringify(attacker));
  $(document).find(".attackerEnvironment").each(function () {
    if($(this).text() == text){
      $(this).trigger("click");
      $("#Properties").show("fast");
      $('#chooseEnvironment').modal('hide');
    }
  });
}

mainContent.on('click', '#addRoletoAttacker', function () {
  var filterList = [];
  $("#attackerRole").find(".attackerRole").each(function(index, role){
    filterList.push($(role).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'role',undefined,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','role');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addRoleToAttacker');
    $('#chooseEnvironment').modal('show');
  },filterList);

});

function addRoleToAttacker() {
  var text = $("#chooseEnvironmentSelect").val();
  var attacker = JSON.parse($.session.get("Attacker"));
  var theEnvName = $.session.get("attackerEnvironmentName");
  $.each(attacker.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theRoles.push(text);
      $.session.set("Attacker", JSON.stringify(attacker));
      appendAttackerRole(text);
      $('#chooseEnvironment').modal('hide');
    }
  });
}

mainContent.on('click', '#UpdateAttacker', function (e) {
  e.preventDefault();
  $("#editAttackerOptionsForm").validator('validate');
  var attacker = JSON.parse($.session.get("Attacker"));
  if (attacker.theEnvironmentProperties.length == 0) {
    alert("Environments not defined");
  }
  else {
    var oldName = attacker.theName;
    attacker.theName = $("#theName").val();
    attacker.theDescription = $("#theDescription").val();
    var tags = $("#theTags").text().split(", ");
    if(tags[0] != ""){
      attacker.theTags = tags;
    }
    if($("#editAttackerOptionsForm").hasClass("new")){
      postAttacker(attacker, function () {
        $("#editAttackerOptionsForm").removeClass("new")
        $('#menuBCClick').attr('dimension','attacker');
        refreshMenuBreadCrumb('attacker');
      });
    } 
    else {
      putAttacker(attacker, oldName, function () {
        $('#menuBCClick').attr('dimension','attacker');
        refreshMenuBreadCrumb('attacker');
      });
    }
  }
});

$(document).on("click", "#addNewAttacker", function () {
  refreshObjectBreadCrumb('New Attacker');
  activeElement("objectViewer"); 
  fillOptionMenu("fastTemplates/editAttackerOptions.html", "#objectViewer", null, true, true, function () {
    $("#editAttackerOptionsForm").validator();
    $("#UpdateAttacker").text("Create");
    $("#editAttackerOptionsForm").addClass("new");
    $("#Properties").hide();
    $.session.set("Attacker", JSON.stringify(jQuery.extend(true, {},attackerDefault )));
  });
});

/*
mainContent.on('click', "#UpdateAttackerCapability", function () {
  var attacker = JSON.parse($.session.get("Attacker"));
  var theEnvName = $.session.get("attackerEnvironmentName");
  if($("#addAttackerPropertyDiv").hasClass("new")){
    $.each(attacker.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        var prop = {};
        prop.name = $("#theCap option:selected").text();
        prop.value = $("#thePropValue option:selected").text();
        env.theCapabilities.push(prop);
        $.session.set("Attacker", JSON.stringify(attacker));
        appendAttackerCapability(prop);
        attackerToggle();
      }
    });
  }
  else {
    var oldCapName = $.session.get("AttackerCapName");
    $.each(attacker.theEnvironmentProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        $.each(env.theCapabilities, function (index, cap) {
          if(oldCapName == cap.name){
            cap.name = $("#theCap option:selected").text();
            cap.value = $("#thePropValue option:selected").text();
          }
        });
        $.session.set("Attacker", JSON.stringify(attacker));
        $("#theAttackerEnvironments").find(".attackerEnvironment:first").trigger('click');
        attackerToggle();
      }
    });
  }
}); 
*/

mainContent.on("click", ".removeAttackerCapability", function () {
  var text = $(this).closest('tr').find(".attackerCapability").text();
  $(this).closest("tr").remove();
  var attacker = JSON.parse($.session.get("Attacker"));
  var theEnvName = $.session.get("attackerEnvironmentName");
  $.each(attacker.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theCapabilities, function (index2, cap) {
        if(cap.name == text){
          env.theCapabilities.splice( index2 ,1 );
          $.session.set("Attacker", JSON.stringify(attacker));
          return false;
        }
      });
    }
  });
});

$(document).on('click', 'td.deleteAttackerButton', function (e) {
  e.preventDefault();
  var attackerName = $(this).find('i').attr("value");
  deleteObject('attacker',attackerName,function(attackerName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/attackers/name/" + encodeURIComponent(attackerName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        showPopup(true);
        $('#menuBCClick').attr('dimension','attacker');
        refreshMenuBreadCrumb('attacker');
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




var uploading = false;
$("#objectViewer").on('click', '#theAttackerImage', function () {
  if(!uploading) {
    $('#fileupload').trigger("click");
  }
});

$("#objectViewer").on('change','#fileupload', function () {
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
      updateAttackerImage(data.filename, getImagedir(data.filename));
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

function updateAttackerImage(imagedir, actualDir) {
  var attacker = JSON.parse($.session.get("Attacker"));
  attacker.theImage = imagedir;
  $("#theAttackerImage").attr("src", actualDir);
  rescaleImage($("#theAttackerImage"),200);
  $.session.set("Attacker", JSON.stringify(attacker));
}

function appendAttackerEnvironment(environment){
  $("#theAttackerEnvironments").find("tbody").append('<tr><td class="deleteAttackerEnv"><i class="fa fa-minus"></i></td><td class="attackerEnvironment">'+environment+'</td></tr>');
}
function appendAttackerRole(role){
  $("#attackerRole").find("tbody").append("<tr><td class='removeAttackerRole'><i class='fa fa-minus'></i></td><td class='attackerRole'>" + role + "</td></tr>").animate('slow');
}
function appendAttackerMotive(motive){
  $("#attackerMotive").find("tbody").append("<tr><td class='removeAttackerMotive' ><i class='fa fa-minus'></i></td><td class='attackerMotive'>" + motive + "</td></tr>").animate('slow');
}
function appendAttackerCapability(prop){
  $("#attackerCapability").find("tbody").append("<tr class='changeCapability'><td class='removeAttackerCapability'><i class='fa fa-minus'></i></td><td class='attackerCapability'>" + prop.name + "</td><td>"+ prop.value +"</td></tr>").animate('slow');
}
function clearAttackerEnvInfo(){
  $("#attackerCapability").find("tbody").empty();
  $("#attackerMotive").find("tbody").empty();
  $("#attackerRole").find("tbody").empty();
}

mainContent.on('click', '#CloseAttacker', function (e) {
  e.preventDefault();
  $('#menuBCClick').attr('dimension','attacker');
  refreshMenuBreadCrumb('attacker');
});

function putAttacker(attacker, oldName, callback){
  var output = {};
  output.object = attacker;
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
    url: serverIP + "/api/attackers/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
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

function postAttacker(attacker, callback){
  var output = {};
  output.object = attacker;
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
    url: serverIP + "/api/attackers" + "?session_id=" + $.session.get('sessionID'),
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

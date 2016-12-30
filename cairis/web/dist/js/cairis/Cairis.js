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

window.serverIP = "http://"+ window.location.host;

window.activeTable ="Requirements";
window.boxesAreFilled = false;
window.debug = true;

function debugLogger(info){
  if(debug){
    console.log(info);
  }
}

$(document).ready(function() {
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
        startingTable();
        hideLoading();
      },
      error: function(data, status, xhr) {
        console.log(this.url);
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + status + ", thrown: " + data);
        alert("There is a problem with the server...");
      }
    });
  }
  else {
    startingTable();
  }
});

function showLoading(){
  $(".loadingWrapper").fadeIn(500);
}
function hideLoading(){
  $(".loadingWrapper").fadeOut(500);
}

// For converting the form in JSON
$.fn.serializeObject = function()
{
  var o = {};
  var a = this.serializeArray();
  $.each(a, function() {
    if (o[this.name] !== undefined) {
      if (!o[this.name].push) {
        o[this.name] = [o[this.name]];
      }
      o[this.name].push(this.value || '');
    } 
    else {
      o[this.name] = this.value || '';
    }
  });
  return o;
};


$('#gmgoalbox').change(function() {
  var selection = $(this).find('option:selected').text();
  getGoalview($('#gmenvironmentsbox').val(),selection);
});

$('#tmtaskbox').change(function() {
  var selection = $(this).find('option:selected').text();
  getTaskview($('#tmenvironmentsbox').val(),selection,'');
});

$('#tmmisusecasebox').change(function() {
  var selection = $(this).find('option:selected').text();
  getTaskview($('#tmenvironmentsbox').val(),'',selection);
});

$('#remrolebox').change(function() {
  var selection = $(this).find('option:selected').text();
  getResponsibilityview($('#remenvironmentsbox').val(),selection);
});


$('#omobstaclebox').change(function() {
  var selection = $(this).find('option:selected').text();
  getObstacleview($('#omenvironmentsbox').val(),selection);
});

$('#appersonasbox').change(function() {
  var selection = $(this).find('option:selected').text();
  appendPersonaCharacteristics(selection,'All','All');
  getPersonasview(selection,'All','All');
});

$('#apbtbox').change(function() {
  var selection = $(this).find('option:selected').text();
  var pName = $('#appersonasbox').val();
  appendPersonaCharacteristics(pName,'All','All');
  getPersonaview(pName,selection,'All');
});

$('#apcharacteristicbox').change(function() {
  var selection = $(this).find('option:selected').text();
  var pName = $('#appersonasbox').val();
  var bvName = $('#apbtbox').val();
  appendPersonaCharacteristics(pName,bvName,'All');
  getPersonaview(pName,bvName,selection);
});

function appendPersonaCharacteristics(pName,bvName,pcName) {

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/personas/characteristics/name/" + pName.replace(" ","%20") + "/variable/" + bvName.replace(" ","%20") + "/characteristic/" + pcName.replace(" ","%20"),
    success: function (data) {
      $('#apcharacteristicbox').empty();
      $('#apcharacteristicbox').append($('<option>', {value: 'All', text: 'All'},'</option>'));
      $.each(data, function (index, item) {
        $('#apcharacteristicbox').append($('<option>', {value: item, text: item},'</option>'));
      });
      $('#apcharacteristicbox').val(pcName);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}


$('#gmenvironmentsbox').change(function() {
  var selection = $(this).find('option:selected').text();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID')),
    },
    crossDomain: true,
    url: serverIP + "/api/goals/environment/" + selection.replace(" ","%20") + "/names",
    success: function (data) {
      $('#gmgoalbox').empty();
      $('#gmgoalbox').append($('<option>', {value: 'All', text: 'All'},'</option>'));
      $.each(data, function (index, item) {
        $('#gmgoalbox').append($('<option>', {value: item, text: item},'</option>'));
      });
      $('#gmgoalbox').change();
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$('#tmenvironmentsbox').change(function() {
  var selection = $(this).find('option:selected').text();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID')),
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/task/environment/" + selection.replace(" ","%20"),
    success: function (data) {
      $('#tmtaskbox').empty();
      $('#tmtaskbox').append($('<option>', {value: 'All', text: 'All'},'</option>'));
      $.each(data, function (index, item) {
        $('#tmtaskbox').append($('<option>', {value: item, text: item},'</option>'));
      });
      $('#tmtaskbox').change();
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});


$('#omenvironmentsbox').change(function() {
  var selection = $(this).find('option:selected').text();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID')),
    },
    crossDomain: true,
    url: serverIP + "/api/obstacles/environment/" + selection.replace(" ","%20") + "/names",
    success: function (data) {
      $('#omobstaclebox').empty();
      $('#omobstaclebox').append($('<option>', {value: 'All', text: 'All'},'</option>'));
      $.each(data, function (index, item) {
        $('#omobstaclebox').append($('<option>', {value: item, text: item},'</option>'));
      });
      $('#omobstaclebox').change();
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$('#remenvironmentsbox').change(function() {
  var selection = $(this).find('option:selected').text();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID')),
    },
    crossDomain: true,
    url: "/api/dimensions/table/role/environment/" + selection.replace(" ","%20"),
    success: function (data) {
      $('#remrolebox').empty();
      $('#remrolebox').append($('<option>', {value: 'All', text: 'All'},'</option>'));
      $.each(data, function (index, item) {
        $('#remrolebox').append($('<option>', {value: item, text: item},'</option>'));
      });
      $('#remrolebox').change();
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});



$('#rmenvironmentsbox').change(function() {
  var envName = $(this).find('option:selected').val();
  $('#rmdimensionbox').val('All');
  var modelLayout = $('#rmlayout').val();

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID')),
    },
    crossDomain: true,
    url: "/api/risks/model/environment/" + envName.replace(" ","%20") + "/names",
    success: function (data) {
      fillObjectBox('#rmobjectbox','All',data);
      $('#rmobjectbox').val('All');
      getRiskview(envName,'All','All',modelLayout);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

function fillObjectBox(cBoxId,dimName,objtNames) {
  $(cBoxId).empty();
  $(cBoxId).append($('<option>', {value: 'All', text: 'All'},'</option>'));
  $.each(objtNames, function (index, item) {
    $(cBoxId).append($('<option>', {value: item, text: item},'</option>'));
  });
  $(cBoxId).change();
}

$('#rmdimensionbox').change(function() {
  var envName = $('#rmenvironmentsbox').val();
  var dimName = $(this).find('option:selected').val();
  var modelLayout = $('#rmlayout').val();

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID')),
    },
    crossDomain: true,
    url: "/api/dimensions/table/" + dimName.replace(" ","%20") + "/environment/" + envName.replace(" ","%20"),
    success: function (data) {
      fillObjectBox('#rmobjectbox',dimName,data);
      $('#rmobjectbox').val('All');
      getRiskview(envName,dimName,'All',modelLayout);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });

});

$('#rmobjectbox').change(function() {
  var envName = $('#rmenvironmentsbox').val()
  var dimName = $('#rmdimensionbox').val()
  var objtName = $('#rmobjectbox').val()
  var modelLayout = $('#rmlayout').val()
  getRiskview(envName,dimName,objtName,modelLayout);
});


$('#rmlayout').change(function() {
  var envName = $('#rmenvironmentsbox').val()
  var dimName = $('#rmdimensionbox').val()
  var objtName = $('#rmobjectbox').val()
  var modelLayout = $('#rmlayout').val()
  getRiskview(envName,dimName,objtName,modelLayout);
});

$('#amconcernsbox').change(function() {
  if (window.theVisualModel == 'asset') {
    getAssetview($('#amenvironmentsbox').val());
  }
});

function getAssetview(environment){
  window.assetEnvironment = environment;
  $('#amenvironmentsbox').val(environment);
  var assetName = $('#amassetsbox').val();
  assetName = assetName == "All" ? "all" : assetName;
  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID')),
      hide_concerns: $('#amconcernsbox').find('option:selected').text() == 'Yes' ? '1' : '0'
    },
    crossDomain: true,
    url: serverIP + "/api/assets/model/environment/" + environment.replace(" ","%20") + "/asset/" + assetName.replace(" ","%20"),
    success: function(data){
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getGoalview(environment,goalName,ucName){
  window.assetEnvironment = environment;
  $('#gmenvironmentsbox').val(environment);
  if (goalName == undefined) {
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/goals/environment/" + environment.replace(" ","%20") + "/names",

      success: function (data) {
        $("#gmgoalbox").empty()
        $('#gmgoalbox').append($('<option>', {value: 'All', text: 'All'},'</option>'));
        $.each(data, function (index, item) {
          $('#gmgoalbox').append($('<option>', {value: item, text: item},'</option>'));
        });
        goalName = 'all';
      },
      error: function (xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  }
  if (ucName == undefined) {
    $("#gmusecasebox").empty()
    $('#gmusecasebox').append($('<option>', {value: 'All', text: 'All'},'</option>'));
  }
  goalName = (goalName == undefined || goalName == 'All') ? "all" : goalName;
  ucName = (ucName == undefined || ucName == 'All') ? "all" : ucName;

  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/goals/model/environment/" + environment.replace(" ","%20") + "/goal/" + goalName.replace(" ","%20") + "/usecase/" + ucName.replace(" ","%20"),
    success: function(data){
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getObstacleview(environment,obstacle){
  window.assetEnvironment = environment;
  $('#omenvironmentsbox').val(environment);

  if (obstacle == undefined) {
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/obstacles/environment/" + environment.replace(" ","%20") + "/names",

      success: function (data) {
        $("#omobstaclebox").empty()
        $('#omobstaclebox').append($('<option>', {value: 'All', text: 'All'},'</option>'));
        $.each(data, function (index, item) {
          $('#omobstaclebox').append($('<option>', {value: item, text: item},'</option>'));
        });
        obstacle = 'all';
      },
      error: function (xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  }
  obstacle = (obstacle == undefined || obstacle == 'All') ? "all" : obstacle;

  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/obstacles/model/environment/" + environment.replace(" ","%20") + "/obstacle/" + obstacle.replace(" ","%20"),
    success: function(data){
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getResponsibilityview(environment,role){
  window.assetEnvironment = environment;
  $('#remenvironmentsbox').val(environment);
  if (role == undefined) {
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: "/api/dimensions/table/role/environment/" + environment.replace(" ","%20"),
      success: function (data) {
        $("#remrolebox").empty()
        $('#remrolebox').append($('<option>', {value: 'All', text: 'All'},'</option>'));
        $.each(data, function (index, item) {
          $('#remrolebox').append($('<option>', {value: item, text: item},'</option>'));
        });
        role = 'all';
        $('#remrolebox').val('All');
      },
      error: function (xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  }
  role = (role == undefined || role == 'All') ? "all" : role;

  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/responsibility/model/environment/" + environment.replace(" ","%20") + "/role/" + role.replace(" ","%20"),
    success: function(data){
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}


function getRiskview(environment,dimName,objtName,modelLayout){
  window.assetEnvironment = environment;
  $('#rmenvironmentsbox').val(environment);
  dimName = (dimName == undefined || dimName == 'All') ? 'all' : dimName;
  objtName = (objtName == undefined || objtName == 'All') ? 'all' : objtName;
  modelLayout = modelLayout == undefined  ? "Hierarchical" : modelLayout;
  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID')),
      dimension_name : dimName,
      object_name : objtName,
      layout : modelLayout
    },
    crossDomain: true,
    url: serverIP + "/api/risks/model/environment/" + environment.replace(" ","%20"),
    success: function(data){
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getTaskview(environment,task,misusecase){
  window.assetEnvironment = environment;

  $('#tmenvironmentsbox').val(environment);
  if (task == undefined) {
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/tasks/environment/" + environment.replace(" ","%20") + "/names",

      success: function (data) {
        $("#tmtaskbox").empty()
        $('#tmtaskbox').append($('<option>', {value: 'All', text: 'All'},'</option>'));
        $.each(data, function (index, item) {
          $('#tmtaskbox').append($('<option>', {value: item, text: item},'</option>'));
        });
        task = 'all';
      },
      error: function (xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  }
  if (misusecase == undefined) {
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/dimensions/table/misusecase/environment/" + environment.replace(" ","%20"),

      success: function (data) {
        $("#tmmisusecasebox").empty()
        $('#tmmisusecasebox').append($('<option>', {value: 'All', text: 'All'},'</option>'));
        $.each(data, function (index, item) {
          $('#tmmisusecasebox').append($('<option>', {value: item, text: item},'</option>'));
        });
        task = 'all';
      },
      error: function (xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  }
  task = (task == undefined || task == 'All') ? "all" : task;
  misusecase = (misusecase == undefined || misusecase == 'All') ? "all" : misusecase;

  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/tasks/model/environment/" + environment.replace(" ","%20") + "/task/" + task.replace(" ","%20") + "/misusecase/" + misusecase.replace(" ","%20"),
    success: function(data){
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getPersonaview(pName,bvName,pcName){
  window.personaName = pName;
  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/personas/model/name/" + personaName.replace(" ","%20") + "/variable/" + bvName.replace(" ","%20") + "/characteristic/" + pcName.replace(" ","%20"),
    success: function(data){
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getLocationsView(locsName,envName){
  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/locations/model/locations/" + encodeURIComponent(locsName) + "/environment/" + encodeURIComponent(envName),
    success: function(data){
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getRisks(callback){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/risks",
    success: function (data) {
      if(jQuery.isFunction(callback)){
        callback(data);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      return null;
    }
  });
}

function getRoles(callback) {
  getDimensions('role',callback);
}

function getRolesInEnvironment(envName,callback) {
  getDimensionsInEnvironment('role',envName,callback);
}

function getAssetsInEnvironment(envName,callback) {
  getDimensionsInEnvironment('asset',envName,callback);
}


function getEnvironments(callback) {
  getDimensions('environment',callback);
}

function getDimensions(dimName,callback) {
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/" + dimName,
    success: function (data) {
      if(jQuery.isFunction(callback)){
        callback(data);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      return null;
    }
  });
}

function getDimensionsInEnvironment(dimName,envName,callback) {
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/" + dimName + "/environment/" + envName,
    success: function (data) {
      if(jQuery.isFunction(callback)){
        callback(data);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      return null;
    }
  });
}


// Dialog for choosing an asset
function assetsDialogBox(haveEnv,callback){
  var dialogwindow = $("#ChooseAssetDialog");
  var select = dialogwindow.find("select");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/assets",
    success: function (data) {
      select.empty();
      var none = true;
      $.each(data, function(key, object) {
        var found = false;
        $.each(haveEnv,function(index, text) {
          if(text == key){
            found = true
          }
        });
        //if not found in assets
        if(!found) {
          select.append("<option value=" + key + ">" + key + "</option>");
          none = false;
        }
      });
      if(!none) {
        dialogwindow.dialog({
          modal: true,
          buttons: {
            Ok: function () {
              var text =  select.find("option:selected" ).text();
              if(jQuery.isFunction(callback)){
                callback(text);
              }
              $(this).dialog("close");
            }
          }
        });
        $(".comboboxD").css("visibility", "visible");
      }
      else {
        alert("All assets are already added");
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function fileExportDialogbox(callback) {
  var dialogwindow = $("#typeOfFile");
  var select = dialogwindow.find("select");
  dialogwindow.dialog({
    modal: true,
    buttons: {
      Ok: function () {
        var text =  select.find("option:selected" ).text();
        if(jQuery.isFunction(callback)){
          callback(text);
          $("#exportFile").trigger('click')
        }
        $(this).dialog("close");
      }
    }
  });
  $(".comboboxD").css("visibility", "visible");
}

// Dialog for choosing a new role for the responses
function newRoleDialogbox(callback){
  var dialogwindow = $("#ChooseRoleForResponse");
  var roleSelect = dialogwindow.find("#theNewRole");
  var costSelect = dialogwindow.find("#theRoleCost");
  getRoles(function (roles) {
    $.each(roles, function (key, obj) {
      roleSelect.append($('<option>', { value : obj }).text(obj));
    });
  });
  dialogwindow.dialog({
    modal: true,
    buttons: {
      Ok: function () {
        var role =  roleSelect.find("option:selected" ).text();
        var cost =  costSelect.find("option:selected" ).text();
        if(jQuery.isFunction(callback)){
          var newRole =  jQuery.extend(true, {}, respRoleDefault );
          newRole.roleName = role;
          newRole.cost = cost;
          callback(newRole);
        }
        $(this).dialog("close");
      }
    }
  });
  $(".comboboxD").css("visibility", "visible");
}


// Dialog for choosing an asset in a certain environment
function assetsInEnvDialogBox(environ, haveEnv, callback){
  var dialogwindow = $("#ChooseEnvAssetsDialog");
  var select = dialogwindow.find("select");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/assets/environment/" + environ.replace(" ", "%20")+ "/names",
    success: function (data) {
      select.empty();
      var none = true;
      $.each(data, function(index1, object) {
        var found = false;
        $.each(haveEnv,function(index, text) {
          if(text == object){
            found = true
          }
        });
        if(!found) {
          select.append("<option value=" + object + ">" + object + "</option>");
          none = false;
        }
      });
      if(!none) {
        dialogwindow.dialog({
          modal: true,
          buttons: {
            Ok: function () {
              var text =  select.find("option:selected" ).text();
              if(jQuery.isFunction(callback)){
                callback(text);
              }
              $(this).dialog("close");
            }
          }
        });
        $(".comboboxD").css("visibility", "visible");
      }
      else {
        alert("All assets are already added");
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}


function environmentDialogBox(haveEnv,callback){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/all/names",
    success: function (data) {

      $("#comboboxDialogSelect").empty();
      var none = true;
      $.each(data, function(i, item) {
        var found = false;
        $.each(haveEnv,function(index, text) {
          if(text == item){
            found = true
          }
        });
        if(!found) {
          $("#comboboxDialogSelect").append("<option value=" + item + ">" + item + "</option>");
          none = false;
        }
      });
      if(!none) {
        $("#comboboxDialog").dialog({
          modal: true,
          buttons: {
            Ok: function () {
              var text =  $( "#comboboxDialogSelect").find("option:selected" ).text();
              if(jQuery.isFunction(callback)){
                callback(text);
              }
              $(this).dialog("close");
            }
          }
        });
        $(".comboboxD").css("visibility", "visible");
      }
      else {
        alert("All environments are already added");
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

// Dialog for choosing an attacker
function attackerDialogBox(hassAtt, environment ,callback){
  var dialogwindow = $("#ChooseAssetDialog");
  var select = dialogwindow.find("select");
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
      select.empty();
      var none = true;
      $.each(data, function(key, attacker) {
        var found = false;
        $.each(hassAtt,function(index, text) {
          if(text == key){
            found = true
          }
        });
        if(!found) {
          $.each(attacker.theEnvironmentProperties, function (index, prop) {
            if(prop.theEnvironmentName == environment){
              select.append("<option value=" + key + ">" + key + "</option>");
              none = false;
            }
          });
        }
      });
      if(!none) {
        dialogwindow.dialog({
          modal: true,
          buttons: {
            Ok: function () {
              var text =  select.find("option:selected" ).text();
              if(jQuery.isFunction(callback)){
                callback(text);
              }
              $(this).dialog("close");
            }
          }
        });
        $(".comboboxD").css("visibility", "visible");
      }
      else {
        alert("All possible attackers are already added");
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

// Dialog for choosing a role
function roleDialogBox(hasRole ,callback){
  var dialogwindow = $("#ChooseRoleDialog");
  var select = dialogwindow.find("select");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/roles",
    success: function (data) {
      select.empty();
      var none = true;
      $.each(data, function(key, role) {
        var found = false;
        $.each(hasRole,function(index, text) {
          if(text == key){
            found = true
          }
        });
        if(!found) {
          select.append("<option value=" + key + ">" + key + "</option>");
          none = false;
        }
      });
      if(!none) {
        dialogwindow.dialog({
          modal: true,
          buttons: {
            Ok: function () {
              var text =  select.find("option:selected" ).text();
              if(jQuery.isFunction(callback)){
                callback(text);
              }
              $(this).dialog("close");
            }
          }
        });
        $(".comboboxD").css("visibility", "visible");
      }
      else {
        alert("All possible attackers are already added");
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

// Dialog for choosing a concern
function concernDialogBox(hasRole ,callback){
  var dialogwindow = $("#ChooseConcernDialog");
  var select = dialogwindow.find("select");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/assets",
    success: function (data) {
      select.empty();
      var none = true;
      $.each(data, function(key, asset) {
        var found = false;
        $.each(hasAsset,function(index, text) {
          if(text == key){
            found = true
          }
        });
        if(!found) {
          select.append("<option value=" + key + ">" + key + "</option>");
          none = false;
        }
      });
      if(!none) {
        dialogwindow.dialog({
          modal: true,
          buttons: {
            Ok: function () {
              var text =  select.find("option:selected" ).text();
              if(jQuery.isFunction(callback)){
                callback(text);
              }
              $(this).dialog("close");
            }
          }
        });
        $(".comboboxD").css("visibility", "visible");
      }
      else {
        alert("All possible concerns are already added");
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

// Function for creating the comboboxes
function createComboboxes(){
  var sess = String($.session.get('sessionID'));
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/assets/all/names",

    success: function (data) {
      var options = $("#assetsbox");
      var amoptions = $("#amassetsbox");
      options.empty();
      amoptions.empty();
      options.append("<option>All</option>");
      amoptions.append("<option>All</option>");
      $.each(data, function () {
        options.append($("<option />").val(this).text(this));
        amoptions.append($("<option />").val(this).text(this));
      });
      $(".topCombobox").css("visibility", "visible");
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/all/names",

    success: function (data) {
      var envBox = $("#environmentsbox");
      var amEnvBox = $("#amenvironmentsbox");
      var gmEnvBox = $("#gmenvironmentsbox");
      var omEnvBox = $("#omenvironmentsbox");
      var tmEnvBox = $("#tmenvironmentsbox");
      var remEnvBox = $("#remenvironmentsbox");
      var rmEnvBox = $("#rmenvironmentsbox");
      envBox.empty();
      amEnvBox.empty();
      gmEnvBox.empty();
      omEnvBox.empty();
      tmEnvBox.empty();
      remEnvBox.empty();
      rmEnvBox.empty();
      $.each(data, function () {
        envBox.append($("<option />").val(this).text(this));
        amEnvBox.append($("<option />").val(this).text(this));
        gmEnvBox.append($("<option />").val(this).text(this));
        omEnvBox.append($("<option />").val(this).text(this));
        tmEnvBox.append($("<option />").val(this).text(this));
        remEnvBox.append($("<option />").val(this).text(this));
        rmEnvBox.append($("<option />").val(this).text(this));
      });
      envBox.css("visibility", "visible");
      window.boxesAreFilled = true;
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function startingTable(){
  createComboboxes();
  $.ajax({
    type:"GET",
    dataType: "json",
    accept:"application/json",
    crossDomain: true,
    url: serverIP + "/api/requirements",
    data: {session_id: String($.session.get('sessionID')),
      ordered: "1"
    },
    success: function(data) {
      setTableHeader("Requirements");
      createRequirementsTable(data);
      activeElement("reqTable");
      $(".loadingWrapper").fadeOut(500);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

// This is for saying which element has the main focus
function activeElement(elementid){
  if(elementid == "svgViewer" || elementid == 'homePanel'){
    $("#reqTable").hide();
    $("#objectViewer").hide();
    $("#filtercontent").hide();
    $("#filterassetmodelcontent").hide();
    $("#filterriskmodelcontent").hide();
    $("#filterresponsibilitymodelcontent").hide();
    $("#filtergoalmodelcontent").hide();
    $("#filterapmodelcontent").hide();
    $("#filtertaskmodelcontent").hide();
    $("#filterobstaclemodelcontent").hide();
    $("#rightnavGear").hide();

    if (elementid == 'svgViewer') {
      $("#rightnavGear").show();
    }

    if (window.theVisualModel == 'risk') {
      $("#filterriskmodelcontent").show();
    }
    else if (window.theVisualModel == 'goal') {
      $("#filtergoalmodelcontent").show();
    }
    else if (window.theVisualModel == 'obstacle') {
      $("#filterobstaclemodelcontent").show();
    }
    else if (window.theVisualModel == 'task') {
      $("#filtertaskmodelcontent").show();
    }
    else if (window.theVisualModel == 'responsibility') {
      $("#filterresponsibilitymodelcontent").show();
    }
    else if (window.theVisualModel == 'asset') {
      $("#filterassetmodelcontent").show();
    }
    else if (window.theVisualModel == 'persona') {
      $("#filterapmodelcontent").show();
    }
  }
  if(elementid != "svgViewer"){
    $("#svgViewer").hide();
    $("#homePanel").hide();
    $("#objectViewer").hide();
    $("#filterassetmodelcontent").hide();
    $("#filterriskmodelcontent").hide();
    $("#filtergoalmodelcontent").hide();
    $("#filtertaskmodelcontent").hide();
    $("#filterapmodelcontent").hide();
    $("#filterresponsibilitymodelcontent").hide();
    $("#filterobstaclemodelcontent").hide();
    $("#rightnavGear").hide();
  }

  if(elementid == "reqTable"){
    //If it is the table, we need to see which table it is
    window.theVisualModel = 'None';
    setActiveOptions();
  }
  if (elementid == 'objectViewer') {
    $("#reqTable").hide();
  }

  elementid = "#" + elementid;
  $(elementid).show();
}

// function for setting the table head
function setTableHeader(){
  var thead = "";

  switch (window.activeTable) {
    case "Requirements":
      debugLogger("Is Requirement");
      thead = "<th width='50px'></th><th>Requirement</th><th>Description</th><th>Priority</th><th>Rationale</th><th>Fit Citerion</th><th>Originator</th><th>Type</th>";
      break;
    case "TemplateRequirements":
      debugLogger("Is Template Requirement");
      thead = "<th width='50px' id='addTemplateRequirement'><i class='fa fa-plus floatCenter'></i></th><th>Requirement</th><th>Type</th>";
      break;
    case "TemplateGoals":
      debugLogger("Is Template Goal");
      thead = "<th width='50px' id='addTemplateGoal'><i class='fa fa-plus floatCenter'></i></th><th>Goal</th><th>Definition</th>";
      break;
    case "Goals":
      debugLogger("Is Goal");
      thead = "<th width='50px'></th><th>Goal</th><th>Definition</th><th>Category</th><th>Priority</th><th>Fit Citerion</th><th>Issue</th><th>Originator</th>";
      break;
    case "Obstacles":
      debugLogger("Is Obstacle");
      thead = "<th width='50px'></th><th>Obstacle</th><th>Definition</th><th>Category</th><th>Originator</th>";
      break;
    case "EditGoals":
      debugLogger("Is EditGoals");
      thead = "<th width='50px' id='addNewGoal'><i class='fa fa-plus floatCenter'></i></th><th>Goal</th><th>Originator</th><th>Status</th>";
      break;
    case "EditObstacles":
      debugLogger("Is EditObstacles");
      thead = "<th width='50px' id='addNewObstacle'><i class='fa fa-plus floatCenter'></i></th><th>Obstacle</th><th>Originator</th><th>Status</th>";
      break;
    case "Assets":
      debugLogger("Is Asset");
      thead = "<th width='50px' id='addNewAsset'><i class='fa fa-plus floatCenter'></i></th><th>Asset</th><th>Type</th>";
      break;
    case "TemplateAssets":
      debugLogger("Is TemplateAsset");
      thead = "<th width='50px' id='addNewTemplateAsset'><i class='fa fa-plus floatCenter'></i></th><th>Template Asset</th><th>Type</th>";
      break;
    case "Roles":
      debugLogger("Is Role");
      thead = "<th width='50px' id='addNewRole'><i class='fa fa-plus floatCenter'></i></th><th>Role</th><th>Shortcode</th><th>Type</th>";
      break;
    case "Environment":
      debugLogger("Is Environment");
      thead = "<th width='50px' id='addNewEnvironment'><i class='fa fa-plus floatCenter'></i></th><th>Environment</th><th>Description</th>";
      break;
    case "Vulnerability":
      debugLogger("Is Vulnerability");
      thead = "<th width='50px' id='addNewVulnerability'><i class='fa fa-plus floatCenter'></i></th><th>Vulnerability</th><th>Type</th>";
      break;
    case "Threats":
      debugLogger("Is Threat");
      thead = "<th width='50px' id='addNewThreat'><i class='fa fa-plus floatCenter'></i></th><th>Threat</th><th>Type</th>";
      break;
    case "Attackers":
      debugLogger("Is Attacker");
      thead = "<th width='50px' id='addNewAttacker'><i class='fa fa-plus floatCenter'></i></th><th>Attacker</th><th>Description</th>";
      break;
    case "Personas":
      debugLogger("Is Persona");
      thead = "<th width='50px' id='addNewPersona'><i class='fa fa-plus floatCenter'></i></th><th>Persona</th><th>Type</th>";
      break;
    case "Risks":
      debugLogger("Is Risk");
      thead = "<th width='50px' id='addNewRisk'><i class='fa fa-plus floatCenter'></i></th><th>Risk</th><th>Vulnerability</th><th>Threat</th>";
      break;
    case "Responses":
      debugLogger("Is Response");
      thead = "<th width='50px' id='addNewResponse'><i class='fa fa-plus floatCenter'></i></th><th>Response</th><th>Type</th>";
      break;
    case "Countermeasures":
      debugLogger("Is Countermeasure");
      thead = "<th width='50px' id='addNewCountermeasure'><i class='fa fa-plus floatCenter'></i></th><th>Countermeasure</th><th>Type</th>";
      break;
    case "Tasks":
      debugLogger("Is Task");
      thead = "<th width='50px' id='addNewTask'><i class='fa fa-plus floatCenter'></i></th><th>Task</th><th>Objective</th>";
      break;
    case "UseCases":
      debugLogger("Is UseCase");
      thead = "<th width='50px' id='addNewUseCase'><i class='fa fa-plus floatCenter'></i></th><th>Use Case</th><th>Description</th>";
      break;
    case "DomainProperties":
      debugLogger("Is Domain Property");
      thead = "<th width='50px' id='addNewDomainProperty'><i class='fa fa-plus floatCenter'></i></th><th>Domain Property</th><th>Type</th>";
      break;
    case "Dependency":
      debugLogger("Is Dependency");
      thead = "<th width='50px' id='addNewDependency'><i class='fa fa-plus floatCenter'></i></th><th>Environment</th><th>Depender</th><th>Dependee</th><th>Noun</th><th>Dependency</th>";
      break;
    case "ExternalDocuments":
      debugLogger("Is External Documents");
      thead = "<th width='50px' id='addNewExternalDocument'><i class='fa fa-plus floatCenter'></i></th><th>External Document</th><th>Description</th>";
      break;
    case "DocumentReferences":
      debugLogger("Is Document References");
      thead = "<th width='50px' id='addNewDocumentReference'><i class='fa fa-plus floatCenter'></i></th><th>Document Reference</th><th>Document</th>";
      break;
    case "PersonaCharacteristics":
      debugLogger("Is Persona Characteristics");
      thead = "<th width='50px' id='addNewPersonaCharacteristic'><i class='fa fa-plus floatCenter'></i></th><th>Persona</th><th>Variable</th><th>Characteristic</th>";
      break;
    case "ArchitecturalPatterns":
      debugLogger("Is Architectural Patterns");
      thead = "<th width='50px' id='addNewArchitecturalPattern'><i class='fa fa-plus floatCenter'></i></th><th>Model</th><th>Interfaces DER</th><th>Channels DER</th><th>Untrusted Surface DES</th>";
      break;
    case "Locations":
      debugLogger("Is Locations");
      thead = "<th width='50px' id='addNewLocations'><i class='fa fa-plus floatCenter'></i></th><th>Locations</th>";
      break;
    case "asset_value":
      debugLogger("Is Asset Value");
      thead = "<th width='50px' id='addNewValueType'><i class='fa fa-plus floatCenter'></i></th><th>Asset Value</th><th>Description</th>";
      break;
    case "asset_type":
      debugLogger("Is Asset Type");
      thead = "<th width='50px' id='addNewValueType'><i class='fa fa-plus floatCenter'></i></th><th>Asset Type</th><th>Description</th>";
      break;
    case "access_right":
      debugLogger("Is Access Right");
      thead = "<th width='50px' id='addNewValueType'><i class='fa fa-plus floatCenter'></i></th><th>Access Right</th><th>Description</th>";
      break;
    case "protocol":
      debugLogger("Is Protocol");
      thead = "<th width='50px' id='addNewValueType'><i class='fa fa-plus floatCenter'></i></th><th>Protocol</th><th>Description</th>";
      break;
    case "privilege":
      debugLogger("Is Privilege");
      thead = "<th width='50px' id='addNewValueType'><i class='fa fa-plus floatCenter'></i></th><th>Privilege</th><th>Description</th>";
      break;
    case "surface_type":
      debugLogger("Is Surface Type");
      thead = "<th width='50px' id='addNewValueType'><i class='fa fa-plus floatCenter'></i></th><th>Surface Type</th><th>Description</th>";
      break;
    case "vulnerability_type":
      debugLogger("Is Vulnerability Type");
      thead = "<th width='50px' id='addNewValueType'><i class='fa fa-plus floatCenter'></i></th><th>Vulnerability Type</th><th>Description</th>";
      break;
    case "severity":
      debugLogger("Is Severity");
      thead = "<th width='50px' id='addNewValueType'><i class='fa fa-plus floatCenter'></i></th><th>Severity</th><th>Description</th>";
      break;
    case "capability":
      debugLogger("Is Capability");
      thead = "<th width='50px' id='addNewValueType'><i class='fa fa-plus floatCenter'></i></th><th>Capability</th><th>Description</th>";
      break;
    case "motivation":
      debugLogger("Is Motivation");
      thead = "<th width='50px' id='addNewValueType'><i class='fa fa-plus floatCenter'></i></th><th>Motivation</th><th>Description</th>";
      break;
    case "threat_type":
      debugLogger("Is Threat Type");
      thead = "<th width='50px' id='addNewValueType'><i class='fa fa-plus floatCenter'></i></th><th>Threat Type</th><th>Description</th>";
      break;
    case "likelihood":
      debugLogger("Is Likelihood");
      thead = "<th width='50px' id='addNewValueType'><i class='fa fa-plus floatCenter'></i></th><th>Likelihood</th><th>Description</th>";
      break;
    case "threat_value":
      debugLogger("Is Threat Value");
      thead = "<th width='50px' id='addNewValueType'><i class='fa fa-plus floatCenter'></i></th><th>Threat Value</th><th>Description</th>";
      break;
    case "risk_value":
      debugLogger("Is Risk Value");
      thead = "<th width='50px' id='addNewValueType'><i class='fa fa-plus floatCenter'></i></th><th>Risk Value</th><th>Description</th>";
      break;
  }
  $("#reqTable").find("thead").empty();
  $("#reqTable").find("thead").append(thead);
  $("#reqTable").find("tbody").empty();
}

// This sets the right comboboxes etc in the main window
function setActiveOptions(){
  $("#filtercontent").hide();
  $("#filterassetmodelcontent").hide();
  $("#filterriskmodelcontent").hide();
  $("#filtergoalmodelcontent").hide();
  $("#filtertaskmodelcontent").hide();
  $("#filterapmodelcontent").hide();
  $("#filterobstaclemodelcontent").hide();
  $("#editAssetsOptions").hide();

  switch (window.activeTable) {
    case "Requirements":
      $("#filtercontent").show();
      break;
    case "Goals":
      break;
    case "Obstacles":
    case "Roles":
      break;
    case "EditGoals":
      break;
    case "Assets":
      $("#editAssetsOptions").show();
      break;
  }
}

function fillSvgViewer(data){

  var xmlString = (new XMLSerializer()).serializeToString(data);
  var svgDiv = $("#svgViewer");
  svgDiv.show();
  svgDiv.css("height",$("#mainContent").height());
  svgDiv.css("width","100%");
  svgDiv.html(xmlString);
  $("svg").attr("id","svg-id");
  activeElement("svgViewer");
  var panZoomInstance = svgPanZoom('#svg-id', {
    zoomEnabled: true,
    controlIconsEnabled: true,
    fit: true,
    center: true,
    minZoom: 0.2
  });
}

// finding the lowest label in the table
function findLabel() {
  var numbers = [];
  var index = 0;
  $("tbody").find("tr").each(function () {
    numbers[index] = parseInt($(this).find("td:first").text());
    index++;
  });
  numbers.sort();
  var number = numbers.length + 1;
  for(var i =0; i < numbers.length; i++){
    if(i+1 !=numbers[i]){
      return i+1;
    }
  }
  return i+1;
}

function getAllAssets(callback) {
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/assets",
    success: function (data) {
      if (jQuery.isFunction(callback)) {
        callback(data);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      return null;
    }
  });
}

function getAllAssetsInEnv(env,callback) {
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/assets/environment/" + env.replace(" ", "%20") + "/names" ,
    success: function (data) {
      if (jQuery.isFunction(callback)) {
        callback(data);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      return null;
    }
  });
}

function getAllRequirements(callback) {
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/requirements",
    success: function (data) {
      if (jQuery.isFunction(callback)) {
        callback(data);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      return null;
    }
  });
}

function sortTable(){
  var tbl = document.getElementById("reqTable").tBodies[0];
  var store = [];
  for(var i=0, len=tbl.rows.length; i<len; i++){
    var row = tbl.rows[i];
    var sortnr = parseFloat(row.cells[0].textContent || row.cells[0].innerText);
    if(!isNaN(sortnr)) store.push([sortnr, row]);
  }
  store.sort(function(x,y){
    return x[0] - y[0];
  });
  for(var i=0, len=store.length; i<len; i++){
    tbl.appendChild(store[i][1]);
  }
  store = null;
}

function sortTableByRow(rownumber){
  var tbl = document.getElementById("reqTable").tBodies[0];
  var store = [];
  for(var i=0, len=tbl.rows.length; i<len; i++){
    var row = tbl.rows[i];
    var sortnr = parseFloat(row.cells[rownumber].textContent || row.cells[rownumber].innerText);
    if(!isNaN(sortnr)) store.push([sortnr, row]);
  }
  store.sort(function(x,y){
    return x[0] - y[0];
  });
  for(var i=0, len=store.length; i<len; i++){
    tbl.appendChild(store[i][1]);
  }
  store = null;
}

function newSorting(rownr){
  var $sort = this;
  var $table = $('#reqTable');
  var $rows = $('tbody > tr',$table);
  $rows.sort(function(a, b){
    var keyA = $('td:eq('+rownr+')',a).text();
    var keyB = $('td:eq('+rownr+')',b).text();
    if($($sort).hasClass('asc')){
      return (keyA > keyB) ? 1 : 0;
    } 
    else {
      return (keyA < keyB) ? 1 : 0;
    }
  });
  $.each($rows, function(index, row){
    $table.append(row);
  });
}

function getImagedir(imageName){
  return serverIP + "/images/"+ imageName;
}

function deepEquals(o1, o2) {
  var k1 = Object.keys(o1).sort();
  var k2 = Object.keys(o2).sort();
  if (k1.length != k2.length) return false;
  return k1.zip(k2, function(keyPair) {
    if(typeof o1[keyPair[0]] == typeof o2[keyPair[1]] == "object"){
      return deepEquals(o1[keyPair[0]], o2[keyPair[1]])
    } 
    else {
      return o1[keyPair[0]] == o2[keyPair[1]];
    }
  }).all();
}

function showPopup(succes, text){
  var popup = $('.popupMessage');
  var time = 0;
  popup.css("margin-left",$(document).width()/2);

  if(succes){
    //just 5 seconds
    time = 5000;
    popup.css("width","175px");
    popup.css("height","50px");

    $(".Succes").show();
    $(".Fail").hide();
  }
  else{
    var charcount = text.length;
    charcount = charcount/47;
    time = 7000;
    popup.css("width","350px");
    popup.css("height",30*(charcount+1));
    $(".Fail").show();
    $(".Fail").find(".faultInfo").text(text);
    $(".Succes").hide();
  }
  popup.show("slide", { direction: "down" },1500).delay(time).fadeOut("slow",function(){
  });
}

function deleteObject(dimName,objtName,deleteFn) {
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    async:false,
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/object_dependency/dimension/" + dimName + "/object/" + objtName.replace(" ", "%20"),
    success: function (data) {
      if (data['theDependencies'].length == 0) {
       $("#confirmObjectDelete").data("deleteFn",deleteFn);
       $("#confirmObjectDelete").data("deleteFnParameter",objtName);
       $("#confirmObjectDelete").modal('show');
      }
      else {
        $("#objectDependencyTable").find("tbody").empty();
        $.each(data['theDependencies'], function(index,dep) {
          $("#objectDependencyTable").find("tbody").append('<tr><td>' + dep['theDimensionName'] + '</td><td>' + dep['theObjectName'] + '</td></tr>');
        });
        $("#reportObjectDependencies").data("deleteFn",deleteFn);
        $("#reportObjectDependencies").data("deleteFnParameter",objtName);
        $("#reportObjectDependencies").data("deleteFnDimension",dimName);
        $("#reportObjectDependencies").modal('show');
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function objectDependenciesDialogBox(callback){
  var dialogwindow = $("#reportObjectDependencies");
  var select = dialogwindow.find("select");
  dialogwindow.dialog({
    modal: true,
    buttons: {
      Ok: function () {
        callback(true);
        $(this).dialog("close");
      },
      Close: function () {
        callback(false);
        $(this).dialog("close");
      }
    }
  });
  $(".comboboxD").css("visibility", "visible");
}

function encodeQueryList(q,data) {
  var l = [];
  for (let d in data) {
    l.push(q + '=' + encodeURIComponent(data[d]));
  }
  return l.join('&');
}

function resetSecurityPropertyList() {
  $("#theSecurityPropertyName").find('option').remove();
  var spList = ['Confidentiality','Integrity','Availability','Accountability','Anonymity','Pseudonymity','Unobservability','Unlinkability'];
  $.each(spList,function(idx,spValue) {
    $("#theSecurityPropertyName").append('<option value="' + spValue + '">' + spValue + '</option>');
  });
}

$("#chooseSecurityProperty").on('shown.bs.modal', function() {
  var cmd = eval($("#chooseSecurityProperty").attr("data-updatepropertylist"));
  cmd();
});

$("#chooseSecurityProperty").on('click', '#saveSecurityProperty',function(e) {
  var cmd = eval($("#chooseSecurityProperty").attr("data-buildproperty"));
  cmd(e);
});

$("#confirmObjectDelete").on('click', '#confirmDelete',function(e) {
  var cmd = $("#confirmObjectDelete").data("deleteFn");
  var cmdParameter = $("#confirmObjectDelete").data("deleteFnParameter");
  cmd(cmdParameter);
  $("#confirmObjectDelete").modal('hide');
});

$("#reportObjectDependencies").on('click', '#confirmODDelete',function(e) {
  var dimName = $("#reportObjectDependencies").data("deleteFnDimension");
  var objtName = $("#reportObjectDependencies").data("deleteFnParameter");
  $.ajax({
    type: "DELETE",
    dataType: "json",
    accept: "application/json",
    async:false,
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/object_dependency/dimension/" + dimName + "/object/" + objtName.replace(" ", "%20"),
    success: function (data) {
      var deleteFn = $("#reportObjectDependencies").data("deleteFn");
      deleteFn(objtName);
      $("#reportObjectDependencies").modal('hide');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$(document).on('shown.bs.modal','#addInterfaceDialog',function() {
  var selectedInt = $('#addInterfaceDialog').attr('data-selectedInterface');
  if (selectedInt != undefined) {
    selectedInt = JSON.parse(selectedInt);
    $('#AddInterface').text('Update');
    $('#theInterfaceName').val(selectedInt.theName);
    $('#theInterfaceType').val(selectedInt.theType);
  }
  else {
    $('#theInterfaceName').val('');
    $('#theInterfaceType').val('');
    $('#AddInterface').text('Add');
  }

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/access_right",
    success: function (accessRights) {
      $("#theAccessRight option").remove();
      $.each(accessRights,function(idx,accessRight) {
        $('#theAccessRight').append($("<option></option>").attr("value",accessRight).text(accessRight));
      });
      if (selectedInt != undefined) {
        $('#theAccessRight').val(selectedInt.theAccessRight);
      }
      else {
        $('#theAccessRight').val('');
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/privilege",
    success: function (privileges) {
      $("#thePrivilege option").remove();
      $.each(privileges,function(idx,privilege) {
        $('#thePrivilege').append($("<option></option>").attr("value",privilege).text(privilege));
      });
      if (selectedInt != undefined) {
        $('#thePrivilege').val(selectedInt.thePrivilege);
      }
      else {
        $('#thePrivilege').val('');
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

$("#addInterfaceDialog").on('click', '#AddInterface',function(e) {
  var cmd = eval($("#addInterfaceDialog").attr("data-updateinterface"));
  cmd(e);
});


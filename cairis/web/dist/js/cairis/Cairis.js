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
        $.session.set("sessionID", data.session_id);
        refreshHomeBreadCrumb();
//        summaryTables();
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
    summaryTables();
    hideLoading();
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
  getGoalview($('#gmenvironmentsbox').val(),selection,$('#gmusecasebox').val());
});

$('#gmusecasebox').change(function() {
  var selection = $(this).find('option:selected').text();
  getGoalview($('#gmenvironmentsbox').val(),$('#gmgoalbox').val(),selection);
});



$('#tmtaskbox').change(function() {
  var selection = $(this).find('option:selected').text();
  var envName = $('#tmenvironmentsbox').val();
  var mcName = $('#tmmisusecasebox').val();
  getTaskview(envName,selection,mcName);
});

$('#tmmisusecasebox').change(function() {
  var selection = $(this).find('option:selected').text();
  var taskName = $('#tmtaskbox').val();
  getTaskview($('#tmenvironmentsbox').val(),taskName,selection);
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
  getPersonaView(selection,'All','All');
});

$('#apbtbox').change(function() {
  var selection = $(this).find('option:selected').text();
  var pName = $('#appersonasbox').val();
  appendPersonaCharacteristics(pName,selection,'All');
  getPersonaView(pName,selection,'All');
});

$('#apcharacteristicbox').change(function() {
  var selection = $(this).find('option:selected').text();
  var pName = $('#appersonasbox').val();
  var bvName = $('#apbtbox').val();
  appendPersonaCharacteristics(pName,bvName,'All');
  getPersonaView(pName,bvName,selection);
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
    url: serverIP + "/api/personas/characteristics/name/" + encodeURIComponent(pName) + "/variable/" + encodeURIComponent(bvName) + "/characteristic/" + encodeURIComponent(pcName),
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
  if (window.theVisualModel == 'goal') {
    var envName = $('#gmenvironmentsbox').val();
    refreshDimensionSelector($('#gmgoalbox'),'goal',envName,function() {
      refreshDimensionSelector($('#gmusecasebox'),'usecase',envName,function() {
        $('#gmenvironmentsbox').val(envName);
        $('#gmgoalbox').val('All');
        $('#gmusecasebox').val('All');
        getGoalview(envName,'All','All');
      });
    });
  }
});

$('#aparchitecturalpatternsbox').change(function() {
  var selection = $(this).find('option:selected').text();
  getArchitecturalPatternView(selection);
});




$('#tmenvironmentsbox').change(function() {
  var envName = $(this).find('option:selected').text();
  refreshDimensionSelector($('#tmtaskbox'),'task',envName,function() {
    refreshDimensionSelector($('#tmmisusecasebox'),'misusecase',envName,function() {
      $('#tmtaskbox').val('All');
      $('#tmmisusecasebox').val('All');
      getTaskview(envName,'all','all');
    });
  });
});


$('#omenvironmentsbox').change(function() {
  var envName = $(this).find('option:selected').text();
  refreshDimensionSelector($('#omobstaclebox'),'obstacle',envName,function() {
    $('#omenvironmentsbox').val(envName);
    $('#omobstaclebox').val('All');
    getObstacleview(envName,'All');
  });
});

$('#remenvironmentsbox').change(function() {
  var envName = $(this).find('option:selected').text();
  refreshDimensionSelector($('#remrolebox'),'role',envName,function() {
    $('#remenvironmentsbox').val(envName);
    $('#remrolebox').val('All');
    getResponsibilityview(envName,'All');
  });
});



$('#rmenvironmentsbox').change(function() {
  var envName = $(this).find('option:selected').val();
  $('#rmenvironmentsbox').val(envName);
  $('#rmdimensionbox').val('All');
  $('#rmobjectbox').empty();
  var modelLayout = $('#rmlayout').val();
  getRiskview(envName,'all','all',modelLayout);
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
  refreshDimensionSelector($('#rmobjectbox'),dimName,envName,function() {
    getRiskview(envName,dimName,'all',modelLayout);
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

$('#amenvironmentsbox').change(function() {
  if (window.theVisualModel == 'asset') {
    var envName = $('#amenvironmentsbox').val();
    refreshDimensionSelector($('#amassetsbox'),'asset',envName,function() {
      $('#amenvironmentsbox').val(envName);
      getAssetview(envName);
    });
  }
});



$('#cmenvironmentsbox').change(function() {
  var envName = $('#cmenvironmentsbox').val()
  refreshDimensionSelector($('#cmrequirementsbox'),'requirement',envName,function() {
    $('#cmenvironmentsbox').val(envName);
    $('#cmrequirementsbox').val('All')
    getRequirementView(envName,'All');
  });
});

$('#cmrequirementsbox').change(function() {
  if (window.theVisualModel == 'requirement') {
    var envName = $('#cmenvironmentsbox').val()
    var reqName = $('#cmrequirementsbox').val()
    getRequirementView(envName,reqName);
  }
});

$('#amassetsbox').change(function() {
  if (window.theVisualModel == 'asset') {
    getAssetview($('#amenvironmentsbox').val());
  }
});

function getAssetview(environment){
  $('#menuBCClick').attr('dimension','model');
  refreshMenuBreadCrumb('model');
  window.assetEnvironment = environment;
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
    url: serverIP + "/api/assets/model/environment/" + encodeURIComponent(environment) + "/asset/" + encodeURIComponent(assetName),
    success: function(data){
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getArchitecturalPatternView(apName){
  $('#menuBCClick').attr('dimension','model');
  refreshMenuBreadCrumb('model');
  $('#aparchitecturalpatternsbox').val(apName);
  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/architectural_patterns/component/model/" + encodeURIComponent(apName),
    success: function(data){
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}


function getMisusabilityView(mcName,tcName){
//  $('#mmmisusabilitycasesbox').val(mcName);
  if (tcName == undefined) {
    tcName = 'All'
  }
  tcName = tcName == "All" ? "all" : tcName;

  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/tasks/model/misusability/" + encodeURIComponent(mcName) + "/characteristic/" + encodeURIComponent(tcName),
    success: function(data){
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

$('#mmtaskcharacteristicsbox').change(function() {
  if (window.theVisualModel == 'misusability') {
    getMisusabilityView($('#mmmisusabilitycasesbox').val(),$('#mmtaskcharacteristicsbox').val());
  }
});

$('#mmmisusabilitycasesbox').change(function() {
  var mcName = $(this).find('option:selected').val();
  $('#mmtaskcharacteristicsbox').val('All');
  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/task_characteristic/environment/" + encodeURIComponent(mcName),
    success: function(data) {
      fillObjectBox('#mmtaskcharacteristicsbox','All',data);
      $('#mmtaskcharacteristicsbox').val('All');
      getMisusabilityView(mcName,'All');
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});



function getGoalview(environment,goalName,ucName){
  $('#menuBCClick').attr('dimension','model');
  refreshMenuBreadCrumb('model');
  window.assetEnvironment = environment;
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
  $('#menuBCClick').attr('dimension','model');
  refreshMenuBreadCrumb('model');
  window.assetEnvironment = environment;
  obstacle = (obstacle == undefined || obstacle == 'All') ? "all" : obstacle;

  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/obstacles/model/environment/" + encodeURIComponent(environment) + "/obstacle/" + encodeURIComponent(obstacle),
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
  $('#menuBCClick').attr('dimension','model');
  refreshMenuBreadCrumb('model');
  window.assetEnvironment = environment;
  role = (role == undefined || role == 'All') ? "all" : role;
  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/responsibility/model/environment/" + encodeURIComponent(environment) + "/role/" + encodeURIComponent(role),
    success: function(data){
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getRequirementLabels(data) {
  var lbls = [];
  d3.select(data).selectAll('a').each(function(d) {
    if (((d3.select(this).attr('xlink:href').indexOf('/api/requirements/shortcode') >= 0) && (d3.select(this).attr('xlink:title') != null)) || ((d3.select(this).attr('xlink:href').indexOf('/api/requirements/name') >= 0) && (d3.select(this).attr('xlink:title') != null)))  {
      lbls.push(d3.select(this).attr('xlink:title'));
      d3.select(this).attr('class','requirement');
    }
  });
  return lbls;
}

function getRequirementScores(lbls) {

  var IMPERATIVES = ['shall','must','is required to','are applicable','are to','responsible for','will','should'];
  var OPTIONS = ['can','may','optionally'];
  var WEAKPHRASES = ['adequate','as appropriate','be able to','be capable of','capability of','capability to','effective','as required','normal','provide for','timely','easy to'];
  var FUZZY = ['mostly','as needed','might','make sense','appropriate','might make sense','graceful','at minimum','major','slowly','may be of use','including but not limited to','and/or','suitable','various','clean and stable interface','several'];
  var INCOMPLETES = ['TBD','TBS','TBE','TBC','TBR','not defined','not determined','but not limited to','as a minimum','None']

  var reqDict = {};
  $.each(lbls,function(idx,reqLabel) {
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      async: false,
      url: serverIP + "/api/requirements/name/" + encodeURIComponent(reqLabel),
      success: function (req) {
        var reqDesc = req.theDescription;
        var reqRat = req.attrs.rationale;
        var reqFC = req.attrs.fitCriterion;
        var reqOrig = req.attrs.originator;
       
        var completeScore = 0;
        if (reqDesc == '') {
          completeScore += 1;
        }
        if (reqRat == '') {
          completeScore += 1;
        }
        if (reqFC == '') {
          completeScore += 1;
        }
        if (reqOrig == '') {
          completeScore += 1;
        }
        $.each(INCOMPLETES,function(idx,w) {
          if (reqDesc.indexOf(w) >= 0) {
            completeScore += 1;
          }
          if (reqRat.indexOf(w) >= 0) {
            completeScore += 1;
          }
          if (reqFC.indexOf(w) >= 0) {
            completeScore += 1;
          }
          if (reqOrig.indexOf(w) >= 0) {
            completeScore += 1;
          }
        });

        var impScore = 0;
        $.each(IMPERATIVES,function(idx,w) {
          if (reqDesc.indexOf(w) > 0) {
            impScore += 1;
          }
        });

        var ambScore = 0;
        $.each(OPTIONS.concat(WEAKPHRASES).concat(FUZZY),function(idx,w) {
          if (reqDesc.indexOf(w) > 0) {
            ambScore += 1;
          }
        });

        var scObjt = {};
        if (completeScore == 0) {
          scObjt.completeness = 2;
        }
        else if (completeScore == 1) {
          scObjt.completeness = 0;
        }
        else {
          scObjt.completeness = -2;
        }

        if (impScore == 0) {
          scObjt.imperative = [1,1];
        }
        else {
          scObjt.imperative = [1.5,0.5];
        }
 
        if (ambScore == 0) {
          scObjt.ambiguity = 2;
        }
        else if (ambScore < 2) {
          scObjt.ambiguity = 0;
        }
        else {
          scObjt.ambiguity = -2;
        }
        reqDict[reqLabel] = scObjt;
      },
      error: function (xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  });
  return reqDict;
}

function replaceRequirementNodes(data,reqDict) {

  d3.select(data).selectAll('a').each(function(d) {
    if (((d3.select(this).attr('xlink:href').indexOf('/api/requirements/shortcode') >= 0) && (d3.select(this).attr('xlink:title') != null)) || ((d3.select(this).attr('xlink:href').indexOf('/api/requirements/name') >= 0) && (d3.select(this).attr('xlink:title') != null))) {
      var reqLabel = d3.select(this).attr('xlink:title');

      var labelY = d3.select(this).selectAll('text').attr('y');
      d3.select(this).selectAll('text').attr('y',labelY - 30);

      var cxi = d3.select(this).select('ellipse').attr('cx');
      var cyi = d3.select(this).select('ellipse').attr('cy');
      var ri = 25;
      d3.select(this).select('ellipse').remove();
      var svg = d3.select(this).attr("id","face" + reqLabel);
      var c = d3.chernoff()
          .xloc(function(d) { return d.cx; })
          .yloc(function(d) { return d.cy; })
          .frad(function(d) { return d.r; })
          .mouth(function(d) { return d.m; })
          .eyew(function(d) { return d.ew; })
          .eyeh(function(d) { return d.eh; })
          .brow(function(d) { return d.b; });

      var scObjt = reqDict[reqLabel];
      var dat = [{cx: cxi, cy: cyi, r: ri, m: scObjt.ambiguity, ew: scObjt.imperative[1], eh: scObjt.imperative[0], b: scObjt.completeness, face: svg}];

      svg.selectAll("g.chernoff").data(dat).enter()
         .append("svg:g")
         .attr("class", "chernoff")
         .call(c);
    }
  });
}

function getRiskview(environment,dimName,objtName,modelLayout){
  $('#menuBCClick').attr('dimension','model');
  refreshMenuBreadCrumb('model');
  window.assetEnvironment = environment;
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
      var lbls = getRequirementLabels(data);
      var reqDict = getRequirementScores(lbls);
      replaceRequirementNodes(data,reqDict);
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getRequirementView(environment,reqName){
  $('#menuBCClick').attr('dimension','model');
  refreshMenuBreadCrumb('model');
  window.assetEnvironment = environment;
  reqName = (reqName == undefined || reqName == 'All') ? 'all' : reqName;
  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID')),
    },
    crossDomain: true,
    url: serverIP + "/api/requirements/model/environment/" + encodeURIComponent(environment) + "/requirement/" + encodeURIComponent(reqName),
    success: function(data){
      var lbls = getRequirementLabels(data);
      var reqDict = getRequirementScores(lbls);
      replaceRequirementNodes(data,reqDict);
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}


function getTaskview(environment,task,misusecase){
  $('#menuBCClick').attr('dimension','model');
  refreshMenuBreadCrumb('model');
  window.assetEnvironment = environment;
  task = (task == undefined || task == 'All') ? "all" : task;
  misusecase = (misusecase == undefined || misusecase == 'All') ? "all" : misusecase;

  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/tasks/model/environment/" + encodeURIComponent(environment) + "/task/" + encodeURIComponent(task) + "/misusecase/" + encodeURIComponent(misusecase),
    success: function(data){
      fillSvgViewer(data);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getPersonaView(pName,bvName,pcName){
  $('#menuBCClick').attr('dimension','model');
  refreshMenuBreadCrumb('model');
  window.personaName = pName;
  $('#appersonasbox').val(pName);
  $.ajax({
    type:"GET",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/personas/model/name/" + encodeURIComponent(personaName) + "/variable/" + encodeURIComponent(bvName) + "/characteristic/" + encodeURIComponent(pcName),
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
  $('#menuBCClick').attr('dimension','model');
  refreshMenuBreadCrumb('model');
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


function refreshDimensionSelector(sBox,dimName,envName,callback,filterList) {
  var urlText = serverIP + "/api/dimensions/table/" + dimName;
  if (envName != undefined) {
    urlText += '/environment/' + envName
  }
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: urlText,
    success: function (data) {
      data.sort();
      sBox.empty();
      if ((dimName == 'asset' && filterList == undefined) || (dimName == 'goal' && filterList == undefined) || (dimName == 'obstacle' && filterList == undefined) || (dimName == 'task' && filterList == undefined) || (dimName == 'usecase' && filterList == undefined) || (dimName == 'misusecase' && filterList == undefined) || (dimName == 'requirement' && filterList == undefined)) {
        sBox.append("<option>All</option>");
      }
      if (filterList != undefined) {
        data = data.filter(x => filterList.indexOf(x) < 0);
      }
      if (data.length == 0 && filterList != undefined) {
        alert('All ' + dimName + 's have already been added.');
      }
      else {
        $.each(data, function () {
          sBox.append($("<option />").val(this).text(this));
        });
        if (callback != undefined) {
          callback();
        }
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function refreshSpecificSelector(sBox,urlPrefix,callback,filterList) {
  var urlText = serverIP + urlPrefix;
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: urlText,
    success: function (data) {
      data.sort();
      sBox.empty();
      if (filterList != undefined) {
        data = data.filter(x => filterList.indexOf(x) < 0);
      }
      if (data.length == 0 && filterList != undefined) {
        alert('All ' + dimName + 's have already been added.');
      }
      else {
        $.each(data, function () {
          sBox.append($("<option />").val(this).text(this));
        });
        if (callback != undefined) {
          callback();
        }
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function requirementsTable(dimName){
  refreshDimensionSelector($('#assetsbox'),'asset',undefined,function(){
    refreshDimensionSelector($('#environmentsbox'),'environment',undefined,function(){
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
          $(".topCombobox").css("visibility", "visible");
          $('#environmentsbox').css("visibility", "visible");
          $(".loadingWrapper").fadeOut(500);
        },
        error: function(xhr, textStatus, errorThrown) {
          debugLogger(String(this.url));
          debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
      });
    });
  });
}

function summaryTables() {
  activeElement("homePanel");
  refreshDimensionSelector($('#summaryenvironmentsbox'),'environment',undefined,function() {
    activeElement("homePanel");
    $('#summaryenvironmentsbox').change();
    $(".loadingWrapper").fadeOut(500);
  });
}


// This is for saying which element has the main focus
function activeElement(elementid){
  if(elementid == "svgViewer" || elementid == 'homePanel'){
    $("#mainTable").hide();
    $("#objectViewer").hide();
    $("#filterrequirementscontent").hide();
    $("#filtersummarytables").hide();
    $("#filterassetmodelcontent").hide();
    $("#filterriskmodelcontent").hide();
    $("#filterresponsibilitymodelcontent").hide();
    $("#filtergoalmodelcontent").hide();
    $("#filterapmodelcontent").hide();
    $("#filtertaskmodelcontent").hide();
    $("#filterobstaclemodelcontent").hide();
    $("#filterconceptmapmodelcontent").hide();
    $("#filterarchitecturalpatternmodelcontent").hide();
    $("#filtermisusabilitymodelcontent").hide();
    $("#rightnavGear").hide();

    if (elementid == 'svgViewer') {
      $('#homePanel').hide();
      $("#rightnavGear").show();
    }


    if (window.theVisualModel == 'risk') {
      $("#filterriskmodelcontent").show();
    }
    if (window.theVisualModel == 'requirement') {
      $("#filterconceptmapmodelcontent").show();
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
    else if (window.theVisualModel == 'architectural_pattern') {
      $("#filterarchitecturalpatternmodelcontent").show();
    }
    else if (window.theVisualModel == 'misusability') {
      $("#filtermisusabilitymodelcontent").show();
    }
  }
  if(elementid != "svgViewer"){
    $("#svgViewer").hide();
    $('#homePanel').hide();
    $("#filtersummarytables").hide();
    $("#objectViewer").hide();
    $("#filterassetmodelcontent").hide();
    $("#filterriskmodelcontent").hide();
    $("#filtergoalmodelcontent").hide();
    $("#filtertaskmodelcontent").hide();
    $("#filterapmodelcontent").hide();
    $("#filterresponsibilitymodelcontent").hide();
    $("#filterobstaclemodelcontent").hide();
    $("#filterconceptmapmodelcontent").hide();
    $("#filterarchitecturalpatternmodelcontent").hide();
    $("#filtermisusabilitymodelcontent").hide();
    $("#rightnavGear").hide();
  }

  if(elementid == "mainTable"){
    //If it is the table, we need to see which table it is
    window.theVisualModel = 'None';
    $("#filterrequirementscontent").hide();
  }
  if(elementid == "reqTable"){
    //If it is the table, we need to see which table it is
    window.theVisualModel = 'None';
    $("#filterrequirementscontent").show();
    elementid = 'mainTable'
  }

  if (elementid == 'objectViewer') {
    $("#mainTable").hide();
  }

  if (elementid == 'homePanel') {
    $("#mainTable").hide();
    $("#filtersummarytables").show();
  }

  elementid = "#" + elementid;
  $(elementid).show();
}

// function for setting the table head
function setTableHeader(activeTable){
  var thead = "";

  switch (activeTable) {
    case "Requirements":
      debugLogger("Is Requirement");
      thead = "<th width='50px' id='addReqMenu'><i class='fa fa-plus floatCenter'></i></th></th><th>Requirement</th><th>Description</th><th>Priority</th><th>Rationale</th><th>Fit Citerion</th><th>Originator</th><th>Type</th>";
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
      thead = "<th width='50px'></th><th>Obstacle</th><th>Definition</th><th>Originator</th>";
      break;
    case "EditGoals":
      debugLogger("Is EditGoals");
      thead = "<th width='50px' id='addNewGoal'><i class='fa fa-plus floatCenter'></i></th><th>Goal</th><th>Originator</th><th>Status</th>";
      break;
    case "EditObstacles":
      debugLogger("Is EditObstacles");
      thead = "<th width='50px' id='addNewObstacle'><i class='fa fa-plus floatCenter'></i></th><th>Obstacle</th><th>Originator</th>";
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
    case "ConceptReferences":
      debugLogger("Is Concept References");
      thead = "<th width='50px' id='addNewConceptReference'><i class='fa fa-plus floatCenter'></i></th><th>Concept Reference</th><th>Dimension</th>";
      break;
    case "PersonaCharacteristics":
      debugLogger("Is Persona Characteristics");
      thead = "<th width='50px' id='addNewPersonaCharacteristic'><i class='fa fa-plus floatCenter'></i></th><th>Persona</th><th>Variable</th><th>Characteristic</th>";
      break;
    case "TaskCharacteristics":
      debugLogger("Is Task Characteristics");
      thead = "<th width='50px' id='addNewTaskCharacteristic'><i class='fa fa-plus floatCenter'></i></th><th>Task</th><th>Characteristic</th>";
      break;
    case "ArchitecturalPatterns":
      debugLogger("Is Architectural Patterns");
      thead = "<th width='50px' id='addNewArchitecturalPattern'><i class='fa fa-plus floatCenter'></i></th><th>Model</th><th>Interfaces DER</th><th>Channels DER</th><th>Untrusted Surface DES</th>";
      break;
    case "SecurityPatterns":
      debugLogger("Is Security Patterns");
      thead = "<th width='50px' id='addNewSecurityPattern'><i class='fa fa-plus floatCenter'></i></th><th>Security Pattern</th>";
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
  $("#mainTable").find("thead").empty();
  $("#mainTable").find("thead").append(thead);
  $("#mainTable").find("tbody").empty();
}

function fillSvgViewer(data){

  var xmlString = (new XMLSerializer()).serializeToString(data);
  var svgDiv = $("#svgViewer");
  svgDiv.show();
  svgDiv.css("height","100%");
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
  var tbl = document.getElementById("mainTable").tBodies[0];
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
  var tbl = document.getElementById("mainTable").tBodies[0];
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
  var $table = $('#mainTable');
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

function encodeQueryList(q,data) {
  var l = [];
  for (let d in data) {
    l.push(q + '=' + encodeURIComponent(data[d]));
  }
  return l.join('&');
}

function resetSecurityPropertyList() {
  $('#theSecurityPropertyValue').val('None');
  $('#theSecurityPropertyRationale').val('');
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

function traceExplorer(objtType,objtName,is_from) {
  $('#traceExplorer').attr('data-objtType',objtType);
  $('#traceExplorer').attr('data-objtName',objtName);
  $('#traceExplorer').attr('data-is_from',is_from);
  $('#traceExplorer').modal('show');
}

$("#traceExplorer").on('shown.bs.modal', function() {
  $('#dimensionTable').find('tbody').empty();
  $('#valueTable').find('tbody').empty();
  var objtType = $('#traceExplorer').attr('data-objtType');
  var isFrom = $('#traceExplorer').attr('data-is_from');

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/traces/dimensions/" + objtType + "/is_from/" + isFrom,
    success: function (dims) {
      $.each(dims,function(idx,dim) {
        appendTraceDimension(dim);
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

function appendTraceDimension(dim) {
  $('#dimensionTable').find("tbody").append('<tr class="clickable-row"><td class="trace-dimension">' + dim + '</td></tr>');
}

$('#dimensionTable').on('click', '.clickable-row', function(event) {
 if($(this).hasClass('bg-primary')){
   $(this).removeClass('bg-primary'); 
 } 
 else {
   $(this).addClass('bg-primary').siblings().removeClass('bg-primary');
 }
});

$('#traceExplorer').on('click',"td.trace-dimension", function() {
  $('#valueTable').find('tbody').empty();
  var dimName = $(this).closest("tr").find('td:eq(0)').text();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/" + dimName,
    success: function (vs) {
      $.each(vs,function(idx,v) {
        appendTraceValue(v);
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

function appendTraceValue(tValue) {
  $('#valueTable').find("tbody").append('<tr class="clickable-row"><td>' + tValue + '</td></tr>');
}

$('#valueTable').on('click', '.clickable-row', function(event) {
 if($(this).hasClass('bg-primary')){
   $(this).removeClass('bg-primary'); 
 } 
 else {
   $(this).addClass('bg-primary').siblings().removeClass('bg-primary');
 }
});

$("#traceExplorer").on('click', '#AddTrace',function(e) {
  var fromObjt = $('#traceExplorer').attr('data-objtType');
  var fromName = $('#traceExplorer').attr('data-objtName')
  var toObjt = $('#dimensionTable').find("tr.bg-primary").text();
  var toName = $('#valueTable').find("tr.bg-primary").text();

  var postUrl = serverIP + "/api/traces"
  var isFrom = $('#traceExplorer').attr('data-is_from');
  var tr = {};
  if (isFrom == '1') {
    tr.theFromObject = fromObjt;
    tr.theFromName = fromName;
    tr.theToObject = toObjt;
    tr.theToName = toName;
  }
  else {
    tr.theFromObject = toObjt;
    tr.theFromName = toName;
    tr.theToObject = fromObjt;
    tr.theToName = fromName;
  }

  var output = {};
  output.object = tr;
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
    url: serverIP + "/api/traces" + "?session_id=" + $.session.get('sessionID'),
    success: function (data) {
      $('#traceExplorer').modal('hide');
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

$("#chooseEnvironment").on('shown.bs.modal', function() {
  $('#chooseTitle').text('Choose the ' + $('#chooseEnvironment').attr('data-chooseDimension') );
});

$("#chooseEnvironment").on('click', '#chooseEnvironmentButton',function(e) {
  if ($('#chooseEnvironment').attr('data-chooseDimension') == 'persona') {
    refreshDimensionSelector($('#appersonasbox'),'persona',undefined,function() {
      getPersonaView($('#chooseEnvironmentSelect').val(),'All','All');
    });
  }
  else if ($('#chooseEnvironment').attr('data-chooseDimension') == 'misusability case') {
    var mcName = $('#chooseEnvironmentSelect').val();
    $.ajax({
      type:"GET",
      accept:"application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/dimensions/table/task_characteristic/environment/" + encodeURIComponent(mcName),
      success: function(data) {
        fillObjectBox('#mmtaskcharacteristicsbox','All',data);
        $('#mmtaskcharacteristicsbox').val('All');
        getMisusabilityView(mcName,'All');
      },
      error: function(xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  }
  else {
    $('#chooseEnvironment').attr('data-chosenDimension',$('#chooseEnvironmentSelect').val());
    var cmd = eval($("#chooseEnvironment").attr("data-applyEnvironmentSelection"));
    cmd($('#chooseEnvironmentSelect').val());
  }
  $('#chooseEnvironment').modal('hide');
});

function getNoOfRisks(callback) {
  $.ajax({
    type:"GET",
    dataType: "json",
    accept:"application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/risk",
    success: function(data) {
      callback(data.length);
    },
    error: function(xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

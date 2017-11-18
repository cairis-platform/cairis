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

$("#trustBoundariesMenuClick").click(function(){
  validateClick('trust_boundary',function() {
    $('#menuBCClick').attr('dimension','trust_boundary');
    refreshMenuBreadCrumb('trust_boundary');
  });
});

function createTrustBoundariesTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/trust_boundaries",
    success: function (data) {
      var tbs = [];
      setTableHeader("TrustBoundaries");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;
      var tbi = 0;

      $.each(data, function(count, item) {
        tbs[tbi] = item;
        textToInsert[i++] = "<tr>";
        var itemKey = item.theName;
        textToInsert[i++] = '<td class="deleteTrustBoundaryButton"><i class="fa fa-minus" value="' + itemKey + '"></i></td>';

        textToInsert[i++] = '<td class="trustboundary-rows" name="theName" value="' + item.theName + '">';
        textToInsert[i++] = item.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="trustboundary-rows" name="theDescription" value="' + item.theDescription + '">';
        textToInsert[i++] = item.theDescription;
        textToInsert[i++] = '</td>';
        textToInsert[i++] = '</tr>';
        tbi += 1;
      });
      $.session.set("TrustBoundaries",JSON.stringify(tbs));
      theTable.append(textToInsert.join(''));

      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.trustboundary-rows'));
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
  });
}

$(document).on('click', "td.trustboundary-rows", function(){
  activeElement("objectViewer");
  var tbs = JSON.parse($.session.get("TrustBoundaries"));
  var tb = tbs[$(this).closest('tr').index()];
  $.session.set("TrustBoundary", JSON.stringify(tb));

  fillOptionMenu("fastTemplates/editTrustBoundaryOptions.html","#objectViewer",null,true,true, function(){
    $('#editTrustBoundaryOptionsForm').validator();
    $('#UpdateTrustBoundary').text("Update");
    $('#theTrustBoundaryName').val(tb.theName);
    $('#theTrustBoundaryDescription').val(tb.theDescription);

    $.each(tb.theEnvironmentProperties, function (index, envprop) {
      appendTrustBoundaryEnvironment(envprop.theName);
    });
    $("#theTrustBoundaryEnvironments").find(".trustBoundaryEnvironmentProperties:first").trigger('click');
    $.session.set("TrustBoundaryEnvironmentName", $("#theTrustBoundaryEnvironments").find(".trustBoundaryEnvironmentProperties:first").text());
  });
});
    
function appendTrustBoundaryEnvironment(text) {
  $("#theTrustBoundaryEnvironments").append("<tr class='clickable-environments'><td class='deleteTrustBoundaryEnvironment'><i class='fa fa-minus'></i></td><td class='trustBoundaryEnvironmentProperties'>" + text + "</td></tr>");

}


function appendTrustBoundaryComponent(tbComponent) {
  $("#theTrustBoundaryComponents").find("tbody").append("<tr><td class='removeTrustBoundaryComponent'><i class='fa fa-minus'></i></td><td class='trustboundary-component'>" + tbComponent.theName + "</td><td>" + tbComponent.theType + "</td></tr>").animate('slow');
}

var mainContent = $("#objectViewer");

function commitTrustBoundary() {
  var tb = JSON.parse($.session.get("TrustBoundary"));
  var oldTbName = tb.theName;
  tb.theName = $("#theTrustBoundaryName").val();
  tb.theDescription = $("#theTrustBoundaryDescription").val();

  if($("#editTrustBoundaryOptionsForm").hasClass("new")){
    postTrustBoundary(tb, function () {
      $("#editTrustBoundaryOptionsForm").removeClass("new")
      $('#menuBCClick').attr('dimension','trust_boundary');
      refreshMenuBreadCrumb('trust_boundary');
    });
  }
  else {
    putTrustBoundary(tb, oldTbName,  function () {
      $('#menuBCClick').attr('dimension','trust_boundary');
      refreshMenuBreadCrumb('trust_boundary');
    });
  }
}

$(document).on("click", "#addNewTrustBoundary", function () {
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editTrustBoundaryOptions.html", "#objectViewer", null, true, true, function () {
    $('#editTrustBoundaryOptionsForm').validator();
    $('#UpdateTrustBoundary').text("Create");
    $("#editTrustBoundaryOptionsForm").addClass("new");
    $('#theTrustBoundaryName').val('');
    $('#theTrustBoundaryDescription').val('');
    $("#trustBoundariesTabID").hide();
    $.session.set("TrustBoundary", JSON.stringify(jQuery.extend(true, {},trustBoundaryDefault )));
    $('#editTrustBoundaryOptionsForm').loadJSON(trustBoundaryDefault, null);
  });
});

$(document).on('click', 'td.deleteTrustBoundaryButton', function (e) {
  e.preventDefault();
  var tbs = JSON.parse($.session.get("TrustBoundaries"));
  var tb = tbs[$(this).index()];
  deleteTrustBoundary(tb, function () {
    $('#menuBCClick').attr('dimension','trust_boundary');
    refreshMenuBreadCrumb('trust_boundary');
  });
});

mainContent.on('click', '#CloseTrustBoundary', function (e) {
  e.preventDefault();
  $('#menuBCClick').attr('dimension','trust_boundary');
  refreshMenuBreadCrumb('trust_boundary');
});

function deleteTrustBoundary(tb, callback){
  var output = {};
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);

  $.ajax({
    type: "DELETE",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP +  "/api/trust_boundaries/name/" + encodeURIComponent(tb.theName),
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

function putTrustBoundary(tb, oldTbName, callback){
  var output = {};
  output.object = tb;
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
    url: serverIP +  "/api/trust_boundaries/name/" + encodeURIComponent(oldTbName),
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

function postTrustBoundary(tb, callback){
  var output = {};
  output.object = tb;
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
    url: serverIP +  "/api/trust_boundaries",
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

mainContent.on('click', '.deleteTrustBoundaryEnvironment', function () {
  var propEnvName = $(this).next("td").text();
  var tb = JSON.parse($.session.get("TrustBoundary"));

  $.each(tb.theEnvironmentProperties, function (index, prop) {
    if(tb.theEnvironmentName == propEnvName){
      tb.theEnvironmentProperties.splice(index,1);
    }
  });
  $.session.set("TrustBoundary", JSON.stringify(tb));
  $(this).closest("tr").remove();
  var UIenv = $("#theTrustBoundaryEnvironments").find("tbody");
  if(jQuery(UIenv).has(".trustBoundaryEnvironmentProperties").length){
    UIenv.find(".trustBoundaryEnvironmentProperties:first").trigger('click');
  }
  else{
    $("#trustBoundariesTabID").hide("fast");
  }
});

mainContent.on("click", ".trustBoundaryEnvironmentProperties", function () {
  var name = $(this).text();
  $.session.set("TrustBoundaryEnvironmentName", name);
  $("#theTrustBoundaryComponents").find("tbody").empty();
  var tb = JSON.parse($.session.get("TrustBoundary"));
  $.each(tb.theEnvironmentProperties, function (index, prop) {
    if(prop.theName == name){
      $.each(prop.theComponents, function (index, tbComponent) {
        appendTrustBoundaryComponent(tbComponent);
      });
    }
  });
});

mainContent.on("click", "#addComponentToTrustBoundary", function () {
  var filterList = [];
  $(".trustboundary-component").next("td").each(function (index, tag) {
    filterList.push($(tag).text());
  });

  $('#theTrustBoundaryComponentType').val('process');
  refreshDimensionSelector($('#theTrustBoundaryComponentName'),'process',$.session.get('TrustBoundaryEnvironmentName'),function(){
    $('#trustBoundaryComponentDialog').modal('show');
  },filterList);
});

mainContent.on('shown.bs.modal',"#trustBoundaryComponentDialog", function() {
  var currentComponent = JSON.parse($('#trustBoundaryComponentDialog').attr('data-currentComponent'));
  if (currentComponent != undefined) {
    $('#theTrustBoundaryComponentType').val(currentComponent.theType);
    $('#theTrustBoundaryComponentName').val(currentComponent.theName);
    $('#AddTrustBoundaryComponentButton').text('Edit');
  }
});

mainContent.on('click',"#AddTrustBoundaryComponentButton", function(e) {
  e.preventDefault();
  var updComp = {};
  updComp.theName = $("#theTrustBoundaryComponentName").val();
  updComp.theType = $("#theTrustBoundaryComponentType").val();
  var tb = JSON.parse($.session.get("TrustBoundary"));
  var envName = $.session.get("TrustBoundaryEnvironmentName");

  $.each(tb.theEnvironmentProperties, function (index, env) {
    if(env.theName == envName){
      var selectedIdx = $('#trustBoundaryComponentDialog').attr('data-selectedIndex');
      if (selectedIdx == undefined) {
        tb.theEnvironmentProperties[index].theComponents.push(updComp);
        $.session.set("TrustBoundary", JSON.stringify(tb));
        appendTrustBoundaryComponent(updComp);
        $('#trustBoundaryComponentDialog').modal('hide');
      }
      else {
        $.each(env.theComponents,function(idx,comp) {
          if (comp.name == updComp.theName) {
            tb.theEnvironmentProperties[index].theComponents[idx].theName = updComp.theName;
            tb.theEnvironmentProperties[index].theComponents[idx].theType = updComp.theType;
            $.session.set("TrustBoundary", JSON.stringify(tb));
            $('#theTrustBoundaryComponents').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(1)").text(updComp.theName);
            $('#theTrustBoundaryComponents').find('tbody').find('tr:eq(' + selectedIdx + ')').find("td:eq(2)").text(updComp.theValue);
             $('#trustBoundaryComponentDialog').modal('hide');
          }
        });
      }
    }
  });
});

mainContent.on('click', ".trustboundary-component", function () {
  var compRow = $(this).closest("tr");
  var tb = JSON.parse($.session.get("TrustBoundary"));
  var envName = $.session.get("TrustBoundaryEnvironmentName");

  var filterList = [];
  $(".trustboundary-component").next("td").each(function (index, tag) {
    filterList.push($(tag).text());
  });

  var currentComp = {};
  currentComp.theName = compRow.find("td:eq(1)").text();
  currentComp.theType = compRow.find("td:eq(2)").text();

  $('#theTrustBoundaryComponentType').val(currentComp.theType);
  refreshDimensionSelector($('#theTrustBoundaryComponentName'),currentComp.theType,$.session.get('TrustBoundaryEnvironmentName'),function(){
    $('#trustBoundaryComponentDialog').attr('data-currentComponent',JSON.stringify(currentComp));
    $('#trustBoundaryComponentDialog').attr('data-selectedIndex',compRow.index());
    $('#trustBoundaryComponentDialog').modal('show');
  },filterList);
});

mainContent.on('change','#theTrustBoundaryComponentType',function() {
  refreshDimensionSelector($('#theTrustBoundaryComponentName'),$(this).val(),$.session.get('TrustBoundaryEnvironmentName'),undefined,['All']);
});

mainContent.on('click', ".removeTrustBoundaryComponent", function () {
  var compRow = $(this).closest("tr");
  var compTxt = compRow.find("td:eq(1)").text();
  var tb = JSON.parse($.session.get("TrustBoundary"));
  var envName = $.session.get("TrustBoundaryEnvironmentName");

  $.each(tb.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      $.each(env.theComponents, function (index2, comp) {
        if(comp.theName == compText){
          env.theComponents.splice( index2 ,1 );
          $.session.set("TrustBoundary", JSON.stringify(tb));
          compRow.remove();
          return false;
        }
      });
    }
  });
});

mainContent.on("click", "#addTrustBoundaryEnvironment", function () {
  var filterList = [];
  $(".trustBoundaryEnvironmentProperties").each(function (index, tag) {
    filterList.push($(tag).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'environment',undefined,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','environment');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addTrustBoundaryEnvironment');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addTrustBoundaryEnvironment() {
  var text = $("#chooseEnvironmentSelect").val();
  appendTrustBoundaryEnvironment(text);
  var environment =  jQuery.extend(true, {},{"theName" : text, "theComponents" : []} );
  var tb = JSON.parse($.session.get("TrustBoundary"));
  tb.theEnvironmentProperties.push(environment);
  $.session.set("TrustBoundary", JSON.stringify(tb));
  $(document).find(".trustBoundaryEnvironmentProperties").each(function () {
    if($(this).text() == text){
      $(this).trigger("click");
      $("#trustBoundariesTabID").show("fast");
      $('#chooseEnvironment').modal('hide');
    }
  });
}


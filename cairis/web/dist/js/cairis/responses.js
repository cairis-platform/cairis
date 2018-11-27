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

$("#responseMenuClick").click(function () {
  validateClick('response',function() {
    clearLocalStorage($('#menuBCClick').attr('dimension'));
    $("#objectViewer").empty();
    $('#menuBCClick').attr('dimension','response');
    refreshMenuBreadCrumb('response');
  });
});

$(document).on("click", "#addNewResponse", function () {

  getNoOfRisks(function(noOfRisks) {
    if (noOfRisks == 0) {
      $('#noRisksModal').modal('show');
    }
    else {
      $("#chooseResponseDialog").modal('show');
    }
  });
});

$(document).on('click', "#SelectResponseButton", function () {

  var responseType = $("#theResponse").val();
  $("#chooseResponseDialog" ).modal('hide');
  refreshObjectBreadCrumb('New Response');
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editResponseOptions.html", "#objectViewer", null, true, true, function () {
    $("#UpdateResponse").text("Create");
    $("#editResponseOptionsform").addClass("newResponse");
    var select = $("#chooseRisk");
    $.session.set("response", JSON.stringify(jQuery.extend(true, {},responseDefault )));

    refreshDimensionSelector(select,'risk',undefined,function() {
      var resp = JSON.parse($.session.get("response"));
      resp.theRisk = $("#chooseRisk").val();
      resp.theResponseType = responseType;
      $.session.set("response", JSON.stringify(resp));
      $("#chooseRisk").trigger('click');
      $.session.set("responseKind",responseType);
      $("#editResponseOptionsform").validator('update');
      switch (responseType){
        case "Transfer":
          toggleResponse("#transferWindow");
          break;
        case "Prevent":
        case "Detect":
        case "Deter":
        case "React":
          toggleResponse("#mitigateWindow");
          break;
        case "Accept":
          toggleResponse("#acceptWindow");
          break;
        default :
          toggleResponse("#mitigateWindow");
          break;
      }
      $('#respMitigateType').trigger('change');
      $("#Properties").hide();
    });
  });
});


$(document).on('click', "td.response-rows", function () {
  var responseName = $(this).closest("tr").find("td:eq(1)").text();
  refreshObjectBreadCrumb(responseName);
  viewResponse(responseName);
});

function viewResponse(responseName) {
  activeElement("objectViewer");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/responses/name/" + encodeURIComponent(responseName),
    success: function (data) {
      fillOptionMenu("fastTemplates/editResponseOptions.html", "#objectViewer", null, true, true, function () {
        $("#UpdateResponse").text("Update");

        $("#theResponseName").val(data.theName);
        $.session.set("ResponseName", data.theName);
        $.session.set("response", JSON.stringify(data));

        $('#theTags').val(data.theTags.join(', '));
        if (data.theResponseType == 'Prevent' || data.theResponseType == 'Deter' || data.theResponseType == 'Detect' || data.theResponseType == 'React') {
          data.theResponseType = 'Mitigate';
        }
        $.session.set("responseKind",data.theResponseType);
        $.each(data.theEnvironmentProperties[data.theResponseType.toLocaleLowerCase()], function (index, env) {
          appendResponseEnvironment(env.theEnvironmentName);
        });

        refreshDimensionSelector($('#chooseRisk'),'risk',undefined,function(){
          $('#chooseRisk').val(data.theRisk);
          switch (data.theResponseType){
            case "Transfer":
              toggleResponse("#transferWindow");
              break;
            case "Prevent":
              toggleResponse("#mitigateWindow");
              break;
            case "Deter":
              toggleResponse("#mitigateWindow");
              break;
            case "Detect":
              toggleResponse("#mitigateWindow");
              break;
            case "React":
              toggleResponse("#mitigateWindow");
              break;
            case "Accept":
              toggleResponse("#acceptWindow");
              break;
            default :
              toggleResponse("#mitigateWindow");
              break;
          }
          $("#editResponseOptionsform").validator('update');
          $("#theRespEnvironments").find(".responseEnvironment:first").trigger('click');
        },['All']);


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
mainContent.on('click', ".deleteTransferRole", function () {
  var roleName = $(this).next(".roleName").text();
  var resp = JSON.parse($.session.get("response"));
  var envName = $.session.get("responseEnvironment");
  $.each(resp.theEnvironmentProperties, function (iex, trans) {
    if(envName == trans.theEnvironmentName) {
      $.each(trans, function (index, role) {
        if (roleName = role.roleName) {
          resp.theEnvironmentProperties[0][0].theRoles.splice(index, 1);
        }
      });
    }
  });
  $(this).closest("tr").remove();
  $.session.set("response", JSON.stringify(resp));
});


mainContent.on('click', "#addRespEnv", function () {
  $('#chooseRiskEnvironmentTitle').text('Choose the response environment');
  var riskName = $("#chooseRisk").val();
  var urlText = serverIP + "/api/environments/risk/" + encodeURIComponent(riskName) + "/names";

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
      var filterList = [];
      $(".responseEnvironment").each(function (index, tag) {
        filterList.push($(tag).text());
      });
      data = data.filter(x => filterList.indexOf(x) < 0);
      $('#chooseRiskEnvironmentSelect').empty();
      $.each(data, function () {
        $('#chooseRiskEnvironmentSelect').append($("<option />").val(this).text(this));
      });
      $('#chooseRiskEnvironment').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

mainContent.on('click', '#chooseRiskEnvironmentButton', function() {
  var text = $("#chooseRiskEnvironmentSelect").val();
  var type =  $.session.get("responseKind");
  var envObjt = mitigateEnvDefault;
  if (type == 'Accept') {
    envObjt = acceptEnvDefault;
  }
  else if (type == 'Transfer') {
    envObjt = transferEnvDefault;
  } 
  var environment =  jQuery.extend(true, {},envObjt );
  environment.theEnvironmentName = text;
  var resp = JSON.parse($.session.get("response"));
  appendResponseEnvironment(text);
  resp.theEnvironmentProperties[type.toLowerCase()].push(environment);
  $.session.set("response", JSON.stringify(resp));
  $(document).find(".responseEnvironment").each(function () {
    if($(this).text() == text){
      $(this).trigger("click");
      $("#Properties").show("fast");
      $('#chooseRiskEnvironment').modal('hide');
    }
  });
});

mainContent.on('click', ".deleteRespEnv", function () {
  var envi = $(this).next(".responseEnvironment").text();
  $(this).closest("tr").remove();
  var resp = JSON.parse($.session.get("response"));
  $.each(resp.theEnvironmentProperties, function (index, tran) {
    $.each(tran, function (index2, env) {
      if(env.theEnvironmentName == envi){
        tran.splice( index2 ,1 );
        $.session.set("response", JSON.stringify(resp));

        var UIenv = $("#theAttackerEnvironments").find("tbody");
        if(jQuery(UIenv).has(".responseEnvironment").length){
          UIenv.find(".responseEnvironment:first").trigger('click');
        }
        else {
          $("#Properties").hide("fast");
        }
        return false;
      }
    });
  });
});


mainContent.on('click', ".responseEnvironment", function () {
  $(this).closest('tr').addClass('active').siblings().removeClass('active');
  var type =  $.session.get("responseKind");
  var resp = JSON.parse($.session.get("response"));
  var environmentName = $(this).text();
  $.session.set("responseEnvironment", environmentName);
  switch (type){
    case "Transfer":
      $.each(resp.theEnvironmentProperties["transfer"], function (index, env) {
        if(env.theEnvironmentName == environmentName) {
          $("#theRespTransferRationale").val(env.theRationale);
          $("#transferRolesTable").find("tbody").empty()
          $.each(env.theRoles, function (ind, role) {
            appendResponseTransferRole(role);
          });
        }
      });
      break;
    case "Mitigate":
      $.each(resp.theEnvironmentProperties["mitigate"], function (index, obj) {
        if(obj.theEnvironmentName == environmentName) {
          if (obj.theType == "Detect") {
            $('#theDetectionDimensionLabel').text('Detection Point');
            $('#theDetectionDimension').empty();
            $('#theDetectionDimension').append("<option value='Before'>Before</option><option value='At'>At</option><option value='After'>After</option></select>");
            $("#theDetectionDimension").prop('disabled', false);
          }
          else if (obj.theType == 'React') {
            $('#theDetectionDimensionLabel').text('Detection Mechanism');
            refreshDimensionSelector($('#theDetectionDimension'),'detection_mechanism',$.session.get('responseEnvironment'),undefined,['All']);
          }
          else {
            $("#theDetectionDimension").prop('disabled', true);
            $("#theDetectionDimension").val(" ");
          }
          $("#respMitigateType").val(obj.theType);
        }
      });
      break;
    case "Accept":
      $.each(resp.theEnvironmentProperties["accept"], function (index, obj) {
        if(obj.theEnvironmentName == environmentName) {
          $("#theAcceptanceCost").val(obj.theCost);
          $("#acceptRationale").val(obj.theRationale);
        }
      });
      break;
  }
});

mainContent.on('change', "#theAcceptanceCost", function () {
  var cost = $(this).val();
  var resp = JSON.parse($.session.get("response"));
  var envName = $.session.get("responseEnvironment");
  $.each(resp.theEnvironmentProperties["accept"], function (index, obj) {
    if(obj.theEnvironmentName == envName) {
      obj.theCost = cost;
    }
  });
  $.session.set("response", JSON.stringify(resp));
});

mainContent.on('change', "#acceptRationale", function () {
  var rat = $(this).val();
  var resp = JSON.parse($.session.get("response"));
  var envName = $.session.get("responseEnvironment");
  $.each(resp.theEnvironmentProperties["accept"], function (index, obj) {
    if(obj.theEnvironmentName == envName) {
      obj.theRationale = rat;
    }
  });
  $.session.set("response", JSON.stringify(resp));
});

mainContent.on('change', "#respMitigateType", function () {

  if ($('#theResponse').val() != 'Mitigate') {
    $("#theResponseName").val($("#theResponse").val() + " " + $("#chooseRisk").val());
  }
  else {
    var resp = JSON.parse($.session.get("response"));
    $("#theResponseName").val($("#respMitigateType").val() + " " + $("#chooseRisk").val());
    var newType = $(this).val().toLowerCase();
    var type =  $.session.get("responseKind");
    var envName = $.session.get("responseEnvironment");
    if(newType == "detect"){
      $('#theDetectionDimensionLabel').text('Detection Point');
      $('#theDetectionDimension').empty();
      $('#theDetectionDimension').append("<option value='Before'>Before</option><option value='At'>At</option><option value='After'>After</option></select>");
      $("#theDetectionDimension").prop('disabled',false);
    }
    else if (newType == 'react') {
      $('#theDetectionDimensionLabel').text('Detection Mechanism');
      refreshDimensionSelector($('#theDetectionDimension'),'detection_mechanism',$.session.get('responseEnvironment'),undefined,['All']);
    }
    else{
      $('#theDetectionDimensionLabel').text('Detection Point');
      $("#theDetectionDimension").prop('disabled',true);
      $("#theDetectionDimension").val(" ");
    }
    $.each(resp.theEnvironmentProperties[type.toLowerCase()], function (index, env) {
      if(env.theEnvironmentName == envName){
        env.theType = newType;
      }
    });
    $.session.set("response", JSON.stringify(resp));
  }
});

mainContent.on('change', "#theDetectionDimension", function () {

  var value = $(this).val();
  var resp = JSON.parse($.session.get("response"));
  var type =  $.session.get("responseKind");
  var envName = $.session.get("responseEnvironment");
  if(value != " "){
    $.each(resp.theEnvironmentProperties[type.toLowerCase()], function (index, env) {
      if(env.theEnvironmentName == envName){
        if ($('#respMitigateType') == 'Detect') {
          env.theDetectionPoint = value;
        }
        else {
          env.theDetectionMechanisms = [value];
        }
      }
    });
  }
  $.session.set("response", JSON.stringify(resp));
});

mainContent.on('change', "#theRespTransferRationale", function () {
  var resp = JSON.parse($.session.get("response"));
  var type =  $.session.get("responseKind");
  var envName = $.session.get("responseEnvironment");
  $.each(resp.theEnvironmentProperties[type.toLowerCase()], function (index, env) {
    if(env.theEnvironmentName == envName){
      env.theRationale = $("#theRespTransferRationale").val();
    }
  });
  $.session.set("response", JSON.stringify(resp));
});

mainContent.on('click', "#addRespTransferRole", function () {
  var resp = JSON.parse($.session.get("response"));
  var envName = $.session.get("responseEnvironment");

  var filterList = [];
  $(".roleName").each(function (index, tag) {
    filterList.push($(tag).text());
  });

  refreshDimensionSelector($('#chooseRoleSelect'),'role',undefined,function(){
    $('#chooseRoleCost').modal('show');
  },filterList);
});

mainContent.on('click', '#chooseRoleCostButton', function() {
  var role = {};
  role.roleName = $('#chooseRoleSelect').val();
  role.cost = $('#chooseRoleCostSelect').val();
  appendResponseTransferRole(role);
  var envName = $.session.get("responseEnvironment");
  var resp = JSON.parse($.session.get("response"));
  $.each(resp.theEnvironmentProperties["transfer"], function (index, env) {
    if(env.theEnvironmentName == envName){
      env.theRoles.push(role);
      $.session.set("response", JSON.stringify(resp));
      $('#chooseRoleCost').modal('hide');
    }
  });
});

function toggleResponse(window){
  $("#mitigateWindow").hide();
  $("#acceptWindow").hide();
  $("#transferWindow").hide();
  $(window).show();

}

function createResponsesTable(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/responses",
    success: function (data) {
      setTableHeader("Responses");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      for (var key in data) {
        var item = data[key];
        textToInsert[i++] = "<tr>";

        textToInsert[i++] = '<td class="deleteResponseButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';
        textToInsert[i++] = '<td class="response-rows" name="theName">';
        textToInsert[i++] = item.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="response-rows" name="theType">';
        textToInsert[i++] = item.theResponseType;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      }

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
      $("#mainTable").find("tbody").removeClass();

      $("#mainTable").find("tbody").addClass('response-rows');
      $('.response-rows').contextMenu({
        selector: 'td',
        items: {
          "generate": {
            name: "Generate Goal",
            callback: function(key, opt) {
              var goalName = $(this).closest("tr").find("td").eq(1).html();
              generateGoal(goalName);
            }
          }
        }
      });
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

function generateGoal(respName) {
  $.ajax({
    type: "POST",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    url: serverIP + "/api/responses/name/" + encodeURIComponent(respName) + "/generate_goal?session_id=" + $.session.get('sessionID'),
    success: function (data) {
      showPopup(true);
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function appendResponseEnvironment(environment){
  $("#theRespEnvironments").find("tbody").append('<tr><td class="deleteRespEnv"><i class="fa fa-minus"></i></td><td class="responseEnvironment">'+environment+'</td></tr>');
}

function appendResponseTransferRole(role){
  $("#transferRolesTable").find("tbody").append('<tr><td class="deleteTransferRole"><i class="fa fa-minus"></i></td><td class="roleName">'+role.roleName+'</td><td>'+ role.cost +'</td></tr>');
}

mainContent.on('click', '#CloseResponse', function (e) {
  e.preventDefault();
  clearLocalStorage('response');
  $("#objectViewer").empty();
  $('#menuBCClick').attr('dimension','response');
  refreshMenuBreadCrumb('response');
});

$(document).on('click', 'td.deleteResponseButton', function (e) {
  e.preventDefault();
  var respName = $(this).find('i').attr("value");
  deleteObject('response', respName, function (respName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/responses/name/" + encodeURIComponent(respName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        showPopup(true);
        $('#menuBCClick').attr('dimension','response');
        refreshMenuBreadCrumb('response');
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

$(document).on('click','#chooseRisk', function(e) {
  var responseType = $.session.get("responseKind");
  if (responseType == 'Mitigate') {
    responseType = $("#respMitigateType").val();
  }
  $("#theResponseName").val(responseType + " " + $("#chooseRisk").val());
});


function putResponse(response, oldName, callback){
  var output = {};
  output.object = response;
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
    url: serverIP + "/api/responses/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
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

function postResponse(response, callback){
  var output = {};
  output.object = response;
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
    url: serverIP + "/api/responses" + "?session_id=" + $.session.get('sessionID'),
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



function commitResponse() {
  var resp = JSON.parse($.session.get("response"));
  var respKind = $.session.get("responseKind");
  
  if (resp.theEnvironmentProperties[respKind.toLowerCase()].length == 0) {
    alert("Environments not defined");
    return;
  }
  if ((respKind == 'Accept') && ($('#theAcceptanceCost').val() == undefined)) {
    alert("Cost of accepting risk not specified");
    return;
  }
  var valid = true;
  if (respKind == 'Transfer') {
    $.each(resp.theEnvironmentProperties[respKind.toLowerCase()],function(idx,env) {
      if (env['theRoles'].length == 0) {
        alert("Risk not transferred to any roles in environment" + env.theEnvironmentName);
        valid = false; 
        return;
      }
    });
  }
  if (valid) {
    resp.theName = $("#theResponseName").val();
  
    if ($('#theTags').val() != '') {
      resp.theTags = $('#theTags').val().split(',').map(function(t){return t.trim();});
    }
    else {
      resp.theTags = [];
    }

    resp.theRisk = $("#chooseRisk").val();
    resp.theResponseType = respKind;

    if($("#editResponseOptionsform").hasClass("newResponse")){
      postResponse(resp, function () {
        clearLocalStorage('response');
        $("#editResponseOptionsform").removeClass("newResponse")
        $('#menuBCClick').attr('dimension','response');
        refreshMenuBreadCrumb('response');
      });
    }
    else {
      putResponse(resp, $.session.get("ResponseName"), function () {
        clearLocalStorage('response');
        $('#menuBCClick').attr('dimension','response');
        refreshMenuBreadCrumb('response');
      });
    }
  }
}

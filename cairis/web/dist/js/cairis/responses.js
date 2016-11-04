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
  createResponsesTable();
});

$(document).on("click", "#addNewResponse", function () {

  $("#ChooseResponseDialog" ).dialog({
    modal: true,
    buttons: {
      Ok: function() {
        $( this ).dialog( "close" );
        var responseType = $("#ChooseResponseDialog").find("option:selected").attr("id");

        activeElement("objectViewer");
        fillOptionMenu("fastTemplates/editResponseOptions.html", "#objectViewer", null, true, true, function () {
          $("#editResponseOptionsform").addClass("newResponse");
          var select = $("#chooseRisk");
          $.session.set("response", JSON.stringify(jQuery.extend(true, {},responseDefault )));
          select.empty();
          getRisks(function (risks) {
            $.each(risks, function (key, obj) {
              select.append($('<option>', { value : key }).text(key));
            });
            var resp = JSON.parse($.session.get("response"));
            resp.theRisk = $("#chooseRisk").val();
            resp.theResponseType = responseType;
            $.session.set("response", JSON.stringify(resp));
            $("#chooseRisk").trigger('click');
          });

          $.session.set("responseKind",responseType);
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
          $("#Properties").hide();
        });
      }
    }
  });
});


$(document).on('click', "td.response-rows", function () {
  activeElement("objectViewer");
  var name = $(this).text();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/responses/name/" + name,
    success: function (data) {
      fillOptionMenu("fastTemplates/editResponseOptions.html", "#objectViewer", null, true, true, function () {
        var tags = data.theTags;
        $("#theResponseName").val(data.theName);
        $.session.set("ResponseName", data.theName);
        $.session.set("response", JSON.stringify(data));
        var text = "";
        $.each(tags, function (index, type) {
          text += type + ", ";
        });
        $("#theTags").val(text);
        if (data.theResponseType == 'Prevent' || data.theResponseType == 'Deter' || data.theResponseType == 'Detect' || data.theResponseType == 'React') {
          data.theResponseType = 'Mitigate';
        }
        $.session.set("responseKind",data.theResponseType);
        $.each(data.theEnvironmentProperties[data.theResponseType.toLocaleLowerCase()], function (index, env) {
          appendResponseEnvironment(env.theEnvironmentName);
        });
        var select = $("#chooseRisk");
        select.empty();
        getRisks(function (risks) {
          $.each(risks, function (key, obj) {
            select.append($('<option>', { value : key }).text(key));
          });
          select.val(data.theRisk);
        });

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
        $("#theRespEnvironments").find(".responseEnvironment:first").trigger('click');
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

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
  var hasEnv = [];
  $(".responseEnvironment").each(function (index, tag) {
    hasEnv.push($(tag).text());
  });
  var riskName = $("#chooseRisk").val();
  riskEnvironmentDialogBox(hasEnv, riskName, function (text) {
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
      }
    });
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
            $("#theDetectionPoint").prop('disabled', false);
          }
          else {
            $("#theDetectionPoint").prop('disabled', true);
            $("#theDetectionPoint").val(" ");
          }
          $("#respMitigateType").val(obj.theType);
        }
      });
      break;
    case "Accept":
      $.each(resp.theEnvironmentProperties["accept"], function (index, obj) {
        if(obj.theEnvironmentName == environmentName) {
          $("#theCost").val(obj.theCost);
          $("#acceptRationale").val(obj.theRationale);
        }
      });
      break;
  }
});

mainContent.on('change', "#theCost", function () {
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
  $("#theResponseName").val($("#respMitigateType").val() + " " + $("#chooseRisk").val());
  var newType = $(this).val().toLowerCase();
  var resp = JSON.parse($.session.get("response"));
  var type =  $.session.get("responseKind");
  var envName = $.session.get("responseEnvironment");
  if(newType == "detect"){
    $("#theDetectionPoint").prop('disabled',false);
  }
  else{
    $("#theDetectionPoint").prop('disabled',true);
    $("#theDetectionPoint").val(" ");
  }
  $.each(resp.theEnvironmentProperties[type.toLowerCase()], function (index, env) {
    if(env.theEnvironmentName == envName){
      env.theType = newType;
    }
  });
  $.session.set("response", JSON.stringify(resp));
});

mainContent.on('change', "#theDetectionPoint", function () {
  var value = $(this).val();
  var resp = JSON.parse($.session.get("response"));
  var type =  $.session.get("responseKind");
  var envName = $.session.get("responseEnvironment");
  if(value != " "){
    $.each(resp.theEnvironmentProperties[type.toLowerCase()], function (index, env) {
      if(env.theEnvironmentName == envName){
        env.theDetectionPoint = newType;
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
  newRoleDialogbox(function (role) {
    appendResponseTransferRole(role);
    $.each(resp.theEnvironmentProperties["transfer"], function (index, env) {
      if(env.theEnvironmentName == envName){
        env.theRoles.push(role);
      }
    });
    $.session.set("response", JSON.stringify(resp));
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
      window.activeTable = "Responses";
      setTableHeader();
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";

        textToInsert[i++] = '<td class="deleteResponseButton"><i class="fa fa-minus" value="' + key + '"></i></td>';
        textToInsert[i++] = '<td class="response-rows" name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theType">';
        textToInsert[i++] = item.theResponseType;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      });

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
      $("#reqTable").find("tbody").removeClass();

      $("#reqTable").find("tbody").addClass('response-rows');
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
      activeElement("reqTable");
      sortTableByRow(0);
    },
    error: function (xhr, textStatus, errorThrown) {
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
    url: serverIP + "/api/responses/name/" + respName.replace(" ","%20") + "/generate_goal?session_id=" + $.session.get('sessionID'),
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
  createResponsesTable();
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
      url: serverIP + "/api/responses/name/" + respName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        createResponsesTable();
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

$(document).on('click','#chooseRisk', function(e) {
  var responseType = $.session.get("responseKind");
  if (responseType == 'Mitigate') {
    responseType = $("#respMitigateType").val();
  }
  $("#theResponseName").val(responseType + " " + $("#chooseRisk").val());
});


function putResponse(response, oldName, usePopup, callback){
  var output = {};
  output.object = response;
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
    url: serverIP + "/api/responses/name/" + oldName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
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

function postResponse(response, callback){
  var output = {};
  output.object = response;
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

mainContent.on('click', '#UpdateResponse', function (e) {
  e.preventDefault();

  $("#editResponseOptionsform").validator();

  var resp = JSON.parse($.session.get("response"));
  var respKind = $.session.get("responseKind");
  if (resp.theEnvironmentProperties[respKind.toLowerCase()].length == 0) {
    alert("Environments not defined");
  }
  else {
    resp.theName = $("#theResponseName").val();
    var arr = $("#theTags").val().split(", ")
    resp.TheTags = arr;
    resp.theRisk = $("#chooseRisk").val();
    resp.theResponseType = respKind;

    if($("#editResponseOptionsform").hasClass("newResponse")){
      postResponse(resp, function () {
        createResponsesTable();
        $("#editResponseOptionsform").removeClass("newResponse")
      });
    }
    else {
      putResponse(resp, $.session.get("ResponseName"), function () {
        createResponsesTable();
      });
    }
  }
});

function riskEnvironmentDialogBox(haveEnv,riskName,callback){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/environments/risk/" + encodeURIComponent(riskName) + "/names",
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


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

$("#assetMenuClick").click(function(){
  validateClick('asset',function() {
    clearLocalStorage($('#menuBCClick').attr('dimension'));
    $("#objectViewer").empty();
    $('#menuBCClick').attr('dimension','asset');
    refreshMenuBreadCrumb('asset');
  });
});


function createAssetsTable(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    crossDomain: true,
    url: serverIP + "/api/assets/summary",
    success: function (data) {
      setTableHeader("Assets");

      var theTable = $(".theTable");
      var textToInsert = [];
      var i = 0;

      for (var r = 0; r < data.length; r++) {
        var item = data[r];
        textToInsert[i++] = '<tr>'

        textToInsert[i++] = '<td class="deleteAssetButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';

        textToInsert[i++] = '<td class="asset-row" name="theName" value="' + item.theName + '">';
        textToInsert[i++] = item.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td class="asset-row" name="theType">';
        textToInsert[i++] = item.theType;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      }

      theTable.append(textToInsert.join(''));
      $.contextMenu('destroy',$('.requirement-rows'));
      $.contextMenu('destroy',$('.asset-rows'));
      theTable.css("visibility","visible");
      $("#mainTable").find("tbody").removeClass();
      $("#mainTable").find("tbody").addClass('asset-rows');
      $('.asset-rows').contextMenu({
        selector: 'td',
        items: {
          "contributes": {
            name: "Contributes to",
            callback: function(key, opt) {
              var assetName = $(this).closest("tr").find("td").eq(1).html();
              traceExplorer('asset',assetName,'1');
            }
          },
        }
      });
      activeElement("mainTable");
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

$(document).on('click', "td.asset-row", function(){
  var assetName = $(this).closest("tr").find("td:eq(1)").attr('value');
  refreshObjectBreadCrumb(assetName);
  viewAsset(assetName);
});

function viewAsset(assetName) {
  activeElement("objectViewer");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    crossDomain: true,
    url: serverIP + "/api/assets/name/" + encodeURIComponent(assetName),
    success: function (newdata) {
      fillOptionMenu("fastTemplates/editAssetsOptions.html","#objectViewer",null,true,true, function(){
        $("#UpdateAsset").text("Update");
        $.session.set("Asset", JSON.stringify(newdata));
        refreshDimensionSelector($('#theType'),'asset_type',undefined,function() {
          $('#theType').val(newdata.theType);
        });
        $.each(newdata.theInterfaces,function(idx,aInt) {
          appendAssetInterface(aInt);
        });
        $('#theTags').val(newdata.theTags.join(', '));
        newdata.theTags = []
        $('#editAssetsOptionsform').loadJSON(newdata,null);
        if (newdata.isCritical) {
          $('#theCriticalRationale').prop("disabled",false); 
          $('#isCritical').prop('checked',true);
        }
        else {
          $('#isCritical').prop('checked',false);
        }
        fillAssetEnvironments(newdata.theEnvironmentProperties);
        $('#editAssetsOptionsform').validator('update');
        $("#theEnvironmentDictionary").find("tbody").find(".assetEnvironmentRow:first").trigger('click');
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
};

function appendAssetInterface(aInt) {
  $("#theAssetInterfaces").find("tbody").append('<tr><td class="deleteAssetInterface"><i class="fa fa-minus"></i></td><td class="asset-interface">'+ aInt.theInterfaceName +'</td><td>' + aInt.theInterfaceType + '</td><td>' + aInt.theAccessRight + '</td><td>' + aInt.thePrivilege + '</td></tr>');
}

var mainContent = $("#objectViewer");
mainContent.on('click','td.deleteAssetInterface',function() {
  var intRow = $(this).closest("tr");
  var rowIdx = intRow.index();
  intRow.remove();
  var asset = JSON.parse($.session.get("Asset"));
  asset.theInterfaces.splice(rowIdx,1);
  $.session.set("Asset", JSON.stringify(asset));
});

mainContent.on('click', ".removeAssetEnvironment", function () {
  var envi = $(this).next(".clickable-environments").text();
  var row =  $(this).closest("tr");
  var asset = JSON.parse($.session.get("Asset"));
  $.each(asset.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envi){
      asset.theEnvironmentProperties.splice( index ,1 );
      $.session.set("Asset", JSON.stringify(asset));

      row.remove();
      var UIenv = $("#theEnvironmentDictionary").find("tbody");
      if(jQuery(UIenv).has(".removeAssetEnvironment").length){
        UIenv.find(".clickable-environments:first").trigger('click');
      }
      else {
        $("#assetstabsID").hide("fast");
      }
      return false;
    }
  });
});

mainContent.on('click', ".removeAssetAssociation", function (e) {
  e.preventDefault();
  var envName = $.session.get("assetEnvironmentName");
  var assocRow = $(this).closest('tr');
  var rowIdx = assocRow.index();
  assocRow.remove();
  var asset = JSON.parse($.session.get("Asset"));
  $.each(asset.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == envName){
      env.theAssociations.splice( rowIdx ,1 );
      $.session.set("Asset", JSON.stringify(asset));
      return false;
    }
  });
});

mainContent.on('click', ".removeAssetEnvironment", function () {
  var envName = $.session.get("assetEnvironmentName");
  $(this).closest("tr").remove();
  var asset = JSON.parse($.session.get("Asset"));
  $.each(asset.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theProperties.splice( index ,1 );
      $.session.set("Asset", JSON.stringify(asset));
    }
  });
});


mainContent.on('click', '.assetEnvironmentRow', function(event){
  $(this).closest('tr').addClass('active').siblings().removeClass('active');
  var asset = JSON.parse($.session.get("Asset"));
  var text = $(this).text();
  $.session.set("assetEnvironmentName", text);
  var props;
  $.each(asset.theEnvironmentProperties, function(arrayID,group) {
    if(group.theEnvironmentName == text){
      props = group.theProperties;
      $.session.set("Arrayindex", arrayID);
      getAssetDefinition(props);
      $("#assetAssociationsTable > tbody").empty();
      $.each(asset.theEnvironmentProperties[arrayID].theAssociations,function(idx,assoc) {
        appendAssetAssociation(assoc);
      });
      $("#assetstabsID").show("fast");
    }
  });
});

function updateAssetSecurityProperty() {
  var currentProperty = JSON.parse($("#chooseSecurityProperty").attr("data-currentproperty"));
  var propRow = undefined;

  $("#definitionTable").find("tr").each(function(index, row){
    if (currentProperty.name == $(row).find("td:eq(2)").text()) {
      propRow = $(row);
    }
  });

  var updProp = {};
  updProp.name =  $("#theSecurityPropertyName").find("option:selected").text();
  updProp.value =  $("#theSecurityPropertyValue").val();
  updProp.rationale =  $("#theSecurityPropertyRationale").val();

  var asset = JSON.parse($.session.get("Asset"));
  var theEnvName = $.session.get("assetEnvironmentName");

  $.each(asset.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theProperties, function(idx, secProp){
        if (updProp.name == secProp.name) {
          asset.theEnvironmentProperties[index].theProperties[idx] = updProp;
          $.session.set("Asset", JSON.stringify(asset));
          propRow.find("td:eq(2)").text(updProp.name);
          propRow.find("td:eq(3)").text(updProp.value);
          propRow.find("td:eq(4)").text(updProp.rationale);
        }
      });
    }
  });
  $("#chooseSecurityProperty").modal('hide');
}

mainContent.on('click', '.theAssetPropName', function(){
  var propRow = $(this).closest("tr");
  var selectedProp = {};
  selectedProp.name = propRow.find("td:eq(2)").text();
  selectedProp.value = propRow.find("td:eq(3)").text();
  selectedProp.rationale = propRow.find("td:eq(4)").text();

  $("#chooseSecurityProperty").attr('data-updatepropertylist',"updateAssetPropertyList");
  $("#chooseSecurityProperty").attr("data-buildproperty","updateAssetSecurityProperty");
  $("#chooseSecurityProperty").attr("data-currentproperty",JSON.stringify(selectedProp));
  $("#chooseSecurityProperty").modal('show');
});

mainContent.on('click', '.clickable-association', function(){
  var row =  $(this).closest("tr");
  $.session.set("AssociationIndex",row.index());
  $("#editAssetsOptionsform").hide();
  $("#editAssociationsWindow").show(function() {
    refreshDimensionSelector($('#tailAsset'),'asset', $.session.get('assetEnvironmentName'), function(){
      $("#headNav").val(row.find("#hNav").text());
      $("#headAdorn").val(row.find("#hAdorn").text());
      $("#headNry").val(row.find("#hNry").text());
      $("#headRole").val(row.find("#hRole").text());
      $("#tailRole").val(row.find("#tRole").text());
      $("#tailNry").val(row.find("#tNry").text());
      $("#tailAdorn").val(row.find("#tAdorn").text());
      $("#tailNav").val(row.find("#tNav").text());
      $("#tailAsset").val(row.find("#tAsset").text());
    },['All']);
  });
});

mainContent.on('click', '.addEnvironmentPlus',function(){
  var filterList = [];
  $.each($('#theEnvironmentDictionary tbody tr td:nth-child(2)'),function(idx,row) {
    filterList.push($(row).text());
  });

  refreshDimensionSelector($('#chooseEnvironmentSelect'),'environment',undefined,function(){
    $('#chooseEnvironment').attr('data-chooseDimension','environment');
    $('#chooseEnvironment').attr('data-applyEnvironmentSelection','addAssetEnvironment');
    $('#chooseEnvironment').modal('show');
  },filterList);
});

function addAssetEnvironment() {
  var chosenText = $("#chooseEnvironmentSelect").val();
  $("#theEnvironmentDictionary").find("tbody").append("<tr><td class='deleteAssetEnv'><i class='fa fa-minus'></i></td><td class='clickable-environments assetEnvironmentRow'>" + chosenText +"</td></tr>");
  var asset = JSON.parse($.session.get("Asset"));
  if(asset.theEnvironmentProperties.length == 0) {
    var newProp = jQuery.extend(true, {}, assetEnvironmentDefault);
    newProp.theEnvironmentName = chosenText;
    $.session.set("assetEnvironmentName", newProp.theEnvironmentName);
    asset.theEnvironmentProperties.push(newProp);
  } 
  else {
    var newProp = jQuery.extend(true, {}, assetEnvironmentDefault);
    newProp.theEnvironmentName = chosenText;
    $.session.set("assetEnvironmentName", newProp.theEnvironmentName);
    asset.theEnvironmentProperties.push(newProp);
  }
  $.session.set("Asset", JSON.stringify(asset));
  $("#theEnvironmentDictionary").find("tbody").find(".assetEnvironmentRow:last").trigger('click');
}


mainContent.on("click", "#updateButtonAsset", function(){
  var asset = JSON.parse($.session.get("Asset"));
  var allprops = asset.theEnvironmentProperties;
  var props;

  if($("#editAssociationsWindow").hasClass("newAssociation")){
    $("#editAssociationsWindow").removeClass("newAssociation");
    var assoc = {};
    assoc['theHeadNav'] = $("#headNav").val();
    assoc['theHeadType'] = $("#headAdorn").val();
    assoc['theHeadMultiplicity'] = $("#headNry").val();
    assoc['theHeadRole'] = $("#headRole").val();
    assoc['theTailRole'] = $("#tailRole").val();
    assoc['theTailMultiplicity'] = $("#tailNry").val();
    assoc['theTailType'] = $("#tailAdorn").val();
    assoc['theTailNav'] = $("#tailNav").val();
    assoc['theTailName'] = $("#tailAsset").val();
    var arrIndex = $.session.get('Arrayindex');
    allprops[arrIndex].theAssociations.push(assoc);
    appendAssetAssociation(assoc);
    $("#editAssetsOptionsform").toggle();
    $("#editAssociationsWindow").toggle();
  }
  else {
    var row = $.session.get("associationRow");	
    var assoc = {};
    assoc['theHeadNav'] = $("#headNav").val();
    assoc['theHeadType'] = $("#headAdorn").val();
    assoc['theHeadMultiplicity'] = $("#headNry").val();
    assoc['theHeadRole'] = $("#headRole").val();
    assoc['theTailRole'] = $("#tailRole").val();
    assoc['theTailMultiplicity'] = $("#tailNry").val();
    assoc['theTailType'] = $("#tailAdorn").val();
    assoc['theTailNav'] = $("#tailNav").val();
    assoc['theTailName'] = $("#tailAsset").val();
    var arrIndex = $.session.get("Arrayindex");

    var associationIdx = $.session.get("AssociationIndex");
    $.each(allprops[arrIndex].theAssociations, function(idx,eAssoc) {
      if (idx == associationIdx) {
        allprops[arrIndex].theAssociations[idx] = assoc;
        $("#assetAssociationsTable").find("tr").eq(associationIdx + 1).replaceWith(assocToTr(assoc));
        $.session.set("Asset", JSON.stringify(asset))
        $("#editAssetsOptionsform").toggle();
        $("#editAssociationsWindow").toggle();
        $("#theEnvironmentDictionary").find("tbody").find(".clickable-environments:first").trigger('click');
      }
    });
  }
  $.session.set("Asset", JSON.stringify(asset));
});

function appendAssetAssociation(assoc) {
  $("#assetAssociationsTable").find("tbody").append(assocToTr(assoc)).animate('slow');
}

function assocToTr(assoc) {
  return "<tr><td class='removeAssetAssociation'><i class='fa fa-minus'></i></td><td class='assetAssociation' id='hNav'>" + assoc['theHeadNav'] + "</td><td class='clickable-association' id='hAdorn'>" + assoc['theHeadType'] + "</td><td class='clickable-association' id='hNry'>" + assoc['theHeadMultiplicity'] + "</td><td class='clickable-association' id='hRole'>" + assoc['theHeadRole'] + "</td><td class='clickable-association' id='tRole'>" + assoc['theTailRole'] + "</td><td class='clickable-association' id='tNry'>" + assoc['theTailMultiplicity'] + "</td><td class='clickable-association' id='tAdorn'>" + assoc['theTailType'] + "</td><td class='clickable-association' id='tNav'>" + assoc['theTailNav'] + "</td><td class='clickable-association' id='tAsset'>" + assoc['theTailName'] + "</td></tr>";
}

mainContent.on('click', '.removeEnvironment', function () {
  var asset = JSON.parse($.session.get("Asset"));
  var text = $(this).next('td').text();
  var theIndex = -1;
  $.each(asset.theEnvironmentProperties, function(arrayID,prop) {
    if(prop.environment == text){
      theIndex = arrayID;
    }
  });
  //Splice = removes element at "theIndex", 1 = only one item
  asset.theEnvironmentProperties.splice(theIndex, 1);
  $.session.set("Asset", JSON.stringify(asset));
});

mainContent.on("click",".deleteProperty", function(){
  var propName = $(this).closest("tr").find("td:eq(2)").text();
  $(this).closest("tr").remove();
  var asset = JSON.parse($.session.get("Asset"));
  var theEnvName = $.session.get("assetEnvironmentName");
  $.each(asset.theEnvironmentProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theProperties, function(idx,prop) {
        if (prop.name == propName) {
          asset.theEnvironmentProperties[index].theProperties[idx].value = 'None';
          asset.theEnvironmentProperties[index].theProperties[idx].rationale = 'None';
        }
      });
      $.session.set("Asset", JSON.stringify(asset));
    }
  });
});

$(document).on('click', "#addNewAsset",function(){
  refreshObjectBreadCrumb('New Asset');
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editAssetsOptions.html","#objectViewer",null,true,true,function(){
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      crossDomain: true,
      url: serverIP + "/api/assets/types",
      success: function (data) {
        $('#editAssetsOptionsform').validator();
        $("#UpdateAsset").text("Create");
        var typeSelect =  $('#theType');
        $.each(data, function (index, type) {
          typeSelect.append($("<option></option>").attr("value",type.name).text(type.theName));
        });
        $("#assetstabsID").hide();
        $.session.set("Asset", JSON.stringify(jQuery.extend(true, {},assetDefault )));
      },
      error: function (xhr, textStatus, errorThrown) {
        var error = JSON.parse(xhr.responseText);
        showPopup(false, String(error.message));
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
    // empty it because new environment;
    $("#editAssetsOptionsform").addClass("new");
  });
});

$(document).on('click', "td.deleteAssetButton",function(e){
  var assetName = $(this).find('i').attr('value');
  e.preventDefault();
  deleteObject('asset',assetName, function(assetName) {

    $.ajax({
      type: "DELETE",
      dataType: "json",
      accept: "application/json",
      crossDomain: true,
      url: serverIP + "/api/assets/name/" + encodeURIComponent(assetName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        showPopup(true);
        $('#menuBCClick').attr('dimension','asset');
        refreshMenuBreadCrumb('asset');
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

function updateAssetPropertyList() {
  resetSecurityPropertyList();

  var currentProperty = $("#chooseSecurityProperty").attr('data-currentproperty');
  if ((currentProperty != '') && (currentProperty != undefined)) {
    currentProperty = JSON.parse(currentProperty);
  }

  $("#definitionTable").find(".theAssetPropName").each(function(index, prop){
    if ((currentProperty != '') && (currentProperty != undefined) && (currentProperty.name == $(prop).text())) {
      // don't remove
    }
    else {
      $("#theSecurityPropertyName option[value='" + $(prop).text() + "']").remove();
    }
  });
  if ((currentProperty != '') && (currentProperty != undefined)) {
    $("#theSecurityPropertyName").val(currentProperty.name);
    $("#theSecurityPropertyValue").val(currentProperty.value);
    $("#theSecurityPropertyRationale").val(currentProperty.rationale);
  }
}

function addAssetSecurityProperty(e) {
  e.preventDefault()
  var prop = {};
  prop.name =  $("#theSecurityPropertyName").find("option:selected").text();
  prop.value =  $("#theSecurityPropertyValue").val();
  prop.rationale =  $("#theSecurityPropertyRationale").val()
  var asset = JSON.parse( $.session.get("Asset"));
  var secProperties = asset.theEnvironmentProperties;
  var theEnvName = $.session.get("assetEnvironmentName");
  $.each(secProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theProperties, function(idx, secProp){
        if (prop.name == secProp.name) {
          secProp.value = prop.value;
          secProp.rationale = prop.rationale;
          secProperties[index].theProperties[idx] = secProp;
          $.session.set("Asset", JSON.stringify(asset));
          appendSecurityProperty(prop);
        }
      });
    }
  });
  $("#chooseSecurityProperty").modal('hide');
}

mainContent.on("click", "#addNewProperty", function(){
  $('#chooseSecurityProperty').removeAttr('data-currentproperty');
  $("#chooseSecurityProperty").attr('data-updatepropertylist',"updateAssetPropertyList");
  $("#chooseSecurityProperty").attr("data-buildproperty","addAssetSecurityProperty");
  $("#chooseSecurityProperty").modal('show');
});


function appendSecurityProperty(prop){
  $("#definitionTable").find("tbody").append('<tr class="clickable-properties"><td style="display: none;">' + prop.id + '</td><td><div class="fillparent deleteProperty"><i class="fa fa-minus"></i></div></td><td class="theAssetPropName" name="name">' + prop.name + '</td><td name="value">'+ prop.value +'</td><td name="rationale">'+ prop.rationale +'</td></tr>').animate('slow');
};



mainContent.on("click", "#addNewAssociation", function(){
  var envName = $.session.get("assetEnvironmentName");
  var ursl = serverIP + "/api/assets/environment/" + encodeURIComponent(envName) + "/names";
  $("#editAssetsOptionsform").hide();
  $("#editAssociationsWindow").show(function(){
    $.ajax({
      type: "GET",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
/*      data: {
        session_id: String($.session.get('sessionID'))
      }, */
      crossDomain: true,
      url: ursl,
      success: function (data) {
        var tailAssetBox = $("#tailAsset");
        tailAssetBox.empty()
        $.each(data, function(idx,assetName) {
          tailAssetBox.append('<option value="' + assetName + '">' + assetName + '</option>');
        });
      },
      error: function (xhr, textStatus, errorThrown) {
        var error = JSON.parse(xhr.responseText);
        showPopup(false, String(error.message));
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
    $(this).addClass("newAssociation");
  });
});

mainContent.on('click', '#cancelButtonAsset', function(){
  $("#editAssetsOptionsform").show();
  $("#editAssociationsWindow").hide();
});


function commitAsset(){
  var assetName = (JSON.parse($.session.get("Asset"))).theName;
  var asset = JSON.parse($.session.get("Asset"));
  var envProps = asset.theEnvironmentProperties;
  if (envProps == undefined || envProps.length == 0) {
    alert("Environments not defined");
  }
  else {
    if($("#editAssetsOptionsform").hasClass("new")){
      postAssetForm($("#editAssetsOptionsform"), function(){
        $('#menuBCClick').attr('dimension','asset');
        refreshMenuBreadCrumb('asset');
      });
    }
    else{
      putAsset(assetName,assetFormToJSON($('#editAssetsOptionsform')), function () {
        $('#menuBCClick').attr('dimension','asset');
        refreshMenuBreadCrumb('asset');
      });
    }
  }
}


function fillAssetEnvironments(data){
  var i = 0;
  var textToInsert = [];
  $.each(data, function(arrayindex, value) {
    textToInsert[i++] = '<tr><td class="removeAssetEnvironment"><i class="fa fa-minus"></i></td><td class="clickable-environments assetEnvironmentRow">';
    textToInsert[i++] = value.theEnvironmentName;
    textToInsert[i++] = '</td></tr>';
  });
  $('#theEnvironmentDictionary').find("tbody").empty();
  $('#theEnvironmentDictionary').append(textToInsert.join(''));
  $("#theEnvironmentDictionary").find(".clickable-environments:first").trigger('click');
}

function assetFormToJSON(data){
  var json =  JSON.parse($.session.get("Asset"));
  json.theName = $(data).find('#theName').val();

  json["theShortCode"] = $(data).find('#theShortCode').val();
  json["theDescription"] = $(data).find('#theDescription').val();
  json["theSignificance"] = $(data).find('#theSignificance').val();
  json["theCriticalRationale"] = $(data).find('#theCriticalRationale').val();
  json["isCritical"] = +$("#isCritical").is( ':checked' );
  json.theType =  $(data).find( "#theType option:selected" ).text().trim();
  
  if ($('#theTags').val() != '') {
    json["theTags"] = $(data).find('#theTags').val().split(',').map(function(t){return t.trim();});
  }
  else {
    json["theTags"] = [];
  }

  $(data).children().each(function () {
    if(String($(this).prop("tagName")).toLowerCase() == "p"){
      $(this).children().each(function() {
        if(String($(this).prop("tagName")).toLowerCase() == "input"){
          json[$(this).prop("name")] = $(this).val();
        }

        if(String($(this).prop("tagName")).toLowerCase() == "select"){
          var id = $(this).attr('id');
          $(this).children().each(function() {
            var attr = $(this).attr('selected');
            if (typeof attr !== typeof undefined && attr !== false) {
              json[id] = $(this).val();
            }
          });
        }
      });
    }
  });
  json['theEnvironmentProperties'] = json.theEnvironmentProperties;
  clearLocalStorage("asset");
  return json
}

function postAssetForm(data,callback){
  var newAsset = assetFormToJSON(data);
  var assetName = $(data).find('#theName').val();
  var asobject = {};
  asobject.object = newAsset
  postAsset(asobject,callback);
}

function getAssetDefinition(props){
  $('#Properties').find('tbody').empty();
  var i = 0;
  var textToInsert = [];
  $.each(props, function(index, object) {
    if (object.value != "None") {
      appendSecurityProperty(object);
    }
  });
  $('#Properties').find('tbody').append(textToInsert.join(''));
}

function putAsset(assetName,json,callback){
  var ursl = serverIP + "/api/assets/name/"+ encodeURIComponent(assetName) + "?session_id=" + String($.session.get('sessionID'));
  var output = {};
  output.object = json;
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
    url: ursl,
    success: function (data) {
      showPopup(true);
      if(typeof(callback) == "function"){
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

function postAsset(json,callback){
  var ursl = serverIP + "/api/assets?session_id=" + String($.session.get('sessionID'));

  var output = JSON.stringify(json);

  $.ajax({
    type: "POST",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: ursl,
    success: function (data) {
      showPopup(true);
      if(typeof(callback) == "function"){
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

mainContent.on('click','td.asset-interface',function(){
  var intRow = $(this).closest("tr");
  var selectedInt = {};
  selectedInt.theName = intRow.find("td:eq(1)").text();
  selectedInt.theType = intRow.find("td:eq(2)").text();
  selectedInt.theAccessRight = intRow.find("td:eq(3)").text();
  selectedInt.thePrivilege = intRow.find("td:eq(4)").text();

  $('#addInterfaceDialog').attr('data-selectedInterface',JSON.stringify(selectedInt));
  $('#addInterfaceDialog').attr('data-selectedIndex',intRow.index());
  $("#addInterfaceDialog").attr('data-updateinterface',"updateAssetInterface");
  $('#addInterfaceDialog').modal('show');
});


mainContent.on('click','#addAssetInterface',function() {
  $('#addInterfaceDialog').removeAttr('data-selectedInterface');
  $('#addInterfaceDialog').removeAttr('data-selectedIndex');
  $("#addInterfaceDialog").attr('data-updateinterface',"updateAssetInterface");
  $('#addInterfaceDialog').modal('show');
});

mainContent.on('click','#isCritical', function() {
  if ($("#isCritical").is(':checked')) {
    $('#theCriticalRationale').prop("disabled",false); 
  }
  else {
    $('#theCriticalRationale').prop("disabled",true); 
  }
});


mainContent.on('click', '#CloseAsset', function (e) {
  e.preventDefault();
  clearLocalStorage("asset");
  $("#objectViewer").empty();
  $('#menuBCClick').attr('dimension','asset');
  refreshMenuBreadCrumb('asset'); 
});

function updateAssetInterface() {
  var selectedInt = {};
  selectedInt.theInterfaceName = $('#theInterfaceName').val();
  selectedInt.theInterfaceType = $('#theInterfaceType').val();
  selectedInt.theAccessRight = $('#theAccessRight').val();
  selectedInt.thePrivilege = $('#thePrivilege').val();

  var asset = JSON.parse($.session.get("Asset"));
  var selectedIdx = $('#addInterfaceDialog').attr('data-selectedIndex');
  if (selectedIdx != undefined) {
    asset.theInterfaces[selectedIdx] = selectedInt;
    $.session.set("Asset", JSON.stringify(asset));
    $('#theAssetInterfaces').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(selectedInt.theInterfaceName);
    $('#theAssetInterfaces').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(2)').text(selectedInt.theInterfaceType);
    $('#theAssetInterfaces').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(3)').text(selectedInt.theAccessRight);
    $('#theAssetInterfaces').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(4)').text(selectedInt.thePrivilege);
  }
  else {
    asset.theInterfaces.push(selectedInt);
    $.session.set("Asset", JSON.stringify(asset));
    appendAssetInterface(selectedInt);
  }
  $('#addInterfaceDialog').modal('hide');
}


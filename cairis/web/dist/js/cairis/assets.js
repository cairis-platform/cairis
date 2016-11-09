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
   fillAssetTable();
});

function fillAssetTable(){
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
      window.activeTable = "Assets";
      setTableHeader();
      createAssetsTable(data, function(){
        newSorting(1);
      });
      $.session.set("allAssets", JSON.stringify(data));
      activeElement("reqTable");
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function createAssetsTable(data, callback){
  var theTable = $(".theTable");
  var textToInsert = [];
  var i = 0;

  $.each(data, function(count, item) {
    textToInsert[i++] = '<tr>'

    textToInsert[i++] = '<td class="deleteAssetButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';

    textToInsert[i++] = '<td class="asset-rows" name="theName" value="' + item.theName + '">';
    textToInsert[i++] = item.theName;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '<td name="theType">';
    textToInsert[i++] = item.theType;
    textToInsert[i++] = '</td>';

    textToInsert[i++] = '<td name="theId" style="display:none;">';
    textToInsert[i++] = item.theId;
    textToInsert[i++] = '</td>';
    textToInsert[i++] = '</tr>';

  });
  theTable.append(textToInsert.join(''));
  $.contextMenu('destroy',$('.requirement-rows'));
  $("#reqTable").find("tbody").removeClass();

  callback();
}

$(document).on('click', "td.asset-rows", function(){
  activeElement("objectViewer");
  var name = $(this).attr('value');
  $.session.set("AssetName", name.trim());

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/assets/name/" + name.replace(" ", "%20"),
    success: function (newdata) {
      fillOptionMenu("fastTemplates/editAssetsOptions.html","#objectViewer",null,true,true, function(){
        $.session.set("Asset", JSON.stringify(newdata));
        $('#editAssetsOptionsform').loadJSON(newdata,null);
        $.ajax({
          type: "GET",
          dataType: "json",
          accept: "application/json",
          data: {
            session_id: String($.session.get('sessionID'))
          },
          crossDomain: true,
          url: serverIP + "/api/assets/name/" + newdata.theName + "/properties",
          success: function (data) {
            $.session.set("AssetProperties", JSON.stringify(data));
            fillEditAssetsEnvironment();
            $.ajax({
              type: "GET",
              dataType: "json",
              accept: "application/json",
              data: {
                session_id: String($.session.get('sessionID'))
              },
              crossDomain: true,
              url: serverIP + "/api/assets/types",
              success: function (data) {
                var typeSelect =  $('#theType');
                $.each(data, function (index, type) {
                  typeSelect
                    .append($("<option></option>")
                    .attr("value",type.theName)
                    .text(type.theName));
                });
                $("#theEnvironmentDictionary").find("tbody").find(".assetEnvProperties:first").trigger('click');
                $("#assetstabsID").show("fast");
              },
              error: function (xhr, textStatus, errorThrown) {
                debugLogger(String(this.url));
                debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
              }
            });
          },
          error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
          }
        });
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

var mainContent = $("#objectViewer");
mainContent.on('click', ".removeAssetEnvironment", function () {
  var envi = $(this).next(".clickable-environments").text();
  var row =  $(this).closest("tr");
  var asset = JSON.parse($.session.get("AssetProperties"));
  $.each(asset, function (index, env) {
    if(env.theEnvironmentName == envi){
      asset.splice( index ,1 );
      $.session.set("AssetProperties", JSON.stringify(asset));

      row.remove();
      var UIenv = $("#theEnvironmentDictionary").find("tbody");
      if(jQuery(UIenv).has(".removeAssetEnvironment").length){
        UIenv.find(".assetEnvProperties:first").trigger('click');
      }
      else {
        $("#assetstabsID").hide("fast");
      }
      return false;
    }
  });
});

mainContent.on('click', ".removeAssetAssociation", function () {
  var envName = $.session.get("assetEnvironmentName");
  $(this).closest("tr").remove();
  var asset = JSON.parse($.session.get("AssetProperties"));
  $.each(asset, function (index, env) {
    if(env.theEnvironmentName == envName){
      env.theAssociations.splice( index ,1 );
      $.session.set("AssetProperties", JSON.stringify(asset));
      return false;
    }
  });
});

mainContent.on('click', ".removeAssetEnvironment", function () {
  var envName = $.session.get("assetEnvironmentName");
  $(this).closest("tr").remove();
  var asset = JSON.parse($.session.get("AssetProperties"));
  $.each(asset, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      env.theProperties.splice( index ,1 );
      $.session.set("AssetProperties", JSON.stringify(asset));
    }
  });
});


mainContent.on('click', '.assetEnvironmentRow', function(event){
  var assts = JSON.parse($.session.get("AssetProperties"));
  var text = $(this).text();
  $.session.set("assetEnvironmentName", text);
  var props;
  $.each(assts, function(arrayID,group) {
    if(group.theEnvironmentName == text){
      props = group.theProperties;
      $.session.set("thePropObject", JSON.stringify(group));
      $.session.set("Arrayindex", arrayID);
      $.session.set("UsedProperties", JSON.stringify(props));
      getAssetDefinition(props);
      $("#assetAssociationsTable > tbody").empty();
      $.each(assts[arrayID].theAssociations,function(idx,assoc) {
        appendAssetAssociation(assoc);
      });
    }
  });
});

mainContent.on('click', '.clickable-properties', function(){
  var propRow = $(this).closest("tr");
  var propName = propRow.find("td:eq(2)").text();
  var assetProperties = JSON.parse( $.session.get("AssetProperties"));
  var theEnvName = $.session.get("assetEnvironmentName");

  var currentProp = {};
  $.each(assetProperties, function (index, env) {
    if(env.theEnvironmentName == theEnvName){
      $.each(env.theProperties, function(idx, assetProp){
        if (propName == assetProp.name) {
          currentProp = assetProp;
          var defaultProp = {};
          defaultProp.name = propName;
          defaultProp.value = 'None';
          defaultProp.rationale = '';
          assetProperties[index].theProperties[idx] = defaultProp;
        }
      });
    }
  });

  var hasProperties = [];
  $("#definitionTable").find(".theAssetPropName").each(function(index, prop){
    hasProperties.push($(prop).text());
  });

  securityPropertyDialogBox(hasProperties, currentProp, function (updProp) {
    $.each(assetProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        $.each(env.theProperties, function(idx, assetProp){
          if (updProp.name == assetProp.name) {

            assetProperties[index].theProperties[idx] = updProp;
            $.session.set("AssetProperties", JSON.stringify(assetProperties));
            propRow.find("td:eq(2)").text(updProp.name);
            propRow.find("td:eq(3)").text(updProp.value);
            propRow.find("td:eq(4)").text(updProp.rationale);
          }
        });
      }
    });
  });
});

mainContent.on('dblclick', '.clickable-associations', function(){
  $.session.set("AssociationIndex",$(this).index());
  var row =  $(this).closest("tr");
  $("#editAssetsOptionsform").hide();
  $("#editAssociationsWindow").show(function() {
    $("#headNav").val(row.find("#hNav").text());
    $("#headAdorn").val(row.find("#hAdorn").text());
    $("#headNry").val(row.find("#hNry").text());
    $("#headRole").val(row.find("#hRole").text());
    $("#tailRole").val(row.find("#tRole").text());
    $("#tailNry").val(row.find("#tNry").text());
    $("#tailAdorn").val(row.find("#tAdorn").text());
    $("#tailNav").val(row.find("#tNav").text());

    var envName = $.session.get("assetEnvironmentName");
    $.ajax({
      type: "GET",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/assets/environment/" + envName.replace(' ',"%20") + "/names",
      success: function (data) {
        var tailAssetBox = $("#tailAsset");
        tailAssetBox.empty()
        $.each(data, function(idx,assetName) {
          tailAssetBox.append("<option value=" + assetName + ">" + assetName + "</option>");
        });
      },
      error: function (xhr, textStatus, errorThrown) {
        var error = JSON.parse(xhr.responseText);
        showPopup(false, String(error.message));
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
    $("#tailAsset").val(row.find("#tAsset").text());
  });
});




mainContent.on('click', '.addEnvironmentPlus',function(){
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
        $(".clickable-environments  td").each(function() {
          if(this.innerHTML.trim() == item){
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
              $(this).dialog("close");
              var chosenText = $( "#comboboxDialogSelect").find("option:selected" ).text();
              $("#theEnvironmentDictionary").find("tbody").append("<tr><td class='deleteAssetEnv'><i class='fa fa-minus'></i></td><td class='clickable-environments'>" + chosenText +"</td></tr>");
              var sessionProps = $.session.get("AssetProperties");
              if(! sessionProps) {
                var Assetprops = [];
                var newProp = jQuery.extend(true, {}, AssetEnvironmentProperty);
                newProp.theEnvironmentName = chosenText;
                Assetprops.push(newProp);
              } 
              else {
                var Assetprops = JSON.parse($.session.get("AssetProperties"));
                var newProp = jQuery.extend(true, {}, AssetEnvironmentProperty);
                newProp.theEnvironmentName = chosenText;
                Assetprops.push(newProp);
              }
              $.session.set("AssetProperties", JSON.stringify(Assetprops));
              $("#theEnvironmentDictionary").find("tbody").find(".assetEnvProperties:first").trigger('click');
              $("#assetstabsID").show("fast");
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
});

mainContent.on("click", "#updateButtonAsset", function(){
  var allprops = JSON.parse($.session.get("AssetProperties"));
  var props;

  if($("#editAssociationsWindow").hasClass("newAssociation")){
    $("#editAssociationsWindow").removeClass("newAssociation");
    var assoc = [];
    assoc.push( $("#headNav").val());
    assoc.push( $("#headAdorn").val());
    assoc.push( $("#headNry").val());
    assoc.push( $("#headRole").val());
    assoc.push( $("#tailRole").val());
    assoc.push( $("#tailNry").val());
    assoc.push( $("#tailAdorn").val());
    assoc.push( $("#tailNav").val());
    assoc.push( $("#tailAsset").val());
    var arrIndex = $.session.get("Arrayindex");
    allprops[arrIndex].theAssociations.push(assoc);
    appendAssetAssociation(assoc);
    $("#editAssetsOptionsform").toggle();
    $("#editAssociationsWindow").toggle();
  }
  else {
    var row = $.session.get("associationRow");	
    var assoc = [];
    assoc.push( $("#headNav").val());
    assoc.push( $("#headAdorn").val());
    assoc.push( $("#headNry").val());
    assoc.push( $("#headRole").val());
    assoc.push( $("#tailRole").val());
    assoc.push( $("#tailNry").val());
    assoc.push( $("#tailAdorn").val());
    assoc.push( $("#tailNav").val());
    assoc.push( $("#tailAsset").val());
    var arrIndex = $.session.get("Arrayindex");

    var associationIdx = $.session.get("AssociationIndex");
    $.each(allprops[arrIndex].theAssociations, function(idx,eAssoc) {
      if (idx == associationIdx) {
        allprops[arrIndex].theAssociations[idx] = assoc;
        $("#assetAssociationsTable").find("tr").eq(associationIdx + 1).replaceWith(assocToTr(assoc));
        $.session.set("AssetProperties", JSON.stringify(allprops))
        $("#editAssetsOptionsform").toggle();
        $("#editAssociationsWindow").toggle();
        $("#theEnvironmentDictionary").find("tbody").find(".assetEnvironmentRow:first").trigger('click');

      }
    });
  }
  $.session.set("AssetProperties", JSON.stringify(allprops));
  fillEditAssetsEnvironment();
});

function appendAssetAssociation(assoc) {
  $("#assetAssociationsTable").find("tbody").append(assocToTr(assoc)).animate('slow');
}

function assocToTr(assoc) {
  return "<tr class='clickable-associations'><td class='removeAssetAssociation'><i class='fa fa-minus'></i></td><td class='assetAssociation' id='hNav'>" + assoc[0] + "</td><td id='hAdorn'>" + assoc[1] + "</td><td id='hNry'>" + assoc[2] + "</td><td id='hRole'>" + assoc[3] + "</td><td id='tRole'>" + assoc[4] + "</td><td id='tNry'>" + assoc[5] + "</td><td id='tAdorn'>" + assoc[6] + "</td><td id='tNav'>" + assoc[7] + "</td><td id='tAsset'>" + assoc[8] + "</td></tr>";
}

mainContent.on('click', '.removeEnvironment', function () {
  var assetProps = JSON.parse($.session.get("AssetProperties"));
  var text = $(this).next('td').text();
  var theIndex = -1;
  $.each(assetProps, function(arrayID,prop) {
    if(prop.environment == text){
      theIndex = arrayID;
    }
  });
  //Splice = removes element at "theIndex", 1 = only one item
  assetProps.splice(theIndex, 1);
  debugLogger(JSON.stringify(assetProps));
  $.session.set("AssetProperties", JSON.stringify(assetProps));
});

mainContent.on("click",".deleteProperty", function(){
   var removablerow = AssetEnvironmentPropertyAttribute;
   $(this).closest('tr').find("td").each( function(index, object){
     var attr = $(object).attr('name');
     if (typeof attr !== typeof undefined && attr !== false) {
       if (attr == "name" || attr == "rationale" || attr == "value") {
         removablerow[attr] = object.innerText;
       }
     }
   });
   var assts = JSON.parse($.session.get("AssetProperties"));
   var props = assts[  $.session.get("Arrayindex")];
   $.each(props.attributes, function(index, obj){
     if (removablerow["name"] == obj["name"] &&  removablerow["value"] == obj["value"]){
       props.attributes.splice(index, 1);
       assts[  $.session.get("Arrayindex")] = props;
       /*updating webpage & database*/
       updateAssetEnvironment(assts);
       $.session.set("AssetProperties", JSON.stringify(assts));
       fillEditAssetsEnvironment();
     }
   });
});

$(document).on('click', "#addNewAsset",function(){
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editAssetsOptions.html","#objectViewer",null,true,true,function(){
    $.ajax({
      type: "GET",
      dataType: "json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: serverIP + "/api/assets/types",
      success: function (data) {
        var typeSelect =  $('#theType');
        $.each(data, function (index, type) {
          typeSelect.append($("<option></option>").attr("value",type.name).text(type.theName));
        });
        $("#assetstabsID").hide();
      },
      error: function (xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
    // empty it because new environment;
    $.session.set("AssetProperties","");
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
      data: {
        session_id: String($.session.get('sessionID')),
        name: assetName
      },
      crossDomain: true,
      url: serverIP + "/api/assets/name/" + assetName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
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
            window.activeTable = "Assets";
            setTableHeader();
            createAssetsTable(data, function(){
              newSorting(1);
            });
            activeElement("reqTable");
          },
          error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
          }
        });
      },
      error: function (xhr, textStatus, errorThrown) {
        debugLogger(String(this.url));
        debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
      }
    });
  });
});

mainContent.on("click", "#addNewProperty", function(){

  var hasProperties = [];
  $("#definitionTable").find(".theAssetPropName").each(function(index, prop){
    hasProperties.push($(prop).text());
  });

  securityPropertyDialogBox(hasProperties, undefined, function (prop) {
    var assetProperties = JSON.parse( $.session.get("AssetProperties"));
    var theEnvName = $.session.get("assetEnvironmentName");
    $.each(assetProperties, function (index, env) {
      if(env.theEnvironmentName == theEnvName){
        $.each(env.theProperties, function(idx, assetProp){
          if (prop.name == assetProp.name) {
            assetProp.value = prop.value;
            assetProp.rationale = prop.rationale;
            assetProperties[index].theProperties[idx] = assetProp;
            $.session.set("AssetProperties", JSON.stringify(assetProperties));
            appendSecurityProperty(prop);
          }
        });
      }
    });
  });
});

function appendSecurityProperty(prop){
  $("#definitionTable").find("tbody").append('<tr class="clickable-properties"><td style="display: none;">' + prop.id + '</td><td><div class="fillparent deleteProperty"><i class="fa fa-minus"></i></div></td><td class="theAssetPropName" name="name">' + prop.name + '</td><td name="value">'+ prop.value +'</td><td name="rationale">'+ prop.rationale +'</td></tr>').animate('slow');
};



mainContent.on("click", "#addNewAssociation", function(){
  var envName = $.session.get("assetEnvironmentName");
  var ursl = serverIP + "/api/assets/environment/" + envName.replace(' ',"%20") + "/names";
  $("#editAssetsOptionsform").hide();
  $("#editAssociationsWindow").show(function(){
    $.ajax({
      type: "GET",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      data: {
        session_id: String($.session.get('sessionID'))
      },
      crossDomain: true,
      url: ursl,
      success: function (data) {
        var tailAssetBox = $("#tailAsset");
        tailAssetBox.empty()
        $.each(data, function(idx,assetName) {
          tailAssetBox.append("<option value=" + assetName + ">" + assetName + "</option>");
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

mainContent.on('click', '#UpdateAsset',function(e){
  $("#editAssetsOptionsform").validator();
  var envProps = $.session.get("AssetProperties");
  if (envProps == undefined || envProps.length == 0) {
    alert("Environments not defined");
  }
  else {
    if($("#editAssetsOptionsform").hasClass("new")){
      postAssetForm($("#editAssetsOptionsform"), function(){});
    }
    else{
      putAssetForm($("#editAssetsOptionsform"));
    }
    fillAssetTable();

  }
  e.preventDefault();
});

mainContent.on('click', '#CloseAsset', function (e) {
  e.preventDefault();
  fillAssetTable();
});

function fillEditAssetsEnvironment(){
  var data = JSON.parse( $.session.get("AssetProperties"));
  var i = 0;
  var textToInsert = [];
  $.each(data, function(arrayindex, value) {
    textToInsert[i++] = '<tr><td class="removeAssetEnvironment"><i class="fa fa-minus"></i></td><td class="clickable-environments assetEnvironmentRow">';
    textToInsert[i++] = value.theEnvironmentName;
    textToInsert[i++] = '</td></tr>';
  });
  $('#theEnvironmentDictionary').find("tbody").empty();
  $('#theEnvironmentDictionary').append(textToInsert.join(''));

  var env = $.session.get("assetEnvironmentName");

  var props;
  $.each(data, function(arrayID,group) {
    if(group.environment == env){
      getAssetDefinition(group.attributes);
      $.session.set("thePropObject", JSON.stringify(group));
    }
  });
  $("#theEnvironmentDictionary").find(".assetEnvironmentRow:first").trigger('click');
}

function assetFormToJSON(data, newAsset){
  var json
  if(newAsset){
    json = jQuery.extend(true, {},mainAssetObject );
  }
  else{
    json =  JSON.parse($.session.get("Asset"));
  }
  json.theName = $(data).find('#theName').val();

  json["theShortCode"] = $(data).find('#theShortCode').val();
  json["theDescription"] = $(data).find('#theDescription').val();
  json["theSignificance"] = $(data).find('#theSignificance').val();
  json["theCriticalRationale"] = $(data).find('#theCriticalRationale').val();
  json["isCritical"] = +$("#isCritical").is( ':checked' );
  json.theType =  $(data).find( "#theType option:selected" ).text().trim();


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
  json['theEnvironmentProperties'] = JSON.parse($.session.get("AssetProperties"));
  return json
}

function putAssetForm(data){
  putAsset(assetFormToJSON(data));
}

function postAssetForm(data,callback){
  var newAsset = assetFormToJSON(data,true);
  var assetName = $(data).find('#theName').val();
  var asobject = {};
  asobject.object = newAsset
  $.session.set("AssetName",assetName);
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

function putAssetProperty(assetSON){
  var ursl = serverIP + "/api/assets/name/"+ $.session.get("AssetName").replace(' ',"%20") + "/properties?session_id=" + String($.session.get('sessionID'));
  var propsJon = JSON.parse($.session.get("thePropObject")).attributes;
  var theWholeObject = JSON.parse($.session.get("AssetProperties"));

  var index = -1;
  var theEnvProps = JSON.parse($.session.get("thePropObject"));
  theEnvProps.attributes[$.session.get("Arrayindex")] = assetSON;

  $.each(theWholeObject, function(index, obje){
    if(obje.environment == theEnvProps.environment){
      theWholeObject[index] = theEnvProps;
    }
  });

  $.session.set("AssetProperties", theWholeObject);

  $.ajax({
    type: "PUT",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    origin: serverIP,
    data: output,
    url: ursl,
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

function putAsset(json){
  var ursl = serverIP + "/api/assets/name/"+ $.session.get("AssetName").replace(' ',"%20") + "?session_id=" + String($.session.get('sessionID'));

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

function updateAssetEnvironment(json,callback){
  var ursl = serverIP + "/api/assets/name/"+ $.session.get("AssetName").replace(' ',"%20") + "/properties?session_id=" + String($.session.get('sessionID'));

  var output = {};
  output.object = json;
  var output2 = JSON.stringify(output);

  $.ajax({
    type: "PUT",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output2,
    url: ursl,
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

function newAssetEnvironment(jsonString,callback){
  var ursl = serverIP + "/api/assets/name/"+ $.session.get("AssetName").replace(' ',"%20") + "/properties?session_id=" + String($.session.get('sessionID'));
  var output = {};

  if(typeof jsonString == 'undefined'){
    output = jQuery.extend(true, {},AssetEnvironmentProperty );
  }
  else{
    output.object = JSON.parse(jsonString);
    var output2 = JSON.stringify(output);
  }
  $.ajax({
    type: "PUT",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output2,
    url: ursl,
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


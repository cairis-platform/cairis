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


$(document).on('click', "button.editAssetsButton",function(){
  var name = $(this).attr("value");
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
      // console.log(JSON.stringify(rawData));
      fillOptionMenu("fastTemplates/editAssetsOptions.html","#optionsContent",null,true,true, function(){
        $.session.set("Asset", JSON.stringify(newdata));
        $('#editAssetsOptionsform').loadJSON(newdata,null);
        $("#optionsHeaderGear").text("Asset properties");
        forceOpenOptions();
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

optionsContent.on('click', ".removeAssetEnvironment", function () {
  var envi = $(this).next(".clickable-environments").text();
  var row =  $(this).closest("tr")
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

optionsContent.on('click', '.assetEnvironmetRow', function(event){
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
    }
  });
});

optionsContent.on('dblclick', '.clickable-properties', function(){
  var test = $(this);
  $("#editAssetsOptionsform").hide();
  var label = test.find(".theAssetPropName").text();

  $("#editpropertiesWindow").show(function(){
    var jsonn = JSON.parse($.session.get("thePropObject"));
    var theRightprop;
    $.each(jsonn.theProperties,function(arrayID,data){
      if(data.name == label){
        theRightprop = data;
        $("#property").val(theRightprop.name);
        $('#editpropertiesWindow').loadJSON(theRightprop,null);
      }
    });
  });
});

optionsContent.on('click', '.addEnvironmentPlus',function(){
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
              $("#optionsHeaderGear").text("Asset properties");
              forceOpenOptions();
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

optionsContent.on("click", "#updateButtonAsset", function(){
  var allprops = JSON.parse($.session.get("AssetProperties"));
  var props;

  if($("#editpropertiesWindow").hasClass("newProperty")){
    props =  jQuery.extend(true, {},AssetEnvironmentPropertyAttribute );
    props.name =   $("#property").find("option:selected").text().trim();
    props.value =  $("#value").find("option:selected").text().trim();
    props.rationale = $("#rationale").val();
    var idx = $.session.get("Arrayindex") || 0;
    allprops[idx].theProperties.push(props);
    $("#editAssetsOptionsform").show();
    $("#editpropertiesWindow").hide();
  }
  else if($("#editAssociationsWindow").hasClass("newAssociation")){
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
    var idx = $.session.get("Arrayindex") || 0;
    allprops[idx].theAssociations.push(assoc);
    $("#editAssetsOptionsform").show();
    $("#editAssociationsWindow").hide();
  }
  else {
    props = JSON.parse($.session.get("thePropObject"));
    props.name =   $("#property").find("option:selected").text().trim();
    props.value =  $("#value").find("option:selected").text().trim();
    props.rationale = $("#rationale").val();
    var arrIndex = $.session.get("Arrayindex");
    $.each(allprops[arrIndex].theProperties, function(index, object){
      if(object.name == props.name){
        allprops[$.session.get("Arrayindex")].theProperties[index].name = props.name;
        allprops[$.session.get("Arrayindex")].theProperties[index].value = props.value;
        allprops[$.session.get("Arrayindex")].theProperties[index].rationale = props.rationale;
        $.session.set("AssetProperties", JSON.stringify(allprops))
      }
      updateAssetEnvironment(allprops,function(){
        $("#editAssetsOptionsform").show();
        $("#editpropertiesWindow").hide();
      });
    });
  }
  $.session.set("AssetProperties", JSON.stringify(allprops));
  fillEditAssetsEnvironment();
});

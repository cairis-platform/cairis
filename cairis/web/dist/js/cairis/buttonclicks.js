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



/*
 Function for adding a row to the table
 */
$("#addReq").click(function() {
  addReq();
});

$("#addReqMenu").click(function() {
  addReq();
});

function addReq() {

    var kind  = "";

    //var clonedRow = $("#reqTable tr:last").clone();
    if($( "#assetsbox").find("option:selected" ).text() == "All" && $( "#environmentsbox").find("option:selected" ).text() == "All"){
        alert("Please select an asset or an environment");
    }
    else{
        if($( "#assetsbox").find("option:selected" ).text() != ""){
            kind = "asset:" + $( "#assetsbox").find("option:selected" ).text();
        }else{
            kind = "environment:"+$( "#environmentsbox").find("option:selected" ).text();
        }
        var template = "";
        var num = findLabel();
        switch (window.activeTable) {
            case "Requirements":
                template = '<tr class="' + kind + '">' +
                    '<td name="theLabel">' + num + '</td>' +
                '<td name="theName" contenteditable="true"></td>'+
                '<td name="theDescription" contenteditable="true"></td>'+
                '<td name="thePriority" contenteditable="true">1</td>'+
                '<td name="theId" style="display:none;"></td>'+
                '<td name="theVersion" style="display:none;"></td>'+
                '<td name="rationale" contenteditable="true">None</td>'+
                '<td name="fitCriterion" contenteditable="true">None</td>'+
                '<td name="originator" contenteditable="true"></td>'+
                '<td name="type" contenteditable="true">Functional</td>'+
                '</tr>';
                break;
            case "Goals":
                template = '<tr><td name="theLabel">' + num + '</td><td name="theName" contenteditable="true" ></td><td name="theDefinition" contenteditable="true"></td><td name="theCategory" contenteditable="true">Maintain</td><td name="thePriority" contenteditable="true">Low</td><td name="theId" style="display:none;"></td><td name="fitCriterion" contenteditable="true" >None</td><td  name="theIssue" contenteditable="true">None</td><td name="originator" contenteditable="true"></td></tr>';
                break;
            case "Obstacles":
                template = '<tr><td name="theLabel">' + num + '</td><td name="theName" contenteditable="true">Name</td><td name="theDefinition" contenteditable="true">Definition</td><td name="theCategory" contenteditable="true">Category</td><td name="theId" style="display:none;"></td><td name="originator" contenteditable="true">Originator</td></tr>';
                break;
        }
        $("#reqTable").append(template);
        sortTableByRow(0);
    }

}

/*
 Removing the active tr
 */
$("#removeReq").click(function() {
  removeReq();
});

$("#removeReqMenu").click(function() {
  removeReq();
});

function removeReq(reqName) {
  if(window.activeTable =="Requirements"){
    var ursl = serverIP + "/api/requirements/name/" + reqName.replace(' ',"%20");
    var object = {};
    object.session_id= $.session.get('sessionID');
    var objectoutput = JSON.stringify(object);

    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      data: objectoutput,
      crossDomain: true,
      url: ursl,
      success: function (data) {
        $("tr").eq(getActiveindex()).detach();
        showPopup(true);
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
}

$("#requirementsClick").click(function(){
  window.activeTable = "Requirements";
  startingTable();
});

//Just for debugLogger
$("#testingButton").click(function(){
   showPopup(true);
});

//For debugLogger
$("#removesessionButton").click(function() {
  $.session.remove('sessionID');
  location.reload();
});

$("#gridGoals").click(function() {
  window.activeTable = "Goals";
  setTableHeader();
});
//gridObstacles
$("#gridObstacles").click(function() {
  window.activeTable = "Obstacles";
  setTableHeader();
});


$('#assetModelClick').click(function(){
  window.theVisualModel = 'asset';
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
      $.each(data, function(i, item) {
        $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>")
      });
      $( "#comboboxDialog" ).dialog({
        modal: true,
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
            getAssetview($( "#comboboxDialogSelect").find("option:selected" ).text());
          }
        }
      });
      $(".comboboxD").css("visibility","visible");
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
});

$('#goalModelClick').click(function(){
  window.theVisualModel = 'goal';
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
      $.each(data, function(i, item) {
        $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>")
      });
      $( "#comboboxDialog" ).dialog({
        modal: true,
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
            getGoalview($( "#comboboxDialogSelect").find("option:selected" ).text());
          }
        }
      });
      $(".comboboxD").css("visibility","visible");
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
});

$('#responsibilityModelClick').click(function(){
    window.theVisualModel = 'responsibility';
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
            $.each(data, function(i, item) {
                $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>")
            });
            $( "#comboboxDialog" ).dialog({
                modal: true,
                buttons: {
                    Ok: function() {
                        $( this ).dialog( "close" );
                        //Created a function, for readability
                        getResponsibilityview($( "#comboboxDialogSelect").find("option:selected" ).text());
                    }
                }
            });
            $(".comboboxD").css("visibility","visible");
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    })});

/*
 When goalview is clicked
 */
$('#obstacleModelClick').click(function(){
    window.theVisualModel = 'obstacle';
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
            $.each(data, function(i, item) {
                $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>")
            });
            $( "#comboboxDialog" ).dialog({
                modal: true,
                buttons: {
                    Ok: function() {
                        $( this ).dialog( "close" );
                        //Created a function, for readability
                        getObstacleview($( "#comboboxDialogSelect").find("option:selected" ).text());
                    }
                }
            });
            $(".comboboxD").css("visibility","visible");
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    })});

$('#riskModelClick').click(function(){
  window.theVisualModel = 'risk';
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
      $.each(data, function(i, item) {
        $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>")
      });
      $( "#comboboxDialog" ).dialog({
        modal: true,
        position: {my: 'center', at: 'center', collision: 'fit'},
        buttons: {
          Ok: function() {
            $( this ).dialog( "close" );
            getRiskview($( "#comboboxDialogSelect").find("option:selected" ).text());
          }
        }
      });
      $(".comboboxD").css("visibility","visible");
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
    })});


$('#taskModelClick').click(function(){
    window.theVisualModel = 'task';
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
            $.each(data, function(i, item) {
                $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>")
            });
            $( "#comboboxDialog" ).dialog({
                modal: true,
                buttons: {
                    Ok: function() {
                        $( this ).dialog( "close" );
                        //Created a function, for readability
                        getTaskview($( "#comboboxDialogSelect").find("option:selected" ).text());
                    }
                }
            });
            $(".comboboxD").css("visibility","visible");
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    })});


/*
 When personaview is clicked
 */
$('#personaModelClick').click(function(){
    window.theVisualModel = 'persona';
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))

        },
        crossDomain: true,
        url: serverIP + "/api/personas/all/names",
        success: function (data) {
            $("#comboboxDialogSelect").empty();
            $("#appersonasbox").empty();
            $.each(data, function(i, item) {
                $("#comboboxDialogSelect").append("<option value=" + item + ">"  + item + "</option>")
                $("#appersonasbox").append("<option value=" + item + ">"  + item + "</option>")
            });
            $( "#comboboxDialog" ).dialog({
                modal: true,
                buttons: {
                    Ok: function() {
                        $( this ).dialog( "close" );
                        //Created a function, for readability
                        var pName = $( "#comboboxDialogSelect").find("option:selected" ).text();
                        appendPersonaCharacteristics(pName,'All','All');
                        getPersonaview(pName,'All','All');
                    }
                }
            });
            $(".comboboxD").css("visibility","visible");
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    })});


$("#newClick").click(function () {
    postNewProject(function () {
        window.activeTable = "Requirements";
        startingTable();
    });
});

$(document).on('click', "button.editEnvironmentButton",function(){
    var name = $(this).attr("value");
    if(name == "AnewEnvironment"){
        fillOptionMenu("fastTemplates/editEnvironmentOptions.html", "#optionsContent", null, true, true, function () {
            forceOpenOptions();
            $("#editEnvironmentOptionsform").addClass("newEnvironment");
        });
    } else {
        $.session.set("EnvironmentName", name);

        $.ajax({
            type: "GET",
            dataType: "json",
            accept: "application/json",
            data: {
                session_id: String($.session.get('sessionID'))
            },
            crossDomain: true,
            url: serverIP + "/api/environments/name/" + name.replace(" ", "%20"),
            success: function (data) {
                // console.log(JSON.stringify(rawData));
                fillOptionMenu("fastTemplates/editEnvironmentOptions.html", "#optionsContent", null, true, true, function () {
                        forceOpenOptions();

                        $.session.set("editableEnvironment", JSON.stringify(data));
                        $('#editEnvironmentOptionsform').loadJSON(data, null);

                        $.each(data.theTensions, function (index, tension) {
                            setTimeout(function () {
                                var comboID = "#" + tension.attr_id + "-" + tension.base_attr_id;
                                $(comboID).val(String(tension.value));
                                $(comboID).attr("rationale", tension.rationale);
                            }, 10);
                        });
                        $.each(data.theEnvironments, function (index, env) {
                            $("#envToEnvTable").append("<tr><td><i class='fa fa-minus'></i></td><td>" + env + "</td></tr>");
                            $("#overrideCombobox").append($("<option />").text(env));
                        });
                        switch (data.theDuplicateProperty) {
                            case "Maximise":
                                $("#MaximiseID").prop('checked', true);
                                break;
                            case "Override":
                                $("#OverrideID").prop('checked', true);
                                $("#overrideCombobox").prop("disabled", false);

                                break;
                            case "None":
                                $("#overrideCombobox").prop("disabled", false);
                                $("#OverrideID").prop('checked', false);
                                $("#MaximiseID").prop('checked', false);
                                break;
                        }
                    }
                );
            },
            error: function (xhr, textStatus, errorThrown) {
                debugLogger(String(this.url));
                debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
            }
        });
    }
});
$(document).on('click', "button.deleteEnvironmentButton",function(){
    var name = $(this).attr("value");
    deleteEnvironment(name, function () {
        fillEnvironmentsTable();
    });
});

$("#environmentsClick").click(function () {
    fillEnvironmentsTable();
});

$("#environmentMenuClick").click(function () {
    fillEnvironmentsTable();
});



//This is delegation
var optionsContent = $('#optionsContent');
optionsContent.on('contextmenu', '.clickable-environments', function(){
    return false;
});


/*
 on evnironment radio change
 */
optionsContent.on('change', "#OverrideID", function () {
    if($("#OverrideID").prop("checked")){
        $("#overrideCombobox").prop("disabled",false);
    }
});
optionsContent.on('change', "#MaximiseID", function () {
    if($("#MaximiseID").prop("checked")){
        $("#overrideCombobox").prop("disabled",true);
    }
});

optionsContent.on('click', ".removeEnvinEnv", function () {
   var text = $(this).next().text();
    $(this).closest("tr").remove();
    $("#overrideCombobox").find("option").each(function () {
        var optionText = $(this).text();
        if(optionText == text){
            $(this).remove();
        }
    });
    if ($('#envToEnvTable').find("tbody").is(':empty')){
        $("input:radio[name='duplication']").each(function(i) {
            this.checked = false;
        });
    }
});

/* For the rationale in the environments edit*/
optionsContent.on("click", ".tensionCombobox", function () {
    optionsContent.find("#rationale").val(String($(this).attr("rationale")));
    $.session.set("tensionMatrix", this.id);
});
optionsContent.on("keyup", "#rationale", function () {
    $("#"+ $.session.get("tensionMatrix")).attr("rationale", $(this).val());
});

optionsContent.on("click", "#addEnvtoEnv", function () {
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
                $("#overrideCombobox").find("option").each(function() {
                    if(this.innerHTML.trim() == item){
                        found = true
                    }
                });
                //if not found in environments
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
                            $("#envToEnvTable").append("<tr><td class='removeEnvinEnv'><i class='fa fa-minus'></i></td><td>"+ text +"</td></tr>");
                            $("#overrideCombobox").append("<option value='" + text + "'>" + text + "</option>");
                            $(this).dialog("close");
                            //Only update when update is pressed!
                            /*var environment = JSON.parse($.session.get("editableEnvironment"));
                            environment.theEnvironments.push($( "#comboboxDialogSelect").find("option:selected" ).text());
                            $.session.set("editableEnvironment", JSON.stringify(environment));*/
                        }
                    }
                });
                $(".comboboxD").css("visibility", "visible");
            }else {
                alert("All environments are already added");
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });

});
optionsContent.on('click', "#updateButtonEnvironment", function () {
if($("#editEnvironmentOptionsform").hasClass("newEnvironment")){
    $("#editEnvironmentOptionsform").removeClass("newEnvironment");
    var env = jQuery.extend(true, {}, environmentDefault);
    env = fillupEnvironmentObject(env);
    postEnvironment(env, function () {
        fillEnvironmentsTable();
    });


}else{
    var env = JSON.parse($.session.get("editableEnvironment"));
    var oldName = env.theName;
    env =  fillupEnvironmentObject(env);
    putEnvironment(env, oldName, function () {
        fillEnvironmentsTable();
    });
}


});


$("#reqTable").on("click", "#addNewEnvironment", function () {
    var tbody = $("#reqTable").find("tbody");

    tbody.append('<tr><td><button class="editEnvironmentButton" value="AnewEnvironment">Edit</button> <button class="deleteEnvironmentButton" value="">Delete</button></td><td name="theName"></td><td name="theType"></td></tr>');
});

$("#reqTable").on("click", "td", function() {
   // console.log(getActiveindex());
    if(window.activeTable == "Requirements"){

    }
    //$('#reqTable').find('td:last').focus();
    $('#reqTable tr').eq(getActiveindex()).find('td:first').focus();
});

/*
Add a persona
 */
$(document).on('click', "#addNewPersona",function(){
    fillOptionMenu("fastTemplates/editPersonasOptions.html","#optionsContent",null,true,true,function(){
    forceOpenOptions();
    var typeSelect = $('#theType');
    typeSelect.append($('<option value="Primary"></option>'));
    typeSelect.append($('<option value="Secondary"></option>'));
})});

/*
Delete an asset
 */
$(document).on('click', "button.deletePersonaButton",function(){
    var name = $(this).attr("value");
    $.ajax({
        type: "DELETE",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID')),
            name: name
        },
        crossDomain: true,
        url: serverIP + "/api/persona/name/" + name,
        success: function (data) {
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
                    createPersonasTable(data, function(){
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


optionsContent.on('click', '#cancelButtonPersona', function(){
    $("#editPersonaOptionsform").show();
    $("#editpropertiesWindow").hide();
});
optionsContent.on('click', '#UpdatePersonainGear',function(e){
    e.preventDefault();
    //alert($('#theName').val());
   //var AssetSon =  JSON.parse($.session.get("Asset"));
    //If new aset
    if($("#editPersonasOptionsform").hasClass("new")){
        alert("HasClass");
        postPersonaForm($("#editPersonasOptionsform"), function(){
            //INHERE
            newPersonaEnvironment($.session.get("PersonaProperties"));
        });

    }
    else{
        putPersonaForm($("#editPersonasOptionsform"));
        updatePersonaEnvironment($.session.get("PersonaProperties"));
    }

    fillPersonaTable();

});

/**
 * Created by Raf on 30/04/2015.
 */



/*
 Function for adding a row to the table
 */
$("#addRow").click(function() {
    var kind  = "";

    //var clonedRow = $("#reqTable tr:last").clone();
    if($( "#assetsbox").find("option:selected" ).text() == "All" && $( "#environmentsbox").find("option:selected" ).text() == "All"){
        alert("Please select an asset or an environment");
    }
    else{
        if($( "#assetsbox").find("option:selected" ).text() != "All"){
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

});

/*
 Removing the active tr
 */
$("#removeReq").click(function() {
    if(window.activeTable =="Requirements"){
        var oldrow = $("tr").eq(getActiveindex()).detach();
    }

    //of remove
    //TODO: AJAX CALL BEFORE REMOVE
});

$("#gridReq").click(function(){
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
$("#showRolesButton").click(function () {
   fillRolesTable();
});
/*
 When assetview is clicked
 */
$('#assetView').click(function(){

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
    })});



$("#vulnerabilitiesClick").click(function(){
   createVulnerabilityTable()
});




$(document).on('click', "button.editRoleButton",function() {
   var name = $(this).val();
    if(name == undefined || name == "") {
        fillOptionMenu("fastTemplates/editRoleOptions.html", "#optionsContent", null, true, true, function () {
            forceOpenOptions();
            $("#editRoleOptionsform").addClass("newRole");
        });
    } else{
        $.ajax({
            type: "GET",
            dataType: "json",
            accept: "application/json",
            data: {
                session_id: String($.session.get('sessionID'))
            },
            crossDomain: true,
            url: serverIP + "/api/roles/name/" + name.replace(" ", "%20"),
            success: function (json) {
                fillOptionMenu("fastTemplates/editRoleOptions.html", "#optionsContent", null, true, true, function () {
                    forceOpenOptions();
                    var form = $('#editRoleOptionsform');
                    form.loadJSON(json, null);
                    $.session.set("RoleObject", JSON.stringify(json));

                    $.ajax({
                        type: "GET",
                        dataType: "json",
                        accept: "application/json",
                        data: {
                            session_id: String($.session.get('sessionID'))
                        },
                        crossDomain: true,
                        url: serverIP + "/api/roles/name/" + name.replace(" ", "%20") + "/properties",
                        success: function (json) {
                            $.each(json, function (index, value) {
                                $("#theEnvironments").find("tbody").append("<tr><td class='roleEnvironmentClick'>" + value.theEnvironmentName + "</td></tr>");
                            });
                            $.session.set("RoleEnvironments", JSON.stringify(json))
                        },
                        error: function (xhr, textStatus, errorThrown) {
                            var error = JSON.parse(xhr.responseText);
                            showPopup(false, String(error.message));
                            debugLogger(String(this.url));
                            debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
                        }
                    });


                });
            },
            error: function (xhr, textStatus, errorThrown) {
                var error = JSON.parse(xhr.responseText);
                showPopup(false, String(error.message));
                debugLogger(String(this.url));
                debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
            }
        });

    }
});
$("#startNewProject").click(function () {
    postNewProject(function () {
        window.activeTable = "Requirements";
        startingTable();
    });
});

$(document).on('click', "button.editVulnerabilityButton",function(){
    if($(this).hasClass("newVulnerability")){
        var vul = jQuery.extend(true, {}, vulnerabilityDefault);
        $.session.set("Vulnerability", JSON.stringify(vul));
        fillOptionMenu("fastTemplates/editVulnerabilityOptions.html", "#optionsContent", null, true, true, function () {
            $("#UpdateVulnerability").addClass("newVulnerability");
            $.ajax({
                type: "GET",
                dataType: "json",
                accept: "application/json",
                data: {
                    session_id: String($.session.get('sessionID'))
                },
                crfossDomain: true,
                url: serverIP + "/api/vulnerabilities/types",
                success: function (data) {
                    $.each(data, function (index, type) {
                        $('#theSeverity')
                            .append($("<option></option>")
                                .attr("value", type.theName)
                                .text(type.theName));
                    });
                },
                error: function (xhr, textStatus, errorThrown) {
                    debugLogger(String(this.url));
                    debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
                }
            });
            forceOpenOptions();
        });
    }
    else {
        var name = $(this).attr("value");
        $.session.set("VulnerabilityName", name.trim());

        $.ajax({
            type: "GET",
            dataType: "json",
            accept: "application/json",
            data: {
                session_id: String($.session.get('sessionID'))
            },
            crossDomain: true,
            url: serverIP + "/api/vulnerabilities/name/" + name.replace(" ", "%20"),
            success: function (newdata) {
                fillOptionMenu("fastTemplates/editVulnerabilityOptions.html", "#optionsContent", null, true, true, function () {
                        $.session.set("Vulnerability", JSON.stringify(newdata));
                        //removing theTags, because LOADJSON does some strange things with them.
                        var jsondata = $.extend(true, {}, newdata);
                        jsondata.theTags = [];
                        $('#editVulnerabilityOptionsform').loadJSON(jsondata, null);

                        $.ajax({
                            type: "GET",
                            dataType: "json",
                            accept: "application/json",
                            data: {
                                session_id: String($.session.get('sessionID'))
                            },
                            crfossDomain: true,
                            url: serverIP + "/api/vulnerabilities/types",
                            success: function (data) {
                                $.each(data, function (index, type) {
                                    $('#theSeverity')
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

                        var text = "";
                        $.each(newdata.theTags, function (index, tag) {
                            text += tag + ", ";
                        });
                        $("#theTags").val(text);

                        $.each(newdata.theEnvironmentProperties, function (index, envprop) {
                            $("#theVulEnvironments").append("<tr class='clickable-environments'><td class='deleteVulEnv'><i class='fa fa-minus'></i></td><td class='vulEnvProperties'>" + envprop.theEnvironmentName + "</td></tr>");
                        });

                        forceOpenOptions();
                        $("#theVulEnvironments").find(".vulEnvProperties:first").trigger('click');
                        $.session.set("VulnEnvironmentName", $("#theVulEnvironments").find(".vulEnvProperties:first").text());
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


$(document).on('click', "button.editEnvironmentButton",function(){
    var name = $(this).attr("value");
    if(name == "AnewEnvironment"){
        fillOptionMenu("fastTemplates/editEvironmentOptions.html", "#optionsContent", null, true, true, function () {
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
                fillOptionMenu("fastTemplates/editEvironmentOptions.html", "#optionsContent", null, true, true, function () {
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

$("#editEnvironmentsButton").click(function () {

    fillEnvironmentsTable();

});

$("#reqTable").on("click", "#addNewRole", function () {
    $("#reqTable").find("tbody").append('<tr><td><button class="editRoleButton" value="">Edit</button> <button class="deleteRoleButton" value="">Delete</button></td><td name="theName"></td><td name="theShortCode"></td><td name="theType"></td></tr>')
});
//addNewVulnerability
$("#reqTable").on("click", "#addNewVulnerability", function () {
    //$("#reqTable").find("tbody").append('<tr><td><button class="editVulnerabilityButton newVulnerability" value="">Edit</button> <button class="deleteVulnerabilityButton" value="">Delete</button></td><td name="theVulnerabilityName"></td><td name="theVulnerabilityType"></td></tr>');
    var vul = jQuery.extend(true, {}, vulnerabilityDefault);
    $.session.set("Vulnerability", JSON.stringify(vul));
    fillOptionMenu("fastTemplates/editVulnerabilityOptions.html", "#optionsContent", null, true, true, function () {
        $("#UpdateVulnerability").addClass("newVulnerability");
        $("#Properties").hide();
    });
    forceOpenOptions();
});

//This is delegation
var optionsContent = $('#optionsContent');
optionsContent.on('contextmenu', '.clickable-environments', function(){
    return false;
});
optionsContent.on('click', '.deleteVulEnv', function () {
   var propName = $(this).next("td").text();
   var vuln = JSON.parse($.session.get("Vulnerability"));

    $.each(vuln.theEnvironmentProperties, function (index, prop) {
       if(prop.theEnvironmentName == propName){
           vuln.theEnvironmentProperties.splice(index,1);
       }
    });
    $.session.set("Vulnerability", JSON.stringify(vuln));
    $(this).closest("tr").remove();
    var UIenv = $("#theVulEnvironments").find("tbody");
    if(jQuery(UIenv).has(".vulEnvProperties").length){
        UIenv.find(".vulEnvProperties:first").trigger('click');
    }else{
        $("#Properties").hide("fast");
    }

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
/*
Watch env props in Vulnerability
 */
optionsContent.on("click", ".vulEnvProperties", function () {
    var name = $(this).text();
    $.session.set("VulnEnvironmentName", name);
    $("#vulnEnvAssets").find("tbody").empty();
    var theVul = JSON.parse($.session.get("Vulnerability"));
    $.each(theVul.theEnvironmentProperties, function (index, prop) {
       if(prop.theEnvironmentName == name){
           if(prop.theSeverity == ""){
               //if new environment, choose first
               $("#theSeverity").val($("#theSeverity option:first").val());
           }else{
               $("#theSeverity").val(prop.theSeverity);
           }

           $.each(prop.theAssets, function (index, asset) {
               $("#vulnEnvAssets").find("tbody").append("<tr><td class='removeVulnEnvAsset'><i class='fa fa-minus'></i></td><td>"+ asset+"</td></tr>");
           });
       }
    })
});

/*
adding an Asset to an evironment of a Vulnerabilty
 */
optionsContent.on("click", "#addAssetToEnvFromVuln", function () {
    if($("#theVulEnvironments").find("tbody").children().length == 0){
        alert("First you have to add an environment");
    }
    else {
        var hasAssets = [];
        $(".removeVulnEnvAsset").next("td").each(function (index, tag) {
            hasAssets.push($(tag).text());
        });
        assetsDialogBox(hasAssets, function (text) {
            $("#vulnEnvAssets").find("tbody").append('<tr><td class="removeVulnEnvAsset"><i class="fa fa-minus"></i></td><td>' + text + '</td></tr>');
            var theVul = JSON.parse($.session.get("Vulnerability"));
            var EnvName = $.session.get("VulnEnvironmentName");
            $.each(theVul.theEnvironmentProperties, function (index, prop) {
                if (prop.theEnvironmentName == EnvName) {
                    prop.theAssets.push(text);
                }
            });
            debugLogger(theVul);
            $.session.set("Vulnerability", JSON.stringify(theVul));
        });
    }
});
/*
 removing an Asset to an evironment of a Vulnerabilty
 */
optionsContent.on("click", ".removeVulnEnvAsset", function () {
    var name = $(this).next("td").text();
    var theVul = JSON.parse($.session.get("Vulnerability"));
    var EnvName =$.session.get("VulnEnvironmentName");
    $.each(theVul.theEnvironmentProperties, function (index, prop) {
        if(prop.theEnvironmentName == EnvName){
            $.each(prop.theAssets, function (i, key) {
               if(key == name){
                   theVul.theEnvironmentProperties[index].theAssets.splice(i,1);
                   $.session.set("Vulnerability", JSON.stringify(theVul));
               }
            });
        }
    });
    $(this).closest("tr").remove();
});

optionsContent.on('click', '#UpdateVulnerability', function (e) {
    e.preventDefault();

    var theVul = JSON.parse($.session.get("Vulnerability"));
    theVul.theVulnerabilityName = $("#theVulnerabilityName").val();
   var arr = $("#theTags").val().split(", ")
    arr = $.grep(arr,function(n){ return(n) });
    theVul.TheType = arr;
    theVul.theVulnerabilityDescription = $("#theVulnerabilityDescription").val();
   // var test = $("#theVulnerabilityType");
    theVul.theVulnerabilityType = $("#theVulnerabilityType").val();

    var name = $.session.get("VulnEnvironmentName");
    $.each(theVul.theEnvironmentProperties, function (index, key) {
        if(key.theEnvironmentName == name){
            theVul.theEnvironmentProperties[index].theSeverity= $("#theSeverity").val();
        }
    });
    if($(this).hasClass("newVulnerability")){
        postVulnerability(theVul, function () {
            createVulnerabilityTable();
        });
    }
    else {
        putVulnerability(theVul, $.session.get("VulnerabilityName"), function () {
            createVulnerabilityTable();
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

/*
updating a role
 */
optionsContent.on('click','#UpdateRole', function (event) {
    event.preventDefault();

        if ($("#editRoleOptionsform").hasClass("newRole")) {
            //NEW ROLE
            //roleDefaultObject
            var theRoleObject = jQuery.extend(true, {},roleDefaultObject );
            theRoleObject.theName = optionsContent.find("#theName").val();
            theRoleObject.theShortCode = optionsContent.find("#theShortCode").val();
            theRoleObject.theDescription = optionsContent.find("#theDescription").val();
            theRoleObject.theType = optionsContent.find("#theType option:selected").text().trim();
            if (theRoleObject.theName == "" || theRoleObject.theShortCode == "" || theRoleObject.theDescription == "" || theRoleObject.theType == "") {
                alert("The Name, Shortcode, Description and Type must have a value");
            }else {
                postRole(theRoleObject, function () {
                    fillRolesTable();
                });
            }
        } else {
            //UPDATE ROLE
            var theRoleObject = JSON.parse($.session.get("RoleObject"));
            var oldname = theRoleObject.theName;
            theRoleObject.theName = optionsContent.find("#theName").val();
            theRoleObject.theShortCode = optionsContent.find("#theShortCode").val();
            theRoleObject.theDescription = optionsContent.find("#theDescription").val();
            theRoleObject.theType = optionsContent.find("#theType option:selected").text().trim();
            //debugLogger(JSON.stringify(theRoleObject));
            if (theRoleObject.theName == "" || theRoleObject.theShortCode == "" || theRoleObject.theDescription == "" || theRoleObject.theType == "") {
                alert("The Name, Shortcode, Description and Type must have a value");
            }else {
                updateRole(theRoleObject, oldname, function () {
                    fillRolesTable();
                });
            }
        }




});
$("#reqTable").on('click','.deleteVulnerabilityButton', function (event) {
    event.preventDefault();
    var name = $(this).attr("value");
    debugLogger("Delete: " + name + ".");
    deleteVulnerability( name, function () {
        createVulnerabilityTable();
    });
});

$("#reqTable").on('click','.deleteRoleButton', function (event) {
    event.preventDefault();
    var name = $(this).attr("value");
    debugLogger("Delete: " + name + ".");
    deleteRole( name, function () {
        fillRolesTable();
    });
});

optionsContent.on("click", '.roleEnvironmentClick', function () {
    $("#theCounterMeasures").find('tbody').empty();
     $("#theResponses").find('tbody').empty();


       var text =  $(this).text();
       var environments = JSON.parse($.session.get("RoleEnvironments"));
    var textForCounterMeasures = [];
    var textForResponses = [];
    var i =0;
     var j  = 0;
    $.each(environments, function (index, obj) {
        if(obj.theEnvironmentName == text){
            $.each(obj.theCountermeasures, function (index, val) {
                debugLogger("Found one" + val);
                textForCounterMeasures[i++] = "<tr><td>"+ val + "</td><tr>";
                //$("#theCounterMeasures").find('tbody').append( val );
            });
            var theResp = obj.theResponses;
            $.each(theResp , function (index1, valu) {
                textForResponses[j++] = "<tr><td>"+ valu.__python_tuple__[0] +"</td><td>"+ valu.__python_tuple__[1] +"</td></tr>";
            });
            $("#theCounterMeasures").find('tbody').append(textForCounterMeasures.join(''));
            $("#theResponses").find('tbody').append(textForResponses.join(''));
        }
    })

});
/*
adding an asset env to the Vulne.
 */
optionsContent.on('click', "#addVulEnv", function () {
    var hasEnv = [];
    $(".vulEnvProperties").each(function (index, tag) {
        hasEnv.push($(tag).text());
    });
    environmentDialogBox(hasEnv, function (text) {
        $("#theVulEnvironments").find("tbody").append('<tr class="clickable-environments"><td class="deleteVulEnv"><i class="fa fa-minus"></i></td><td class="vulEnvProperties">'+text+'</td></tr>');
        var environment =  jQuery.extend(true, {},vulEnvironmentsDefault );
        environment.theEnvironmentName = text;
        var theVul = JSON.parse($.session.get("Vulnerability"));
        theVul.theEnvironmentProperties.push(environment);
        $.session.set("Vulnerability", JSON.stringify(theVul));
        $.session.set("VulnEnvironmentName",text);
        $("#Properties").show("fast");
    });
});


optionsContent.on('click', '.removeEnvironment', function () {
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
/*
removing a prop
 */
 optionsContent.on("click",".deleteProperty", function(){

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
/*
Add an asset
 */
$(document).on('click', "#addNewAsset",function(){
    fillOptionMenu("fastTemplates/editAssetsOptions.html","#optionsContent",null,true,true,function(){
    forceOpenOptions();
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

/*
Delete an asset
 */
$(document).on('click', "button.deleteAssetButton",function(){
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
        url: serverIP + "/api/assets/name/" + newdata.theName + "/properties",
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




optionsContent.on("click", "#addNewProperty", function(){
    $("#editAssetsOptionsform").hide();
    $("#editpropertiesWindow").show(function(){
            $(this).addClass("newProperty");
    });

});

optionsContent.on('change', "#theType",function (){
  // alert($(this).val());
    //$(this).val("selected", $(this).val());
});

optionsContent.on('click', '#cancelButtonAsset', function(){
    $("#editAssetsOptionsform").show();
    $("#editpropertiesWindow").hide();
});
optionsContent.on('click', '#UpdateAssetinGear',function(e){
    e.preventDefault();
    //alert($('#theName').val());
   //var AssetSon =  JSON.parse($.session.get("Asset"));
    //If new aset
    if($("#editAssetsOptionsform").hasClass("new")){
        alert("HasClass");
        postAssetForm($("#editAssetsOptionsform"), function(){
            //INHERE
            newAssetEnvironment($.session.get("AssetProperties"));
        });

    }
    else{
        putAssetForm($("#editAssetsOptionsform"));
        updateAssetEnvironment($.session.get("AssetProperties"));
    }

    fillAssetTable();

});

$("#reqTable").on("click", "td", function() {
   // console.log(getActiveindex());
    if(window.activeTable == "Requirements"){

    }
    //$('#reqTable').find('td:last').focus();
    $('#reqTable tr').eq(getActiveindex()).find('td:first').focus();
});
$("#editAssetsClick").click(function(){
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

/*
For updating the Assets
 */

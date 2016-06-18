/**
 * Created by Raf on 24/04/2015.
 */
window.serverIP = "http://"+ window.location.host;

window.activeTable ="Requirements";
window.boxesAreFilled = false;
window.debug = true;

function debugLogger(info){
    if(debug){
        console.log(info);
    }
}
//The config window at start
var dialogwindow = $( "#dialogContent" ).dialog({
    autoOpen: false,
    modal: true,
    buttons: {
        OK: function() {
            showLoading();
            var json_text = JSON.stringify($('#configForm').serializeObject());
            var portArr  = json_text.match('port":"(.*)","user');
            var port = portArr[1];
            json_text = json_text.replace('"'+port+'"',port);
            debugLogger(json_text);
            $.ajax({
                type: 'POST',
                url: serverIP + '/api/user/config',
                data: json_text,
                accept:"application/json",
                contentType : "application/json",
                success: function(data, status, xhr) {
                    // console.log("DB Settings saved");
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

            /*$('#response').html('The value entered was ' + $('#myInput').val());
             record.find('.name').html($('#myInput').val());*/
            $( this ).dialog( "close" );

        },
        Cancel: function() {
            $( this ).dialog( "close" );
            $( "#errorDialog" ).dialog();
        }
    }
});



$(document).ready(function() {
  //  localStorage.removeItem('sessionID');
    var sessionID = $.session.get('sessionID');
    if(!sessionID){
        dialogwindow.dialog( "open" );
        hideLoading();
    }
    else{
        //Else we can show the table
       startingTable();
    }


});
function showLoading(){
    $(".loadingWrapper").fadeIn(500);
}
function hideLoading(){
    $(".loadingWrapper").fadeOut(500);
}

/*
Filling the asset environment in the HTML
 */
function fillEditAssetsEnvironment(){
    var data = JSON.parse( $.session.get("AssetProperties"));
    var i = 0;
    var textToInsert = [];
    $.each(data, function(arrayindex, value) {
        textToInsert[i++] = '<tr><td class="removeAssetEnvironment"><i class="fa fa-minus"></i></td><td class="clickable-environments assetEnvironmetRow">';
        textToInsert[i++] = value.theEnvironmentName;
        textToInsert[i++] = '</td></tr>';
    });
    $('#theEnvironmentDictionary').find("tbody").empty();
    $('#theEnvironmentDictionary').append(textToInsert.join(''));
    // $(".clickable-environments").contextMenu(menu);

    var env = $( "#theEnvironmentDictionary").find("tbody tr:eq(0) > td:eq(0)").text();

    var props;
    $.each(data, function(arrayID,group) {
        if(group.environment == env){
            getAssetDefinition(group.attributes);
            //props = group.attributes;
            $.session.set("thePropObject", JSON.stringify(group));

           // $.session.set("Arrayindex",arrayID);

        }
    });
    $("#theEnvironmentDictionary").find(".assetEnvironmetRow:first").trigger('click');

}

/*
For converting the form in JSON
 */
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
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

// For the assetsbox, if filter is selected
$('#assetsbox').change(function() {
    var selection = $(this).find('option:selected').text();
    debugLogger("Selection: " + selection);
    // Clearing the environmentsbox
    $('#environmentsbox').prop('selectedIndex', -1);

        if (selection.toLowerCase() == "all") {
            startingTable();
        } else {
            $.ajax({
                type: "GET",
                dataType: "json",
                accept: "application/json",
                data: {
                    session_id: String($.session.get('sessionID'))
                },
                crossDomain: true,
                url: serverIP + "/api/requirements/asset/" + encodeURIComponent(selection),
                success: function (data) {
                    createRequirementsTable(data);
                },
                error: function (xhr, textStatus, errorThrown) {
                    debugLogger(String(this.url));
                    debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
                }

            });
        }

});
/*
Same for the environments
*/
$('#environmentsbox').change(function() {
    var selection = $(this).find('option:selected').text();
    // Clearing the assetsbox
    $('#assetsbox').prop('selectedIndex', -1);

    if (selection.toLowerCase() == "all") {
        startingTable();
    } else {
        //Assetsbox
        $.ajax({
            type: "GET",
            dataType: "json",
            accept: "application/json",
            data: {
                session_id: String($.session.get('sessionID'))
            },
            crossDomain: true,
            url: serverIP + "/api/requirements/environment/" + encodeURIComponent(selection),
            success: function (data) {
                createRequirementsTable(data);
            },
            error: function (xhr, textStatus, errorThrown) {
                debugLogger(String(this.url));
                debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
            }

        });
    }

});
function getAssetview(environment){
    window.assetEnvironment = environment;
    $.ajax({
        type:"GET",
        accept:"application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + "/api/assets/model/environment/" + environment.replace(" ","%20"),
        success: function(data){
          // console.log("in getAssetView " + data.innerHTML);
           // console.log(this.url);
           fillSvgViewer(data);

        },
        error: function(xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }

    });
}


/*
A function for filling the table with requirements
 */
function createRequirementsTable(data){
    var tre;
    var theTable = $(".theTable");
    $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
    //var arr = reallyLongArray;
    var textToInsert = [];
    var  originator, rationale, fitCriterion, type = "";

    var theRows = [];
    var i = 0;
    var j = 0;
    $.each(data, function(count, item) {
        textToInsert[i++] = '<tr><td name="theLabel">';
        textToInsert[i++] = item.theLabel;
        textToInsert[i++] = '<'+'/td>';

        textToInsert[i++] = '<td name="theName" contenteditable=true>';
        textToInsert[i++] = item.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theDescription" contenteditable=true>';
        textToInsert[i++] = item.theDescription;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="thePriority"  contenteditable=true>';
        textToInsert[i++] = item.thePriority;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theId"  style="display:none;">';
        textToInsert[i++] = item.theId;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theVersion"  style="display:none;">';
        textToInsert[i++] = item.theVersion;
        textToInsert[i++] = '</td>';

        var datas = eval(item.attrs);
        for (var key in datas) {
            if (datas.hasOwnProperty(key)) {
                /*
                Made this so the TD's are in the right order.
                 */
                switch(key){
                    case "originator":
                        originator =   '<td name=' + key + ' contenteditable=true >'+ datas[key] + '</td>';
                        break;
                    case "rationale":
                        rationale =   '<td name=' + key + ' contenteditable=true >'+ datas[key] + '</td>';
                        break;
                    case "fitCriterion":
                        fitCriterion =   '<td name=' + key + ' contenteditable=true >'+ datas[key] + '</td>';
                        break;
                    case "type":
                        type =   '<td name=' + key + ' contenteditable=true >'+ datas[key] + '</td>';
                        break;
                }
              /*  if(key == ("originator") || key == ("rationale") || key == ("fitCriterion") || key == ("type")) {
                    // alert(key+': '+datas[key]); // this will show each key with it's value
                    // tre.append("<td name=" + key + " contenteditable=true >" + datas[key] + "</td>");
                    textToInsert[i++] = '<td name=';
                    textToInsert[i++] = key;
                    textToInsert[i++] = ' contenteditable=true >';
                    textToInsert[i++] = datas[key];
                    textToInsert[i++] = '</td>';

                }*/
            }
        }
        textToInsert[i++] = rationale;
        textToInsert[i++] = fitCriterion;
        textToInsert[i++] = originator;
        textToInsert[i++] = type;
        textToInsert[i++] = '</tr>';
    });

    // theRows[j++]=textToInsert.join('');
    theTable.append(textToInsert.join(''));

    theTable.css("visibility","visible");
}

/*
 A function for filling the table with requirements
 */
function createEditGoalsTable(){
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crfossDomain: true,
        url: serverIP + "/api/goals",
        success: function (data) {
            window.activeTable = "EditGoals";
            setTableHeader();
            var theTable = $(".theTable");
            $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
            //var arr = reallyLongArray;
            var textToInsert = [];
            var i = 0;

            $.each(data, function(count, item) {
                textToInsert[i++] = "<tr>";
                textToInsert[i++] = '<td><button class="editGoalsButton" value="' + item.theName + '">' + 'Edit' + '</button> <button class="deleteGoalButton" value="' + item.theName + '">' + 'Delete' + '</button></td>';

                textToInsert[i++] = '<td name="theName">';
                textToInsert[i++] = item.theName;
                textToInsert[i++] = '</td>';

                textToInsert[i++] = '<td name="theOriginator">';
                textToInsert[i++] = item.theOriginator;
                textToInsert[i++] = '</td>';

                textToInsert[i++] = '<td name="Status">';
                if(item.theColour == 'black'){
                    textToInsert[i++] = "Check";
                }else if(item.theColour == 'red'){
                    textToInsert[i++] = "To refine";
                }else{
                    textToInsert[i++] = "OK";
                }

                textToInsert[i++] = '</td>';

                textToInsert[i++] = '<td name="theId"  style="display:none;">';
                textToInsert[i++] = item.theId;
                textToInsert[i++] = '</td>';

                textToInsert[i++] = '</tr>';
            });

            // theRows[j++]=textToInsert.join('');
            theTable.append(textToInsert.join(''));

            theTable.css("visibility","visible");
            activeElement("reqTable");
            sortTableByRow(0);
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    })

}

function createAssetsTable(data, callback){

    var theTable = $(".theTable");
    var textToInsert = [];
    var i = 0;

    //var thedata = $.parseJSON(data);
    $.each(data, function(count, item) {
        textToInsert[i++] = "<tr>"

        textToInsert[i++] = '<td><button class="editAssetsButton" value="' + item.theName + '">' + 'Edit' + '</button> <button class="deleteAssetButton" value="' + item.theName + '">' + 'Delete' + '</button></td>';

        textToInsert[i++] = '<td name="theName">';
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
    callback();


}
/*
filling up the environment table
 */
function createEnvironmentsTable(data, callback){

    var theTable = $("#reqTable");
    var textToInsert = [];
    var i = 0;

    //var thedata = $.parseJSON(data);
    $.each(data, function(count, item) {
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td><button class="editEnvironmentButton" value="' + item.theName + '">' + 'Edit' + '</button> <button class="deleteEnvironmentButton" value="' + item.theName + '">' + 'Delete' + '</button></td>';

        textToInsert[i++] = '<td name="theName">';
        textToInsert[i++] = item.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theType">';
        textToInsert[i++] = item.theDescription;
        textToInsert[i++] = '</td></tr>';
    });
    theTable.append(textToInsert.join(''));
    callback();

}

/*
 A function for filling the table with Vulnerabilities
 */
function createVulnerabilityTable(){

    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crfossDomain: true,
        url: serverIP + "/api/vulnerabilities",
        success: function (data) {
            window.activeTable = "Vulnerability";
            setTableHeader();
            var theTable = $(".theTable");
            $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
            //var arr = reallyLongArray;
            var textToInsert = [];
            var i = 0;

            $.each(data, function(count, item) {
                textToInsert[i++] = "<tr>"
                textToInsert[i++] = '<td><button class="editVulnerabilityButton" value="' + item.theVulnerabilityName + '">' + 'Edit' + '</button> <button class="deleteVulnerabilityButton" value="' + item.theVulnerabilityName + '">' + 'Delete' + '</button></td>';
                textToInsert[i++] = '<td name="theVulnerabilityName">';
                textToInsert[i++] = item.theVulnerabilityName;
                textToInsert[i++] = '</td>';

                textToInsert[i++] = '<td name="theVulnerabilityType">';
                textToInsert[i++] = item.theVulnerabilityType;
                textToInsert[i++] = '</td>';


                textToInsert[i++] = '</tr>';
            });

            // theRows[j++]=textToInsert.join('');
            theTable.append(textToInsert.join(''));

            theTable.css("visibility","visible");
            activeElement("reqTable");
            sortTableByRow(0);
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    })


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
function getRoles(callback){
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
/*
Dialog for choosing an asset
 */
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
                //dialogwindow.show();
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
            }else {
                alert("All assets are already added");
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });
}
/*
 Dialog for choosing a file
 */
function fileDialogbox(callback){
    var dialogwindow = $("#typeOfFile");
    var select = dialogwindow.find("select");
    dialogwindow.dialog({
        modal: true,
        buttons: {
            Ok: function () {
                var text =  select.find("option:selected" ).text();
                if(jQuery.isFunction(callback)){
                    callback(text);
                    $("#importFile").trigger('click')
                }
                $(this).dialog("close");
            }
        }
    });
    $(".comboboxD").css("visibility", "visible");

}
/*
 Dialog for choosing a new role for the responses
 */
function newRoleDialogbox(callback){
    var dialogwindow = $("#ChooseRoleForResponse");
    var roleSelect = dialogwindow.find("#theNewRole");
    var costSelect = dialogwindow.find("#theRoleCost");
    getRoles(function (roles) {
        $.each(roles, function (key, obj) {
            roleSelect.append($('<option>', { value : key })
                .text(key));
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


/*
 Dialog for choosing an asset in a certain environment
 */
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
                //if not found in assets
                if(!found) {
                    select.append("<option value=" + object + ">" + object + "</option>");
                    none = false;
                }
            });
            if(!none) {
                //dialogwindow.show();
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
            }else {
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
                            if(jQuery.isFunction(callback)){
                                callback(text);
                            }
                            $(this).dialog("close");
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
}
/*
 Dialog for choosing an attacker
 */
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
                //if not found in assets
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
                //dialogwindow.show();
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
            }else {
                alert("All possible attackers are already added");
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });
}
/*
 Dialog for choosing a role
 */
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
                //if not found in assets
                if(!found) {
                            select.append("<option value=" + key + ">" + key + "</option>");
                            none = false;
                }
            });
            if(!none) {
                //dialogwindow.show();
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
            }else {
                alert("All possible attackers are already added");
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });
}

/*
 Dialog for choosing a motive
 */
function motivationDialogBox(hasMotive ,callback){
    var dialogwindow = $("#ChooseMotivationsDialog");
    var select = dialogwindow.find("select");
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))

        },
        crossDomain: true,
        url: serverIP + "/api/attackers/motivations",
        success: function (data) {
            select.empty();
            var none = true;
            $.each(data, function(index, motive) {
                var found = false;
                $.each(hasMotive,function(index, text) {
                    if(text == motive.theName){
                        found = true
                    }
                });
                //if not found in assets
                if(!found) {
                    select.append("<option value=" + motive.theName + ">" + motive.theName + "</option>");
                    none = false;
                }
            });
            if(!none) {
                //dialogwindow.show();
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
            }else {
                alert("All possible attackers are already added");
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });
}


/*
Function for creating the comboboxes
 */
function createComboboxes(){
var sess = String($.session.get('sessionID'));
    //Assetsbox
    if(!window.boxesAreFilled) {
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
                // we make a successful JSONP call!
                var options = $("#assetsbox");
                options.empty();
                options.append("<option>All</option>");
                $.each(data, function () {
                    options.append($("<option />").val(this).text(this));
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
            // async: false,
            accept: "application/json",
            data: {
                session_id: String($.session.get('sessionID'))
            },
            crossDomain: true,
            url: serverIP + "/api/environments/all/names",

            success: function (data) {
                var boxoptions = $("#environmentsbox");
                boxoptions.empty();
                boxoptions.append("<option>All</option>");
                $.each(data, function () {
                    boxoptions.append($("<option />").val(this).text(this));
                });
                boxoptions.css("visibility", "visible");
                window.boxesAreFilled = true;
            },
            error: function (xhr, textStatus, errorThrown) {
                debugLogger(String(this.url));
                debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
            }

        });
    }

   /* }))).map(function () {
        return $('<option>').val(this.value).text(this.label);
    }).appendTo('#assetsbox');*/
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
            // $("#test").append(JSON.stringify(data));
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
/*
This is for saying which element has the main focus
 */
function activeElement(elementid){
    if(elementid != "reqTable"){
        $("#reqTable").hide();
        $("#filtercontent").hide();
    }
    if(elementid != "svgViewer"){
        $("#svgViewer").hide();
    }

    if(elementid == "reqTable"){
       //If it is the table, we need to see which table it is
        setActiveOptions();
    }
    //////ADDED
    setActiveOptions();

    elementid = "#" + elementid;
    $(elementid).show();

}
/*
function for setting the table head
 */
function setTableHeader(){
    thead = "";

    switch (window.activeTable) {
        case "Requirements":
            debugLogger("Is Requirement");
            thead = "<th width='50px'></th><th>Name</th><th>Description</th><th>Priority</th><th>Rationale</th><th>Fit Citerion</th><th>Originator</th><th>Type</th>";
            break;
        case "Goals":
           debugLogger("Is Goal");
            thead = "<th width='50px'></th><th>Name</th><th>Definition</th><th>Category</th><th>Priority</th><th>Fit Citerion</th><th>Issue</th><th>Originator</th>";
            break;
        case "Obstacles":
            debugLogger("Is Obstacle");
            thead = "<th width='50px'></th><th>Name</th><th>Definition</th><th>Category</th><th>Originator</th>";
            break;
        case "EditGoals":
            debugLogger("Is EditGoals");
            thead = "<th width='120px' id='addNewGoal'><i class='fa fa-plus floatCenter'></i></th><th>Name</th><th>Originator</th><th>Status</th>";
            break;
        case "Assets":
            debugLogger("Is Asset");
            thead = "<th width='120px' id='addNewAsset'><i class='fa fa-plus floatCenter'></i></th><th>Name</th><th>Type</th>";
            break;
        case "Roles":
           debugLogger("Is Role");
            thead = "<th width='120px' id='addNewRole'><i class='fa fa-plus floatCenter'></i></th><th>Name</th><th>Shortcode</th><th>Type</th>";
            break;
        case "Environment":
            debugLogger("Is Environment");
            thead = "<th width='120px' id='addNewEnvironment'><i class='fa fa-plus floatCenter'></i></th><th>Name</th><th>Description</th>";
            break;
        case "Vulnerability":
            debugLogger("Is Vulnerability");
            thead = "<th width='120px' id='addNewVulnerability'><i class='fa fa-plus floatCenter'></i></th><th>Name</th><th>Type</th>";
            break;
        case "Threats":
            debugLogger("Is Threat");
            thead = "<th width='120px' id='addNewThreat'><i class='fa fa-plus floatCenter'></i></th><th>Name</th><th>Type</th>";
            break;
        case "Attackers":
            debugLogger("Is Attacker");
            thead = "<th width='120px' id='addNewAttacker'><i class='fa fa-plus floatCenter'></i></th><th>Name</th><th>Description</th>";
            break;
        case "Risks":
            debugLogger("Is Risk");
            thead = "<th width='120px' id='addnewRisk'><i class='fa fa-plus floatCenter'></i></th><th>Name</th>";
            break;
        case "Respones":
            debugLogger("Is Response");
            thead = "<th width='120px' id='addNewResponse'><i class='fa fa-plus floatCenter'></i></th><th>Name</th><th>Type</th>";
            break;
    }
    $("#reqTable").find("thead").empty();
   // $("#reqTable").empty();
    $("#reqTable").find("thead").append(thead);
    $("#reqTable").find("tbody").empty();

}
/*
 This sets the right comboboxes etc in the main window
 */
function setActiveOptions(){
//filtercontent
    //If chosen to create a new function for this, because this will increase readability
    //First disable them all
    $("#filtercontent").hide();
    $("#editAssetsOptions").hide();

    //VERY OLD FUNCTION
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

/*
for filling up the SVG viewer
 */
function fillSvgViewer(data){
    var xmlString = (new XMLSerializer()).serializeToString(data);
    //console.log(String(xmlString));
    var svgDiv = $("#svgViewer");
    svgDiv.show();
    svgDiv.css("height",$("#maincontent").height());
    svgDiv.css("width","100%");
    svgDiv.html(xmlString);
    $("svg").attr("id","svg-id");
    activeElement("svgViewer");
    panZoomInstance = svgPanZoom('#svg-id', {
        zoomEnabled: true,
        controlIconsEnabled: true,
        fit: true,
        center: true,
        minZoom: 0.2
    })
}

/*
finding the lowest label in the table
 */
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
          // console.log(i+1 + " is the number");
            return i+1;
        }
    }
   // console.log(i+1 + " is the number");
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
    })
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
    })
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
    })
}
function getAllgoals(callback) {
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + "/api/goals",
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
    })
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
        } else {
            return (keyA < keyB) ? 1 : 0;
        }
    });
    $.each($rows, function(index, row){
        $table.append(row);
    });
}

/*
for edit assets
 */

function getAssetDefinition(props){
    $('#Properties').find('tbody').empty();
    var i = 0;
    var textToInsert = [];
    $.each(props, function(index, object) {
        //fa-minus
        if(object.value != "None") {

            textToInsert[i++] = '<tr class="clickable-properties" ><td style="display:none;">';
            textToInsert[i++] = object.id;
            textToInsert[i++] = '</td>';

            textToInsert[i++] = '<td>';
            textToInsert[i++] = '<div class="fillparent deleteProperty"><i class="fa fa-minus"></i></div>';
            textToInsert[i++] = '</td>';

            textToInsert[i++] = '<td class="theAssetPropName" name="name">';
            textToInsert[i++] = object.name;
            textToInsert[i++] = '</td>';

            textToInsert[i++] = '<td name="value">';
            textToInsert[i++] = object.value;
            textToInsert[i++] = '</td>';

            textToInsert[i++] = '<td name="rationale">';
            textToInsert[i++] = object.rationale;
            textToInsert[i++] = '</td>';

            textToInsert[i++] = '</tr>';
        }
     });
    $('#Properties').find('tbody').append(textToInsert.join(''));

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
        } else {
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
function fillRolesTable(){
    window.activeTable = "Roles";
    setTableHeader();
    activeElement("reqTable");
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))

        },
        crossDomain: true,
        url: serverIP + "/api/roles",
        success: function (json) {
            $.session.set("allRoles", JSON.stringify(json));
            var i = 0;
            var textToInsert = [];
            $.each(json, function (key, value) {

                textToInsert[i++] = "<tr>";
                textToInsert[i++] = '<td><button class="editRoleButton" value="' + key + '">' + 'Edit' + '</button> <button class="deleteRoleButton" value="' + key + '">' + 'Delete' + '</button></td>';

                textToInsert[i++] = '<td name="theName">';
                textToInsert[i++] = value.theName;
                textToInsert[i++] = '</td>';

                textToInsert[i++] = '<td name="theShortCode">';
                textToInsert[i++] = value.theShortCode;
                textToInsert[i++] = '</td>';

                textToInsert[i++] = '<td name="theType">';
                textToInsert[i++] = value.theType;
                textToInsert[i++] = '</td>';
                textToInsert[i++] = '</tr>';
            });
            $("#reqTable").append(textToInsert.join(''));

        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });
    sortTableByRow(1);
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

    //var data = $("#editAssetsOptionsform");
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
                    // console.log($(this).prop("name") +" " +$(this).val());
                }

                if(String($(this).prop("tagName")).toLowerCase() == "select"){

                    var id = $(this).attr('id');

                    $(this).children().each(function() {
                        var attr = $(this).attr('selected');
                        if (typeof attr !== typeof undefined && attr !== false) {
                            json[id] = $(this).val();
                            // console.log( id + "  " +$(this).val());
                        }
                    });
                }


            });
        }
    });
    return json
}

function putAssetForm(data){
    putAsset(assetFormToJSON(data));
}

function postAssetForm(data,callback){
    //var allAssets = JSON.parse($.session.get("allAssets"));
    var newAsset = assetFormToJSON(data,true);
   var assetName = $(data).find('#theName').val();
    var asobject = {};
    asobject.object = newAsset
    $.session.set("AssetName",assetName);
    //allAssets[assetName] = newAsset;
    postAsset(asobject,callback);
}

function fillupEnvironmentObject(env){
    env.theName = $("#theName").val();
    env.theShortCode = $("#theShortCode").val();
    env.theDescription = $("#theDescription").val();

    env.theTensions = [];
    env.theDuplicateProperty = "";

    var tensions = [];
    $("#tensionsTable").find("td").each(function() {
        var attr = $(this).find("select").attr('rationale');
        if(typeof attr !== typeof undefined && attr !== false) {
            var select = $(this).find("select");
            var tension = jQuery.extend(true, {}, tensionDefault);
            tension.rationale = select.attr("rationale");
            tension.value = parseInt(select.val());
            var ids = select.attr("id");
            values = ids.split('-');
            tension.attr_id = parseInt(values[0]);
            tension.base_attr_id = parseInt(values[1]);
            env.theTensions.push(tension);
        }
    });

    var envInEnv = [];
    $("#envToEnvTable").find("tbody").find("tr .removeEnvinEnv").each(function () {
        envInEnv.push($(this).next("td").text());
    });
    env.theEnvironments = envInEnv;
    var theDupProp = $("input:radio[name ='duplication']:checked").val();
    if(theDupProp == "" || theDupProp == undefined){
        theDupProp = "None";
    }

    var theEnvinEnvArray = [];
    env.theOverridingEnvironment = theDupProp;
    $("#overrideCombobox").find("option").each(function (index, option) {
        //This is for adding env to env, but wait!! first need to remove them when presssed minus!
        theEnvinEnvArray.push($(option).text());
    });
    env.theEnvironments = theEnvinEnvArray;
    return env;
}
function fillEnvironmentsTable(){
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + "/api/environments",
        success: function (data) {
            window.activeTable = "Environment";
            setTableHeader();
            createEnvironmentsTable(data, function(){
                newSorting(1);
            });
            activeElement("reqTable");

        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });
}

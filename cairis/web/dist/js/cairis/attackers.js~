/**
 * Created by Raf on 27/05/2015.
 */
/*
 I've made this file to make it easier for me to program. Everything (except PUT POST and DELETE) for the attackers will be coded here
 It is possible that I will use some already developed functions inside some other files
 */
$("#attackerClick").click(function () {
    createAttackersTable();
});
/*
 A function for filling the table with Threats
 */
function createAttackersTable(){

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
            window.activeTable = "Attackers";
            setTableHeader();
            var theTable = $(".theTable");
            $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
            var textToInsert = [];
            var i = 0;

            $.each(data, function(key, item) {
                textToInsert[i++] = "<tr>";
                textToInsert[i++] = '<td><button class="editAttackerButton" value="' + key + '">' + 'Edit' + '</button> <button class="deleteAttackerButton" value="' + key + '">' + 'Delete' + '</button></td>';

                textToInsert[i++] = '<td name="theName">';
                textToInsert[i++] = key;
                textToInsert[i++] = '</td>';

                textToInsert[i++] = '<td name="theType">';
                textToInsert[i++] = item.theDescription;
                textToInsert[i++] = '</td>';

                textToInsert[i++] = '</tr>';
            });

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
$(document).on('click', ".editAttackerButton", function () {
    var name = $(this).val();
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + "/api/attackers/name/" + name.replace(" ", "%20"),
        success: function (data) {
            // console.log(JSON.stringify(rawData));
            fillOptionMenu("fastTemplates/editAttackerOptions.html", "#optionsContent", null, true, true, function () {
                    forceOpenOptions();
                    $("#addAttackerPropertyDiv").hide();
                    $.session.set("Attacker", JSON.stringify(data));
                    $('#editAttackerOptionsForm').loadJSON(data, null);
                    var tags = data.theTags;
                    var text = "";
                    $.each(tags, function (index, type) {
                        text += type + ", ";
                    });
                    $("#theTags").val(text);
                    $.each(data.theEnvironmentProperties, function (index, env) {
                       appendAttackerEnvironment(env.theEnvironmentName);
                    });
                    $("#theAttackerEnvironments").find(".attackerEnvironment:first").trigger('click');
                    $("#theImages").attr("src",getImagedir(data.theImage));
                    resaleImage($("#theImages"));

                }
            );
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });
});
var optionsContent = $("#optionsContent");
optionsContent.on("click",".attackerEnvironment", function () {
    clearAttackerEnvInfo();
   var attacker = JSON.parse($.session.get("Attacker"));
    var theEnvName = $(this).text();
    $.session.set("attackerEnvironmentName", theEnvName);
    $.each(attacker.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == theEnvName){
            $.each(env.theMotives, function (index, motive) {
                appendAttackerMotive(motive);
            });
            $.each(env.theRoles, function (index, role) {
                appendAttackerRole(role);
            });
            $.each(env.theCapabilities, function (index, cap) {
                appendAttackerCapability(cap);
            });
        }
    });
});
optionsContent.on("click", "#addMotivetoAttacker", function () {
    var hasMot = [];
    var theEnvName =  $.session.get("attackerEnvironmentName");
    $(".attackerMotive").each(function (index, tag) {
        hasMot.push($(tag).text());
    });
    motivationDialogBox(hasMot, function (text) {
        var attacker = JSON.parse($.session.get("Attacker"));

        $.each(attacker.theEnvironmentProperties, function (index, env) {
            if(env.theEnvironmentName == theEnvName){
                env.theMotives.push(text);
            }
        });
        appendAttackerMotive(text);
        $.session.set("Attacker", JSON.stringify(attacker));
    });
});

optionsContent.on('click', "#addCapabilitytoAttacker", function () {
    $("#addAttackerPropertyDiv").addClass("new");
    var hasCaps = [];
    $("#attackerCapability").find(".attackerCapability").each(function(index, asset){
        hasCaps.push($(asset).text());
    });
    capabilityfilling(hasCaps);
    attackerToggle();

});
/*
filling Capability when changing
*/
function capabilityfilling(hasCap, original){

    var select = $(document).find("#theCap");
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))

        },
        crossDomain: true,
        url: serverIP + "/api/attackers/capabilities",
        success: function (data) {
            select.empty();
            var none = true;
            if(typeof original != 'undefined' ){
                select.append("<option value=" + original + ">" + original + "</option>");
                select.val(original);
            }
            $.each(data, function(key, object) {
                var found = false;
                $.each(hasCap,function(index, text) {
                    if(text == object.theName){
                        found = true
                    }
                });
                if(!found) {
                    select.append("<option value=" + object.theName + ">" + object.theName + "</option>");
                    none = false;
                }
            });
            /*if(!none) {
             //dialogwindow.show();

             }else {
             alert("All assets are already added");
             }*/
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }

    });

}
optionsContent.on('click', ".removeAttackerMotive", function () {
    var text = $(this).next(".attackerMotive").text();
    $(this).closest("tr").remove();
    var attacker = JSON.parse($.session.get("Attacker"));
    var theEnvName = $.session.get("attackerEnvironmentName");
    $.each(attacker.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == theEnvName){
            $.each(env.theMotives, function (index2, mot) {
                if(mot == text){
                    env.theMotives.splice( index2 ,1 );
                    $.session.set("Attacker", JSON.stringify(attacker));
                    return false;
                }
            });
        }
    });
});

optionsContent.on('click', ".removeAttackerRole", function () {
    var text = $(this).next(".attackerRole").text();
    $(this).closest("tr").remove();
    var attacker = JSON.parse($.session.get("Attacker"));
    var theEnvName = $.session.get("attackerEnvironmentName");
    $.each(attacker.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == theEnvName){
            $.each(env.theRoles, function (index2, role) {
                if(role == text){
                    env.theRoles.splice( index2 ,1 );
                    $.session.set("Attacker", JSON.stringify(attacker));
                    return false;
                }
            });
        }
    });
});

optionsContent.on('click', ".deleteAttackerEnv", function () {
    var envi = $(this).next(".attackerEnvironment").text();
    $(this).closest("tr").remove();
    var attacker = JSON.parse($.session.get("Attacker"));
    $.each(attacker.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == envi){
            attacker.theEnvironmentProperties.splice( index ,1 );
            $.session.set("Attacker", JSON.stringify(attacker));
            clearAttackerEnvInfo();
           // $("#theAttackerEnvironments").find(".attackerEnvironment:first").trigger('click');

            var UIenv = $("#theAttackerEnvironments").find("tbody");
            if(jQuery(UIenv).has(".attackerEnvironment").length){
                UIenv.find(".attackerEnvironment:first").trigger('click');
            }else{
                $("#Properties").hide("fast");
            }

             return false;
        }
    });
});

optionsContent.on("click", "#addAttackerEnv", function () {
    var hasEnv = [];
    $(".attackerEnvironment").each(function (index, tag) {
        hasEnv.push($(tag).text());
    });
        environmentDialogBox(hasEnv, function (text) {
            appendAttackerEnvironment(text);
            var environment =  jQuery.extend(true, {},attackerEnvDefault );
            environment.theEnvironmentName = text;
            var attacker = JSON.parse($.session.get("Attacker"));
            attacker.theEnvironmentProperties.push(environment);
            $.session.set("Attacker", JSON.stringify(attacker));
            $(document).find(".attackerEnvironment").each(function () {
                if($(this).text() == text){
                    $(this).trigger("click");
                    $("#Properties").show("fast");
                }
            });
        });


});

optionsContent.on('click', '#addRoletoAttacker', function () {
    var hasRole = [];
    $("#attackerRole").find(".attackerRole").each(function(index, role){
        hasRole.push($(role).text());
    });
    roleDialogBox(hasRole, function (text) {

        var attacker = JSON.parse($.session.get("Attacker"));
        var theEnvName = $.session.get("attackerEnvironmentName");
        $.each(attacker.theEnvironmentProperties, function (index, env) {
            if(env.theEnvironmentName == theEnvName){
                env.theRoles.push(text);
                $.session.set("Attacker", JSON.stringify(attacker));
                appendAttackerRole(text);
            }
        });
    });
});
optionsContent.on('click', '#UpdateAttacker', function (e) {
    e.preventDefault();
    var attacker = JSON.parse($.session.get("Attacker"));
    var oldName = attacker.theName;
    attacker.theName = $("#theName").val();
    attacker.theDescription = $("#theDescription").val();
    var tags = $("#theTags").text().split(", ");
    if(tags[0] != ""){
        attacker.theTags = tags;
    }
    //IF NEW Attacker
    if($("#editAttackerOptionsForm").hasClass("new")){
        postAttacker(attacker, function () {
            createAttackersTable();
            $("#editAttackerOptionsForm").removeClass("new")
        });
    } else {
        putAttacker(attacker, oldName, function () {
            createAttackersTable();
        });
    }
});
$(document).on("click", "#addNewAttacker", function () {
    fillOptionMenu("fastTemplates/editAttackerOptions.html", "#optionsContent", null, true, true, function () {
        $("#addAttackerPropertyDiv").hide();
        $("#editAttackerOptionsForm").addClass("new");
        $("#Properties").hide();
        $.session.set("Attacker", JSON.stringify(jQuery.extend(true, {},attackerDefault )));
        forceOpenOptions();
    });
});

optionsContent.on('click', "#UpdateAttackerCapability", function () {
    var attacker = JSON.parse($.session.get("Attacker"));
    var theEnvName = $.session.get("attackerEnvironmentName");
    if($("#addAttackerPropertyDiv").hasClass("new")){
        $.each(attacker.theEnvironmentProperties, function (index, env) {
            if(env.theEnvironmentName == theEnvName){
               var prop = {};
                prop.name = $("#theCap option:selected").text();
                prop.value = $("#thePropValue option:selected").text();
                env.theCapabilities.push(prop);
                $.session.set("Attacker", JSON.stringify(attacker));
                appendAttackerCapability(prop);
                attackerToggle();
            }
        });
    }else{
        var oldCapName = $.session.get("AttackerCapName");
        $.each(attacker.theEnvironmentProperties, function (index, env) {
            if(env.theEnvironmentName == theEnvName){
                $.each(env.theCapabilities, function (index, cap) {
                    if(oldCapName == cap.name){
                        cap.name = $("#theCap option:selected").text();
                        cap.value = $("#thePropValue option:selected").text();
                    }
                });
                $.session.set("Attacker", JSON.stringify(attacker));
                $("#theAttackerEnvironments").find(".attackerEnvironment:first").trigger('click');
                attackerToggle();
            }
        });
    }
});
optionsContent.on("click", ".removeAttackerCapability", function () {
    var text = $(this).closest('tr').find(".attackerCapability").text();
    $(this).closest("tr").remove();
    var attacker = JSON.parse($.session.get("Attacker"));
    var theEnvName = $.session.get("attackerEnvironmentName");
    $.each(attacker.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == theEnvName){
            $.each(env.theCapabilities, function (index2, cap) {
                if(cap.name == text){
                    env.theCapabilities.splice( index2 ,1 );
                    $.session.set("Attacker", JSON.stringify(attacker));
                    return false;
                }
            });

        }
    });

});
optionsContent.on('dblclick', ".changeCapability", function () {
    var hasCaps = [];
    var currentCap = $(this).find(".attackerCapability").text();
    $.session.set("AttackerCapName", currentCap);
    $("#attackerCapability").find(".attackerCapability").each(function(index, asset){
       // if(asset != currentCap) {
            hasCaps.push($(asset).text());
        //}
    });
    capabilityfilling(hasCaps, currentCap);
    attackerToggle();
});
//deleteAttackerButton
$(document).on('click', '.deleteAttackerButton', function (e) {
    e.preventDefault();
    deleteAttacker($(this).val(), function () {
        createAttackersTable();
    });
});
/*
Image uploading functions
 */
var uploading = false;
$("#optionsContent").on('click', '#theImages', function () {
    //$("#addAttackerPropertyDiv").addClass("new");
    if(!uploading) {
        $('#fileupload').trigger("click");
    }
    else if($("#addAttackerPropertyDiv").hasClass("new")){
        alert("First, update the attacker.");
    }
});

$("#optionsContent").on('change','#fileupload', function () {
    uploading = true;
    var test = $(document).find('#fileupload');
    var fd = new FormData();
    fd.append("file", test[0].files[0]);
    var bar = $(".progress-bar");
    var outerbar = $(".progress");
    bar.css("width", 0);
    outerbar.show("slide", { direction: "up" }, 750);

    $.ajax({
        type: "POST",
        accept: "application/json",
        processData:false,
        contentType:false,
        data: fd,
        crossDomain: true,
        url: serverIP + "/api/upload/image?session_id="+  String($.session.get('sessionID')),
        success: function (data) {
            outerbar.hide("slide", { direction: "down" }, 750);
            uploading = false;
            data = JSON.parse(data);

            postImage(data.filename, getImagedir(data.filename));


        },
        error: function (xhr, textStatus, errorThrown) {
            uploading = false;
            outerbar.hide("slide", { direction: "down" }, 750);
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        },
        xhr: function() {
            var xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function(evt) {
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    percentComplete = (percentComplete) * outerbar.width();
                    bar.css("width", percentComplete)
                }
            }, false);
            return xhr;
        }
    });

});
function postImage(imagedir, actualDir) {
    var attacker = JSON.parse($.session.get("Attacker"));

    attacker.theImage = imagedir;
    $("#theImages").attr("src", actualDir);
    putAttacker(attacker, attacker.theName, false, function () {
        $("#theImages").attr("src", actualDir);
        resaleImage($("#theImages"),200);
    });

    $.session.set("Attacker", JSON.stringify(attacker));
    //appendAttackerCapability(prop);

}

function attackerToggle(){
    $("#addAttackerPropertyDiv").toggle();
    $("#editAttackerOptionsForm").toggle();
}
function appendAttackerEnvironment(environment){
    $("#theAttackerEnvironments").find("tbody").append('<tr><td class="deleteAttackerEnv"><i class="fa fa-minus"></i></td><td class="attackerEnvironment">'+environment+'</td></tr>');
}
function appendAttackerRole(role){
    $("#attackerRole").find("tbody").append("<tr><td class='removeAttackerRole'><i class='fa fa-minus'></i></td><td class='attackerRole'>" + role + "</td></tr>").animate('slow');
}
function appendAttackerMotive(motive){
    $("#attackerMotive").find("tbody").append("<tr><td class='removeAttackerMotive' ><i class='fa fa-minus'></i></td><td class='attackerMotive'>" + motive + "</td></tr>").animate('slow');
}
function appendAttackerCapability(prop){
    $("#attackerCapability").find("tbody").append("<tr class='changeCapability'><td class='removeAttackerCapability'><i class='fa fa-minus'></i></td><td class='attackerCapability'>" + prop.name + "</td><td>"+ prop.value +"</td></tr>").animate('slow');
}
function clearAttackerEnvInfo(){
    $("#attackerCapability").find("tbody").empty();
    $("#attackerMotive").find("tbody").empty();
    $("#attackerRole").find("tbody").empty();
}
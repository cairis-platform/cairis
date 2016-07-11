/**
 * Created by Raf on 8/06/2015.
 */
$("#responsesTable").click(function () {
    createResponsesTable();
});
$(document).on('click', ".editResponseButton", function () {
    var name = $(this).val();
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
            // console.log(JSON.stringify(rawData));
            fillOptionMenu("fastTemplates/editResponseOptions.html", "#optionsContent", null, true, true, function () {

                    var tags = data.theTags;

                    $("#theResponseName").val(data.theName);
                    $.session.set("response", JSON.stringify(data));
                    var text = "";
                    $.each(tags, function (index, type) {
                        text += type + ", ";
                    });
                    $("#theTags").val(text);
                    $.session.set("responseKind",data.theResponseType);
                    $.each(data.theEnvironmentProperties[data.theResponseType.toLocaleLowerCase()], function (index, env) {
                        appendResponseEnvironment(env.theEnvironmentName);
                    });
                    var select = $("#chooseRisk");
                    select.empty();
                    getRisks(function (risks) {
                        $.each(risks, function (key, obj) {
                            select.append($('<option>', { value : key })
                                .text(key));
                        });
                        select.val(data.theRisk);
                    });

                    switch (data.theResponseType){
                        case "Transfer":
                            toggleResponse("#transferWindow");
                            break;
                        case "Mitigate":
                          //  $.session.set("responseKind", "prevent");
                            toggleResponse("#mitigateWindow");
                            break;
                        case "Accept":
                            toggleResponse("#acceptWindow");
                            break;
                        default :
                            alert("You have an old, unsupported project");
                            break;
                    }
                    $("#theRespEnvironments").find(".responseEnvironment:first").trigger('click');
                    forceOpenOptions();
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
optionsContent.on('click', ".deleteTransferRole", function () {
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
optionsContent.on('click', "#addRespEnv", function () {
    var hasEnv = [];
    $(".responseEnvironment").each(function (index, tag) {
        hasEnv.push($(tag).text());
    });
    environmentDialogBox(hasEnv, function (text) {
        appendAttackerEnvironment(text);
        var environment =  jQuery.extend(true, {},respEnvDefault );
        environment.theEnvironmentName = text;
        var resp = JSON.parse($.session.get("response"));
        var type =  $.session.get("responseKind");
        appendResponseEnvironment(text);
        resp.theEnvironmentProperties[type.toLowerCase()].push(environment);
        $("#Properties").show("fast");
        $.session.set("response", JSON.stringify(resp));
    });
});
//TODO: ADD NEW RESPONSE

optionsContent.on('click', ".deleteRespEnv", function () {
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
                }else{
                    $("#Properties").hide("fast");
                }
                return false;
            }
        });
    });

});


optionsContent.on('click', ".responseEnvironment", function () {
   var type =  $.session.get("responseKind");
    var resp = JSON.parse($.session.get("response"));
    var environmentName = $(this).text();
    $.session.set("responseEnvironment", environmentName);
    switch (type){
        case "Transfer":
            $.each(resp.theEnvironmentProperties["transfer"], function (index, env) {
                if(env.theEnvironmentName == environmentName) {
                    $("#theRespTransferRationale").val(resp.theRationale);
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
optionsContent.on('change', "#theCost", function () {
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

optionsContent.on('change', "#acceptRationale", function () {
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

optionsContent.on('change', "#respMitigateType", function () {
    var newType = $(this).val().toLowerCase();
    var resp = JSON.parse($.session.get("response"));
    var type =  $.session.get("responseKind");
    var envName = $.session.get("responseEnvironment");
    //resp.theEnvironmentProperties["transfer"]
    if(newType == "detect"){
        $("#theDetectionPoint").prop('disabled',false);
    }else{
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
optionsContent.on('change', "#theDetectionPoint", function () {
    var value = $(this).val();
    var resp = JSON.parse($.session.get("response"));
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
optionsContent.on('change', "#theRespTransferRationale", function () {
    var resp = JSON.parse($.session.get("response"));
    var type =  $.session.get("responseKind");
    var envName = $.session.get("responseEnvironment");
    $.each(resp.theEnvironmentProperties[type.toLowerCase()], function (index, env) {
       if(env.theEnvironmentName == envName){
          env.theRationale = $(this).val();
       }
    });
    $.session.set("response", JSON.stringify(resp));
});
optionsContent.on('click', "#addRespTransferRole", function () {
    var resp = JSON.parse($.session.get("response"));
    var envName = $.session.get("responseEnvironment");
    newRoleDialogbox(function (role) {
       appendResponseTransferRole(role);
        $.each(resp.theEnvironmentProperties["transfer"], function (index, env) {
           if(env.theEnvironmentName == envName){
               env.theRoles.push(role);
           }
        })

    });
    $.session.set("response", JSON.stringify(resp));
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
            window.activeTable = "Respones";
            setTableHeader();
            var theTable = $(".theTable");
            $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
            var textToInsert = [];
            var i = 0;

            $.each(data, function(key, item) {
                textToInsert[i++] = "<tr>";
                textToInsert[i++] = '<td><button class="editResponseButton" value="' + key + '">' + 'Edit' + '</button> <button class="deleteResponseButton" value="' + key + '">' + 'Delete' + '</button></td>';

                textToInsert[i++] = '<td name="theName">';
                textToInsert[i++] = key;
                textToInsert[i++] = '</td>';

                textToInsert[i++] = '<td name="theType">';
                textToInsert[i++] = item.theResponseType;
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
    });
}
function appendResponseEnvironment(environment){
    $("#theRespEnvironments").find("tbody").append('<tr><td class="deleteRespEnv"><i class="fa fa-minus"></i></td><td class="responseEnvironment">'+environment+'</td></tr>');
}
function appendResponseTransferRole(role){
    $("#transferRolesTable").find("tbody").append('<tr><td class="deleteTransferRole"><i class="fa fa-minus"></i></td><td class="roleName">'+role.roleName+'</td><td>'+ role.cost +'</td></tr>');
}

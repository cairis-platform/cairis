/**
 * Created by Raf on 29/05/2015.
 */
$("#EditGoals").click(function(){
    createEditGoalsTable()
});

$(document).on('click', "button.editGoalsButton",function() {
    var name = $(this).attr("value");
    getGoalOptions(name);
});

/*
 on environment in Goals edit
 */
var optionsContent = $("#optionsContent");
optionsContent.on('click', ".goalEnvProperties", function () {
    var goal = JSON.parse($.session.get("Goal"));

    var name = $(this).text();
    $.session.set("GoalEnvName", name);

    emptyGoalEnvTables();

    $.each(goal.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == name){
            $('#goalsProperties').loadJSON(env,null);
            $("#theIssue").val(env.theIssue);
            $("#theDefinition").val(env.theDefinition);
            $("#theFitCriterion").val(env.theFitCriterion);
            //theDef fitcrit issue

            $.each(env.theGoalRefinements, function (index, goal) {
                appendGoalEnvGoals(goal);
            });
            $.each(env.theSubGoalRefinements, function (index, subgoal) {
                appendGoalSubGoal(subgoal);
            });
            $.each(env.theConcerns, function (index, concern) {
                appendGoalConcern(concern);
            });
            $.each(env.theConcernAssociations, function (index, assoc) {
                appendGoalConcernAssoc(assoc);
            });
        }

    });
});

optionsContent.on('click', '.deleteGoalEnvConcernAssoc', function () {
    var goal = JSON.parse($.session.get("Goal"));
    var envName = $.session.get("GoalEnvName");
    var theAssoc =  $(this).closest("tr").find(".assocName").text();
    $(this).closest("tr").remove();
    $.each(goal.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == envName){
            $.each(env.theConcernAssociations, function (ix, assoc) {
                if(assoc[0] == theAssoc){
                    env.theConcernAssociations.splice(ix,1)
                }
            });
        }
    });
    $.session.set("Goal", JSON.stringify(goal));
});
optionsContent.on('click', '#updateGoalConcernAss', function () {
    var goal = JSON.parse($.session.get("Goal"));
    var envName = $.session.get("GoalEnvName");
    var arr = [];
    arr[0] = $("#theSourceSelect").val();
    arr[1] = $("#theNSelect").val();
    arr[2] = $("#theLink").val();
    arr[3] = $("#theTargetSelect").val();
    arr[4] = $("#theN2Select").val();

if($("#editgoalConcernAssociations").hasClass("new")){
    $.each(goal.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == envName){
            env.theConcernAssociations.push(arr);
        }
    });
}else{
    var oldname = $.session.get("goalAssocName");
    $.each(goal.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == envName){
            $.each(env.theConcernAssociations, function (index, concern) {
                if(concern[0] == oldname){
                    concern[0] = $("#theSourceSelect").val();
                    concern[1] = $("#theNSelect").val();
                    concern[2] = $("#theLink").val();
                    concern[3] = $("#theTargetSelect").val();
                    concern[4] = $("#theN2Select").val();
                }
            });
        }
    });
}
    toggleGoalwindow("#editGoalOptionsForm");
    fillGoalOptionMenu(goal);
    $.session.set("Goal", JSON.stringify(goal));
});

optionsContent.on('click',".deleteGoalSubGoal", function () {
    var goal = JSON.parse($.session.get("Goal"));
    var envName = $.session.get("GoalEnvName");
    var subGoalName =  $(this).closest("tr").find(".subGoalName").text();
    $(this).closest("tr").remove();
    $.each(goal.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == envName){
            $.each(env.theSubGoalRefinements, function (ix, subgoal) {
                if(subgoal[0] == subGoalName){
                    env.theSubGoalRefinements.splice(ix,1)
                }
            });
        }
    });
    $.session.set("Goal", JSON.stringify(goal));
});
optionsContent.on('click',"#addConcerntoGoal", function () {
    hasAsset = [];
    $("#editgoalsConcernTable").find('tbody').find('.GoalConcernName').each(function (index, td) {
       hasAsset.push($(td).text());
    });
    var envName = $.session.get("GoalEnvName");
    assetsInEnvDialogBox(envName, hasAsset, function (text) {
        var goal = JSON.parse($.session.get("Goal"));

        $.each(goal.theEnvironmentProperties, function (index, env) {
            if(env.theEnvironmentName == envName){
                env.theConcerns.push(text);
            }
        });
        appendGoalConcern(text);
        $.session.set("Goal", JSON.stringify(goal));
    });
});
optionsContent.on('click',".deleteGoalGoal", function () {
    var goal = JSON.parse($.session.get("Goal"));
    var envName = $.session.get("GoalEnvName");
    var subGoalName =  $(this).closest("tr").find(".envGoalName").text();
    $(this).closest("tr").remove();
    $.each(goal.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == envName){
            $.each(env.theGoalRefinements, function (ix, thegoal) {
                if(typeof thegoal != "undefined"){
                    if(thegoal[0] == subGoalName){
                        env.theGoalRefinements.splice(ix,1)
                    }
                }
            });
        }
    });
    $.session.set("Goal", JSON.stringify(goal));
});
//deleteGoalEnvConcern
optionsContent.on('click',".deleteGoalEnvConcern", function () {
    var goal = JSON.parse($.session.get("Goal"));
    var envName = $.session.get("GoalEnvName");
    var name =  $(this).closest("tr").find(".GoalConcernName").text();
    $(this).closest("tr").remove();
    $.each(goal.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == envName){
            $.each(env.theConcerns, function (ix, thecon) {
                if(typeof thecon != "undefined"){
                    if(thecon == name){
                        env.theConcerns.splice(ix,1)
                    }
                }
            });
        }
    });
    $.session.set("Goal", JSON.stringify(goal));
});

optionsContent.on('click', '#addConcernAssociationstoGoal', function () {
    toggleGoalwindow("#editgoalConcernAssociations");
    $("#editgoalConcernAssociations").addClass("new");
    var envName = $.session.get("GoalEnvName");
    $("#theSourceSelect").empty();
    $("#theTargetSelect").empty();
    getAllAssetsInEnv(envName, function (data) {
        $.each(data, function (index, asset) {
            $("#theSourceSelect").append($("<option></option>")
                .attr("value",asset)
                .text(asset));
            $("#theTargetSelect").append($("<option></option>")
                .attr("value",asset)
                .text(asset));
        })
    });
});
optionsContent.on('click', '#addSubGoaltoGoal', function () {
    $("#editgoalSubGoal").addClass("new");
    toggleGoalwindow("#editgoalSubGoal");
    fillGoalEditSubGoal();
});
optionsContent.on('click', '#addGoaltoGoal', function () {
    $("#editGoalGoal").addClass("new");
    toggleGoalwindow("#editGoalGoal");
    fillGoalEditGoal();
});
optionsContent.on("click", "#addGoalEnvironment", function () {
    var hasEnv = [];
    $(".goalEnvProperties").each(function (index, tag) {
        hasEnv.push($(tag).text());
    });
    environmentDialogBox(hasEnv, function (text) {
        appendGoalEnvironment(text);
        var environment =  jQuery.extend(true, {},goalEnvDefault );
        environment.theEnvironmentName = text;
        var goal = JSON.parse($.session.get("Goal"));
        goal.theEnvironmentProperties.push(environment);
        $("#goalsProperties").show("fast");
        $.session.set("Goal", JSON.stringify(goal));
    });
});
optionsContent.on('click', ".deleteGoalEnv", function () {
    var envi = $(this).next(".goalEnvProperties").text();
    $(this).closest("tr").remove();
    var goal = JSON.parse($.session.get("Goal"));
    $.each(goal.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == envi){
            goal.theEnvironmentProperties.splice( index ,1 );
            $.session.set("Attacker", JSON.stringify(goal));
            var UIenv =  $("#theGoalEnvironments").find("tbody");
            if(jQuery(UIenv).has(".goalEnvProperties").length){
                UIenv.find(".goalEnvProperties:first").trigger('click');
            }else{
                $("#goalsProperties").hide("fast");
            }

            return false;
        }
    });
});

optionsContent.on('click', '#updateGoalSubGoal', function () {

    var goal = JSON.parse($.session.get("Goal"));
    var envName = $.session.get("GoalEnvName");
       if($("#editgoalSubGoal").hasClass("new")){
           $("#editgoalSubGoal").removeClass("new");
           $.each(goal.theEnvironmentProperties, function (index, env) {
               if(env.theEnvironmentName == envName){
                   var array = [];
                   array[1] = $("#theSubgoalType").val();
                   array[0] = $("#theSubGoalName").val();
                   array[2] = $("#theRefinementSelect").val();
                   array[3] = $("#theAlternate").val();
                   array[4] = $("#theGoalSubGoalRationale").val();
                   env.theSubGoalRefinements.push(array);
               }
           });
       } else{
           var oldName = $.session.get("oldsubGoalName");
           $.each(goal.theEnvironmentProperties, function (index, env) {
               if(env.theEnvironmentName == envName){
                   $.each(env.theSubGoalRefinements, function (index, arr) {
                       if(arr[0] == oldName){
                           arr[1] = $("#theSubgoalType").val();
                           arr[0] = $("#theSubGoalName").val();
                           arr[2] = $("#theRefinementSelect").val();
                           arr[3] = $("#theAlternate").val();
                           arr[4] = $("#theGoalSubGoalRationale").val();
                       }
                   });
               }
           });
       }
    $.session.set("Goal", JSON.stringify(goal));
    fillGoalOptionMenu(goal);
    toggleGoalwindow("#editGoalOptionsForm");
});
optionsContent.on('change', ".goalAutoUpdater" ,function() {
    var goal = JSON.parse($.session.get("Goal"));
    var envName = $.session.get("GoalEnvName");
    var name = $(this).attr("name");
    var element = $(this);

        $.each(goal.theEnvironmentProperties, function (index, env) {
            if(env.theEnvironmentName == envName){
                //This is made for future development.
                if($(element).is("input")){
                    env[name] = $(element).val();
                }
                else if($(element).is("textarea")){
                    env[name] = $(element).val();
                }
                else {
                    env[name] = $(element).find(":selected").text();
                }
                $.session.set("Goal", JSON.stringify(goal));
            }
        });



});
$(document).on('click', '#addNewGoal', function () {
    fillGoalOptionMenu(null, function () {
        $("#editGoalOptionsForm").addClass('new');
        forceOpenOptions();
        $("#goalsProperties").hide();
    });

});


optionsContent.on('click', "#updateGoalButton", function (e) {
    e.preventDefault();
    var goal = JSON.parse($.session.get("Goal"));
    var oldName = goal.theName;
    goal.theName = $("#theName").val();
    goal.theOriginator = $("#theOriginator").val();
    var tags = $("#theTags").text().split(", ");
    if(tags[0] != ""){
        goal.theTags = tags;
    }
    //IF NEW Attacker
    if($("#editGoalOptionsForm").hasClass("new")){
        postGoal(goal, function () {

            createEditGoalsTable();
            $("#editAttackerOptionsForm").removeClass("new")
        });
    } else {
        putGoal(goal, oldName, function () {
            createEditGoalsTable();
        });
    }
});
optionsContent.on('dblclick', '.editGoalSubGoalRow', function () {
    toggleGoalwindow("#editgoalSubGoal");
    var name = $(this).find("td").eq(1).text();
    fillGoalEditSubGoal(name);
        var type = $(this).find("td").eq(2).text();
        var refinement = $(this).find("td").eq(3).text();
        var target = $(this).find("td").eq(4).text();
        var rationale = $(this).find("td").eq(5).text();
        $.session.set("oldsubGoalName", name);

        $("#theSubgoalType").val(type);
        $("#theRefinementSelect").val(refinement);
        $("#theAlternate").val(target);
        $("#theGoalSubGoalRationale").val(rationale);

});
optionsContent.on('dblclick', '.editGoalGoalRow', function () {
    toggleGoalwindow("#editGoalGoal");
    var name = $(this).find("td").eq(1).text();
    fillGoalEditGoal(name);

    var type = $(this).find("td").eq(2).text();
    var refinement = $(this).find("td").eq(3).text();
    var target = $(this).find("td").eq(4).text();
    var rationale = $(this).find("td").eq(5).text();
    $.session.set("oldGoalName", name);

    $("#theGoalType").val(type);
    $("#theGoalRefinementSelect").val(refinement);
    $("#theGoalAlternate").val(target);
    $("#theGoalGoalRationale").val(rationale);

});
//editGoalConcernAssoc
optionsContent.on('dblclick', '.editGoalConcernAssoc', function () {
    var envName = $.session.get("GoalEnvName");
    var tr = $(this);
    getAllAssetsInEnv(envName, function (data) {
        $.each(data, function (index, asset) {
            $("#theSourceSelect").append($("<option></option>")
                .attr("value",asset)
                .text(asset));
            $("#theTargetSelect").append($("<option></option>")
                .attr("value",asset)
                .text(asset));
        });
        var name = $(tr).find(".assocName").text();
        $.session.set("goalAssocName",name);
        var n1 = $(tr).find(".assocN1").text();
        var link = $(tr).find(".assocLink").text();
        var n2 = $(tr).find(".assocN2").text();
        var target = $(tr).find(".assocTarget").text();

        $("#theSourceSelect").val(name);
        $("#theNSelect").val(n1);
        $("#theLink").val(link);
        $("#theTargetSelect").val(target);
        $("#theN2Select").val(n2);
        toggleGoalwindow("#editgoalConcernAssociations");
    });

});
optionsContent.on('click', '.goalCancelButton', function () {
   toggleGoalwindow("#editGoalOptionsForm")
});
optionsContent.on('click',"#updateGoalGoal", function () {
    var goal = JSON.parse($.session.get("Goal"));
    var envName = $.session.get("GoalEnvName");
    if($("#editGoalGoal").hasClass("new")) {
        $("#editGoalGoal").removeClass("new");
        $.each(goal.theEnvironmentProperties, function (index, env) {
            if(env.theEnvironmentName == envName){
                var array = [];
                array[1] = $("#theGoalType").val();
                array[0] = $("#theGoalName").val();
                array[2] = $("#theGoalRefinementSelect").val();
                array[3] = $("#theGoalAlternate").val();
                array[4] = $("#theGoalGoalRationale").val();
                env.theGoalRefinements.push(array);
            }
        });
    }else{
        $.each(goal.theEnvironmentProperties, function (index, env) {
            if(env.theEnvironmentName == envName){
                var oldname = $.session.get("oldGoalName");
                $.each(env.theGoalRefinements, function (index, ref) {
                    if(ref[0] == oldname){
                        ref[1] = $("#theGoalType").val();
                        ref[0] = $("#theGoalName").val();
                        ref[2] = $("#theGoalRefinementSelect").val();
                        ref[3] = $("#theGoalAlternate").val();
                        ref[4] = $("#theGoalGoalRationale").val();
                    }
                });
            }
        });
    }
    $.session.set("Goal", JSON.stringify(goal));
    fillGoalOptionMenu(goal);
    toggleGoalwindow("#editGoalOptionsForm");
});
function getGoalOptions(name){
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + "/api/goals/name/" + name.replace(" ", "%20"),
        success: function (data) {
            fillGoalOptionMenu(data);
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });
}

function fillGoalOptionMenu(data,callback){
    fillOptionMenu("fastTemplates/editGoalsOptions.html","#optionsContent",null,true,true, function(){
            if(data != null) {
                $.session.set("Goal", JSON.stringify(data));
                $('#editGoalOptionsForm').loadJSON(data, null);

                $.each(data.theTags, function (index, tag) {
                    $("#theTags").append(tag + ", ");
                });
                $.each(data.theEnvironmentProperties, function (index, prop) {
                    appendGoalEnvironment(prop.theEnvironmentName);
                });
                forceOpenOptions();
                $("#theGoalEnvironments").find(".goalEnvProperties:first").trigger('click');

            }
            else{
                var goal =  jQuery.extend(true, {},goalDefault );
                $.session.set("Goal", JSON.stringify(goal));
            }
            if (jQuery.isFunction(callback)) {
                callback();
            }
        }

    );
}
function fillGoalEditSubGoal(theSettableValue){
    $("#theSubGoalName").empty();
    var subname = $("#theSubGoalName");
   getAllgoals(function (data) {
        $.each(data, function (key, goal) {
            subname.append($("<option></option>")
                .attr("value", key)
                .text(key));
        });
    });
    getAllRequirements(function (data) {
        $.each(data, function (key, req) {
            subname.append($("<option></option>")
                .attr("value", req.theLabel)
                .text(req.theLabel));
        });
        if (typeof theSettableValue  !== "undefined"){
            subname.val(theSettableValue);
        }

    });

}
function fillGoalEditGoal(theSettableValue){
    var thegoalName = $("#theGoalName");
    thegoalName.empty();
    getAllgoals(function (data) {
        $.each(data, function (key, goal) {
            thegoalName.append($("<option></option>")
                .attr("value", key)
                .text(key));
        });
    });
    getAllRequirements(function (data) {
        $.each(data, function (key, req) {
            thegoalName.append($("<option></option>")
                .attr("value", req.theLabel)
                .text(req.theLabel));
        });
        if (typeof theSettableValue  !== "undefined"){
            thegoalName.val(theSettableValue);
        }
    });
}
function toggleGoalwindow(window){
    $("#editgoalConcernAssociations").hide();
    $("#editGoalOptionsForm").hide();
    $("#editgoalSubGoal").hide();
    $("#editGoalGoal").hide();
    $(window).show();
}

function emptyGoalEnvTables(){
    $("#editgoalsGoalsTable").find("tbody").empty();
    $("#editgoalsSubgoalsTable").find("tbody").empty();
    $("#editgoalsConcernTable").find("tbody").empty();
    $("#editgoalsConcernassociationsTable").find("tbody").empty();
}

function appendGoalEnvironment(text){
    $("#theGoalEnvironments").append("<tr><td class='deleteGoalEnv'><i class='fa fa-minus'></i></td><td class='goalEnvProperties'>"+ text +"</td></tr>");
}
function appendGoalEnvGoals(goal){
    //<td class="deleteAttackerEnv"><i class="fa fa-minus"></i></td>
    $("#editgoalsGoalsTable").append('<tr class="editGoalGoalRow"><td class="deleteGoalGoal"><i class="fa fa-minus"></i></td><td class="envGoalName">'+goal[0]+'</td><td>'+goal[1]+'</td><td>'+goal[2]+'</td><td>'+goal[3]+'</td><td>'+goal[4]+'</td></tr>');
}
function appendGoalSubGoal(subgoal){
    //<td class="deleteAttackerEnv"><i class="fa fa-minus"></i></td>
    $("#editgoalsSubgoalsTable").append('<tr class="editGoalSubGoalRow"><td class="deleteGoalSubGoal"><i class="fa fa-minus"></i></td><td class="subGoalName">'+subgoal[0]+'</td><td>'+subgoal[1]+'</td><td>'+subgoal[2]+'</td><td>'+subgoal[3]+'</td><td>'+subgoal[4]+'</td></tr>');
}
function appendGoalConcern(concern){
    $("#editgoalsConcernTable").append('<tr><td class="deleteGoalEnvConcern" value="'+ concern+'"><i class="fa fa-minus"></i></td><td class="GoalConcernName">'+concern+'</td></tr>');
}
function appendGoalConcernAssoc(assoc){
    $("#editgoalsConcernassociationsTable").append('<tr class="editGoalConcernAssoc"><td class="deleteGoalEnvConcernAssoc"><i class="fa fa-minus"></i></td><td class="assocName">'+assoc[0]+'</td><td class="assocN1">'+assoc[1]+'</td><td class="assocLink">'+assoc[2]+'</td><td class="assocN2">'+assoc[4]+'</td><td class="assocTarget">'+assoc[3]+'</td></tr>');
}
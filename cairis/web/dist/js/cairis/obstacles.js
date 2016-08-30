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

    Authors: Shamal Faily */

$("#EditObstacles").click(function(){
    createEditObstaclesTable();
});

$(document).on('click', "button.editObstaclesButton",function() {
    var name = $(this).attr("value");
    getObstacleOptions(name);
});

/*
 on environment in Goals edit
 */
var optionsContent = $("#optionsContent");
optionsContent.on('click', ".obstacleEnvProperties", function () {
    var obstacle = JSON.parse($.session.get("Obstacle"));

    var name = $(this).text();
    $.session.set("ObstacleEnvName", name);

    emptyGoalEnvTables();

    $.each(obstacle.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == name){
            $('#obstacleProperties').loadJSON(env,null);
            $("#theDefinition").val(env.theDefinition);

            $.each(env.theGoalRefinements, function (index, obstacle) {
                appendGoalEnvGoals(obstacle);
            });
            $.each(env.theSubGoalRefinements, function (index, subobstacle) {
                appendGoalSubGoal(subobstacle);
            });
            $.each(env.theConcerns, function (index, concern) {
                appendObstacleConcern(concern);
            });
        }

    });
});

optionsContent.on('click',".deleteGoalSubGoal", function () {
    var obstacle = JSON.parse($.session.get("Obstacle"));
    var envName = $.session.get("ObstacleEnvName");
    var subGoalName =  $(this).closest("tr").find(".subGoalName").text();
    $(this).closest("tr").remove();
    $.each(obstacle.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == envName){
            $.each(env.theSubGoalRefinements, function (ix, subobstacle) {
                if(subobstacle[0] == subGoalName){
                    env.theSubGoalRefinements.splice(ix,1)
                }
            });
        }
    });
    $.session.set("Obstacle", JSON.stringify(obstacle));
});

optionsContent.on('click',"#addConcerntoObstacle", function () {
    hasAsset = [];
    $("#editObstaclesConcernTable").find('tbody').find('.ObstacleConcernName').each(function (index, td) {
       hasAsset.push($(td).text());
    });
    var envName = $.session.get("ObstacleEnvName");
    assetsInEnvDialogBox(envName, hasAsset, function (text) {
        var obstacle = JSON.parse($.session.get("Obstacle"));

        $.each(obstacle.theEnvironmentProperties, function (index, env) {
            if(env.theEnvironmentName == envName){
                env.theConcerns.push(text);
            }
        });
        appendObstacleConcern(text);
        $.session.set("Obstacle", JSON.stringify(obstacle));
    });
});
optionsContent.on('click',".deleteGoalGoal", function () {
    var obstacle = JSON.parse($.session.get("Obstacle"));
    var envName = $.session.get("ObstacleEnvName");
    var subGoalName =  $(this).closest("tr").find(".envGoalName").text();
    $(this).closest("tr").remove();
    $.each(obstacle.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == envName){
            $.each(env.theGoalRefinements, function (ix, theobstacle) {
                if(typeof theobstacle != "undefined"){
                    if(theobstacle[0] == subGoalName){
                        env.theGoalRefinements.splice(ix,1)
                    }
                }
            });
        }
    });
    $.session.set("Obstacle", JSON.stringify(obstacle));
});

optionsContent.on('click',".deleteObstacleEnvConcern", function () {
    var obstacle = JSON.parse($.session.get("Obstacle"));
    var envName = $.session.get("ObstacleEnvName");
    var name =  $(this).closest("tr").find(".ObstacleConcernName").text();
    $(this).closest("tr").remove();
    $.each(obstacle.theEnvironmentProperties, function (index, env) {
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
    $.session.set("Obstacle", JSON.stringify(obstacle));
});


optionsContent.on('click', '#addSubGoaltoGoal', function () {
    $("#editGoalSubGoal").addClass("new");
    toggleGoalwindow("#editGoalSubGoal");
    fillGoalEditSubGoal();
});
optionsContent.on('click', '#addGoaltoGoal', function () {
    $("#editGoalGoal").addClass("new");
    toggleGoalwindow("#editGoalGoal");
    fillGoalEditGoal();
});
optionsContent.on("click", "#addObstacleEnvironment", function () {
    var hasEnv = [];
    $(".obstacleEnvProperties").each(function (index, tag) {
        hasEnv.push($(tag).text());
    });
    environmentDialogBox(hasEnv, function (text) {
        appendObstacleEnvironment(text);
        var environment =  jQuery.extend(true, {},obstacle.nvDefault );
        environment.theEnvironmentName = text;
        var obstacle = JSON.parse($.session.get("Obstacle"));
        obstacle.theEnvironmentProperties.push(environment);
        $("#obstacleProperties").show("fast");
        $.session.set("Obstacle", JSON.stringify(obstacle));
    });
});
optionsContent.on('click', ".deleteObstacleEnv", function () {
    var envi = $(this).next(".obstacleEnvProperties").text();
    $(this).closest("tr").remove();
    var obstacle = JSON.parse($.session.get("Obstacle"));
    $.each(obstacle.theEnvironmentProperties, function (index, env) {
        if(env.theEnvironmentName == envi){
            obstacle.theEnvironmentProperties.splice( index ,1 );
            $.session.set("Obstacle", JSON.stringify(obstacle));
            var UIenv =  $("#theObstacleEnvironments").find("tbody");
            if(jQuery(UIenv).has(".obstacleEnvProperties").length){
                UIenv.find(".obstacleEnvProperties:first").trigger('click');
            }else{
                $("#obstacleProperties").hide("fast");
            }

            return false;
        }
    });
});

optionsContent.on('click', '#updateGoalSubGoal', function () {

    var obstacle = JSON.parse($.session.get("Obstacle"));
    var envName = $.session.get("ObstacleEnvName");
       if($("#editGoalSubGoal").hasClass("new")){
           $("#editGoalSubGoal").removeClass("new");
           $.each(obstacle.theEnvironmentProperties, function (index, env) {
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
           $.each(obstacle.theEnvironmentProperties, function (index, env) {
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
    $.session.set("Obstacle", JSON.stringify(obstacle));
    fillObstacleOptionMenu(obstacle);
    toggleGoalwindow("#editObstacleOptionsForm");
});
optionsContent.on('change', ".obstacle.utoUpdater" ,function() {
    var obstacle = JSON.parse($.session.get("Obstacle"));
    var envName = $.session.get("ObstacleEnvName");
    var name = $(this).attr("name");
    var element = $(this);

        $.each(obstacle.theEnvironmentProperties, function (index, env) {
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
                $.session.set("Obstacle", JSON.stringify(obstacle));
            }
        });



});
$(document).on('click', '#addNewObstacle', function () {
    fillObstacleOptionMenu(null, function () {
        $("#editObstacleOptionsForm").addClass('new');
        $("#optionsHeaderGear").text("Obstacle properties");
        forceOpenOptions();
        $("#obstacleProperties").hide();
    });

});


optionsContent.on('click', "#updateObstacleButton", function (e) {
    e.preventDefault();
    var obstacle = JSON.parse($.session.get("Obstacle"));
    var oldName = obstacle.theName;
    obstacle.theName = $("#theName").val();
    obstacle.theOriginator = $("#theOriginator").val();
    var tags = $("#theTags").text().split(", ");
    if(tags[0] != ""){
        obstacle.theTags = tags;
    }
    if($("#editObstacleOptionsForm").hasClass("new")){
        postGoal(obstacle, function () {

            createEditObstaclesTable();
            $("#editAttackerOptionsForm").removeClass("new")
        });
    } else {
        putGoal(obstacle, oldName, function () {
            createEditObstaclesTable();
        });
    }
});
optionsContent.on('dblclick', '.editGoalSubGoalRow', function () {
    toggleGoalwindow("#editGoalSubGoal");
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

optionsContent.on('click',"#updateGoalGoal", function () {
    var obstacle = JSON.parse($.session.get("Obstacle"));
    var envName = $.session.get("ObstacleEnvName");
    if($("#editGoalGoal").hasClass("new")) {
        $("#editGoalGoal").removeClass("new");
        $.each(obstacle.theEnvironmentProperties, function (index, env) {
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
        $.each(obstacle.theEnvironmentProperties, function (index, env) {
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
    $.session.set("Obstacle", JSON.stringify(obstacle));
    fillObstacleOptionMenu(obstacle);
    toggleGoalwindow("#editObstacleOptionsForm");
});
function getObstacleOptions(name){
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + "/api/obstacles/name/" + name.replace(" ", "%20"),
        success: function (data) {
            fillObstacleOptionMenu(data);
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });
}

function fillObstacleOptionMenu(data,callback){
    fillOptionMenu("fastTemplates/editObstaclesOptions.html","#optionsContent",null,true,true, function(){
            if(data != null) {
                $.session.set("Obstacle", JSON.stringify(data));
                $('#editObstacleOptionsForm').loadJSON(data, null);

                $.each(data.theTags, function (index, tag) {
                    $("#theTags").append(tag + ", ");
                });
                $.each(data.theEnvironmentProperties, function (index, prop) {
                    appendObstacleEnvironment(prop.theEnvironmentName);
                });
                $("#optionsHeaderGear").text("Obstacle properties");
                forceOpenOptions();
                $("#theObstacleEnvironments").find(".obstacleEnvProperties:first").trigger('click');

            }
            else{
                var obstacle =  jQuery.extend(true, {},obstacle.efault );
                $.session.set("Obstacle", JSON.stringify(obstacle));
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
   getAllGoals(function (data) {
        $.each(data, function (key, goals) {
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
    var theGoalName = $("#theGoalName");
    theGoalName.empty();
    getAllGoals(function (data) {
        $.each(data, function (key, goal) {
            theGoalName.append($("<option></option>")
                .attr("value", key)
                .text(key));
        });
    });
    getAllRequirements(function (data) {
        $.each(data, function (key, req) {
            theGoal.name.append($("<option></option>")
                .attr("value", req.theLabel)
                .text(req.theLabel));
        });
        if (typeof theSettableValue  !== "undefined"){
            theobstacle.same.val(theSettableValue);
        }
    });
}
function toggleGoalwindow(window){
    $("#editObstacleOptionsForm").hide();
    $("#editGoalSubGoal").hide();
    $("#editGoalGoal").hide();
    $(window).show();
}

function emptyObstacleEnvTables(){
    $("#editGoalsGoalsTable").find("tbody").empty();
    $("#editGoalsSubGoals.Table").find("tbody").empty();
    $("#editGoalsConcernTable").find("tbody").empty();
}

function appendObstacleEnvironment(text){
    $("#theObstacleEnvironments").append("<tr><td class='deleteObstacleEnv'><i class='fa fa-minus'></i></td><td class='obstacleEnvProperties'>"+ text +"</td></tr>");
}
function appendGoalEnvGoals(obstacle){
    $("#editGoalsGoalsTable").append('<tr class="editGoalGoalRow"><td class="deleteGoalGoal"><i class="fa fa-minus"></i></td><td class="envGoalName">'+obstacle[0]+'</td><td>'+obstacle[1]+'</td><td>'+obstacle[2]+'</td><td>'+obstacle[3]+'</td><td>'+obstacle[4]+'</td></tr>');
}
function appendGoalSubGoal(subobstacle){
    $("#editGoalsSubGoalsTable").append('<tr class="editGoalSubGoalRow"><td class="deleteGoalSubGoal"><i class="fa fa-minus"></i></td><td class="subGoalName">'+subobstacle[0]+'</td><td>'+subobstacle[1]+'</td><td>'+subobstacle[2]+'</td><td>'+subobstacle[3]+'</td><td>'+subobstacle[4]+'</td></tr>');
}
function appendObstacleConcern(concern){
    $("#editGoalsConcernTable").append('<tr><td class="deleteObstacleEnvConcern" value="'+ concern+'"><i class="fa fa-minus"></i></td><td class="ObstacleConcernName">'+concern+'</td></tr>');
}

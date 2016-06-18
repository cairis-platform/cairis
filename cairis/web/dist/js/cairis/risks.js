$("#risksClick").click(function () {
    createRisksTable();
});

function createRisksTable(){

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
            window.activeTable = "Risks";
            setTableHeader();
            var theTable = $(".theTable");
            $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
            var textToInsert = [];
            var i = 0;

            $.each(data, function(key, item) {
                textToInsert[i++] = "<tr>";
                textToInsert[i++] = '<td><button class="editRiskButton" value="' + key + '">' + 'Edit' + '</button> ' +
                    '<button class="deleteRiskButton" value="' + key + '">' + 'Delete' + '</button></td>';

                textToInsert[i++] = '<td name="theName">';
                textToInsert[i++] = key;
                textToInsert[i++] = '</td>';

                textToInsert[i++] = '</tr>';
            });

            theTable.append(textToInsert.join(''));
            theTable.css("visibility","visible");
            activeElement("reqTable");
            sortTableByRow(1);

        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    })
}
optionsContent.on('dblclick', ".riskEnvironment", function () {

});
optionsContent.on('click', "#editMisusedCase", function (e) {
    e.preventDefault();
    var name = $.session.get("riskName");
    toggleRiskWindows();
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + "/api/misuse-cases/risk/" + name ,
        success: function (data) {
            $("#theMisuseName").val(data.theName);
            $("#theMisuseRisk").val(data.theRiskName);
            $.each(data.theEnvironmentDictionary, function (key, object) {
                appendMisuseEnvironment(key);
                //TODO misuseCASE WHEN API IS READY

            });
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    })

});

function toggleRiskWindows(){
    $("#editMisusedCaseDiv").toggle();
    $("#editRisksForm").toggle();
}


//fillOptionMenu("fastTemplates/editAttackerOptions.html", "#optionsContent", null, true, true, function () {
$(document).on('click', '.editRiskButton', function () {
    var name = $(this).val();
    $.session.set("riskName", name);
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + "/api/risks/name/" + name.replace(" ", "%20"),
        success: function (mainData) {
            // console.log(JSON.stringify(rawData));
            fillOptionMenu("fastTemplates/editRiskOptions.html", "#optionsContent", null, true, true, function () {
                    forceOpenOptions();
                    var threatSelect = $("#theThreatNames");
                    var vulnSelect = $("#theVulnerabilityNames");
                    getThreats(function (data) {
                        $.each(data, function (key, obj) {
                            threatSelect.append($("<option></option>")
                                    .attr("value",key)
                                    .text(key));
                        });
                        threatSelect.val(mainData.theThreatName);
                    });
                    getVulnerabilities(function (data) {
                        $.each(data, function (key, obj) {
                            vulnSelect.append($("<option></option>")
                                .attr("value",key)
                                .text(key));
                        });
                        vulnSelect.val(mainData.theVulnerabilityName);
                        getRiskEnvironments();
                    });
                    $("#theName").val(mainData.theName);
                    var tags = data.theTags;
                    var text = "";
                    $.each(tags, function (index, type) {
                        text += type + ", ";
                    });
                    $("#theTags").val(text);
                }
            );
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });

});
optionsContent.on('click', '.riskEnvironment', function () {
    var env = $(this).text();
    var name = $("#theName").val();
    getRiskEnvironmentDetails(name, env);
});
optionsContent.on('change', ".riskDetailsChanger", function () {
   getRiskEnvironments()
});

function getRiskEnvironments(){
    var threatName = $("#theThreatNames").val();
    var vulName = $("#theVulnerabilityNames").val();
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crfossDomain: true,
        url: serverIP + "/api/environments/threat/" + threatName + "/vulnerability/"+ vulName + "/names",
        success: function (data) {
            $('#theRiskEnvironments').find('tbody').empty();
            $.each(data, function (index, object) {
                appendRiskEnvironment(object);
            })
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });
}

function getRiskEnvironmentDetails(name, environment){
    var threatName = $("#theThreatNames").val();
    var vulName = $("#theVulnerabilityNames").val();
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crfossDomain: true,
        //GET /api/risks/threat/{threat}/vulnerability/{vulnerability}/environment/{environment}
        url: serverIP + "/api/risks/threat/" + threatName + "/vulnerability/"+ vulName + "/environment/" + environment,
        success: function (data) {
            $("#rating").val(data.rating);

            $.ajax({
                type: "GET",
                dataType: "json",
                accept: "application/json",
                data: {
                    session_id: String($.session.get('sessionID'))
                },
                crfossDomain: true,
                //GET /api/risks/threat/{threat}/vulnerability/{vulnerability}/environment/{environment}
                url: serverIP + "/api/risks/name/"+ name +"/threat/" + threatName + "/vulnerability/"+ vulName + "/environment/" + environment,
                success: function (data) {
                    $("#theResponses").find("tbody").empty();
                    $.each(data, function (index, object) {
                        appendRiskResponse(object);
                    })
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
}

//TODO> to CAIRIS.js
function getThreats(callback){
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crfossDomain: true,
        url: serverIP + "/api/threats",
            success: function (data) {
                if(jQuery.isFunction(callback)){
                    callback(data);
                }
            },
            error: function (xhr, textStatus, errorThrown) {
                debugLogger(String(this.url));
                debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
            }
        });

}
function getVulnerabilities(callback){
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
            if(jQuery.isFunction(callback)){
                callback(data);
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });

}
function appendRiskEnvironment(environment){
    $("#theRiskEnvironments").find("tbody").append('<tr></td><td class="riskEnvironment">'+environment+'</td></tr>');
}
function appendRiskResponse(resp){
    $("#theResponses").find("tbody").append('<tr></td><td>'+resp.responseName+'</td><td>'+ resp.unmitScore +'</td><td>'+ resp.mitScore +'</td></tr>');
}
function appendMisuseEnvironment(environment){
    $("#theMisuseEnvironments").find("tbody").append('<tr><td>'+environment+'</td></tr>');
}
/**
 * Created by Raf on 1/05/2015.
 */
$( document ).ajaxComplete(function() {
    $("svg > g > g .node > a ").on('click', function (event) {
        event.stopImmediatePropagation();
        event.preventDefault();
        var link = $(this).attr("xlink:href");

        if(link.indexOf("assets") > -1) {
            $.ajax({
                type: "GET",
                dataType: "json",
                accept: "application/json",
                data: {
                    session_id: String($.session.get('sessionID'))
                },
                crossDomain: true,
                url: serverIP + link.replace(" ", "%20"),
                success: function (data) {
                    /*
                     Explanation: Because the options menu is used in multiple cases, I read in the used HTML from a template.
                     Then, because the reading of this html goes Async (as with every jQuery method), I give my data and the ID's so I can fill it after
                     the read of the template is done.
                     */
                    //forceOpenOptions();
                    var dataArr = [];
                    dataArr["#theName"] = String(data.theName);
                    dataArr["#theDescription"] = String(data.theDescription);
                    dataArr["#theSignificance"] = String(data.theSignificance);
                    var theTableArr =[];

                    $.ajax({
                        type:"GET",
                        dataType: "json",
                        accept:"application/json",
                        data: {
                            session_id: String($.session.get('sessionID'))
                        },
                        crossDomain: true,
                        url: serverIP + "/api/assets/id/"+ data.theId + "/properties",
                        success: function(data2){
                            var jsonObj = eval(data2);
                            var theTableArr = [];
                            for (var key in jsonObj) {
                                if (jsonObj.hasOwnProperty(key)) {
                                    if(key == window.assetEnvironment){
                                        var goodData =  eval(jsonObj[key]);
                                        for (var ky in goodData) {
                                            //goodData[ky] = Availibility  + intgr
                                            for (var k in goodData[ky]) {
                                                if(k == "value"){
                                                    theTableArr[String(ky)] = String(goodData[ky][k]);
                                                    debugLogger(String(ky) + " " + String(goodData[ky][k]));
                                                }
                                                //console.log(goodData[ky][k] + " " + k);
                                            }
                                        }
                                    }
                                }
                            }
                            dataArr["assetproptable"] = theTableArr;
                            fillOptionMenu("fastTemplates/AssetOptions.html", "#optionsContent", dataArr,false,true);
                        },
                        error: function(xhr, textStatus, errorThrown) {
                            console.log(this.url);
                            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
                        }

                    });

                },
                error: function (xhr, textStatus, errorThrown) {
                    console.log(String(this.url));
                    debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
                }

            });
        }else if(link.indexOf("personas") > -1) {
            forceOpenOptions();
            fillOptionMenu("fastTemplates/PersonaProperties.html", "#optionsContent",null,true,false);
            $(function() {
                $( ".tabs" ).tabs();
            });

        }

        forceOpenOptions();
    });
});
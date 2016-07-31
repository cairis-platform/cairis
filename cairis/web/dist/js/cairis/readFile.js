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

    Authors: Raf Vandelaer */


function fillOptionMenu(filePath,theElement,theData,createTabs,optionsHeader,callback) {
    jQuery.get(filePath, function(data) {
        var optionsDIV = $("#optionsHeaderGear");
        if(optionsHeader){
            if(!optionsDIV.is(":visible")){
                optionsDIV.show();
                $("#rightnavMenu").css("padding","10px");
            }
        }else{
            optionsDIV.hide();
            $("#rightnavMenu").css("padding","0px");
        }

        var el = $(theElement);
        el.empty();
        el.append(data); //display output in DOM

        for (var key in theData) {
            if (theData.hasOwnProperty(key)) {
                if(key.indexOf("table") >= 0){
                    var tablevars = theData[key];
                    var testvar = eval(tablevars);
                    for(var prop in tablevars){
                        $("#" + key).append("<tr><td>" + prop + "</td><td>" + tablevars[prop] + "</td></tr>");
                      debugLogger("ID: " + key + " the data: <tr><td>" + prop + "</td><td>" + tablevars[prop] + "</td></tr>");
                    }
                }else {
                    var value = theData[key];
                    // Use `key` and `value`
                    debugLogger("ID: " + key + " Value: " + String(value));
                    $(key).attr("value", String(value));
                }
            }
        }
        if(createTabs){
            $(function() {
                $( ".tabs" ).tabs();
            });
        }
        callback();
    });

}

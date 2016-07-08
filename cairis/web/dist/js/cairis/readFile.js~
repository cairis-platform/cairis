/**
 * Created by Raf on 30/04/2015.
 */
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

/**
 * Created by Raf on 3/06/2015.
 */

$("#editProjectsClick").click(function () {
    getProjectSettings(function (data) {
        fillOptionMenu("fastTemplates/editProjectSettings.html", "#optionsContent", null, true, false, function () {
            forceOpenOptions();
            var image = $("#theImages");
            $('#ProjectsProperties').loadJSON(data, null);
            image.attr("src", getImagedir(data.richPicture));
            resaleImage(image,350);
            //definitions
            $.each(data.definitions, function (key, def) {
                appendNamingConvention(key,def);
            });
            $.each(data.contributions, function (index, contributor) {
                appendContributor(contributor);
            });
            $.each(data.revisions, function (index, rev) {
                editProjectRevisions(rev);
            });
        });
    });

});

function getProjectSettings(callback){
    $.ajax({
        type: "GET",
        dataType: "json",
        accept: "application/json",
        data: {
            session_id: String($.session.get('sessionID'))
        },
        crossDomain: true,
        url: serverIP + "/api/settings",
        success: function (data) {
            $.session.set("ProjectSettings", JSON.stringify(data));
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
/*
 Image uploading functions
 */
var uploading = false;
var optionsContent = $("#optionsContent");
optionsContent.on('click', '#theImages', function () {
    if(!uploading) {
        $('#projectSettingsUpload').trigger("click");
    }
});
optionsContent.on('click',".projectSettingsCancel", function (e) {
    e.preventDefault();
    projectSettingsToggler();
});
optionsContent.on('click', "#addContributor", function () {
    projectSettingsToggler("#editContributorWindow");
});
optionsContent.on('click', '.removeContributor', function () {
    var row = $(this).closest("tr");
    var name = row.find(".projectContributor").text();
    var surname = row.find('.conSurname').text();
    var settings =  JSON.parse($.session.get("ProjectSettings"));
    $.each(settings.contributions, function (index, contr) {
        if(contr.surname == surname && contr.firstName == name){
            settings.contributions.splice(index,1);
            $.session.set("ProjectSettings", JSON.stringify(settings));
            row.remove();
        }
    });
});
optionsContent.on('click', '#addNamingConvention', function () {
    projectSettingsToggler("#editNamingConvention");
    $('#editNamingConvention').addClass("new");
});
optionsContent.on('click', "#updateNamingConventions", function () {
    var tableBody = $("#editNamingConventionsTable").find("tbody");
    var settings =  JSON.parse($.session.get("ProjectSettings"));
    if($('#editNamingConvention').hasClass("new")){
        var key = $("#conventionName").val();
        var value = $("#conventionDefinition").val();
        settings.definitions[key] = value;
    }else{
        var key = $("#conventionName").val();
        var value = $("#conventionDefinition").val();
      delete settings.definitions[$.session.get("namingConvName")];
        settings.definitions[key] = value;

    }
    tableBody.empty();
    $.each(settings.definitions, function (key, val) {
        appendNamingConvention(key, val);
    });
    projectSettingsToggler();
    $.session.set("ProjectSettings", JSON.stringify(settings));
});
optionsContent.on('click', '.removeProjectNamingConvertion', function () {
    var row = $(this).closest('tr');
    var settings =  JSON.parse($.session.get("ProjectSettings"));
    var orikey = row.find(".namingConvention").text();
    var orival = row.find(".theNameingDef").text();

    $.each(settings.definitions, function (key, val) {
       if(key == orikey && val == orival){
            delete settings.definitions[key];
           row.remove();
       }
    });
    $.session.set("ProjectSettings", JSON.stringify(settings));
});
optionsContent.on('dblclick', '.editNamingConvention', function () {
   var row = $(this);
    var key = row.find(".namingConvention").text();
    var val = row.find(".theNameingDef").text();
    $.session.set("namingConvName",key);
    projectSettingsToggler("#editNamingConvention");
    $("#conventionName").val(key);
    $("#conventionDefinition").val(val);

});
optionsContent.on("click", "#updateProjectButton", function (e) {
    e.preventDefault();
    var settings =  JSON.parse($.session.get("ProjectSettings"));
    settings.projectName = $("#projectName").val();
    settings.projectBackground = $("#projectBackground").val();
    settings.projectGoals = $("#projectGoals").val();
    settings.projectScope = $("#projectScope").val();
    putProjectSettings(settings);
    forceCloseOptions();
    $.session.set("ProjectSettings", JSON.stringify(settings));
});

optionsContent.on('click', "#updateContributor", function () {
    var con = {};
    con.firstName = $("#firstName").val();
    con.surname = $("#surname").val();
    con.affliation = $("#affliation").val();
    con.role = $("#role").val();
    con.__python_obj__ = "tools.PseudoClasses.Contributor";

   var settings =  JSON.parse($.session.get("ProjectSettings"));
    if($('editContributorWindow').hasClass("new")){
        appendContributor(con);
        settings.contributions.push(con);

    } else {
        var oldName = $.session.get("contributorOldName");
        $.each(settings.contributions, function (index, contr) {
            if(contr.surname == oldName){
                settings.contributions[index]  = con;
            }
        });
        $("#editContributorTable").find("tbody").empty();
        $.each(settings.contributions, function (index, contr) {
            appendContributor(contr);
        });
    }
    projectSettingsToggler();
    $.session.set("ProjectSettings", JSON.stringify(settings));
});
optionsContent.on('dblclick','.editContributor', function () {
    var row = $(this).closest("tr");
   projectSettingsToggler("#editContributorWindow");
    var name = row.find(".projectContributor").text();
    var theSurname = row.find(".conSurname").text();
    $.session.set("contributorOldName", theSurname);
    var affl = row.find(".conAffliation").text();
    var theRole = row.find(".conRole").text();

    $("#firstName").val(name);
    $("#surname").val(theSurname);
    $("#affliation").val(affl);
    $("#role").val(theRole);
});
optionsContent.on('click',"#addProjectRevision", function () {
    projectSettingsToggler("#addRevision");
});
optionsContent.on('click', '#addRevisionButton', function (e) {
    e.preventDefault();
    var textArea = $("#revisionTextArea");
    if(textArea.val() == ''){
        alert("Give some info please");
    }
    else{
        var settings = JSON.parse($.session.get("ProjectSettings"));
        var rev = {};
        rev.__python_obj__ = "tools.PseudoClasses.Revision";
        rev.date = getDate("dd-MM-yy hh:mm:ss");
        rev.description = textArea.val();
        rev.id = -1;
        //TODO POSTEN REVISION
        $.session.set("ProjectSettings", JSON.stringify(settings));
    }

});



optionsContent.on('change','#projectSettingsUpload', function () {
    uploading = true;
    var test = $(document).find('#projectSettingsUpload');
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
            postProjectImage(data.filename, getImagedir(data.filename));
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

function projectSettingsToggler(window){
    //TO empty
    if(window == "#editContributorWindow"){
        $("#firstName").val('');
        $("#surname").val('');
        $("#affliation").val('');
    }
    else if (window == "#addRevision"){
        $("#revisionTextArea").val('');
    }
    else if (window == "#editNamingConvention"){
        $("#conventionName").val('');
        $("#conventionDefinition").val('');
    }
    //Actual toggler
    if(typeof window == 'undefined'){
        $("#ProjectsProperties").show();
        $("#editContributorWindow").hide();
        $("#addRevision").hide();
        $("#editNamingConvention").hide();
        //editNamingConvention
    }else{
        $("#ProjectsProperties").hide();
        $("#editContributorWindow").hide();
        $("#editNamingConvention").hide()
        $("#addRevision").hide();
        $(window).show();
    }
}

function postProjectImage(imagedir, actualDir) {
    var settings = JSON.parse($.session.get("ProjectSettings"));

    settings.richPicture = imagedir;
    var theImage = $("#theImages");
   putProjectSettings(settings, function () {
       theImage.attr("src", actualDir);
        resaleImage(theImage, 350);
    });
    $.session.set("ProjectSettings", JSON.stringify(settings));

}
function appendNamingConvention(name,def){
    $("#editNamingConventionsTable").find("tbody").append("<tr class='editNamingConvention'><td class='removeProjectNamingConvertion' ><i class='fa fa-minus'></i></td><td class='namingConvention'>" + name + "</td><td class='theNameingDef'>"+ def + "</td></tr>");
}
function appendContributor(con){
    $("#editContributorTable").find("tbody").append("<tr class='editContributor'><td class='removeContributor' ><i class='fa fa-minus'></i></td><td class='projectContributor'>" + con.firstName + "</td><td class='conSurname'>"+ con.surname + "</td><td class='conAffliation'>"+ con.affliation + "</td><td class='conRole'>"+ con.role +"</td></tr>");
}
function editProjectRevisions(rev){
    if(rev.id == -1){
        rev.id = "*";
    }
    $("#editProjectRevisions").find("tbody").append("<tr><td></td><td class='projectRevision'>" + rev.id + "</td><td>"+ rev.date + "</td><td>"+ rev.description + "</td></tr>");
}

function getDate(format, utc) {
    var date =  new Date();
    var MMMM = ["\x00", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    var MMM = ["\x01", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var dddd = ["\x02", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var ddd = ["\x03", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

    function ii(i, len) {
        var s = i + "";
        len = len || 2;
        while (s.length < len) s = "0" + s;
        return s;
    }

    var y = utc ? date.getUTCFullYear() : date.getFullYear();
    format = format.replace(/(^|[^\\])yyyy+/g, "$1" + y);
    format = format.replace(/(^|[^\\])yy/g, "$1" + y.toString().substr(2, 2));
    format = format.replace(/(^|[^\\])y/g, "$1" + y);

    var M = (utc ? date.getUTCMonth() : date.getMonth()) + 1;
    format = format.replace(/(^|[^\\])MMMM+/g, "$1" + MMMM[0]);
    format = format.replace(/(^|[^\\])MMM/g, "$1" + MMM[0]);
    format = format.replace(/(^|[^\\])MM/g, "$1" + ii(M));
    format = format.replace(/(^|[^\\])M/g, "$1" + M);

    var d = utc ? date.getUTCDate() : date.getDate();
    format = format.replace(/(^|[^\\])dddd+/g, "$1" + dddd[0]);
    format = format.replace(/(^|[^\\])ddd/g, "$1" + ddd[0]);
    format = format.replace(/(^|[^\\])dd/g, "$1" + ii(d));
    format = format.replace(/(^|[^\\])d/g, "$1" + d);

    var H = utc ? date.getUTCHours() : date.getHours();
    format = format.replace(/(^|[^\\])HH+/g, "$1" + ii(H));
    format = format.replace(/(^|[^\\])H/g, "$1" + H);

    var h = H > 12 ? H - 12 : H == 0 ? 12 : H;
    format = format.replace(/(^|[^\\])hh+/g, "$1" + ii(h));
    format = format.replace(/(^|[^\\])h/g, "$1" + h);

    var m = utc ? date.getUTCMinutes() : date.getMinutes();
    format = format.replace(/(^|[^\\])mm+/g, "$1" + ii(m));
    format = format.replace(/(^|[^\\])m/g, "$1" + m);

    var s = utc ? date.getUTCSeconds() : date.getSeconds();
    format = format.replace(/(^|[^\\])ss+/g, "$1" + ii(s));
    format = format.replace(/(^|[^\\])s/g, "$1" + s);

    var f = utc ? date.getUTCMilliseconds() : date.getMilliseconds();
    format = format.replace(/(^|[^\\])fff+/g, "$1" + ii(f, 3));
    f = Math.round(f / 10);
    format = format.replace(/(^|[^\\])ff/g, "$1" + ii(f));
    f = Math.round(f / 10);
    format = format.replace(/(^|[^\\])f/g, "$1" + f);

    var T = H < 12 ? "AM" : "PM";
    format = format.replace(/(^|[^\\])TT+/g, "$1" + T);
    format = format.replace(/(^|[^\\])T/g, "$1" + T.charAt(0));

    var t = T.toLowerCase();
    format = format.replace(/(^|[^\\])tt+/g, "$1" + t);
    format = format.replace(/(^|[^\\])t/g, "$1" + t.charAt(0));

    var tz = -date.getTimezoneOffset();
    var K = utc || !tz ? "Z" : tz > 0 ? "+" : "-";
    if (!utc) {
        tz = Math.abs(tz);
        var tzHrs = Math.floor(tz / 60);
        var tzMin = tz % 60;
        K += ii(tzHrs) + ":" + ii(tzMin);
    }
    format = format.replace(/(^|[^\\])K/g, "$1" + K);

    var day = (utc ? date.getUTCDay() : date.getDay()) + 1;
    format = format.replace(new RegExp(dddd[0], "g"), dddd[day]);
    format = format.replace(new RegExp(ddd[0], "g"), ddd[day]);

    format = format.replace(new RegExp(MMMM[0], "g"), MMMM[M]);
    format = format.replace(new RegExp(MMM[0], "g"), MMM[M]);

    format = format.replace(/\\(.)/g, "$1");

    return format;
}
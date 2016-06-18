/**
 * Created by Raf on 8/06/2015.
 */
$("#importClick").click(function () {
    fileDialogbox(function (type) {
        $.session.set("fileType", type);
    }) 
});
$(document).on('change','#importFile', function () {
    var fileTag = $(document).find('#importFile');
    var fd = new FormData();
    fd.append("file", fileTag[0].files[0]);
   var fileType = $.session.get("fileType");

    $.ajax({
        type: "POST",
        accept: "application/json",
        processData:false,
        contentType:false,
        data: fd,
        crossDomain: true,
        url: serverIP + "/api/import/file/type/"+ fileType +"?session_id="+  String($.session.get('sessionID')),
        success: function (data) {
            showPopup(true);
        },
        error: function (xhr, textStatus, errorThrown) {
            var error = JSON.parse(xhr.responseText);
            showPopup(false, String(error.message));
            debugLogger(String(this.url));
            debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
        }
    });
});



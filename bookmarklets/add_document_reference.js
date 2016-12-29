var hTxt=((window.getSelection&&window.getSelection())||(document.getSelection&&document.getSelection())||(document.selection&&document.selection.createRange&&document.selection.createRange().text));
var x = prompt( "Synopsis:", excerpt);
var dr = {'theName':x,'theDocName':'OnlineTest','theContributor':'SF','theExcerpt': hTxt};
var output = {};
output.object = dr;
output.session_id = 'test';
output = JSON.stringify(output);
var serverIP = 'http://germaneriposte.org:7071';
$.ajax({
    type: "POST",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/document_references" + "?session_id=test",
    success: function (data) {
      alert('Reference added');
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      alert(String(error.message));
    }
  });

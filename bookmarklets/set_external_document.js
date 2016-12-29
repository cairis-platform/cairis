var serverIP = 'http://germaneriposte.org:7071';
$.ajax({
  type: "GET",
  dataType: "json",
  accept: "application/json",
  crossDomain: true,
  data: {session_id : 'test'},
  url: serverIP + "/api/external_documents/name/" + encodeURIComponent(document.title) + "?session_id=test",
  success: function (data) {
    document.cookie = 'external_document_name=' + window.document.title;
    alert(document.title + ' set');
  },
  error: function (xhr, textStatus, errorThrown) {
    if (xhr.status == 404) {
      var edoc = {'theName':    document.title,'theVersion':'1','thePublicationDate':document.lastModified,'theAuthors' : 'Unknown','theDescription' : window.location.href};
      var output = {};
      output.object = edoc;
      output.session_id = 'test';
      output = JSON.stringify(output);
      $.ajax({
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        accept: "application/json",
        crossDomain: true,
        processData: false,
        origin: serverIP,
        data: output,
        url: serverIP + "/api/external_documents" + "?session_id=test",
        success: function (data) {
          document.cookie = 'external_document_name=' + edoc['theName'];
          alert('External document "' + edoc['theName'] + '" added');
        },
        error: function (xhr, textStatus, errorThrown) {
          var error = JSON.parse(xhr.responseText);
          alert(String(error.message));
        }
      });
    }
    else {
      alert(String(error.message));
    }
  }
});

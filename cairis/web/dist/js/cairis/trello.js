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

'use strict';

$('#toTrello').click(function(){
  Trello.authorize({
    type: 'popup',
    name: 'CAIRIS',
    scope: {
      read: 'true',
      write: 'true' },
    expiration: 'never',
    success: function() {
      $("#toTrelloModal").modal('show');
    },
    error: function() {
      showPopup(false,'Authentication failed');
    }
  });
});

$('#toTrelloModal').on('shown.bs.modal',function() {
});


function RateLimit(fn, delay, context) {
  var queue = [], timer = null;

  function processQueue() {
    var item = queue.shift();
    if (item) {
      fn.apply(item.context, item.arguments);
    }
    if (queue.length === 0) {
      clearInterval(timer), timer = null;
    }
  }

  return function limited() {
    queue.push({
      context: context || this,
      arguments: [].slice.call(arguments)
    });
    if (!timer) {
      processQueue(); 
      timer = setInterval(processQueue, delay);
    }
  }
}

function postReference(dr,listId) {
  var newCard = {
    name: dr.theName,
    desc: dr.theExcerpt,
    due: null
  };
  Trello.post('/lists/' + listId + '/cards',newCard,function() {
    debugLogger('Card posted');
  });
}

$('#toTrelloModal').on('click','#ExportReferences',function(){
  var boardName = $('#theToBoard').val();
  var newBoard = {
    name: boardName
  }
  Trello.post('/boards/',newBoard,function(createBoardData) {
    var boardId = createBoardData.id;

    Trello.post('/boards/' + boardId + '/labels',{name: 'grounds', color: 'green'},function() {
      debugLogger('grounds label added to ' + boardName);
    });
    Trello.post('/boards/' + boardId + '/labels',{name: 'warrant', color: 'blue'},function() {
      debugLogger('warrant label added to ' + boardName);
    });
    Trello.post('/boards/' + boardId + '/labels',{name: 'rebuttal', color: 'red'},function() {
      debugLogger('rebuttal label added to ' + boardName);
    });

    var newList = {name : 'Uncategorised Factoids', defaultLists: false};

    Trello.post('/boards/' + boardId + '/lists',newList,function(createListData) {
      var listId = createListData.id;
      $.ajax({
         type: "GET",
         dataType: "json",
         accept: "application/json",
         data: {
           session_id: String($.session.get('sessionID'))
         },
         crossDomain: true,
         url: serverIP + "/api/document_references",
         success: function (data) {
           var rlPost = RateLimit(postReference,100);
           $.each(data,function(idx,dr){
             rlPost(dr,listId);
           });
           $("#toTrelloModal").modal('hide');
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
  });
});

$('#fromTrello').click(function(){

  Trello.authorize({
    type: 'popup',
    name: 'CAIRIS',
    scope: {
      read: 'true',
      write: 'true' },
    expiration: 'never',
    success: function() {
      $("#fromTrelloModal").modal('show');
    },
    error: function() {
      showPopup(false,'Authentication failed');
    }
  });
});

$('#fromTrelloModal').on('shown.bs.modal',function() {
  Trello.get('/members/me/boards',function(data){
    $('#theFromBoards').empty();
    $.each(data,function(idx,item){
      $("#theFromBoards").append('<option value="' + item.id + '">' + item.name + '</option>');
    });
  });
});

$('#fromTrelloModal').on('click','#ExportLists',function(){
  var boardId = $('#theFromBoards').val();
  var pName = $("#theFromBoards option[value='" + boardId + "']").text();
  Trello.get('/boards/' + boardId + '/lists',function(data){
    $.each(data,function(idx,item){
      var itemArray = item.name.split(':')
      var pc = {
        "__python_obj__": "PersonaCharacteristic.PersonaCharacteristic",
        "theId": -1,
        "thePersonaName" : pName,
        "theModQual" : "Perhaps",
        "theVariable" : itemArray[1].trim(),
        "theCharacteristic" : itemArray[0].trim(),
        "theGrounds" : [],
        "theWarrant" : [],
        "theRebuttal" : [],
        "theBacking" :[]
      };

      Trello.get('/lists/' + item.id + '/cards',function(cards) {
        $.each(cards,function(idx,card){
          var ref = {
             "__python_obj__" : "cairis.tools.PseudoClasses.CharacteristicReference",
             "theCharacteristicType" : card.labels[0].name,
             "theDimensionName" : "document",
             "theReferenceName" : card.name,
             "theReferenceDescription" : card.desc
          };
          if (ref.theCharacteristicType == 'warrant') {
            pc.theWarrant.push(ref);
          }
          else if (ref.theCharacteristicType == 'rebuttal') {
            pc.theRebuttal.push(ref);
          }
          else {
            pc.theGrounds.push(ref);
          }
        });
        postPersonaCharacteristic(pc,function() {
          $("#fromTrelloModal").modal('hide');
          showPopup(true);
        });
      });
    });
  });
});

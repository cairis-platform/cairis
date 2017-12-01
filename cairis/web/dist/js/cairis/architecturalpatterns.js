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

$("#architecturalPatternsClick").click(function () {
  validateClick('architectural_pattern',function() {
    clearLocalStorage($('#menuBCClick').attr('dimension'));
    $("#objectViewer").empty();
    $('#menuBCClick').attr('dimension','architectural_pattern');
    refreshMenuBreadCrumb('architectural_pattern');
  });
});

function createArchitecturalPatternsTable(){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/architectural_patterns",
    success: function (data) {
      setTableHeader("ArchitecturalPatterns");
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      var apDict = {};
      $.each(data,function(idx,ap) {
        apDict[ap.theName] = ap;
      });

      var keys = [];
      for (key in apDict) {
        keys.push(key);
      }
      keys.sort();

      for (var ki = 0; ki < keys.length; ki++) {
        var key = keys[ki];
        var item = apDict[key];

        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td class="deleteArchitecturalPatternButton"><i class="fa fa-minus" value="' + item.theName + '"></i></td>';
        textToInsert[i++] = '<td class="architecturalpattern-rows" name="theName">';
        textToInsert[i++] = item.theName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theInterfacesDER">';
        textToInsert[i++] = item.theAttackSurfaceMetric[0];
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theChannelsDER">';
        textToInsert[i++] = item.theAttackSurfaceMetric[1];
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theUntrustedSurfaceDER">';
        textToInsert[i++] = item.theAttackSurfaceMetric[2];
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      }

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      $.contextMenu('destroy',$('.requirement-rows'));
      $("#mainTable").find("tbody").removeClass();
      $("#mainTable").find("tbody").addClass('ap-rows');
      $('.ap-rows').contextMenu({
        selector: 'td',
        items: {
          "weaknessanalysis": {
            name: "Weakness Analysis",
            callback: function(key, opt) {
              var apName = $(this).closest("tr").find("td").eq(1).html();
              refreshDimensionSelector($('#chooseEnvironmentSelect'),'environment',undefined,function() {
                $('#chooseEnvironment').attr('data-chooseDimension',"environment");
                $('#chooseEnvironment').attr('data-apName',apName);
                $('#chooseEnvironment').attr('data-applyEnvironmentSelection',"viewWeaknessAnalysis");
                $('#chooseEnvironment').modal('show');
              });
            }
          }
        }
      });

      activeElement("mainTable");
      sortTableByRow(0);
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
}

$(document).on('click', "td.architecturalpattern-rows", function () {
  var apName = $(this).text();
  refreshObjectBreadCrumb(apName);
  viewArchitecturalPattern(apName);
});

function viewArchitecturalPattern(apName) {
  activeElement("objectViewer");
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/architectural_patterns/name/" + encodeURIComponent(apName),
    success: function (data) {
      fillOptionMenu("fastTemplates/editArchitecturalPatternOptions.html", "#objectViewer", null, true, true, function () {
        $("#UpdateArchitecturalPattern").text("Update");
        $.session.set("ArchitecturalPattern", JSON.stringify(data));
        $("#theName").val(data.theName);
        $("#theSynopsis").val(data.theSynopsis);
        $.each(data.theComponents,function(idx,component) {
          appendComponent(component);
        });

        $.each(data.theConnectors,function(idx,connector) {
          appendConnector(connector);
        });
        $("#editArchitecturalPatternOptionsForm").validator('update');

        $("#theComponents").find("tbody").removeClass();
        $("#theComponents").find("tbody").addClass('component-rows');
        $('.component-rows').contextMenu({
          selector: 'td',
          items: {
            "assets": {
              name: "View Assets",
              callback: function(key, opt) {
                var cName = $(this).closest("tr").find("td").eq(1).html();
                viewComponentAssetModel(cName);
              }
            },
            "goals": {
              name: "View Goals",
              callback: function(key, opt) {
                var cName = $(this).closest("tr").find("td").eq(1).html();
                viewComponentGoalModel(cName);
              }
            }
          }
        });
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
};

function viewComponentAssetModel(cName) {
  $.ajax({
    type: "GET",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/architectural_patterns/component/asset/model/" + encodeURIComponent(cName),
    success: function (data) {
      Cookies.set('model','component_asset');
      Cookies.set('parameter',cName);
      Cookies.set('wTitle',cName + " assets");
      var viewerWindow = window.open('viewer.html');
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function viewComponentGoalModel(cName) {
  $.ajax({
    type: "GET",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/architectural_patterns/component/goal/model/" + encodeURIComponent(cName),
    success: function (data) {
      Cookies.set('model','component_goal');
      Cookies.set('parameter',cName);
      Cookies.set('wTitle',cName + " goals");
      var viewerWindow = window.open('viewer.html');
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

$(document).on("click", "#addNewArchitecturalPattern", function () {
  refreshObjectBreadCrumb('New Architectural Pattern');
  activeElement("objectViewer");
  fillOptionMenu("fastTemplates/editArchitecturalPatternOptions.html", "#objectViewer", null, true, true, function () {
    $("#editArchitecturalPatternOptionsForm").validator();
    $("#UpdateArchitecturalPattern").text("Create");
    $("#editArchitecturalPatternOptionsForm").addClass("new");
    $('#theName').val('');
    $('#theSynopsis').val('');
    $('#theComponents').find('tbody').empty();
    $('#theConnectors').find('tbody').empty();
    $.session.set("ArchitecturalPattern", JSON.stringify(jQuery.extend(true, {},architecturalPatternDefault )));
  });
});

function commitArchitecturalPattern() {
  var ap = JSON.parse($.session.get("ArchitecturalPattern"));
  if ($("#editArchitecturalPatternOptionsForm").hasClass("new")) {
    ap.theName = $('#theName').val();
    ap.theSynopsis = $('#theSynopsis').val();
    postArchitecturalPattern(ap,function() {
      clearLocalStorage("architectural_pattern");
      $("#editArchitecturalPatternsOptionsForm").removeClass("new");
      $('#menuBCClick').attr('dimension','architectural_pattern');
      refreshMenuBreadCrumb('architectural_pattern');
    });
  }
  else {
    var oldName = ap.theName;
    ap.theName = $('#theName').val();
    ap.theSynopsis = $('#theSynopsis').val();
    putArchitecturalPattern(ap,oldName,function() {
      clearLocalStorage("architectural_pattern");
      $('#menuBCClick').attr('dimension','architectural_pattern');
      refreshMenuBreadCrumb('architectural_pattern');
    });
  }
}

function postArchitecturalPattern(ap, callback){
  var output = {};
  output.object = ap;
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);
  debugLogger(output);

  $.ajax({
    type: "POST",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/architectural_patterns" + "?session_id=" + $.session.get('sessionID'),
    success: function (data) {
      showPopup(true);
      if(jQuery.isFunction(callback)){
        callback();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function putArchitecturalPattern(ap, oldName, callback){
  var output = {};
  output.object = ap;
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);
  debugLogger(output);
  
  $.ajax({
    type: "PUT",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/architectural_patterns/name/" + encodeURIComponent(oldName) + "?session_id=" + $.session.get('sessionID'),
    success: function (data) {
      showPopup(true);
      if(jQuery.isFunction(callback)){
        callback();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
} 

$(document).on('click', 'td.deleteArchitecturalPatternButton', function (e) {
  e.preventDefault();
  var apName = $(this).find('i').attr("value");
  deleteObject('component_view',apName,function(apName) {
    $.ajax({
      type: "DELETE",
      dataType: "json",
      contentType: "application/json",
      accept: "application/json",
      crossDomain: true,
      processData: false,
      origin: serverIP,
      url: serverIP + "/api/architectural_patterns/name/" + encodeURIComponent(apName) + "?session_id=" + $.session.get('sessionID'),
      success: function (data) {
        showPopup(true);
        $('#menuBCClick').attr('dimension','architectural_pattern');
        refreshMenuBreadCrumb('architectural_pattern');
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

function appendComponent(component) {
    $("#theComponents").find("tbody").append('<tr><td class="deleteComponent"><i class="fa fa-minus"></i></td><td class="component-row">'+ component.theName +'</td><td>' + component.theDescription + '</td></tr>');
};

function appendConnector(connector) {
    $("#theConnectors").find("tbody").append('<tr><td class="deleteConnector"><i class="fa fa-minus"></i></td><td class="connector-row">'+ connector.theConnectorName + '</td><td>' + connector.theFromComponent +'</td><td>' + connector.theFromRole + '</td><td>' + connector.theFromInterface + '</td><td>' + connector.theToComponent + '</td><td>' + connector.theToInterface + '</td><td>' + connector.theToRole + '</td><td>' + connector.theAssetName + '</td><td>' + connector.theProtocol + '</td><td>' + connector.theAccessRight + '</td></tr>');
};

$(document).on('click', "td.component-row", function () {
  var comRow = $(this).closest("tr");
  $('#editComponentDiv').attr('data-selectedIndex',comRow.index());
  var ap = JSON.parse($.session.get("ArchitecturalPattern"));
  var componentName = $(this).text();
  $.each(ap.theComponents,function(idx,apc) {
    if (apc.theName == componentName) {
      $.session.set("Component", JSON.stringify(apc));
      $("#editArchitecturalPatternOptionsForm").hide();
      $("#editComponentDiv").show(function(com) {
        $("#theComponentName").val(apc.theName); 
        $("#theDescription").val(apc.theDescription); 
        $("#theInterfaces").find("tbody").empty();
        $("#theStructure").find("tbody").empty();
        $("#theRequirements").find("tbody").empty();
        $("#theGoals").find("tbody").empty();
        $("#theGoalAssociations").find("tbody").empty();
        $.each(apc.theInterfaces,function(idx,comint) {
          appendComponentInterface(comint);
        });
        $.each(apc.theStructure,function(idx,comstr) {
          appendComponentStructure(comstr);
        });
        $.each(apc.theRequirements,function(idx,comreq) {
          appendComponentRequirement(comreq);
        });
        $.each(apc.theGoals,function(idx,comgoal) {
          appendComponentGoal(comgoal);
        });
        $.each(apc.theGoalAssociations,function(idx,comga) {
          appendComponentGoalAssociation(comga);
        });
      });
    }
  });
});

var mainContent = $("#objectViewer");
mainContent.on('click','#addComponent',function() {
  $.session.set("Component", JSON.stringify(jQuery.extend(true, {},componentDefault )));
  $("#editComponentDiv").addClass('new');
  $("#editArchitecturalPatternOptionsForm").hide();
  $("#editComponentDiv").show();
  $('#theComponentName').val('');
  $('#theDescription').val('');
  $('#theInterfaces').find('tbody').empty();
  $('#theStructure').find('tbody').empty();
  $('#theRequirements').find('tbody').empty();
  $('#theGoals').find('tbody').empty();
  $('#theGoalAssociations').find('tbody').empty();
  
});


function connectorAssets() {
  var ap = JSON.parse($.session.get("ArchitecturalPattern"));
  var fromComponent = $("#theFromComponent").val();
  var toComponent = $("#theToComponent").val();
  var assetSet = new Set();
  $.each(ap.theComponents,function(idx,apc) {
    if ((apc.theName == fromComponent) || (apc.theName == toComponent)) {
      $.each(apc.theStructure,function(idx,cstr) {
        assetSet.add(cstr.theHeadAsset);
        assetSet.add(cstr.theTailAsset);
      });
    }
  });
  return assetSet;
}

function refreshConnectorDetailsPanel() {

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/protocol",
    success: function (protocols) {
      $("#theProtocol option").remove();
      $.each(protocols,function(idx,protocol) {
        $('#theProtocol').append($("<option></option>").attr("value",protocol).text(protocol));
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/access_right",
    success: function (accessRights) {
      $("#theConnectorAccessRight option").remove();
      $.each(accessRights,function(idx,accessRight) {
        $('#theConnectorAccessRight').append($("<option></option>").attr("value",accessRight).text(accessRight));
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}


function refreshConnectorPanels(ap) {
  var ap = JSON.parse($.session.get("ArchitecturalPattern"));
  $("#theFromComponent option").remove();
  $("#theToComponent option").remove();
  $.each(ap.theComponents,function(idx,comp) {
    $('#theFromComponent').append($("<option></option>").attr("value",comp.theName).text(comp.theName));
    $('#theToComponent').append($("<option></option>").attr("value",comp.theName).text(comp.theName));
  });
  
  $("#theFromInterface option").remove();
  $("#theToInterface option").remove();

  var fromCompName = $('#theFromComponent').val();
  var toCompName = $('#theFromComponent').val();
  $.each(ap.theComponents,function(idx,comp) {
    if (comp.theName == fromCompName) {
      $.each(comp.theInterfaces,function(idx,compInt) {
        $("#theFromInterface").append($("<option></option>").attr("value",compInt.theName).text(compInt.theName));
      });
    }
    if (comp.theName == toCompName) {
      $.each(comp.theInterfaces,function(idx,compInt) {
        $("#theToInterface").append($("<option></option>").attr("value",compInt.theName).text(compInt.theName));
      });
    }
  });
}

mainContent.on('click', "td.connector-row", function () {
  var ap = JSON.parse($.session.get("ArchitecturalPattern"));
  var connectorName = $(this).text();
  $.each(ap.theConnectors, function(idx,conn) {
    if (connectorName == conn.theConnectorName) {
      $("#editArchitecturalPatternOptionsForm").hide();
      $("#editConnectorDiv").show(function() {
        $("#theConnectorName").val(connectorName); 
        $("#theFromRole").val(conn.theFromRole); 
        $("#theToRole").val(conn.theToRole); 
        refreshConnectorPanels(ap);
        $('#theFromComponent').val(conn.theFromComponent);
        $('#theToComponent').val(conn.theToComponent);

        $.each(ap.theComponents,function(idx,comp) {
           if (comp.theName == conn.theFromComponent) {
             $.each(comp.theInterfaces,function(idx,compInt) {
               $("#theFromInterface").append($("<option></option>").attr("value",compInt.theName).text(compInt.theName));
             });
             $("#theFromInterface").val(conn.theFromInterface); 
           }

           if (comp.theName == conn.theToComponent) {
             $.each(comp.theInterfaces,function(idx,compInt) {
               $("#theToInterface").append($("<option></option>").attr("value",compInt.theName).text(compInt.theName));
             });
             $("#theToInterface").val(conn.theToInterface); 
           }
        });
        refreshConnectorDetailsPanel();
        $("#theProtocol").val(conn.theProtocol);
        $("#theConnectorAccessRight").val(conn.theAccessRight);
        refreshAssetBox(conn.theAssetName);

        $('#theFromComponent').trigger('change');
        $('#theToComponent').trigger('change');
      });
    }
  });
});

mainContent.on('click','#addConnector',function() {
  $("#editConnectorDiv").addClass('new');
  $("#editArchitecturalPatternOptionsForm").hide();
  $('#theConnectorName').val('');
  $('#theFromRole').val('');
  $('#theToRole').val('');
  var ap = JSON.parse($.session.get("ArchitecturalPattern"));
  refreshConnectorPanels(ap);
  refreshConnectorDetailsPanel();
  $("#editConnectorDiv").show();
});

mainContent.on('change',"#theFromComponent", function() {
  refreshAssetBox();
  refreshInterfaceBox("#theFromInterface",$("#theFromComponent").val());
});

mainContent.on('change',"#theToComponent", function() {
  refreshAssetBox();
  refreshInterfaceBox("#theToInterface",$("#theToComponent").val());
});

function refreshAssetBox(currentAsset) {
  if (currentAsset == undefined) {
    currentAsset = $("#theConnectorAssetName").val();
  }
  $("#theConnectorAssetName option").remove();
  var assets = connectorAssets();
  for (let cAsset of assets) {
    $('#theConnectorAssetName').append($("<option></option>").attr("value",cAsset).text(cAsset));
  }
  if (assets.has(currentAsset)) {
    $("#theConnectorAssetName").val(currentAsset);
  }
};

function refreshInterfaceBox(intCtrlId,cName) {
  var currentInterface = $(intCtrlId).val();
  $(intCtrlId + " option").remove();
  var ap = JSON.parse($.session.get("ArchitecturalPattern"));
  $.each(ap.theComponents,function(idx,comp) {
    if (cName == comp.theName) {
      $.each(comp.theInterfaces,function(idx,compInt) {
        $(intCtrlId).append($("<option></option>").attr("value",compInt.theName).text(compInt.theName));
      });
      $(intCtrlId).val(currentInterface); 
    }
  });
}

function appendComponentInterface(comint) {
    $("#theInterfaces").find("tbody").append('<tr><td class="deleteComponentInterface"><i class="fa fa-minus"></i></td><td class="component-interface">'+ comint.theName +'</td><td>' + comint.theType + '</td><td>' + comint.theAccessRight + '</td><td>' + comint.thePrivilege + '</td></tr>');
};

function appendComponentStructure(comstr) {
    $("#theStructure").find("tbody").append('<tr><td class="deleteComponentStructure"><i class="fa fa-minus"></i></td><td class="component-structure">'+ comstr.theHeadAsset +'</td><td>' + comstr.theHeadAdornment + '</td><td>' + comstr.theHeadNav + '</td><td>' + comstr.theHeadNry + '</td><td>' + comstr.theHeadRole + '</td><td>' + comstr.theTailRole + '</td><td>' + comstr.theTailNry + '</td><td>' + comstr.theTailNav + '</td><td>' + comstr.theTailAdornment + '</td><td>' + comstr.theTailAsset + '</td></tr>');
};

function appendComponentRequirement(comreq) {
    $("#theRequirements").find("tbody").append('<tr><td class="deleteComponentRequirement"><i class="fa fa-minus"></i></td><td class="component-requirement">'+ comreq + '</td></tr>');
};

function appendComponentGoal(comgoal) {
    $("#theGoals").find("tbody").append('<tr><td class="deleteComponentGoal"><i class="fa fa-minus"></i></td><td class="component-goal">'+ comgoal + '</td></tr>');
};

function appendComponentGoalAssociation(comga) {
    $("#theGoalAssociations").find("tbody").append('<tr><td class="deleteComponentGoalAssociation"><i class="fa fa-minus"></i></td><td class="component-goalassociation">'+ comga.theGoalName + '</td><td>' + comga.theRefType + '</td><td>' + comga.theSubGoalName + '</td><td>' + comga.theRationale + '</td></tr>');
};


mainContent.on("click","#UpdateComponent",function() {

  var comp = JSON.parse($.session.get("Component"));
  comp.theName = $('#theComponentName').val();
  comp.theDescription = $('#theDescription').val();
  var ap = JSON.parse($.session.get("ArchitecturalPattern"));

  if ($("#editComponentDiv").hasClass('new')) {
    ap.theComponents.push(comp);
    $.session.set("ArchitecturalPattern",JSON.stringify(ap));
    appendComponent(comp);
  }
  else {
    var selectedIdx = $('#editComponentDiv').attr('data-selectedIndex');
    ap.theComponents[selectedIdx] = comp;
    $.session.set("ArchitecturalPattern",JSON.stringify(ap));
    $('#theComponents').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(comp.theName);
    $('#theComponents').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(2)').text(comp.theDescription);
  }
  $("#editComponentDiv").hide();
  $("#editArchitecturalPatternOptionsForm").show();
});

mainContent.on("click","#CloseComponent",function(e) {
  e.preventDefault();
  $("#editComponentDiv").hide();
  $("#editArchitecturalPatternOptionsForm").show();
});

mainContent.on("click","#UpdateConnector",function() {
  var conn = {};
  conn.theConnectorName = $('#theConnectorName').val();
  conn.theFromComponent = $('#theFromComponent').val();
  conn.theFromRole = $('#theFromRole').val();
  conn.theFromInterface = $('#theFromInterface').val();
  conn.theToComponent = $('#theToComponent').val();
  conn.theToInterface = $('#theToInterface').val();
  conn.theToRole = $('#theToRole').val();
  conn.theAssetName = $('#theConnectorAssetName').val();
  conn.theProtocol = $('#theProtocol').val();
  conn.theAccessRight = $('#theConnectorAccessRight').val();

  var ap = JSON.parse($.session.get("ArchitecturalPattern"));

  if ($("#editConnectorDiv").hasClass('new')) {
    ap.theConnectors.push(conn);
    $.session.set("ArchitecturalPattern",JSON.stringify(ap));
    appendConnector(conn);
  }
  else {
    var selectedIdx = $('#editConnectorDiv').attr('data-selectedIndex');
    ap.theConnectors[selectedIdx] = conn;
    $.session.set("ArchitecturalPattern",JSON.stringify(ap));
    $('#theConnectors').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(conn.theConnectorName);
    $('#theConnectors').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(2)').text(conn.theFromComponent);
    $('#theConnectors').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(3)').text(conn.theFromRole);
    $('#theConnectors').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(4)').text(conn.theFromInterface);
    $('#theConnectors').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(5)').text(conn.theToComponent);
    $('#theConnectors').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(6)').text(conn.theToInterface);
    $('#theConnectors').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(7)').text(conn.theToRole);
    $('#theConnectors').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(8)').text(conn.theAssetName);
    $('#theConnectors').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(9)').text(conn.theProtocol);
    $('#theConnectors').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(10)').text(conn.theAccessRight);
  }

  $("#editConnectorDiv").hide();
  $("#editArchitecturalPatternOptionsForm").show();
});

mainContent.on("click","#CloseConnector",function() {
  $("#editConnectorDiv").hide();
  $("#editArchitecturalPatternOptionsForm").show();
});

mainContent.on('click', '#CloseArchitecturalPattern', function (e) {
  e.preventDefault();
  clearLocalStorage("architectural_pattern");
  $("#objectViewer").empty();
  $('#menuBCClick').attr('dimension','architectural_pattern');
  refreshMenuBreadCrumb('architectural_pattern');
});




$(document).on('shown.bs.modal','#addComponentInterfaceDialog',function() {
  var selectedInt = $('#addComponentInterfaceDialog').attr('data-selectedInterface');
  if (selectedInt != undefined) {
    selectedInt = JSON.parse(selectedInt);
    $('#AddComponentInterface').text('Update');
    $('#theInterfaceName').val(selectedInt.theName);
    $('#theInterfaceType').val(selectedInt.theType);
  }
  else {
    $('#theInterfaceName').val('');
    $('#theInterfaceType').val('');
    $('#AddComponentInterface').text('Add');
  }

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/access_right",
    success: function (accessRights) {
      $("#theAccessRight option").remove();
      $.each(accessRights,function(idx,accessRight) {
        $('#theAccessRight').append($("<option></option>").attr("value",accessRight).text(accessRight));
      });
      if (selectedInt != undefined) {
        $('#theAccessRight').val(selectedInt.theAccessRight);
      }
      else {
        $('#theAccessRight').val('');
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/privilege",
    success: function (privileges) {
      $("#thePrivilege option").remove();
      $.each(privileges,function(idx,privilege) {
        $('#thePrivilege').append($("<option></option>").attr("value",privilege).text(privilege));
      });
      if (selectedInt != undefined) {
        $('#thePrivilege').val(selectedInt.thePrivilege);
      }
      else {
        $('#thePrivilege').val('');
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

mainContent.on('click','#addComponentInterface',function() {
  $('#addComponentInterfaceDialog').removeAttr('data-selectedInterface');
  $('#addComponentInterfaceDialog').removeAttr('data-selectedIndex');
  $('#addComponentInterfaceDialog').modal('show');
});


mainContent.on('click','td.component-interface',function(){
  var intRow = $(this).closest("tr");
  var selectedInt = {};
  selectedInt.theName = intRow.find("td:eq(1)").text();
  selectedInt.theType = intRow.find("td:eq(2)").text();
  selectedInt.theAccessRight = intRow.find("td:eq(3)").text();
  selectedInt.thePrivilege = intRow.find("td:eq(4)").text();

  $('#addComponentInterfaceDialog').attr('data-selectedInterface',JSON.stringify(selectedInt));
  $('#addComponentInterfaceDialog').attr('data-selectedIndex',intRow.index());
  $('#addComponentInterfaceDialog').modal('show');
});

mainContent.on('click','#AddComponentInterface',function() {
  var selectedInt = {};
  selectedInt.theName = $('#theInterfaceName').val();
  selectedInt.theType = $('#theInterfaceType').val();
  selectedInt.theAccessRight = $('#theAccessRight').val();
  selectedInt.thePrivilege = $('#thePrivilege').val();
  
  var comp = JSON.parse($.session.get("Component"));
  var selectedIdx = $('#addComponentInterfaceDialog').attr('data-selectedIndex');
  if (selectedIdx != undefined) {
    comp.theInterfaces[selectedIdx] = selectedInt;
    $.session.set("Component", JSON.stringify(comp));
    $('#theInterfaces').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(selectedInt.theName);
    $('#theInterfaces').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(2)').text(selectedInt.theType);
    $('#theInterfaces').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(3)').text(selectedInt.theAccessRight);
    $('#theInterfaces').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(4)').text(selectedInt.thePrivilege);
  }
  else {
    comp.theInterfaces.push(selectedInt);
    $.session.set("Component", JSON.stringify(comp));
    appendComponentInterface(selectedInt);
  }
  $('#addComponentInterfaceDialog').modal('hide');
});

mainContent.on('click','#addComponentStructure',function() {
  $('#addComponentStructureDialog').removeAttr('data-selectedStructure');
  $('#addComponentStructureDialog').removeAttr('data-selectedIndex');
  $('#addComponentStructureDialog').modal('show');
});

mainContent.on('click','td.component-structure',function(){
  var strRow = $(this).closest("tr");
  var selectedStr = {};
  selectedStr.theHeadAsset = strRow.find("td:eq(1)").text();
  selectedStr.theHeadAdornment = strRow.find("td:eq(2)").text();
  selectedStr.theHeadNav = strRow.find("td:eq(3)").text();
  selectedStr.theHeadNry = strRow.find("td:eq(4)").text();
  selectedStr.theHeadRole = strRow.find("td:eq(5)").text();
  selectedStr.theTailRole = strRow.find("td:eq(6)").text();
  selectedStr.theTailNry = strRow.find("td:eq(7)").text();
  selectedStr.theTailNav = strRow.find("td:eq(8)").text();
  selectedStr.theTailAdornment = strRow.find("td:eq(9)").text();
  selectedStr.theTailAsset = strRow.find("td:eq(10)").text();

  $('#addComponentStructureDialog').attr('data-selectedStructure',JSON.stringify(selectedStr));
  $('#addComponentStructureDialog').attr('data-selectedIndex',strRow.index());
  $('#addComponentStructureDialog').modal('show');
});

$(document).on('shown.bs.modal','#addComponentStructureDialog',function() {
  var selectedStr = $('#addComponentStructureDialog').attr('data-selectedStructure');
  if (selectedStr != undefined) {
    selectedStr = JSON.parse(selectedStr);
    $('#headAdorn').val(selectedStr.theHeadAdornment);
    $('#headNav').val(selectedStr.theHeadNav);
    $('#headNry').val(selectedStr.theHeadNry);
    $('#headRole').val(selectedStr.theHeadRole);
    $('#tailRole').val(selectedStr.theTailRole);
    $('#tailNry').val(selectedStr.theTailNry);
    $('#tailNav').val(selectedStr.theTailNav);
    $('#tailAdorn').val(selectedStr.theTailAdornment);
    $('#AddComponentStructure').text('Update');
  }
  else {
    $('#headAdorn').val('Association');
    $('#headNav').val('0');
    $('#headNry').val('*');
    $('#headRole').val('');
    $('#tailRole').val('');
    $('#tailNry').val('*');
    $('#tailNav').val('0');
    $('#tailAdorn').val('Association');
    $('#AddComponentStructure').text('Add');
  }

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/template_asset",
    success: function (assets) {
      $("#headAsset option").remove();
      $("#tailAsset option").remove();
      $.each(assets,function(idx,asset) {
        $('#headAsset').append($("<option></option>").attr("value",asset).text(asset));
        $('#tailAsset').append($("<option></option>").attr("value",asset).text(asset));
      });
      if (selectedStr != undefined) {
        $('#headAsset').val(selectedStr.theHeadAsset);
        $('#tailAsset').val(selectedStr.theTailAsset);
      }
      else {
        $('#headAsset').val('');
        $('#tailAsset').val('');
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

mainContent.on('click','#AddComponentStructure',function() {
  var selectedStr = {};
  selectedStr.theHeadAsset = $('#headAsset').val();
  selectedStr.theHeadAdornment = $('#headAdorn').val();
  selectedStr.theHeadNav = $('#headNav').val();
  selectedStr.theHeadNry = $('#headNry').val();
  selectedStr.theHeadRole = $('#headRole').val();
  selectedStr.theTailRole = $('#tailRole').val();
  selectedStr.theTailNry = $('#tailNry').val();
  selectedStr.theTailNav = $('#tailNav').val();
  selectedStr.theTailAdornment = $('#tailAdorn').val();
  selectedStr.theTailAsset = $('#tailAsset').val();

  
  var comp = JSON.parse($.session.get("Component"));
  var selectedIdx = $('#addComponentStructureDialog').attr('data-selectedIndex');
  if (selectedIdx != undefined) {
    comp.theStructure[selectedIdx] = selectedStr;
    $.session.set("Component", JSON.stringify(comp));
    $('#theStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(selectedStr.theHeadAsset);
    $('#theStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(2)').text(selectedStr.theHeadAdornment);
    $('#theStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(3)').text(selectedStr.theHeadNav);
    $('#theStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(4)').text(selectedStr.theHeadNry);
    $('#theStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(5)').text(selectedStr.theHeadRole);
    $('#theStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(6)').text(selectedStr.theTailRole);
    $('#theStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(7)').text(selectedStr.theTailNry);
    $('#theStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(8)').text(selectedStr.theTailNav);
    $('#theStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(9)').text(selectedStr.theTailAdornment);
    $('#theStructure').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(10)').text(selectedStr.theTailAsset);
  }
  else {
    comp.theStructure.push(selectedStr);
    $.session.set("Component", JSON.stringify(comp));
    appendComponentStructure(selectedStr);
  }
  $('#addComponentStructureDialog').modal('hide');
});

mainContent.on('click','td.deleteComponent',function() {
  var compRow = $(this).closest("tr");
  var rowIdx = compRow.index();
  compRow.remove();
  var ap = JSON.parse($.session.get("ArchitecturalPattern"));
  ap.theComponents.splice(rowIdx,1);
  $.session.set("ArchitecturalPattern", JSON.stringify(ap));
});

mainContent.on('click','td.deleteConnector',function() {
  var connRow = $(this).closest("tr");
  var rowIdx = connRow.index();
  connRow.remove();
  var ap = JSON.parse($.session.get("ArchitecturalPattern"));
  ap.theConnectors.splice(rowIdx,1);
  $.session.set("ArchitecturalPattern", JSON.stringify(ap));
});

mainContent.on('click','td.deleteComponentStructure',function() {
  var strRow = $(this).closest("tr");
  var rowIdx = strRow.index();
  strRow.remove();
  var comp = JSON.parse($.session.get("Component"));
  comp.theStructure.splice(rowIdx,1);
  $.session.set("Component", JSON.stringify(comp));
});

mainContent.on('click','td.deleteComponentInterface',function() {
  var intRow = $(this).closest("tr");
  var rowIdx = intRow.index();
  intRow.remove();
  var comp = JSON.parse($.session.get("Component"));
  comp.theInterfaces.splice(rowIdx,1);
  $.session.set("Component", JSON.stringify(comp));
});

mainContent.on('click','#addComponentGoal',function() {
  $('#addComponentGoalDialog').modal('show');
});

$(document).on('shown.bs.modal','#addComponentGoalDialog',function() {
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/template_goal",
    success: function (goals) {
      $("#theComponentGoal option").remove();
      var comp = JSON.parse($.session.get("Component"));
      $.each(goals,function(idx,goal) {
        if (comp.theGoals.indexOf(goal) == -1) {
          $('#theComponentGoal').append($("<option></option>").attr("value",goal).text(goal));
        }
      });
      $('#theComponentGoal').val('');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

mainContent.on('click','#AddComponentGoal',function() {
  var goalName = $('#theComponentGoal').val();
  var comp = JSON.parse($.session.get("Component"));
  comp.theGoals.push(goalName);
  $.session.set("Component", JSON.stringify(comp));
  appendComponentGoal(goalName);
  $('#addComponentGoalDialog').modal('hide');
});

mainContent.on('click','td.deleteComponentGoal',function() {
  var goalRow = $(this).closest("tr");
  var rowIdx = goalRow.index();
  goalRow.remove();
  var comp = JSON.parse($.session.get("Component"));
  comp.theGoals.splice(rowIdx,1);
  $.session.set("Component", JSON.stringify(comp));
});


mainContent.on('click','#addComponentRequirement',function() {
  $('#addComponentRequirementDialog').modal('show');
});

$(document).on('shown.bs.modal','#addComponentRequirementDialog',function() {
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/dimensions/table/template_requirement",
    success: function (reqs) {
      $("#theComponentRequirement option").remove();
      var comp = JSON.parse($.session.get("Component"));
      $.each(reqs,function(idx,req) {
        if (comp.theRequirements.indexOf(req) == -1) {
          $('#theComponentRequirement').append($("<option></option>").attr("value",req).text(req));
        }
      });
      $('#theComponentRequirement').val('');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

mainContent.on('click','#AddComponentRequirement',function() {
  var reqName = $('#theComponentRequirement').val();
  var comp = JSON.parse($.session.get("Component"));
  comp.theRequirements.push(reqName);
  $.session.set("Component", JSON.stringify(comp));
  appendComponentRequirement(reqName);
  $('#addComponentRequirementDialog').modal('hide');
});

mainContent.on('click','td.deleteComponentRequirement',function() {
  var reqRow = $(this).closest("tr");
  var rowIdx = reqRow.index();
  reqRow.remove();
  var comp = JSON.parse($.session.get("Component"));
  comp.theRequirements.splice(rowIdx,1);
  $.session.set("Component", JSON.stringify(comp));
});

mainContent.on('click','#addComponentGoalAssociation',function() {
  $('#addComponentGoalAssociationDialog').removeAttr('data-selectedGa');
  $('#addComponentGoalAssociationDialog').removeAttr('data-selectedIndex');
  $('#addComponentGoalAssociationDialog').modal('show');
});

mainContent.on('click','td.component-goalassociation',function(){
  var gaRow = $(this).closest("tr");
  var ga = {};
  ga.theGoalName = gaRow.find("td:eq(1)").text();
  ga.theRefType = gaRow.find("td:eq(2)").text();
  ga.theSubGoalName = gaRow.find("td:eq(3)").text();
  ga.theRationale = gaRow.find("td:eq(4)").text();

  $('#addComponentGoalAssociationDialog').attr('data-selectedGa',JSON.stringify(ga));
  $('#addComponentGoalAssociationDialog').attr('data-selectedIndex',gaRow.index());
  $('#addComponentGoalAssociationDialog').modal('show');
});

$(document).on('shown.bs.modal','#addComponentGoalAssociationDialog',function() {
  var selectedGa = $('#addComponentGoalAssociationDialog').attr('data-selectedGa');
  var comp = JSON.parse($.session.get("Component"));
  $("#theGoalName option").remove();
  $("#theSubGoalName option").remove();
  $.each(comp.theGoals,function(idx,goal) {
    $('#theGoalName').append($("<option></option>").attr("value",goal).text(goal));
    $('#theSubGoalName').append($("<option></option>").attr("value",goal).text(goal));
  });
  if (selectedGa != undefined) {
    var ga = JSON.parse(selectedGa);
    $('#theGoalName').val(ga.theGoalName);
    $('#theSubGoalName').val(ga.theSubGoalName);
    $('#theRefType').val(ga.theRefType);
    $('#theRationale').val(ga.theRationale);
  }
  else {
    $('#theGoalName').val('');
    $('#theSubGoalName').val('');
    $('#theRefType').val('and');
    $('#theRationale').val('');

  }
});


mainContent.on('click','#AddComponentGoalAssociation',function() {
  var ga = {};
  ga.theGoalName = $('#theGoalName').val();
  ga.theSubGoalName = $('#theSubGoalName').val();
  ga.theRefType = $('#theRefType').val();
  ga.theRationale = $('#theRationale').val();
  var comp = JSON.parse($.session.get("Component"));

  var selectedIdx = $('#addComponentGoalAssociationDialog').attr('data-selectedIndex');
  if (selectedIdx != undefined) {
    comp.theGoalAssociations[selectedIdx] = ga;
    $('#theGoalAssociations').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(1)').text(ga.theGoalName);
    $('#theGoalAssociations').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(2)').text(ga.theRefType);
    $('#theGoalAssociations').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(3)').text(ga.theSubGoalName);
    $('#theGoalAssociations').find("tbody").find('tr:eq(' + selectedIdx + ')').find('td:eq(4)').text(ga.theRationale);
  }
  else {
    comp.theGoalAssociations.push(ga);
    appendComponentGoalAssociation(ga);
  }
  $.session.set("Component", JSON.stringify(comp));
  $('#addComponentGoalAssociationDialog').modal('hide');
});


mainContent.on('click','td.deleteComponentGoalAssociation',function() {
  var gaRow = $(this).closest("tr");
  var rowIdx = gaRow.index();
  gaRow.remove();
  var comp = JSON.parse($.session.get("Component"));
  comp.theGoalAssociations.splice(rowIdx,1);
  $.session.set("Component", JSON.stringify(comp));
});


function viewWeaknessAnalysis() {
  var apName = $('#chooseEnvironment').attr('data-apName');
  var envName = $('#chooseEnvironmentSelect').val();

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/architectural_patterns/name/" + encodeURIComponent(apName) + '/environment/' + encodeURIComponent(envName) + '/weakness_analysis',
    success: function (data) {
      $('#theWeaknessAnalysisVulnerabilities').find('tbody').empty();
      $.each(data.theVulnerabilityWeaknesses,function(key,item) {
        $("#theWeaknessAnalysisVulnerabilities").find("tbody").append('<tr><td>'+ item.theTargetName +'</td><td>' + item.theComponents+ '</td><td>' + item.theAssets + '</td></tr>');
      });

      $('#theWeaknessAnalysisThreats').find('tbody').empty();
      $.each(data.theThreatWeaknesses,function(key,item) {
        $("#theWeaknessAnalysisThreats").find("tbody").append('<tr><td>'+ item.theTargetName +'</td><td>' + item.theComponents+ '</td><td>' + item.theAssets + '</td></tr>');
      });

      $('#theWeaknessAnalysisPersonaImpact').find('tbody').empty();
      $.each(data.thePersonaImpact,function(key,item) {
        $("#theWeaknessAnalysisPersonaImpact").find("tbody").append('<tr><td>'+ item.thePersonaName +'</td><td>' + item.theImpactScore+ '</td></tr>');
      });

      $('#theWeaknessAnalysisObstacles').find('tbody').empty();
      $.each(data.theCandidateGoals,function(key,item) {
        $("#theWeaknessAnalysisObstacles").find("tbody").append('<tr><td>'+ item.theObstacleName +'</td><td>' + item.theGoalName+ '</td></tr>');
      });

      $('#weaknessAnalysisDialog').modal('show');
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

$("#weaknessAnalysisDialog").on('click', '#situateArchitecturalPatternButton',function(e) {
  var apName = $('#chooseEnvironment').attr('data-apName');
  var envName = $('#chooseEnvironmentSelect').val();

  $.ajax({
    type: "POST",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    processData: false,
    url: serverIP + "/api/architectural_patterns/name/" + encodeURIComponent(apName) + '/environment/' + encodeURIComponent(envName) + '/situate',
    success: function (data) {
      $('#weaknessAnalysisDialog').modal('hide');
      showPopup(true);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });


});

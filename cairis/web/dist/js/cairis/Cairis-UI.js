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

'use strict';

$(window).on('load', function(){

  resizable();
  makeHorizontalScrollbar();

  //slimscroll for the nav
  $('#sidebar-scrolling').slimScroll({
    height: $('.main-sidebar').height() - 20
    //height: $('.main-sidebar').height(),
    //alert("slimscroll Done")
  });

  var mainh = $(".main-header");
  var footh = $(".main-footer");
  //slimscroll for the content
  $('#maincontent').slimScroll({
    height: $('.content-wrapper').outerHeight() - (mainh.height() + footh.height())
  });


  // console.log("Header:" + mainh.height()+ ", Footer: " + footh.height())
  //For the gear, making it retractable
  $('#rightnavGear').click(function(){
    toggleOptions();
  });
  $(".imgwrapper").hover(function(){

    var p = $(this).find("p");
    $("#inform").text(p.text());

  });
  activeElement("mainTable");

});

function activeElement(elementid){
  if(elementid == "svgViewer" || elementid == 'homePanel'){
    $("#mainTable").hide();
    $("#objectViewer").hide();
    $("#filterrequirementscontent").hide();
    $("#filtersummarytables").hide();
    $("#filterassetmodelcontent").hide();
    $("#filterriskmodelcontent").hide();
    $("#filterresponsibilitymodelcontent").hide();
    $("#filtergoalmodelcontent").hide();
    $("#filterapmodelcontent").hide();
    $("#filtertaskmodelcontent").hide();
    $("#filterobstaclemodelcontent").hide();
    $("#filterconceptmapmodelcontent").hide();
    $("#filterarchitecturalpatternmodelcontent").hide();
    $("#filtermisusabilitymodelcontent").hide();
    $("#filterdfdcontent").hide();
    $("#rightnavGear").hide();

    if (elementid == 'svgViewer') {
      $('#homePanel').hide();
      $("#rightnavGear").show();
    }


    if (window.theVisualModel == 'risk') {
      $("#filterriskmodelcontent").show();
    }
    if (window.theVisualModel == 'requirement') {
      $("#filterconceptmapmodelcontent").show();
    }
    else if (window.theVisualModel == 'goal') {
      $("#filtergoalmodelcontent").show();
    }
    else if (window.theVisualModel == 'obstacle') {
      $("#filterobstaclemodelcontent").show();
    }
    else if (window.theVisualModel == 'task') {
      $("#filtertaskmodelcontent").show();
    }
    else if (window.theVisualModel == 'responsibility') {
      $("#filterresponsibilitymodelcontent").show();
    }
    else if (window.theVisualModel == 'asset') {
      $("#filterassetmodelcontent").show();
    }
    else if (window.theVisualModel == 'persona') {
      $("#filterapmodelcontent").show();
    }
    else if (window.theVisualModel == 'architectural_pattern') {
      $("#filterarchitecturalpatternmodelcontent").show();
    }
    else if (window.theVisualModel == 'misusability') {
      $("#filtermisusabilitymodelcontent").show();
    }
    else if (window.theVisualModel == 'dataflow') {
      $("#filterdfdcontent").show();
    }
  }
  if(elementid != "svgViewer"){
    $("#svgViewer").hide();
    $('#homePanel').hide();
    $("#filtersummarytables").hide();
    $("#objectViewer").hide();
    $("#filterassetmodelcontent").hide();
    $("#filterriskmodelcontent").hide();
    $("#filtergoalmodelcontent").hide();
    $("#filtertaskmodelcontent").hide();
    $("#filterapmodelcontent").hide();
    $("#filterresponsibilitymodelcontent").hide();
    $("#filterobstaclemodelcontent").hide();
    $("#filterconceptmapmodelcontent").hide();
    $("#filterarchitecturalpatternmodelcontent").hide();
    $("#filtermisusabilitymodelcontent").hide();
    $("#filterdfdcontent").hide();
    $("#rightnavGear").hide();
  }

  if(elementid == "mainTable"){
    //If it is the table, we need to see which table it is
    window.theVisualModel = 'None';
    $("#filterrequirementscontent").hide();
  }
  if(elementid == "reqTable"){
    //If it is the table, we need to see which table it is
    window.theVisualModel = 'None';
    $("#filterrequirementscontent").show();
    elementid = 'mainTable'
  }

  if (elementid == 'objectViewer') {
    $("#mainTable").hide();
  }

  if (elementid == 'homePanel') {
    $("#mainTable").hide();
    $("#filtersummarytables").show();
  }

  elementid = "#" + elementid;
  $(elementid).show();
}

$( window ).resize(function() {
  resizable();
});

// Closing the options menu when a new controller is chosen
$(".messages-menu").click(function () {
 forceCloseOptions();
});

// Created for the scrollbar on the top navbar
function makeHorizontalScrollbar() {
  $(".navbar-custom-menu").mCustomScrollbar({
    axis: "x",
    scrollbarPosition: "inside",
    advanced:{ autoExpandHorizontalScroll: true }
    // setWidth: false
  });
}

// For opening the right options menu
function toggleOptions(){
  var navGear = $('#rightnavGear');
  var navMenu = $('#rightnavMenu');
  if (!navGear.hasClass("open")) {
    navGear.animate({"right": "400px"});
    navMenu.animate({"right": "0"});
    navGear.addClass("open");
  } else {
    navGear.animate({"right": "0"});
    navMenu.animate({"right": "-400px"});
    navGear.removeClass("open");
  }
}

// For forcing opening the right options menu
function forceOpenOptions(){
  var navGear = $('#rightnavGear');
  var navMenu = $('#rightnavMenu');
  if (!navGear.hasClass("open")) {
    navGear.animate({"right": "400px"});
    navMenu.animate({"right": "0"});
    navGear.addClass("open");
  }
}

// For opening the right options menu
function forceCloseOptions(){
  var navGear = $('#rightnavGear');
  var navMenu = $('#rightnavMenu');
  navGear.animate({"right": "0"});
  navMenu.animate({"right": "-400px"});
  navGear.removeClass("open");
}

// for rescaling an image
function rescaleImage(image, maxWidth){
  var theImage = new Image();
  theImage.src = image.attr("src");

  var imageWidth = theImage.width;
  var imageHeight = theImage.height;

  var resizeNumber = imageWidth/maxWidth;
  imageHeight = imageHeight/resizeNumber;
  image.attr("width",maxWidth);
  image.attr("height", imageHeight);
}

// Created for the top navbar, which in AdminLTE didn't stick on top.
function resizable() {

  var collapser = $('.sidebar-toggle').outerWidth();
  var docWidth = $(document).width();
  //Was 770
  if ($(window).width() > 0) {
    var logo = $('.logo').outerWidth();
    //If logo takes whole screen
    if (logo > 230) {
      // console.log("logo to big")
      $('.navbar-custom-menu').width(docWidth - (collapser));
    } else {
      $('.navbar-custom-menu').outerWidth(docWidth - (logo + collapser + 20));

      var actwidth = (docWidth - (logo + collapser - 7));
      $("ul.nav.navbar-nav").css("float", "right")
    }
  }
}

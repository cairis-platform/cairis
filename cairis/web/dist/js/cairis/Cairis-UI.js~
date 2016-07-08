/**
 * Created by Raf on 24/04/2015.
 */


$(window).load(function(){

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
    activeElement("reqTable");

});

$( window ).resize(function() {
    resizable();
});

/*
Closing the options menu when a new controller is chosen
 */
$(".messages-menu").click(function () {
   forceCloseOptions();
});

/*
 Created for the scrollbar on the top navbar
 */
function makeHorizontalScrollbar() {
    $(".navbar-custom-menu").mCustomScrollbar({
        axis: "x",
        scrollbarPosition: "inside",
        advanced:{ autoExpandHorizontalScroll: true }
        // setWidth: false
    });
}
/*
For opening the right options menu
 */
function toggleOptions(){
    var navGear = $('#rightnavGear');
    var navMenu = $('#rightnavMenu');
    if (!navGear.hasClass("open")) {
        navGear.animate({"right": "500px"});
        navMenu.animate({"right": "0"});
        navGear.addClass("open");
    } else {
        navGear.animate({"right": "0"});
        navMenu.animate({"right": "-500px"});
        navGear.removeClass("open");
    }
}
/*
 For forcing opening the right options menu
 */
function forceOpenOptions(){
    var navGear = $('#rightnavGear');
    var navMenu = $('#rightnavMenu');
    if (!navGear.hasClass("open")) {
        navGear.animate({"right": "500px"});
        navMenu.animate({"right": "0"});
        navGear.addClass("open");
    }
}
/*
 For opening the right options menu
 */
function forceCloseOptions(){
    var navGear = $('#rightnavGear');
    var navMenu = $('#rightnavMenu');
        navGear.animate({"right": "0"});
        navMenu.animate({"right": "-500px"});
        navGear.removeClass("open");
}
/*
for rescaling an image
 */
function resaleImage(image, maxWidth){
    var theImage = new Image();
    theImage.src = image.attr("src");

    var imageWidth = theImage.width;
    var imageHeight = theImage.height;

    var resizeNumber = imageWidth/maxWidth;
    imageHeight = imageHeight/resizeNumber;
    image.attr("width",maxWidth);
    image.attr("height", imageHeight);
}

/*
 Created for the top navbar, which in AdminLTE didn't stick on top.
 */
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
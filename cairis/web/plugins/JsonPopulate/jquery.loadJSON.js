/*
* File:        jquery.loadJSON.js
* Version:     1.0.0.
* Author:      Jovan Popovic 
* 
* Copyright 2011 Jovan Popovic, all rights reserved.
*
* This source file is free software, under either the GPL v2 license or a
* BSD style license, as supplied with this software.
* 
* This source file is distributed in the hope that it will be useful, but 
* WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
* or FITNESS FOR A PARTICULAR PURPOSE. 
*
* This file contains implementation of the JQuery templating engine that load JSON
* objects into the HTML code. It is based on Alexandre Caprais notemplate plugin 
* with several enchancements that are added to this plugin.
*/
/*
If edited this file, so it's not the same as the source. Raf Vandelaer
 */

(function ($) {
    $.fn.loadJSON = function (obj, options) {

        function setElementValue(element, value, name) {
            //var type = element.type || element.tagName;
            var type = $(element).prop("tagName");
            if(type.toLowerCase() == "input" || typeof  type  == 'undefined' ){
                type = $(element).attr('type').toLowerCase();
            }
            if (type == null) {
                return;
            }
           /* if(String(type) == "checkbox"){
                console.log("test");
            }*/
            type = type.toLowerCase();
            switch (type) {

                case 'radio':
                    if (value.toString().toLowerCase() == element.value.toLowerCase())
                        $(element).attr("checked", "checked");
                    break;

                case 'checkbox':
                    if (value)
                        $(element).attr("checked", "checked");
                    break;

                case 'select-multiple':
                    var values = value.constructor == Array ? value : [value];
                    for (var i = 0; i < element.options.length; i++) {
                        for (var j = 0; j < values.length; j++) {
                            element.options[i].selected |= element.options[i].value == values[j];
                        }
                    }
                    break;

                case 'select':
                    //$("element").val(value);
                    $(element).find("option").each(function() {
                        //alert(this.text + ' ' + this.value);
                       // var $this = $(this);
                        if($(this)[0].label == value){
                            $(this)[0].setAttribute('selected', "selected");
                        }
                    });
                    break;
                case 'input':
                    $(element).attr("innerText", value);
                    break;
                case 'select-one':
                case 'text':
                case 'hidden':
                    $(element).attr("value", value);
                    break;
                case 'a':
                    var href = $(element).attr("href");
                    var iPosition = href.indexOf('?');
                    if (iPosition > 0) // if parameters in the URL exists add new pair using &
                        href = href.substring(0, iPosition) + '?' + name + '=' + value;
                    else//otherwise attach pair to URL
                        href = href + '?' + name + '=' + value;
                    $(element).attr("href", href);
                    break;
                case 'img': //Assumption is that value is in the HREF$ALT format
                    var iPosition = value.indexOf('$');
                    var src = "";
                    var alt = "";
                    if (iPosition > 0) {
                        src = value.substring(0, iPosition);
                        alt = value.substring(iPosition + 1);
                    }
                    else {
                        src = value;
                        var iPositionStart = value.lastIndexOf('/')+1;
                        var iPositionEnd = value.indexOf('.');
                        alt = value.substring(iPositionStart, iPositionEnd);
                    }
                    $(element).attr("src", src);
                    $(element).attr("alt", alt);
                    break;

                case 'textarea':
                case 'submit':
                case 'label':
                case 'button':
                default:
                    try {
                        $(element).html(value);
                    } catch (exc) { }
            }

        }

        function browseJSON(obj, element, name) {

            // no object
            if (obj == undefined) {
            }
            // branch
            else if (obj.constructor == Object) {
                for (var prop in obj) {
                    if (prop == null)
                        continue;
                    //Find an element with class, id, name, or rel attribute that matches the propertu name
                    var child = jQuery.makeArray(jQuery("." + prop, element)).length > 0 ? jQuery("." + prop, element) :
                                                    jQuery("#" + prop, element).length > 0 ? jQuery("#" + prop, element) :
                                                    jQuery('[name="' + prop + '"]', element).length > 0 ? jQuery('[name="' + prop + '"]', element) : jQuery('[rel="' + prop + '"]');
                    if (child.length != 0)
                        browseJSON(obj[prop], jQuery(child, element), prop);
                }
            }
            // array
            else if (obj.constructor == Array) {
                if (element.length > 0 && element[0].tagName == "SELECT") {
                    setElementValue(element[0], obj, name);
                } else {
                    var arr = jQuery.makeArray(element);
                    //how many duplicate
                    var nbToCreate = obj.length - arr.length;
                    var i = 0;
                    for (iExist = 0; iExist < arr.length; iExist++) {
                        if (i < obj.length) {
                            $(element).eq(iExist).loadJSON(obj[i]);
                        }
                        i++;
                    }
                    //fill started by last
                    i = obj.length - 1;
                    for (iCreate = 0; iCreate < nbToCreate; iCreate++) {
                        //duplicate the last
                        $(arr[arr.length - 1]).clone(true).insertAfter(arr[arr.length - 1]).loadJSON(obj[i]);
                        i--;
                    }
                }
            }
            // data only
            else {
                var value = obj;
                var type;
                if (element.length > 0) {
                    for (i = 0; i < element.length; i++)
                        setElementValue(element[i], obj, name);
                }
                else {
                    setElementValue(element, obj, name);
                }
            }
        } //function browseJSON end

        var defaults = {
        };

        properties = $.extend(defaults, options);

        return this.each(function () {

            if (obj.constructor == String) {
                var element = $(this);
                $.get(obj, function (data) {
                    element.loadJSON(data);
                });
            }

            else {
                browseJSON(obj, this);
            }
        });

    };

})(jQuery);
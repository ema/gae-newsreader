/*
 * jQuery "Lynx-like" Keyboard Navigation Plugin 
 */

(function($) {
    $.fn.lynxnav = function (options) {
        var defaults = {
            onClass:  'lynxNavOn',
            offClass: 'lynxNavOff'
        }

        var options =  $.extend(defaults, options);
        
        this.each(function() {
            var onClass = options.onClass;
            var offClass = options.offClass;

            // XXX: not very object oriented :)
            var maxId = 0;

            var getSelectedId = function() {
                var selected = $("." + onClass)[0];
                return parseInt($(selected).attr('id'));
            }

            var setSelectedId = function(oldId, newId) {
                console.log(oldId + " -> " + newId);

                var oldElem = $("#" + oldId);
                var newElem = $("#" + newId);

                $(oldElem).removeClass(onClass);
                $(oldElem).addClass(offClass);

                $(newElem).removeClass(offClass);
                $(newElem).addClass(onClass);
            }

            var goUp = function(sel) {
                if (sel > 0)
                    setSelectedId(sel, sel - 1);
            }

            var goDown = function(sel) {
                console.log("max: " + maxId);

                if (sel < maxId) 
                    setSelectedId(sel, sel + 1);
            }

            var goBack = function(sel) {
                console.log("goBack");
            }

            var goForward = function(sel) {
                console.log("goForward");
            }

            var activate = function(sel) {
                var selectedElem = $("#" + sel);
                window.location.href = selectedElem.attr('href');
            }

            var init = function() {
                $("a, input").each(function(idx, elem) {
                    $(elem).attr('id', idx);

                    if (idx === 0) 
                        $(elem).addClass(onClass);
                    else 
                        $(elem).addClass(offClass);

                    maxId = idx;
                });

                $(document).keydown(function(e) {
                    var key = 0;
                    if (e == null) 
                        key = event.keyCode;
                    else  
                        // mozilla
                        key = e.which;

                    var sel = getSelectedId();

                    switch(key) {
                        case 37: 
                          goBack(sel);
                          break;
                        case 38: 
                          goUp(sel);
                          break;
                        case 39: 
                          goForward(sel);
                          break;
                        case 40: 
                          goDown(sel);
                          break;
                        case 13: 
                          activate(sel);
                          break;
                    }

                    if ((sel % 5) != 0)
                        // XXX ugly !
                        return false;
                });
            }

            init();
        });

        return this;
    }
})(jQuery);

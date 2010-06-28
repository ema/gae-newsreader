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
                var oldElem = $("#" + oldId);
                var newElem = $("#" + newId);

                $(oldElem).removeClass(onClass);
                $(oldElem).addClass(offClass);

                $(newElem).removeClass(offClass);
                $(newElem).addClass(onClass);

                if ($(newElem).attr("type") == "text") 
                    $(newElem).focus();
            }

            var goUp = function(sel) {
                if (sel > 0)
                    setSelectedId(sel, sel - 1);
            }

            var goDown = function(sel) {
                if (sel < maxId) 
                    setSelectedId(sel, sel + 1);
            }

            var goBack = function(sel) {
                history.back();
            }

            var goForward = function(sel) {
                var selectedElem = $("#" + sel);
                window.location.href = $(selectedElem).attr('href');
                return false;
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
                          return goForward(sel);
                          break;
                        case 40: 
                          goDown(sel);
                          break;
                        case 13: 
                          if ($("#" + sel).attr('type') != "text")
                              return goForward(sel);
                          break;
                    }
                });
            }

            init();
        });

        return this;
    }
})(jQuery);

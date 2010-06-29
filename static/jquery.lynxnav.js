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
        
        var onClass = options.onClass;
        var offClass = options.offClass;

        // to keep track of the number of links and input elements
        var maxId = 0;

        var getSelectedElem = function() {
            return $("." + onClass)[0];
        };

        var getSelectedId = function() {
            var selected = getSelectedElem();
            return parseInt($(selected).attr('id'));
        };

        var setSelectedId = function(oldId, newId) {
            var oldElem = $("#" + oldId);
            var newElem = $("#" + newId);

            $(oldElem).removeClass(onClass);
            $(oldElem).addClass(offClass);

            $(newElem).removeClass(offClass);
            $(newElem).addClass(onClass);

            if ($(newElem).attr("type") === "text")
                $(newElem).focus();
        };

        var goUp = function(sel) {
            if (sel > 0)
                setSelectedId(sel, sel - 1);
        };

        var goDown = function(sel) {
            if (sel < maxId)
                setSelectedId(sel, sel + 1);
        };

        var goBack = function(sel) {
            history.back();
        };

        var goForward = function(sel) {
            var selectedElem = $("#" + sel);
            window.location.href = $(selectedElem).attr('href');
            return false;
        };

        var scrollWindow = function() {
            /* window scrolling */
            var position = $(getSelectedElem()).offset();
            var curHeight = $(window).height();
            if (parseInt(position['top']) > parseInt(curHeight)) {
                $('html, body').animate({
                    scrollTop: position['top']
                }, 500);
            }

            return false;
        }

        // main code
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
                  return scrollWindow();
                  break;
                case 39:
                  return goForward(sel);
                  break;
                case 40:
                  goDown(sel);
                  return scrollWindow();
                  break;
                case 13:
                  if ($("#" + sel).attr('type') != "text")
                      return goForward(sel);
                  break;
            }
        });

        return this;
    }
})(jQuery);

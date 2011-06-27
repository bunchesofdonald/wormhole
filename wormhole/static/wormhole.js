;(function ($) {
    // Setup csrf cookie.
    $(document).ajaxSend(
        function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                    // or any other URL that isn't scheme relative or absolute i.e relative.
                    !(/^(\/\/|http:|https:).*/.test(url));
        }
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });

    function Wormhole() {
        var _this = this;

        // These functions handle transport success/error. A
        // transport error occurs when the server cannot be reached,
        // or returns an error code. Transport success may still
        // carry an application error.
        function handleTransportSuccess(userCallback, result) { 
            userCallback(result);
        };

        function handleTransportError(fn, name, args, userCallback, xmlHttpRequest) {
            // Call again in 10ms.
            setTimeout(10, fn(name, args, userCallback));
        };

        function createWormholeCall(name, args) { 
            return { 'name' : name, 
                'args' : JSON.stringify(args) }
        }
        
        // Make a wormhole call and setup success and error handlers.
        this.wormhole_call = function(name, args, cb, url) {
            $.ajax({ type    : "POST",
                   url     : url,
                   success : function(r) { return handleTransportSuccess(cb, r); },
                   error   : function(r) { return handleTransportError(
                       _this.call, name, args, cb, r); },
                       data    : createWormholeCall(name, args),
                       dataType: "json" });
        }

        // Execute a function, and call the callback with the result.
        this.rpc = function(name, args, cb) {
            this.wormhole_call(name, args, cb, '/wormhole/call/')
        };

        // Resolve urls according to django scheme.  'cb' will
        // either be called with a WormholeResult object, whose
        // content will contain the url name, or error flag will be set if not found.
        this.resolve = function(name, args, cb) { 
            this.wormhole_call(name, args, cb, '/wormhole/resolve/');
        }
    };

    $.wormhole = new Wormhole();

})(jQuery);

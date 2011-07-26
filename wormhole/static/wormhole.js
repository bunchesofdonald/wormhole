;(function ($) {
    function Wormhole() {
        var _this = this;
        var _options = getOptionsFromScriptSrc();

        // Handles getting options passed in from script tag.
        // The only expected option is:
        // csrf_token : Django csrf_token
        function getOptionsFromScriptSrc() {
            // Get last script tag in parsed DOM.
            // Due to the way html pages are parsed, the last one is always the one being loaded.
            var options = {}
            var wormhole_src = $('script').last().attr('src');

            if(wormhole_src.match(/\?/)) {
                var options_list = wormhole_src.split('?')[1].split('&');
                for(var i = 0; i < options_list.length; i++) {
                    var tmp = options_list[i].split('=');
                    options[$.trim(tmp[0])] = $.trim(tmp[1]);
                }
            }

            return options;
        }

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
            return {
                'name' : name, 
                'args' : JSON.stringify(args),
                'csrfmiddlewaretoken' : _options['csrf_token'] || ''
            }
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

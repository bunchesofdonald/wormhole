;(function ($) {
      function Wormhole() {
	  var _this = this;
	  
	  // These functions handle transport success/error. A
	  // transport error occurs when the server cannot be reached,
	  // or returns an error code. Transport success may still
	  // carry an application error.
	  function handleTransportSuccess(userCallback, result) { 

	  };

	  function handleTransportError(userCallback, result) { 
	      
	  };

	  // Execute a function, and call the callback with the result.
	  this.call = function(name, args, cb) { 
	      $.ajax({ type    : "POST",
		       url     : "/wormhole/call",
		       success : function(r) { return handleTransportSuccess(cb, r); },
		       error   : function(r) { return handleTransportError(cb, r); },
		       dataType: "json" });
	  };
	  
	  // Resolve urls according to django scheme.  'cb' will
	  // either be called with a WormholeResult object, whose
	  // content will contain the url name, or error flag will be set if not found.
	  this.resolve = function(name, args, cb) { 
	      $.ajax({ type    : "POST",
		       url     : "/wormhole/resolve",
		       success : function(r) { return handleTransportSuccess(cb, r); },
		       error   : function(r) { return handleTransportError(cb, r); },
		       dataType: "json" });
	  }
      };
      $.wormhole = new Wormhole();
  })(jQuery);
;(function ($) {
      function Wormhole() {
	  var _this = this;
	  
	  function handleSuccess(userCallback, result) { 

	  };

	  function handleError(userCallback, result) { 
	      
	  };

	  this.call = function(name, args, cb) { 
	      $.ajax({ type    : "POST",
		       url     : "/wormhole/call",
		       success : function(r) { return handleSuccess(cb, r); },
		       error   : function(r) { return handleError(cb, r); },
		       dataType: "json" });
	  };
      };
      $.wormhole = new Wormhole();
  })(jQuery);
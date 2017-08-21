/*
    This is a temporary fix for the hallotoolbar bug with the position of the icons,
    This would limit the choices to things like Italic, Bold, Underlink, Links, Documents, and Bullets.

    Please see:
    - https://github.com/wagtail/wagtail/issues/3587
    - https://github.com/APSL/puput/pull/83
*/
(function() {
    (function($) {
	return $.widget('IKS.inlineonly', {
	    options: {
            uuid: '',
            editable: null,
            buttonCssClass: null
	    },
	    populateToolbar: function(toolbar) {
		var whitelist = [
		    'halloformat', 'hallowagtaillink', 'hallowagtaildoclink', 'hallolists'
		];
		$(toolbar).children().filter(function() {
		    var className = this.className.split(/\s+/)[0];
		    return $.inArray(className, whitelist) == -1;
		}).remove();
	    }
	});
    })(jQuery);
}).call(this);
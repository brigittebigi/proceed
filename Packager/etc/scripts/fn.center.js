(function($) {
	/*
	 *
	 *	fonction center() qui permet de centrer un élément.
	 *
	 */
	$.fn.center = function() {


		this.css({
			'position': 'absolute',
			'top': '50%',
			'margin-top': -this.width() / 2.5 + 'px',
			'left': '50%',
			'margin-left': -this.width() / 2 + 'px'
		});


	}; // center()
})(jQuery);
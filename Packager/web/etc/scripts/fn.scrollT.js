(function($) {
	/*
	 * fonction srcollT() qui permet de remonter en haut de page.
	 *
	 * @param [(int) d, (int) t]
	 *        d : le delai (en ms) avant le defilement vers le haut, (default = 30ms).
	 *        t : le temps (en ms) du defilement vers le haut, (default = 800ms)
	 *
	 */
	$.fn.scrollT = function(d, t) {
		d = d || 30;
		t = t || 800;

		$('.scrollT').fadeOut(100); // on cache le bouton.


		/*
		 * @event SCROLL
		 *        affiche/cache le bouton selon la hauteur du scroll.
		 *
		 */
		$(window).scroll(function() {

			if ($(this).scrollTop() <= 200) {
				$('.scrollT').fadeOut(100);
			} else {
				$('.scrollT').fadeIn(100);
			}

		}); // scroll()


		/*
		 * @event CLICK
		 *        Remonte en haut de page au clic sur le bouton.
		 *
		 */
		$('.scrollT').click(function(e) {
			e.preventDefault();
			e.stopPropagation();

			$('html, body').animate({
				scrollTop: 0
			}, 'slow');


		}); // click()


	}; // scrollT()
})(jQuery);
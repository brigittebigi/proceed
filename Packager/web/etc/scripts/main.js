$(document).ready(function() {

	// On fait appelle à la fonction center, qui va centrer toutes les div
	// ayant pour class 'js-center'
	$('.js-center').center();

	// On active la fonction permettant de faire apparaitre l'indicateur de scroll pour remonter
	// en haut de page
	$(this).scrollT();
});
$(document).ready(function() {

	// on enlève . et .. du tableau
	TabFiles.splice(0,2);

	// on initalise le compteur
	window.i = 0;

	// on lance la fonction
	change_image();

	// alert(TabFiles);

	window.setInterval(change_image, 3000);
});

function change_image () {
	$('#js-diapo').fadeOut(350, function() {

		$('#js-diapo').attr('src', 'image-diapo/' + TabFiles[window.i]);
		window.i++;
		if (window.i == TabFiles.length) {
			window.i = 0;
		}
		$('#js-diapo').fadeIn(350);
	});
	
}

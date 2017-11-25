var minSize = 3;
var maxSize = 6;

function setPuzzle() {
	var size = $('#size').val();

	if ()
	for (var i = 1; i < Math.pow(size, 2); i++) {
		$('#puzzle').append("<div class='tile' id='tile- " + i + "'>" + i + "</div>");
	}
	$('#puzzle').append("<div class='tile' id='tile-0'>-</div>");
	$('#puzzle').css('height', $('#puzzle').css('width'));
}

function setSize() {
	for (var i = minSize; i <= maxSize; i++) {
		$('#size').append("<option value=" + i + "> " + i + "</option>");
	}
}

$(document).ready(function () {
	setSize();
	setPuzzle();
});

var minSize = 3;
var maxSize = 6;

function setPuzzle() {
	var size = $('#size').val();
	for (var i = 1; i < Math.pow(size, 2); i++) {
		$('#puzzle').append("<div class='tile' id='tile- " + i + "'>" + i + "</div>");
	}
	$('#puzzle').append("<div class='empty' id='tile-0'></div>");
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

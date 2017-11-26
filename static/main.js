var minSize = 3;
var maxSize = 6;
var algoTypes = [{'val': 'adaStar', 'text': 'ADA*'}, {'val': 'ada', 'text': 'A*'}];
var heuristicTypes = [{'val': 'manhattan', 'text': 'Manhattan distance'}];

function setPuzzle() {
	var size = Number($('#size').val());
	var field = $('#puzzle');

	field.html('');
	// field.css('height', 195);
	field.css('width', size * 61 + 18);
	for (var i = 1; i < Math.pow(size, 2); i++) {
		$('#puzzle').append("<div class='tile' id='tile- " + i + "'>" + i + "</div>");
	}
	$('#puzzle').append("<div class='empty' id='tile-0'></div>");
	$('#puzzle').css('height', $('#puzzle').css('width'));
}

function setSize() {
	for (var i = minSize; i <= maxSize; i++) {
		$('#size').append("<option value='" + i + "'>" + i + "</option>");
	}
}

function setAlgoTypes() {
	for (var i = 0; i < algoTypes.length; i++) {
		$('#algorithmType').append("<option value='" + algoTypes[i].val + "'>" + algoTypes[i].text + "</option>");
	}
}

function setHeuristicTypes() {
	var obj = $('#heuristicTypes');
}

function request(page, data) {
	var ret = "";
	xhr = new XMLHttpRequest();

	xhr.open('POST', 'http://127.0.0.1:5000/' + page);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.onload = function() {
		console.log('XHR = ', xhr);
		ret = xhr.responseText;
		if (xhr.status == 200) {
			console.log('ZAEBIS');
			return xhr.responseText;
			// alert('Cool = ' + xhr.responseText);
		} else if (xhr.status != 200) {
			alert('Request failed.  Returned status of ' + xhr.status);
		}
	};
	xhr.send(JSON.stringify(data));
	return ret;
}

function getRandPath() {
	return request('rand', {size: $('#size').val()});
}

$('#size').change(function () {
	setPuzzle();
});

$('#random').click(function () {
	var size = Number($('#size').val());
	var field = $('#puzzle');

	console.log('new');
	$.when( var path = getRandPath(size) ).done(function () {
		console.log('PATH = ', path);
		return;
		field.html('');
		field.css('width', size * 61 + 18);
		for (var i = 1; i < Math.pow(size, 2); i++) {
			$('#puzzle').append("<div class='tile' id='tile- " + i + "'>" + i + "</div>");
		}
		$('#puzzle').append("<div class='empty' id='tile-0'></div>");
		$('#puzzle').css('height', $('#puzzle').css('width'));
	});
});

$(document).ready(function () {
	setSize();
	setPuzzle();
	setAlgoTypes();
	// setHeuristicTypes();
});

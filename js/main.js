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

function getRandPath() {
	        $.ajax({
            url: 'http://127.0.0.1:5000/tst',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                console.log(data);
            },
            data: {wtf: 'htf'}
        });
	// $.ajax({
	// 	url: "http://127.0.0.1:5000/tst",
 //        contentType: 'application/json',
 //        dataType: 'json',
 //        data: {"var1": "value1"},
 //        type: 'POST',
	// }).done(function( data ) {
	// 	console.log(data);
	// });
}




$('#size').change(function () {
	setPuzzle();
});

$('#random').click(function () {
	var size = Number($('#size').val());
	var field = $('#puzzle');

	var path = getRandPath(size);
	field.html('');
	field.css('width', size * 61 + 18);
	for (var i = 1; i < Math.pow(size, 2); i++) {
		$('#puzzle').append("<div class='tile' id='tile- " + i + "'>" + i + "</div>");
	}
	$('#puzzle').append("<div class='empty' id='tile-0'></div>");
	$('#puzzle').css('height', $('#puzzle').css('width'));
});

$(document).ready(function () {
	setSize();
	setPuzzle();
	setAlgoTypes();
	// setHeuristicTypes();
});

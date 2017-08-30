
// Set up python bridge

var wrapper;
window.onload = function() {
	new QWebChannel(qt.webChannelTransport, function (channel) {
	    wrapper = channel.objects.wrapper;
	});
}


// Page elements

// JS to PYTHON
function load_book_page() {
	wrapper.load_book_page();
}


function load_token_definition(token) {
	wrapper.load_token_definition(token);
}


function show_furigana() {
	wrapper.show_furigana();
}


function toggle_translation() {
	wrapper.toggle_translation();
}

// PYTHON to JS

function set_book_page(content) {
	var page = document.getElementById("page_body");
	page.innerHTML = content;
}


function set_token_definition(content) {
	var page = document.getElementById("definition");
	page.innerHTML = content;
}


// Helpers

function output(message)
{
    var output = document.getElementById("output");
    output.innerHTML = output.innerHTML + message + "<br><br>";
}


// Set up python bridge

var wrapper;
window.onload = function() {
	new QWebChannel(qt.webChannelTransport, function (channel) {
	    wrapper = channel.objects.wrapper;
	});
}
// Page elements

// JS to PYTHON
function update_book_page() {
	wrapper.update_tokens();
}


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
	var page = document.getElementById("book_page");
	page.innerHTML = content;
}


function set_token_definition(content) {
	var page = document.getElementById("definition");
	page.innerHTML = content;
}

function set_num_words_total(num_words) {
	var page = document.getElementById("num_words_total");
	page.innerHTML = content;
}

function set_num_new_words(num_words) {
	var page = document.getElementById("num_new_words");
	page.innerHTML = content;
}


// Helpers

function output(message)
{
    var output = document.getElementById("output");
    output.innerHTML = output.innerHTML + message + "<br><br>";
}


var ctrl_pressed = false;

$(document).keydown(function(event) {
    if (event.which == "17")
    {
    	toggle_translation();
    	ctrl_pressed = true;
    }
});

// $(document).keyup(function() {
// 	if (ctrl_pressed) 
// 	{
// 		toggle_translation();
//     	ctrl_pressed = false;
// 	}
// });

// HTML STYLING

var sidebar_is_open = true;
function toggle_sidebar() {
	if (sidebar_is_open == true)
	{
		// document.getElementById("wrapper_div").style.marginLeft = "0";
		document.getElementById("book_info").style.display = "none";
		document.getElementById("book_info_toggle_button").innerText = ">";
		// document.getElementById("page-sidebar").style.width = "15px";
		sidebar_is_open = false;
	}
	else
	{
		// document.getElementById("wrapper_div").style.marginLeft = "220px";
		document.getElementById("book_info").style.width = "200px";
		document.getElementById("book_info").style.display = "block";
		document.getElementById("book_info_toggle_button").innerText = "<";
		// document.getElementById("vocab_toggle").style.left = "200px";
		sidebar_is_open = true;
	}
}

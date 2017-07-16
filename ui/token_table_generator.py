import os
import html
from io import BytesIO
import base64

class TokenTableGenerator(object):
	TABLE_START = "<table class='mother_chars'><tbody><tr>"
	TABLE_END = "</tr></table>"
	TABLE_LINE_START = "<td valign='top'><table class='chars'>"
	TABLE_LINE_END = "</table></td>"
	TOKEN_CELL = "<tr><td onclick=\"document.getElementById('definitioncontent').innerHTML=document.getElementById('%s').innerHTML;\"><div class='container'><img class='token' src='data:image/jpeg;base64, %s'/></div></td></tr>"
	DEFINITION = "<div style='display: none; visibility: hidden;' id='%s'>%s</div>"
	GENERATED_START = "<!-- GENERATED TABLE HERE -->"
	GENERATED_END = "<!-- GENERATED TABLE END HERE -->"
	INDEX_PATH = "ui\\html\\index.html"

	def __init__(self):
		pass

	def escape(self, text):
		escaped_data = ""
		for c in text:
			escaped_data += "&#" + hex(ord(c))[1:]
		# escaped_data = escaped_data.replace("&#xa&", "<br>&")
		return escaped_data

	def generate_definition_html(self, token):
		html = ""

		word = "<h1 class=\"word\">" + self.escape(token.base) + "</h1>"
		hiragana = "<h3 class=\"hiragana\">" + self.escape(token.kana) + "</h3>"
		try:
			definition = "<p class=\"text\">" + token.english[-1] + "</p>"
		except IndexError:
			definition = "<p class=\"text\"></p>"

		html += word + "<br>" + hiragana + "<br>" + definition
		return html

	def generate_index(self, tokens):
		lines = list(set([token.x for token in tokens]))
		lines.sort()

		html = self.TABLE_START
		for x in lines:
			html += self.TABLE_LINE_START
			for token in tokens:
				if token.x == x:

					# Encode image
					image_data = BytesIO()
					token.image.save(image_data, format="JPEG")
					b64_image = base64.b64encode(image_data.getvalue())

					# Add cell
					html += self.TOKEN_CELL % (id(token), b64_image.decode('utf8'))
			html += self.TABLE_LINE_END

		html += self.TABLE_END

		for token in tokens:
			html += self.DEFINITION % (id(token), self.generate_definition_html(token))


		with open(self.INDEX_PATH, "r", encoding="utf8") as f:
			old_html = f.read()

		start = old_html.split(self.GENERATED_START)[0]
		end = old_html.split(self.GENERATED_END)[1]

		new_html = start + self.GENERATED_START + html + self.GENERATED_END + end

		with open(self.INDEX_PATH, "w", encoding="utf8") as f:
			f.write(new_html)

import os

class TokenTableGenerator(object):

	def __init__(self, image_folder_path):
		self.path = image_folder_path

	def generate(self):
		images = {}
		for i in os.listdir(self.path):
			xpos = int(i.split("_")[-1].split(".")[0])
			images.setdefault(xpos, []).append(i)
		
		xpos = list(images)
		xpos.sort()

		table = """<table class="mother_chars"><tbody><tr>"""

		for x in xpos:
			line_images = images[x]
			line_images = sorted(line_images, key=lambda x: int(x.split("_")[0]))
			print(line_images)
			table += "<td valign=\"top\"><table class=\"chars\">"
			for img in line_images:
				table += "<tr ><td><img src=\"../../data/images/" + img + "\" alt=\"\" /></td></tr>"
			table += "</table></td>"

		table += "</tr></table>"

		with open("ui\\html\\index.html", "r") as f:
			html = f.read()

		start = html.split("<!-- GENERATED HERE -->")[0]
		end = html.split("<!-- GENERATED END HERE -->")[1]

		new_html = start + "<!-- GENERATED HERE -->" + table + "<!-- GENERATED END HERE -->" + end

		with open("ui\\html\\index.html", "w") as f:
			f.write(new_html)


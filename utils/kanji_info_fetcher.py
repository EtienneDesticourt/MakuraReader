import urllib.request
from urllib.request import Request
import urllib.parse
import time
import re

if __name__ == "__main__":
	HEADERS = {'User-Agent': 'Mozilla'}
	PATTERN = "Elements: <a href=\".*?>(.*?)<"

	with open("kanji.txt", "r", encoding="utf8") as f:
		kanjis = f.read().split("\n")

	raw_url = "http://tangorin.com/kanji/%s"
	kanji_elements = {}
	i = 0
	for kanji in kanjis:
		url = raw_url % urllib.parse.quote(kanji)
		with urllib.request.urlopen(Request(url, headers=HEADERS)) as resp:
			data = resp.read().decode("utf8")
			elements = re.findall(PATTERN, data)
			if len(elements) > 0:
				elements = elements[0]
			else:
				elements = ""
		kanji_elements[kanji] = elements 

		if i % 100 == 0:
			print("Fetched", i, "out of", len(kanjis), "kanjis.")
		i+= 1

	results = ""
	for kanji in kanji_elements:
		results += kanji + ":" + kanji_elements[kanji] + "\n"

	with open("kanji_elements.txt", "w", encoding="utf8") as f:
		f.write(results)






import os
if __name__ == "__main__":


	# fonts = os.listdir("data\\train\\連")
	# fonts = [font.replace(".jpg","") for font in fonts]
	# print(fonts)

	#--------------

	# with open("kanjidic", "r", encoding="utf8") as f:
	# 	for line in f.read().split("\n"):
			
	#--------------

	top = "kanji_clusters2\\val"
	for cluster in os.listdir(top):
		for f in os.listdir(os.path.join(top, cluster)):
			path = os.path.join(top, cluster, f)
			os.rename(path, path+".jpg")
			


class Character(object):
    "A single character from the media being read."

    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.width, self.height = image.size
        self.text = "UNK"

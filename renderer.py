from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

DEFAULT_FONT_FILE = 'msmincho.ttc'
DEFAULT_FONT_SIZE = 15

class Renderer(object):

    def __init__(self, image_size, line_width, background, text_color, font_file=DEFAULT_FONT_FILE, font_size=DEFAULT_FONT_SIZE):
        self.image_size = image_size
        self.line_width = line_width
        self.background = background
        self.text_color = text_color
        self.font = ImageFont.truetype(font_file, font_size)
        self.font_file = font_file
        self.font_size = font_size

    def render(self, characters):
        spread_ratio = 1.2
        width, height = int(self.image_size[0]*spread_ratio)+self.line_width, self.image_size[1]
        image = Image.new("RGB", (width, height), self.background)

        # Render characters
        for character in characters:
            image.paste(character.segment.image, (int(character.segment.x*spread_ratio), character.segment.y))

        # Render kana
        for character in characters:
            line_index = (character.segment.x / self.line_width) + 1
            text_offset = (int(character.segment.x * spread_ratio + self.line_width), character.segment.y + 2)
            if character.text != None:
                for hiragana in character.text:
                    draw = ImageDraw.Draw(image)
                    draw.text(text_offset, hiragana, font=self.font, fill=self.text_color)
                    text_offset = (text_offset[0], text_offset[1] + self.font_size - 2)
        return image



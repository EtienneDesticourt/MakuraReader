from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import glob
import os
import config
from tokenizer import Token



class Renderer(object):

    def __init__(self, image_size=config.BOX_SIZE,
                       line_width=config.LINE_WIDTH,
                       background_color=config.BACKGROUND_COLOR,
                       text_color=config.TEXT_COLOR,
                       font_file=config.RENDERING_FONT_FILE,
                       font_size=config.RENDERING_FONT_SIZE,
                       spread_ratio=config.SPREAD_RATIO,
                       bottom_margin=config.BOTTOM_MARGIN):
        self.image_size = image_size
        self.line_width = line_width
        self.background_color = background_color
        self.text_color = text_color
        self.font_file = font_file
        self.font_size = font_size
        self.font = ImageFont.truetype(font_file, font_size)
        self.spread_ratio = spread_ratio
        self.bottom_margin = bottom_margin
        self.color_toggle = False

    def next_color(self):
        self.color_toggle = not self.color_toggle
        if self.color_toggle:
            return (255, 0, 0)
        else:
            return (0, 0, 255)

    def split_token(self, token, characters):
        "Splits the characters in a token by line breaks using their x position."
        # TODO: Take into account Vertical/Horizontal text setting 
        parts = []
        current_part = []
        current_x = characters[0].x
        for chara in characters:
            if chara.x != current_x:
                parts.append(current_part)
                current_part = []
            current_part.append(chara)

        if current_part != []:
            parts.append(current_part)

        return parts

    def render_token(self, token, characters):

        height = 0
        for character in characters:
            height += character.height
        width = int(self.line_width * self.spread_ratio)

        image  = Image.new("RGB", (width, height), self.background_color)
        y_offset = 0
        for character in characters:
            image.paste(character.image, (0, y_offset))
            y_offset += character.height

        return image

    def render(self, characters, tokens):
        current_char = 0
        images = []
        for token in tokens:
            last_char_index = current_char+len(token.raw)
            token_chars = characters[current_char:last_char_index]
            image = self.render_token(token, token_chars)
            images += [(image, token_chars[0].x, token)]
            current_char += len(token.raw)

        # TODO: Clean
        test = 'data/images/*'
        test2 = 'data/token_data/*'
        r = glob.glob(test)
        r2 = glob.glob(test2)
        for i in r:
           os.remove(i)
        for i in r2:
           os.remove(i)
        for i, image in enumerate(images):
            image, x, token = image
            image.save("data\\images\\" + str(i) + "_" + str(x) + ".jpg", "JPEG")
            with open("data\\token_data\\" + str(i) + "_" + str(x) + ".txt", "w", encoding="utf8") as f:
                if len(token.english) != 0:
                    english = token.english[-1]
                else:
                    english = token.english
                f.write(str(token.base) + "\n" + str(token.kana) + "\n" + str(english))
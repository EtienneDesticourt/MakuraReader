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
        current_x = characters[0].segment.x
        for chara in characters:
            if chara.segment.x != current_x:
                parts.append(current_part)
                current_part = []
            current_part.append(chara)

        if current_part != []:
            parts.append(current_part)

        return parts

    def render_token(self, token, characters):
        parts = self.split_token(token, characters)

        images = []
        for part in parts:
            x, y = part[0].segment.x, part[0].segment.y
            end_x, end_y = x + self.line_width * self.spread_ratio, part[-1].segment.y + part[-1].segment.height
            width = int(end_x - x)
            height = int(end_y - y)
            image  = Image.new("RGB", (width, height), self.background_color)
            for character in part:
                image.paste(character.segment.image, (0, int(character.segment.y - y)))
            images.append(image)

        return images

    def render(self, characters, tokens):
        current_char = 0
        images = []
        for token in tokens:
            last_char_index = current_char+len(token.raw)
            token_chars = characters[current_char:last_char_index]
            images += [(image, token_chars[0].segment.x) for image in self.render_token(token, token_chars)]
            current_char += len(token.raw)

        # TODO: Clean
        test = 'data/images/*'
        r = glob.glob(test)
        for i in r:
           os.remove(i)
        for i, image in enumerate(images):
            image, x = image
            image.save("data\\images\\"+str(i)+"_"+str(x)+".jpg", "JPEG")
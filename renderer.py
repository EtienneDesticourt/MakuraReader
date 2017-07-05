from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
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

    def render(self, characters, tokens):
        # Create new bigger image to accomodate katakana between each line
        width  = int(self.image_size[0] * self.spread_ratio) + self.line_width
        height = int(self.image_size[1] * (1 + self.bottom_margin))
        image  = Image.new("RGB", (width, height), self.background_color)

        # 
        current_char = 0
        tokens_next = []
        for token in tokens:
            if len(token.kana) != 0:
                token_chars = characters[current_char:current_char+len(token.characters)]
                new_token = Token(characters=token_chars, kana=token.kana)
                tokens_next.append(new_token)
            current_char += len(token.characters)

        # Render characters
        for character in characters:
            image.paste(character.segment.image, (int(character.segment.x*self.spread_ratio), character.segment.y))

        # Render kana
        for token in tokens_next:
            character = token.characters[0]
            line_index = (character.segment.x / self.line_width) + 1
            text_offset = (int(character.segment.x * self.spread_ratio + self.line_width), character.segment.y + 2)
            for hiragana in token.kana:
                draw = ImageDraw.Draw(image)
                draw.text(text_offset, hiragana, font=self.font, fill=self.text_color)
                text_offset = (text_offset[0], text_offset[1] + self.font_size - 2)

        return image

from PIL import Image
import config


class Renderer(object):

    def __init__(self, background_color=config.BACKGROUND_COLOR,
                 spread_ratio=config.SPREAD_RATIO):
        self.background_color = background_color
        self.spread_ratio = spread_ratio

    def render_token(self, token):
        image  = Image.new("RGB", (int(token.width*self.spread_ratio), token.height), self.background_color)
        y_offset = 0
        for character in token.characters:
            image.paste(character.image, (0, y_offset))
            y_offset += character.height

        return image

    def render(self, tokens):
        for token in tokens:
            token.image = self.render_token(token)
        return tokens

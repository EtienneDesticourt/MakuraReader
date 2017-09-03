from PIL import ImageGrab
import utils.misc
import config


class NaiveSegmenter(object):
    "A segmenter to split an image of text into separate characters."

    def __init__(self, line_width=config.KINDLE_LINE_WIDTH,
                 char_min_size=config.KINDLE_CHAR_MIN_SIZE,
                 char_max_size=config.KINDLE_CHAR_MAX_SIZE,
                 background_color=config.BACKGROUND_COLOR,
                 too_big_rectifier=config.KINDLE_TOO_BIG_RECTIFIER):
        self.line_width        = line_width
        self.char_min_size     = char_min_size
        self.char_max_size     = char_max_size
        self.too_big_rectifier = too_big_rectifier
        self.background_color  = background_color

    def get_characters(self, image):
        image = image.convert('RGB')
        image_width, image_height = image.size

        images = []
        for char_start_x in range(0, image_width, self.line_width):
            line_images   = []
            line_height       = 0
            last_char_too_big = False

            while line_height < image_height:
                char_start_y = line_height
                line_height, last_char_too_big = self._go_to_next_char(line_height, last_char_too_big, char_start_x, image)
                character_image = image.crop((char_start_x, char_start_y, char_start_x + self.line_width, line_height))
                line_images.append(character_image)

            # We do top down but left to right
            # So we reverse the vertical line so it's fully reversed:
            # down top, left right and we can reverse the total at the end
            images += reversed(line_images)

        images = [i for i in images if not utils.misc.image_is_blank(i)]
        return list(reversed(images))

    def _does_line_intersect_char(self, char_start_x, line_height, image):
        image_width, image_height = image.size
        for x in range(char_start_x, char_start_x + self.line_width):
            if x >= image_width or line_height >= image_height:
                continue

            if image.getpixel((x, line_height)) != self.background_color:
                return True
        return False

    def _is_char_too_big(self, char_height):
        return char_height > self.char_max_size

    def _is_char_too_small(self, char_height, last_char_too_big):
        if last_char_too_big:
            return char_height < (self.char_min_size - self.too_big_rectifier)
        return char_height < self.char_min_size

    def _go_to_next_char(self, line_height, last_char_too_big, char_start_x, image):
        line_intersects_character = True
        char_size_too_small = True
        char_size_too_big   = False
        char_start_y        = line_height
        while not char_size_too_big and (line_intersects_character or char_size_too_small):
            line_height += 1
            char_height = line_height - char_start_y
            char_size_too_small = self._is_char_too_small(char_height, last_char_too_big)
            char_size_too_big   = self._is_char_too_big(char_height)

            if not char_size_too_small:
                line_intersects_character = self._does_line_intersect_char(char_start_x, line_height, image)
        return line_height, last_char_too_big

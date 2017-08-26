from PIL import ImageDraw


def draw_character(character, background, font, color, offset):
    image = background.copy()
    draw = ImageDraw.Draw(image)
    draw.text(offset, character, font=font, fill=color)
    return image

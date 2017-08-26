from tests.config import recognizer_config
from tests.utils import draw_character
from recognizer import Recognizer
from PIL import Image, ImageFont


def test_transcribe():
    rec = Recognizer(**recognizer_config)

    # Draw test sentences to image list
    test_sentence = "その子、人間じゃないの。ロボットなのよ。アンドロイド。彼女は悲しくて寂しそうだった。ABC"
    background = Image.new("RGB", rec.image_size, rec.background_color)
    font = ImageFont.truetype('ARIALUNI.TTF', 45)
    char_images = [draw_character(c, background, font, (255, 255, 255), (0, 0),) for c in test_sentence]

    recovered_text = rec.transcribe(char_images)
    assert len(recovered_text) == len(test_sentence)
    correct = sum([1 for i, character in enumerate(recovered_text) if test_sentence[i] == character])
    assert correct / len(test_sentence) > 0.6


def test_transcribe_no_images():
    rec = Recognizer(**recognizer_config)
    text = rec.transcribe([])

    assert text == ""

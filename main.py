import ui.app

import tests.ocr.mock_recognizer
import tests.text.mock_tokenizer
import makura_reader
import history
import recorder
import config

tokenizer = tests.text.mock_tokenizer.MockTokenizer()
recognizer = tests.ocr.mock_recognizer.MockRecognizer()
history = history.History(**config.history_config) 
recorder = recorder.Recorder(**config.recorder_config)

reader = makura_reader.MakuraReader(recognizer, tokenizer, recorder, history)

ui.app.start_app(reader)

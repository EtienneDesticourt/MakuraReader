from PIL import Image
import numpy as np


class Record9B(object):
    """
     --------------------------------------------------------------------------------------------
    |             |Number|        |                                                              |
    |     Byte    |  of  |  Type  |            Contents of Logical Record                        |
    |   Position  | Bytes|        |                                                              |
    |============================================================================================|
    |I   1 -    2 |    2 | Integer| Serial Sheet Number (greater than or equal to 1)             |
    |D   3 -    4 |    2 | Binary | JIS Kanji Code (JIS X 0208)                                  |
    |    5 -    8 |    4 | ASCII  | JIS Typical Reading ( ex. "AI.M" )                           |
    |-------------|------|--------|--------------------------------------------------------------|
    |    9 -  512 |  504 | Packed | 2 Level (1bit/pixel) Image Data                              |
    |             |      |        | 64(X-axis size) * 63(Y-axis size) = 4032 pixels              |
    |-------------|------|--------|--------------------------------------------------------------|
    |  513 -  576 |   64 |        | padding                                                      |
     -------------------------------------------------------------------------------------------- """
    SIZE = 576
    IMAGE_SIZE = (64, 63)
    IMAGE_MODE = '1' #b&w
    STRUCTURE = '>2H4s504s64x'

    def __init__(self, sheet_number, JIS_code, JIS_reading, image_data):
        self.sheet_number = sheet_number
        self.JIS_code = JIS_code
        self.JIS_reading = JIS_reading
        self.image_data = image_data

    @property
    def image(self):
        return Image.frombytes(self.IMAGE_MODE, self.IMAGE_SIZE, self.image_data, 'raw')

    @property
    def image_array(self):
        return np.array(self.image)
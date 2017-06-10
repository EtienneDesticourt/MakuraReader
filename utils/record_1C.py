from PIL import Image
import numpy as np


class Record1C(object):
    """
     --------------------------------------------------------------------------------------------
    |             |Number|        |                                                              |
    |     Byte    |  of  |  Type  |            Contents of Logical Record                        |
    |   Position  | Bytes|        |                                                              |
    |============================================================================================|
    |    1 -    2 |    2 | Integer| Data Number (greater than or equal to 1)                     |
    |    3 -    4 |    2 | ASCII  | Character Code ( ex. "0 ", "A ", "$ ", " A", "KA" )          |
    |    5 -    6 |    2 | Integer| Serial Sheet Number (greater than or equal to 0)             |
    |I   7        |    1 | Binary | JIS Code (JIS X 0201)                                        |
    |D   8        |    1 | Binary | EBCDIC Code                                                  |
    |    9        |    1 | Integer| Evaluation of Individual Character Image (0=clean, 1, 2, 3)  |
    |P  10        |    1 | Integer| Evaluation of Character Group (0=clean, 1, 2)                |
    |a  11        |    1 | Integer| Male-Female Code ( 1=male, 2=female ) (JIS X 0303)           |
    |r  12        |    1 | Integer| Age of Writer                                                |
    |t  13 -   16 |    4 | Integer| Serial Data Number (greater than or equal to 1)              |
    |   17 -   18 |    2 | Integer| Industry Classification Code (JIS X 0403)                    |
    |   19 -   20 |    2 | Integer| Occupation Classification Code (JIS X 0404)                  |
    |   21 -   22 |    2 | Integer| Sheet Gatherring Date (19)YYMM                               |
    |   23 -   24 |    2 | Integer| Scanning Date (19)YYMM                                       |
    |   25        |    1 | Integer| Sample Position Y on Sheet (greater than or equal to 1)      |
    |   26        |    1 | Integer| Sample Position X on Sheet (greater than or equal to 1)      |
    |   27        |    1 | Integer| Minimum Scanned Level (0 - 255)                              |
    |   28        |    1 | Integer| Maximum Scanned Level (0 - 255)                              |
    |   29 -   30 |    2 | Integer| (undefined)                                                  |
    |   31 -   32 |    2 | Integer| (undefined)                                                  |
    |-------------|------|--------|--------------------------------------------------------------|
    |   33 - 2048 | 2016 | Packed | 16 Gray Level (4bit/pixel) Image Data                        |
    |             |      |        | 64(X-axis size) * 63(Y-axis size) = 4032 pixels              |
    |-------------|------|--------|--------------------------------------------------------------|
    | 2049 - 2052 |    4 |        | (uncertain)                                                  |
     -------------------------------------------------------------------------------------------- """

    SIZE = 2052
    IMAGE_SIZE = (64, 63)
    IMAGE_MODE = 'F' #tiff
    STRUCTURE = '>H2sH6BI4H4B4x2016s4x'

    def __init__(self, data_number, char_code, sheet_number, JIS_201_code, EBCDIC_code,
        image_evaluation,
        char_group_evaluation,
        gender,
        age,
        serial_data_number,
        JIS_403_code,
        JIS_404_code,
        gathering_gate,
        scanning_date,
        pos_x,
        pos_y,
        min_level,
        max_level,
        image_data):
        self.data_number = data_number
        self.char_code = char_code
        self.sheet_number = sheet_number
        self.JIS_201_code = JIS_201_code
        self.JIS_code = JIS_201_code
        self.EBCDIC_code = EBCDIC_code
        self.image_evaluation = image_evaluation
        self.char_group_evaluation = char_group_evaluation
        self.gender = gender
        self.age = age
        self.serial_data_number = serial_data_number
        self.JIS_403_code = JIS_403_code
        self.JIS_404_code = JIS_404_code
        self.gathering_gate = gathering_gate
        self.scanning_date = scanning_date
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.min_level = min_level
        self.max_level = max_level
        self.image_data = image_data

    @property
    def image(self):
        return Image.frombytes(self.IMAGE_MODE, self.IMAGE_SIZE, self.image_data, 'bit', 4)

    @property
    def image_array(self):
        return np.array(self.image)

from PIL import ImageGrab
import numpy as np
import config


class KindleReader(object):

    def __init__(self, text_bounding_box=config.KINDLE_BBOX,
                 line_width=config.KINDLE_LINE_WIDTH,
                 page_change_threshold=config.PAGE_CHANGE_THRESHOLD):
        self.kindle_bbox = text_bounding_box
        self.line_width = line_width
        self.last_capture = None
        self.page_change_threshold = page_change_threshold
        
    def get_size(self):
        return self.capture_kindle().size # Could be more efficient but eh

    def capture_kindle(self):
        # TODO: LINUX
        return ImageGrab.grab(self.kindle_bbox)

    def background_is_white(self):
        # TODO: IMPLEMENT
        return False

    def page_has_changed(self):
        new_capture = self.capture_kindle()

        if self.last_capture == None:
            self.last_capture = new_capture
            return True

        array1 = np.array(new_capture.getdata())
        array2 = np.array(self.last_capture.getdata())
        self.last_capture = new_capture
        
        return np.sum(abs(array2-array1)) != 0

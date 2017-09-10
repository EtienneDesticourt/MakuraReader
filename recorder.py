from PIL import ImageGrab


class Recorder(object):
    """An object to capture images and monitor changes of the media being read.

    # Arguments
        page_bbox: Bounding box on the screen where the page is located.
    """

    def __init__(self, page_bbox):
        self.page_bbox = page_bbox

    def capture(self):
        """Captures the page currently displayed on screen.

        # Returns
            A PIL image of the bounding box of the screen where the page is displayed.
        """
        capture = ImageGrab.grab(self.page_bbox)
        self.last_capture = capture
        return capture

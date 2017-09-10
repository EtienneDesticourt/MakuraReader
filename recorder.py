from PIL import ImageGrab
import threading
import time


class Recorder(object):
    """An object to capture images and monitor changes of the media being read.

    # Arguments
        page_bbox: Bounding box on the screen where the page is located.
    """

    def __init__(self, page_bbox):
        self.page_bbox = page_bbox
        self.new_page_callback = lambda: None
        self.last_capture = None

    def capture(self):
        """Captures the page currently displayed on screen.

        # Returns
            A PIL image of the bounding box of the screen where the page is displayed.
        """
        capture = ImageGrab.grab(self.page_bbox)
        return capture

    def pages_are_different(self, page1, page2):
        """Compares two images and check if they're more different than a specific threshold.

        # Arguments
            page1: An image of the first page.
            page2: An image of the second page.
            threshold: The percentage of pixels that have to be different for the pages
                to be considered different.

        # Returns
            Whether the pages are different.
        """
        if not page1 or not page2:
            return False
        return True

    def _record(self, delay):
        while self.keep_recording:
            current_page = self.capture()
            if self.pages_are_different(current_page, last_capture):
                self.new_page_callback()

            self.last_capture = current_page
            time.sleep(delay)

    def record(self, recording_delay):
        """Starts checking if the page has been turned.

        # Arguments
            recording_delay: The interval at which the recorder check for a new page.
        """
        self.keep_recording = True
        threading.Thread(target=self._record, args=[recording_delay]).start()

    def stop_recording(self):
        """Stops checking for new pages."""
        self.keep_recording = False
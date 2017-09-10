from abc import ABC, abstractmethod


class Recognizer(ABC):
    """An object that provides optical character recognition functionnalities."""

    @abstractmethod
    def transcribe(self, image):
        """Transcribes the text contained in an image.
        
        # Arguments
            image: An image containing text.

        # Returns
            A list of strings detected in different parts of the image.
        """
        pass
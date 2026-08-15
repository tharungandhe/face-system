import numpy as np
import cv2

class ImageUtils:

    def read_image(self, file_bytes):
        """
        Convert uploaded bytes → OpenCV image
        """

        np_arr = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        return image

    def resize_image(self, image, size=(160, 160)):
        """
        Resize image for FaceNet
        """

        return cv2.resize(image, size)

    def normalize(self, image):
        """
        Normalize pixel values
        """

        image = image.astype("float32") / 255.0
        return image
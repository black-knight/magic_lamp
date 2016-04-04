import cv2
from threading import Thread


class Camera(object):
    stopped = False
    image = None
    camera = None

    def start(self, resolution=(320, 240), framerate=32):
        """
        Starts camera input in a new thread.

        :param resolution Resolution
        :param framerate Framerate
        """
        self.stopped = False

        # Initialize camera
        self.camera = cv2.VideoCapture(0)
        self.grab_image()

        # Start thread
        thread = Thread(target=self.update, args=())
        thread.daemon = True
        thread.start()

    def stop(self):
        """
        Stops camera input.
        """
        self.stopped = True

    def read(self):
        """
        Returns the most recent image read from the camera input.
        """
        return self.image

    def update(self):
        """
        Grabs next image from camera.
        """
        while not self.stopped:
            self.grab_image()

    def grab_image(self):
        """
        Grabs an image from the camera input.
        """
        _, self.image = self.camera.read()

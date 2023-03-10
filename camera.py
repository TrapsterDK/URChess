# import the opencv library
import cv2

class Camera:
    def __init__(self, capture=1) -> None:
        self.vid = cv2.VideoCapture(capture)

        if not self.vid.isOpened():
            raise ValueError("Unable to open camera")

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (None, None)

    def save_frame(self, filename):
        ret, frame = self.get_frame()
        if ret:
            cv2.imwrite(filename, frame)

        return ret, frame

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

class FakeCamera:
    def __init__(self, img_filename, width = None, height = None) -> None:
        self.img = cv2.imread(img_filename)

        if width is not None:
            self.img = cv2.resize(self.img, (width, height))

    def get_frame(self):
        return (True, self.img.copy())

    def save_frame(self, filename):
        return (True, self.img)

    def __del__(self):
        pass
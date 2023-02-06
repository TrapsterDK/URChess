# import the opencv library
import cv2

class Camera:
    def __init__(self, capture=1) -> None:
        self.vid = cv2.VideoCapture(capture)

        if not self.vid.isOpened():
            raise ValueError("Unable to open camera", 0)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

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
    def __init__(self, img_filename) -> None:
        self.img = cv2.imread(img_filename)

    def get_frame(self):
        return (True, self.img.copy())

    def save_frame(self, filename):
        return (True, self.img)

    def __del__(self):
        pass
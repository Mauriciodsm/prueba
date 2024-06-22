import cv2
import threading

class VideoStream:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        self.ret, self.frame = self.cap.read()
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            if self.cap.isOpened():
                self.ret, self.frame = self.cap.read()

    def get_frame(self):
        return self.frame

# Uso del stream
src = 'rtsp://admin:Camara1202@192.168.0.101:554/Streaming/Channels/101'
stream = VideoStream(src)

while True:
    frame = stream.get_frame()
    if frame is not None:
        cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

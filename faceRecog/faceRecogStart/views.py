from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from . import EyeRecogClass as fr
#import EyeRecogClass as fr

@gzip.gzip_page
def Index(request):
    #try:
    cam = VideoCamera()
    return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    #except:
       # pass
    return render(request, 'faceRecogStart\\Index.html')

#to capture video class
class VideoCamera(object):



    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.EyeRecognizer = fr.EyeRecognizer()
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        image=self.EyeRecognizer.recognizeEye(image)

        _, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

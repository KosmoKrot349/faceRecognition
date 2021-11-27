import cv2.cv2
import numpy as np
import dlib
from scipy.spatial import distance as dist
import simpleaudio as sa


class EyeRecognizer:

    def __init__(self):
        self.THRESHOLD_EAR = 0.3
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.counter = 0

    def adjust_gamma(self,image, gamma=1.0):
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

        return cv2.LUT(image, table)


    def calculateEAR(self,eye):
        A=dist.euclidean(eye[1], eye[5])
        B=dist.euclidean(eye[2], eye[4])
        C=dist.euclidean(eye[0], eye[3])
        rez = (A + B) / (2.0 * C)
        return rez




    def recognizeEye(self,img):

        picToShow = img
        #gamma regulator 1 - defoult
        gamma = 3
        img = self.adjust_gamma(img, gamma=gamma)

        #pic to gray color
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #finding face parametrs
        dets = self.detector(img, 1)

        for face in dets:
            shape = self.predictor(img, face)

            #for left
            leftEyeIndex = np.array([42,43,44,45,46,47])
            leftEye = []
            leftEyeClose = False
            for dotIndex in leftEyeIndex:
                pt = shape.parts()[dotIndex]
                tempArr = []
                tempArr.append(pt.x)
                tempArr.append(pt.y)
                leftEye.append(tempArr)
                pt_pos = (pt.x, pt.y)
                cv2.circle(picToShow, pt_pos, 2, (0, 255, 0), 3)

            EARForLeftEye=self.calculateEAR(leftEye)
            if EARForLeftEye<=self.THRESHOLD_EAR:
                leftEyeClose=True

            # for right
            rightEyeIndex = np.array([36, 37, 38, 39, 40, 41])
            rightEye = []
            rightEyeClose = False
            for dotIndex in rightEyeIndex:
                pt = shape.parts()[dotIndex]
                tempArr = []
                tempArr.append(pt.x)
                tempArr.append(pt.y)
                rightEye.append(tempArr)
                pt_pos = (pt.x, pt.y)
                cv2.circle(picToShow, pt_pos, 2, (0, 0, 255), 3)

            EARForRightEye = self.calculateEAR(rightEye)
            if EARForRightEye <= self.THRESHOLD_EAR:
                rightEyeClose = True


            color_yellow = (0, 0, 255)

            cv2.putText(picToShow, F"left: {round(EARForLeftEye,2)} right: {round(EARForRightEye,2)} farame: {self.counter}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)

            if rightEyeClose and leftEyeClose:
                self.counter=self.counter+1
            else: self.counter = 0

            if self.counter>=25:
                self.counter=0
                wave_object = sa.WaveObject.from_wave_file('sound.wav')
                play_object = wave_object.play()
                play_object.wait_done()

        return picToShow












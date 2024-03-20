import cv2
import numpy as np
import math
import tensorflow.keras
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
def capture():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)
    classifier = Classifier("Model/keras_model.h5","Model/labels.txt")
    offset = 20
    imgSize = 300
    counter = 0
    labels = ["Hit","Stand"]
    while True:
        success, img = cap.read()
        imgOutput = img.copy()
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            x,y,w,h = hand['bbox']
            imgCrop = img[y-offset:y+h+offset,x-offset:x+w+offset]
            imgWhite = np.ones((imgSize,imgSize,3),np.uint8)*255
            aspectRatio = h/w
            if aspectRatio>1:
                k = imgSize/h
                wCalc = math.ceil(k*w)
                imgResize = cv2.resize(imgCrop,(wCalc,imgSize))
                wGap = math.ceil((imgSize - wCalc)/2)
                imgWhite[:,wGap:wCalc+wGap] = imgResize
                prediction,index = classifier.getPrediction(imgWhite)
                # print(prediction,index)
                # return prediction
            elif aspectRatio<1:
                k = imgSize/w
                hCalc = math.ceil(k*h)
                imgResize = cv2.resize(imgCrop,(imgSize,hCalc))
                hGap = math.ceil((imgSize - hCalc)/2)
                imgWhite[hGap:hCalc+hGap,:] = imgResize
                prediction,index = classifier.getPrediction(imgWhite)
                # print(prediction,index)
                # return prediction
            cv2.putText(imgOutput,labels[index],(x,y-20),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),2)            
            # cv2.imshow("ImageCrop",imgCrop)
            # cv2.imshow("ImageWhite",imgWhite)
        cv2.imshow("Image",imgOutput)
            
        key = cv2.waitKey(1)
        if key == ord("s"):
            return labels[index]
if __name__ == "__main__":
    capture()
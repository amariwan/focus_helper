import os
import cv2
import numpy as np
#from moviepy.editor import *
import sys
import time
from time import sleep

from picamera2 import PiCamera2


def smile():

    #output = strftime("/home/pi/Shared/image-%d%m%Y_%H%M%S.jpg")
    output = time.strftime("/home/pi/Bilder/calibration/focus_results/image-%d%m%Y_%H%M%S.jpg")
    camera = PiCamera2(resolution = (4056,3040))
    #camera.ISO = 100
    camera.led = False
    #camera.framerate = 25
    #camera.shutter_speed = 2000
    sleep(1)
    camera.exposure_mode = "auto" # off, auto, night, nightprqqeview, backlight, spotlight, sports, snow, beach, verylong, fixedfps, antishake, fireworks
    camera.awb_mode = "auto"
    sleep(1)
    #camera.drc_strength = "none"
    camera.capture(output)
    camera.close()

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.7
color = (255, 255, 255)
thickness = 2
screen_id = 0


#os.environ["DISPLAY"] = ':0.0'

window_name = "Focus"


cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)


cap = cv2.VideoCapture(0)

tmp1 = 0
tmp2 = 0
tmp3 = 0
tmp4 = 0
tmpmid = 0


width = 1280
hight = 1024

org1 = (20,30)
org2 = (int(width/4*3)-30,30)
org3 = (20,int(hight)-20)
org4 = (int(width/4*3)-30,int(hight)-20)
orgmid = (int(width/4)+20,int(hight/4*3)+20)


cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hight)

count = 0
count1 = 0
count2 = 0
count3 = 0
count4 = 0
countmid = 0

calibration = True
focus = False
focustol = 0.005 #Abweichung in Prozent (grün)
focustol2 = 0.08 #Abweichung in Prozent (gelb)



while True:
    
    keys = cv2.waitKey(1)

            
    count = count + 1
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    if ret == True:
        #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #hsv *= np.array((1,0,0),np.uint8)

        #lower_red = np.array([30,150,50])
        #upper_red = np.array([255,255,180])

        #mask = cv2.inRange(hsv, lower_red, upper_red)
        #res = cv2.bitwise_and(frame,frame, mask= mask)
        grayframe = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        cleanframe = frame
        grayframe = cv2.GaussianBlur(grayframe,(3,3),0)

        edges = cv2.Canny(grayframe,100,100)
        
        frame = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
        #print("edges shape", edges.shape)
        #upper_left = edges[0:int(edges.shape[0]/2), 0:int(edges.shape[1]/2)] #3280,2464
        #y:y+h, x:x+w
        cornersplit = 2
        upper_left = edges[0:int(hight/4), 0:int(width/4)]
        print("upper left", upper_left.shape)
        upper_right = edges[0:int(hight/4), int(width*0.75):int(width)]
        print("upper right", upper_right.shape)
        lower_left = edges[int(hight*0.75):int(hight), 0:int(width/4)]
        print("lower left", lower_left.shape)
        lower_right = edges[int(hight*0.75):int(hight), int(width*0.75):int(width)]
        print("lower right", lower_right.shape)
        mid = edges[int(hight/4):int(hight*3/4), int(width/4):int(width*3/4)]
        print("mid", mid.shape)
        white_pixels1 = np.sum(upper_left == 255)
        white_pixels2 = np.sum(upper_right == 255)
        white_pixels3 = np.sum(lower_left == 255)
        white_pixels4 = np.sum(lower_right == 255)
        white_pixelsmid = np.sum(mid == 255)


        #print(white_pixels/1000, end = '\r')
        if calibration:
            if white_pixels1 > tmp1:
                tmp1 = white_pixels1
                count1 = count
            if white_pixels2 > tmp2:
                tmp2 = white_pixels2
                count2 = count

            if white_pixels3 > tmp3:
                tmp3 = white_pixels3
                count3 = count

            if white_pixels4 > tmp4:
                tmp4 = white_pixels4
                count4 = count
                
            if white_pixelsmid > tmpmid:
                tmpmid = white_pixelsmid
                countmid = count
        lineth = 4   
        if focus:
            if (white_pixels1 > tmp1-int(white_pixels1 * focustol)):
                cv2.rectangle(frame, (0+int(lineth/4),0+int(lineth/4)), (int(width/4)-int(lineth/4),int(hight/4)-int(lineth/4)), (0,255,0), lineth)
            elif ((white_pixels1 < tmp1-int(white_pixels1 * focustol)) and (white_pixels1 > tmp1-int(white_pixels1 * focustol2)) ):
                cv2.rectangle(frame, (0+int(lineth/4),0+int(lineth/4)), (int(width/4)-int(lineth/4),int(hight/4)-int(lineth/4)), (0,255,255), lineth)           
            else:
                cv2.rectangle(frame, (0+int(lineth/4),0+int(lineth/4)), (int(width/4)-int(lineth/4),int(hight/4)-int(lineth/4)), (0,0,255), lineth)
            if (white_pixels2 > tmp2-int(white_pixels2 * focustol)):
                cv2.rectangle(frame, (int(width/4*3)+int(lineth/4),0+int(lineth/4)), (int(width)-int(lineth/4),int(hight/4)-int(lineth/4)), (0,255,0), lineth)
            elif (white_pixels2 < tmp2-int(white_pixels2 * focustol)) and (white_pixels2 > tmp2-int(white_pixels2 * focustol2)):
                cv2.rectangle(frame, (int(width/4*3)+int(lineth/4),0+int(lineth/4)), (int(width)-int(lineth/4),int(hight/4)-int(lineth/4)), (0,255,255), lineth)
            else:
                cv2.rectangle(frame, (int(width/4*3)+int(lineth/4),0+int(lineth/4)), (int(width)-int(lineth/4),int(hight/4)-int(lineth/4)), (0,0,255), lineth)
            if (white_pixels3 > tmp3-int(white_pixels3 * focustol)):
                cv2.rectangle(frame, (0+int(lineth/4),int(hight/4*3)+int(lineth/4)), (int(width/4)-int(lineth/4),int(hight)-int(lineth/4)), (0,255,0), lineth)
            elif (white_pixels3 < tmp3-int(white_pixels3 * focustol)) and (white_pixels3 > tmp3-int(white_pixels3 * focustol2)):
                cv2.rectangle(frame, (0+int(lineth/4),int(hight/4*3)+int(lineth/4)), (int(width/4)-int(lineth/4),int(hight)-int(lineth/4)), (0,255,255), lineth)
            else:
                cv2.rectangle(frame, (0+int(lineth/4),int(hight/4*3)+int(lineth/4)), (int(width/4)-int(lineth/4),int(hight)-int(lineth/4)), (0,0,255), lineth)
            if (white_pixels4 > tmp4-int(white_pixels4 * focustol)):
                cv2.rectangle(frame, (int(width/4*3)+int(lineth/4*3),int(hight/4*3)+int(lineth/4*3)), (int(width)-int(lineth/4*3),int(hight)-int(lineth/4*3)), (0,255,0), lineth)
            elif (white_pixels4 < tmp4-int(white_pixels4 * focustol)) and (white_pixels4 > tmp4-int(white_pixels4 * focustol2)):
                cv2.rectangle(frame, (int(width/4*3)+int(lineth/4*3),int(hight/4*3)+int(lineth/4*3)), (int(width)-int(lineth/4*3),int(hight)-int(lineth/4*3)), (0,255,255), lineth)
            else:
                cv2.rectangle(frame, (int(width/4*3)+int(lineth/4*3),int(hight/4*3)+int(lineth/4*3)), (int(width)-int(lineth/4*3),int(hight)-int(lineth/4*3)), (0,0,255), lineth)
                
            if (white_pixelsmid > tmpmid-int(white_pixelsmid * focustol)):
                cv2.rectangle(frame, (int(width/4)+int(lineth/4*3),int(hight/4)+int(lineth/4*3)), (int(width*3/4)-int(lineth/4*3),int(hight*3/4)-int(lineth/4*3)), (0,255,0), lineth)
            elif (white_pixelsmid < tmpmid-int(white_pixelsmid * focustol)) and (white_pixelsmid > tmpmid-int(white_pixelsmid * focustol2)):
                cv2.rectangle(frame, (int(width/4)+int(lineth/4*3),int(hight/4)+int(lineth/4*3)), (int(width*3/4)-int(lineth/4*3),int(hight*3/4)-int(lineth/4*3)), (0,255,255), lineth)
            else:
                cv2.rectangle(frame, (int(width/4)+int(lineth/4*3),int(hight/4)+int(lineth/4*3)), (int(width*3/4)-int(lineth/4*3),int(hight*3/4)-int(lineth/4*3)), (0,0,255), lineth) 

        

        cv2.putText(frame, str(white_pixels1)+"    "+" Max: "+str(tmp1)+" Time: "+str(count1), org1, font, fontScale, color, thickness)
        cv2.putText(frame, str(white_pixels2)+"    "+" Max: "+str(tmp2)+" Time: "+str(count2), org2, font, fontScale, color, thickness)
        cv2.putText(frame, str(white_pixels3)+"    "+" Max: "+str(tmp3)+" Time: "+str(count3), org3, font, fontScale, color, thickness)
        cv2.putText(frame, str(white_pixels4)+"    "+" Max: "+str(tmp4)+" Time: "+str(count4), org4, font, fontScale, color, thickness)
        cv2.putText(frame, str(white_pixelsmid)+"    "+" Max: "+str(tmpmid)+" Time: "+str(countmid), orgmid, font, fontScale, color, thickness)

        cv2.line(frame, (0, int(hight/2)), (int(width), int(hight/2)), (0, 50, 255), thickness = 1)
        cv2.line(frame, (int(width/2), 0), (int(width/2), hight), (0, 50, 255), thickness = 1)
        cv2.putText(frame,"Calibration: " + str(calibration), (int(width-800),int(hight-20)), font, fontScale, color, thickness, cv2.LINE_4)
        cv2.putText(frame,"Focus: " + str(focus), (int(width-800),int(hight-50)), font, fontScale, color, thickness, cv2.LINE_4)

        cv2.imshow('frame', cleanframe)
        #print("edges shape", edges.shape)
        cv2.imshow(window_name,frame)
        #print("frame shape", frame.shape)
        #cv2.imshow('Schaerfe', np.hstack([edges, frame]))
        if keys == ord('c'):
            if calibration:
                calibration = False
            else:
                calibration = True
        if keys == ord('f'):
            if focus:
                focus = False
            else:
                focus = True               
        if keys == ord('q'):
            cv2.imwrite('/home/pi/Bilder/calibration/focus_results/' + "focus_" + time.strftime("%Y%m%d-%H%M%S") +'.jpg',frame) #cleanframe
            #cv2.imwrite('/home/pi/Bilder/calibration/focus_results/' + "edges_" + time.strftime("%Y%m%d-%H%M%S") +'.jpg',edges)
            file = open('/home/pi/Bilder/calibration/focus_results/data_' + time.strftime("%Y%m%d-%H%M%S") +'.txt', 'w')
            # write() - it used to write direct text to the file
            # writelines() - it used to write multiple lines or strings at a time, it takes iterator as an argument
            # writing data using the write() method
            file.write("Upper left: " + str(white_pixels1)+"    "+"Max: "+str(tmp1)+" Time: "+str(count1) + "\nUpper right: " + str(white_pixels2)+"    "+"Max: "+str(tmp2)+" Time: "+str(count2) +"\nLower left: " +str(white_pixels3)+"    "+"Max: "+str(tmp3)+" Time: "+str(count3)+ "\nLower right: " +str(white_pixels4)+"    "+"Max: "+str(tmp4)+" Time: "+str(count4)+ "\nMid: " +str(white_pixelsmid)+"    "+"Max: "+str(tmpmid)+" Time: "+str(countmid))
            # closing the file
            file.close()
            cap.release()
            sleep(1)


            smile()

            break
        if keys == ord('o'):
            cv2.imwrite('/home/pi/Bilder/calibration/focus_results/' + "focus_" + time.strftime("%Y%m%d-%H%M%S") +'.jpg',frame)
            #cv2.imwrite('/home/pi/Bilder/calibration/focus_results/' + "edges_" + time.strftime("%Y%m%d-%H%M%S") +'.jpg',edges)
            # opening a file in 'w'
            file = open('/home/pi/Bilder/calibration/' + sys.argv[1]+'.txt', 'w')
            # write() - it used to write direct text to the file
            # writelines() - it used to write multiple lines or strings at a time, it takes iterator as an argument
            # writing data using the write() method
            file.write("Upper left: " + str(white_pixels1)+"    "+"Max: "+str(tmp1)+" Time: "+str(count1) + "\nUpper right: " + str(white_pixels2)+"    "+"Max: "+str(tmp2)+" Time: "+str(count2) +"\nLower left: " +str(white_pixels3)+"    "+"Max: "+str(tmp3)+" Time: "+str(count3)+ "\nLower right: " +str(white_pixels4)+"    "+"Max: "+str(tmp4)+" Time: "+str(count4)+ "\nMid: " +str(white_pixelsmid)+"    "+"Max: "+str(tmpmid)+" Time: "+str(countmid))
            # closing the file
            file.close()
            
            
            
            break
        
        if keys == ord('r'):
            tmp1 = 0
            tmp2 = 0
            tmp3 = 0
            tmp4 = 0
            tmpmid = 0
            count = 0
            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0
            countmid = 0


cap.release()
cv2.destroyAllWindows()

  #cv2.imshow('Edges', np.hstack([edges, frame]))

        #final_clip = concatenate_videoclips([edges, white_pixels])
        #cv2.imshow('Final', final_clips)
            
        #blendVideo = cv2.add(edges, white_pixels)
        #cv2.imshow ('Blend', blendVideo)


import cv2
import imutils
import numpy as np
import pytesseract
import DB
import serial
import time

pytesseract.pytesseract.tesseract_cmd = "D:\Tesseract\\tesseract.exe"

arduino = serial.Serial('COM3', 9600)
time.sleep(1)

def rec(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # gri tonlama
    gray = cv2.bilateralFilter(gray, 11, 17, 17)  # gürültü düzeltme filtresi
    edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection

    try:
        # en dıştaki kenarları al
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
        screenCnt = None

        # konturlar üzerinde gezin
        for c in cnts:
            # yaklaşık çokgen çiz
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)

            # eğer çokgen dört kenarlı ise al ve döngüyü bitir
            if len(approx) == 4:
                screenCnt = approx
                break

        if screenCnt is None:
            detected = 0
        else:
            detected = 1

        if detected == 1:
            cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

        # plakayı maskele
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1,)
        new_image = cv2.bitwise_and(img, img, mask=mask)

        # kırp
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

        # ocr çalıştır
        text = pytesseract.image_to_string(
            Cropped, config="-c tessedit_char_whitelist='ABCDEFGHIJKLMNOPRSTUVYZ0123456789 '")  # sadece bu karakterleri tanı
        text = text.rstrip("\n")

        # algılanan metnin karakter sayısı 7'den fazla ise çalıştır değilse boşa çalıştırmaya gerek yok
        if len(text) > 7:
            i = 0
            temp = text[i]
            # plaka, rakam ile başlamalı
            while not temp.isdigit() or i == len(text) - 1:
                i += 1
                temp = text[i]
            # son iki karakter tesseracttan new line olark geliyor onları alma
            # text = text[i:-2]
            cv2.putText(img,text,(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),2)
            
            gelen=DB.karsılastırma(text)
            if gelen != []:
                yazi = gelen.pop()
                
                cv2.putText(img,str(yazi[0]),(50,100),cv2.FONT_HERSHEY_COMPLEX_SMALL,1.0,(0,0,255),2)
                cv2.putText(img,str(yazi[1]),(50,150),cv2.FONT_HERSHEY_COMPLEX_SMALL,1.0,(0,0,255),2)
                arduino.write(b'1')
                time.sleep(5)
                arduino.write(b'0')
            # while(1):
                
            #     datafromUser = DB.karsılastırma(text)
                
            #     if datafromUser !=[]:
            #         arduino.write(b'1')
            #     if datafromUser ==[]:
            #         arduino.write(b'0')
            
            
                               
            
    except Exception:
        
        pass
    return img

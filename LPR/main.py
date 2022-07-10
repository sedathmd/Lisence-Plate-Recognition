import cv2
import LPR as lpr
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "D:\Tesseract\\tesseract.exe"
# yakalamayı başlat

cap = cv2.VideoCapture(0)

while True:
    
    # kare yakala
    ret, frame = cap.read()
    # kareyi LPR'ye gönder ve gelen görüntüyü a
    img = lpr.rec(frame)
    # gelen görüntüyü ekranda göster
    cv2.imshow('Lisence Plate Recognition', img)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()



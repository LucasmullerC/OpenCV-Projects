import sys
import cv2 as cv
import numpy as np
#  Global Variables
DELAY_CAPTION = 1500
DELAY_BLUR = 1500
MAX_KERNEL_LENGTH = 31
src = None
dst = None
window_name = 'Segmentação'
opt = 1
def main(argv):
    # Load the source image
    imageName = argv[0] if len(argv) > 0 else 'lena.jpg'
    global src
    src = cv.imread(cv.samples.findFile(imageName))
    if src is None:
        print ('Error opening image')
        print ('Usage: smoothing.py [image_name -- default ../data/lena.jpg] \n')
        return -1
    global dst

    segment(src)

def segment(img):
    #Suavizando
    img = cv.medianBlur(img,5)

    image=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    se=cv.getStructuringElement(cv.MORPH_RECT , (8,8))
    bg=cv.morphologyEx(image, cv.MORPH_DILATE, se)
    out_gray=cv.divide(image, bg, scale=255)

    #Limiarizando
    ret,img = cv.threshold(out_gray,180,255,cv.THRESH_BINARY)

    #Canning para detecção de bordas e segmentação
    edged = cv.Canny(img, 30, 200) #30,200

    cv.imshow("Resultado", edged)
    cv.waitKey(0)


if __name__ == "__main__":
    main(sys.argv[1:])
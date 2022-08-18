import sys
import cv2 as cv
import numpy as np
#  Global Variables
DELAY_CAPTION = 1500
DELAY_BLUR = 1500
MAX_KERNEL_LENGTH = 31
src = None
dst = None
window_name = 'Smoothing Demo'
opt = 1
def main(argv):
    print('1 - Média')
    print('2 - Mediana')
    opcao_escolhida = str(input('Escolha uma opção: '))
    
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
    # Load the source image
    imageName = argv[0] if len(argv) > 0 else 'lena.jpg'
    global src
    src = cv.imread(cv.samples.findFile(imageName))
    if src is None:
        print ('Error opening image')
        print ('Usage: smoothing.py [image_name -- default ../data/lena.jpg] \n')
        return -1
    global dst

    if opcao_escolhida == 1:
        while(opt == 1):
          dst = np.copy(src)
          display_dst(DELAY_CAPTION)
          dst = cv.medianBlur(src, 3)
          display_dst(DELAY_BLUR)
    else:
        while(opt == 1):
          dst = np.copy(src)
          display_dst(DELAY_CAPTION)
          dst = cv.blur(src, (3, 3))
          display_dst(DELAY_BLUR)

def display_caption(caption):
    global dst
    dst = np.zeros(src.shape, src.dtype)
    rows, cols, _ch = src.shape
    cv.putText(dst, caption,
                (int(cols / 4), int(rows / 2)),
                cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
    return display_dst(DELAY_CAPTION)
def display_dst(delay):
    cv.imshow(window_name, dst)
    c = cv.waitKey(delay)
    if c >= 0 : return -1
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])
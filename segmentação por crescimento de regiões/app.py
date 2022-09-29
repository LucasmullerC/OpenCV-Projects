import argparse
import cv2
import numpy as np

refPt = []
cropping = False
type = 0

def click_and_crop(event, x, y, flags, param):
    global refPt, cropping
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(refPt) < type:
            refPt.append((x, y))
        else:
            print("Excedeu o número de pontos!")
    elif event == cv2.EVENT_LBUTTONUP:
        for i in range(len(refPt)):
            cv2.line(image, refPt[i],  refPt[i+1],  (0, 255, 0), 2)
            cv2.imshow("image", image)

#Inicio
print('1 | 4-conectividade')
print('2 | 8-conectividade')
print('3 | m-conectividade')
esc = int(input('Escolha uma opção: '))

if esc == 1:
    type = 5
elif esc == 2:
    type = 9
else:
    type = 99

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		image = clone.copy()
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break

pts = np.array(refPt)
rect = cv2.boundingRect(pts)
x,y,w,h = rect
croped = image[y:y+h, x:x+w].copy()

## (2) make mask
pts = pts - pts.min(axis=0)

mask = np.zeros(croped.shape[:2], np.uint8)
cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

## (3) do bit-op
dst = cv2.bitwise_and(croped, croped, mask=mask)

## (4) add the white background
bg = np.ones_like(croped, np.uint8)*255
cv2.bitwise_not(bg,bg, mask=mask)
dst2 = bg+ dst

cv2.imshow("dst.png", dst)
cv2.waitKey(0)
# close all open windows
cv2.destroyAllWindows()


from __future__ import print_function
import cv2 as cv
import argparse
import numpy as np

window_name = 'Metodo de Segmentacao'

parser = argparse.ArgumentParser(description='Método de Segmentação.')
parser.add_argument('--input', help='Path to input image.', default='stuff.jpg')
args = parser.parse_args()
src = cv.imread(cv.samples.findFile(args.input))
if src is None:
    print('Could not open or find the image: ', args.input)
    exit(0)

# Converter para cinza
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY) 

# Determinando o Limiar
ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV +cv.THRESH_OTSU) 

# Removendo ruidos e segmentando
kernel = np.ones((2, 2), np.uint8) 
closing = cv.morphologyEx(thresh, cv.MORPH_CLOSE,kernel, iterations = 2) 
bg = cv.dilate(closing, kernel, iterations = 1) 
dist_transform = cv.distanceTransform(closing, cv.DIST_L2, 0) 
ret, fg = cv.threshold(dist_transform, 0.02 * dist_transform.max(), 255, 0) 
  
# Exibe imagem
cv.imshow(window_name, fg) 

cv.waitKey()
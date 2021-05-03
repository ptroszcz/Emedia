import cv2 as cv
import numpy as np

def fft(image):
    img=cv.imread(image,cv.IMREAD_GRAYSCALE)
    #img = cv.resize(img,(1024,768),interpolation = cv.INTER_AREA)
    img_fft=np.fft.fft2(img)
    img_fft_shift=np.fft.fftshift(img_fft)
    magnitude_spectrum=20*np.log(np.abs(img_fft_shift))
    magnitude_spectrum=255*magnitude_spectrum/np.max(magnitude_spectrum)
    magnitude_spectrum=np.asarray(magnitude_spectrum, dtype=np.uint8)
    phase=np.angle(img_fft_shift)
    cv.imshow('magnitude',magnitude_spectrum)
    cv.imshow('phase',phase)
    cv.waitKey()
    pass

def show_image(image):
    img = cv.imread(image)
    cv.imshow('image',img)
    cv.waitKey()
    pass

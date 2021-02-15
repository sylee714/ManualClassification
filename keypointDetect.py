import numpy as np
import cv2
import skimage
from cv2 import dnn_superres
import math
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import ImageEnhance
import matplotlib.pyplot as plt
from GPSPhoto import gpsphoto

# Zoom in more to the target so that we can


def get_exif(filename):
    exif = Image.open(filename)._getexif()

    if exif is not None:
        for key, value in exif.items():
            name = TAGS.get(key, key)
            exif[name] = exif.pop(key)

        if 'GPSInfo' in exif:
            for key in exif['GPSInfo'].keys():
                name = GPSTAGS.get(key, key)

                exif['GPSInfo'][name] = exif['GPSInfo'].pop(key)

    return exif


def get_decimal_coordinates(info):
    for key in ['Latitude', 'Longitude']:
        if 'GPS' + key in info and 'GPS' + key + 'Ref' in info:
            e = info['GPS' + key]
            ref = info['GPS' + key + 'Ref']
            info[key] = (e[0][0] / e[0][1] +
                         e[1][0] / e[1][1] / 60 +
                         e[2][0] / e[2][1] / 3600
                         ) * (-1 if ref in ['S', 'W'] else 1)

    if 'Latitude' in info and 'Longitude' in info:
        return [info['Latitude'], info['Longitude']]


def gray_to_black_white(img, threshold):
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Gray', grayImg)
    (tresh, bwImg) = cv2.threshold(grayImg, threshold, 255, cv2.THRESH_BINARY)
    cv2.imshow('BW', bwImg)

def adjust_brightness(input_image, output_image, factor):
    # image = Image.open(input_image)
    enhancer_object = ImageEnhance.Brightness(input_image)
    out = enhancer_object.enhance(factor)
    out.save(output_image)

def adjust_contrast(input_image, output_image, factor):
    image = Image.open(input_image)
    enhancer_object= ImageEnhance.Contrast(image)
    out = enhancer_object.enhance(factor)
    out.save(output_image)

def adjust_sharpness(input_image, output_image, factor):
    image = Image.open(input_image)
    enhancer_object = ImageEnhance.Sharpness(image)
    out = enhancer_object.enhance(factor)
    out.save(output_image)

def get_HSV(imgPath):
    img = cv2.imread(path_to_img, 1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    list = cv2.split(hsv)
    return list

def keypoint_detect(img):
    # Initiate ORB detector
    orb = cv2.ORB_create()
    # find the keypoints with ORB
    kp = orb.detect(img, None)
    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)
    print("Keypoints")
    for keypoint in kp:
        print(keypoint.pt)
    # draw only keypoints location,not size and orientation
    img2 = cv2.drawKeypoints(img, kp, None, color=(0, 255, 0), flags=0)
    plt.imshow(img2), plt.show()

    return len(kp)

def getTopKeyPointRegion():
    pass

def sliding_window(img, imgPath, totalKP):
    imgCopy = img.copy()
    imgCopyPIL = Image.open(imgPath)
    startPtx = int(0)
    startPty = int(0)
    toIncrement = int(100)
    density = 0
    densitySearch = int(0.05 * totalKP)  # looking for 5% of keypoints in any box 100x100
    maxDensityBoxes0 = []  # for the first (x,y) point for a rectangle
    maxDensityBoxes1 = []  # for the second (x,y) point for a rectangle, 9x6 for 1773x1182

    height = int(math.floor(imgCopy.shape[0]))
    # print(height)
    length = int(math.floor(imgCopy.shape[1]))
    # print(length)

    # add conditions for left edge, right edge, bottom and top edges if statements
    for i in range(0, int(height / toIncrement)):
        startPtx = int(0)
        y0 = startPty
        y1 = startPty + toIncrement
        for j in range(0, int(length / toIncrement)):
            density = 0
            x0 = startPtx
            x1 = startPtx + toIncrement
            startSetx = (x0, y0)
            box = cv2.rectangle(imgCopy, (int(x0), int(y0)), (int(x1), int(y1)), (255, 0, 0), 2)
            # cv2.imshow('imgbox', imgCopy)
            # cv2.waitKey(0)
            for k, keypoint in enumerate(kp):
                if x0 <= keypoint.pt[0] <= x1 and y0 <= keypoint.pt[1] <= y1:
                    density = density + 1
            if density >= densitySearch:
                # print(density)
                # print((x0, y0))
                # print((x1, y1))
                maxDensityBoxes0.append((x0, y0))
                maxDensityBoxes1.append((x1, y1))
            startPtx = startPtx + 100
        startPty = startPty + 100

    croppedImgList = []
    for i, pts in enumerate(maxDensityBoxes0):
        print(maxDensityBoxes0[i])
        if (maxDensityBoxes0[i][0] > 0 and maxDensityBoxes0[i][1] > 0) and (maxDensityBoxes1[i][0] > 0 and
                                                                            maxDensityBoxes1[i][1] > 0):
            newImg0 = imgCopyPIL.crop(
                (maxDensityBoxes0[i][0] - 50, maxDensityBoxes0[i][1] - 50, maxDensityBoxes1[i][0] + 50,
                 maxDensityBoxes1[i][1] + 50))
            newImg = newImg0.resize((350, 350))
            newImg.show('croppedimg', newImg)
            croppedImgList.append(newImg)
        else:
            newImg0 = imgCopyPIL.crop((maxDensityBoxes0[i][0], maxDensityBoxes0[i][1], maxDensityBoxes1[i][0],
                                       maxDensityBoxes1[i][1]))
            newImg = newImg0.resize((350, 350))
            newImg.show('croppedimg', newImg)
            croppedImgList.append(newImg)

    path = 'C:/Users/SYL/Desktop'
    for j, imgs in enumerate(croppedImgList):
        # cv2.imwrite(os.path.join(croppedImgList[j]))
        croppedImgList[j].save(path + 'crop_' + str(j) + '.jpg', 'JPEG', optimize=True)

def enhanceDetails(img):
    newImg = cv2.detailEnhance(img, sigma_s=5, sigma_r=0.05)
    cv2.imshow("Details Enhanced", newImg)
    # return newImg

def edgePreserve(img):
    newImg = cv2.edgePreservingFilter(img, flags=2, sigma_s=60, sigma_r=0.4)
    cv2.imshow("Edge Preserving Filter", newImg)
    # return newImg

path_to_img = 'C:/Users/SYL/Desktop/CPP-AUVSI/img-recog/images/crop_1.jpg'

# adjust_brightness(path_to_img, 'darkened.jpg', 1.7)
# adjust_contrast(path_to_img, 'contrasted.jpg', 1.7)
# adjust_sharpness(path_to_img, 'sharp.jpg', 1.7)
#
# path_to_darkened_img = 'darkened.jpg'
# path_to_contrasted_img = 'contrasted.jpg'
# path_to_sharp_img = 'sharp.jpg'


# 2nd parameter is flag: 1(default) for color, 0 for grayscale, and -1 for unchanged
img = cv2.imread(path_to_img, 0)
img2 = cv2.imread(path_to_img, 1)
hsv = get_HSV(path_to_img)
# cv2.imshow("HSV", hsv)
h = hsv[0]
s = hsv[1]
v = hsv[2]
cv2.imshow("H", h)
print("height: " + str(h.shape[0]))
print("width: " + str(h.shape[1]))


keypoint_detect(h)
# keypoint_detect(s)
# cv2.imshow("S", s)
# cv2.imshow("V", v)
# edgePreserve(h)
# enhanceDetails(h)

# print("HSV: " + str(len(get_HSV(path_to_img))));

# dst = cv2.GaussianBlur(s, (5, 5), cv2.BORDER_DEFAULT)
#
# cv2.imshow("Gaussian Smoothing", dst)
# canny = cv2.Canny(dst, 25, 50, )
# cv2.imshow('Lines1', canny)
#
# morph1= cv2.adaptiveThreshold(h, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 1);
# canny = cv2.Canny(h, 25, 50, )
#
# cv2.imshow('Image', h)
# cv2.imshow('Transformed', morph1)
# cv2.imshow('Lines2', canny)

# to use with cv2
# image = np.array(croppedImgList[1])

# image = cv2.imread('C:/Users/SYL/Desktop/CPP-AUVSI/img-recog/images/crop_1.jpg')
# cv2.imshow('Original Image', image)

# gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow('Gray', gray_img)


# Enhance details
# dst = cv2.detailEnhance(image, sigma_s=5, sigma_r=0.05)
# cv2.imshow("Detail Enhanced", dst)

# Edge Preserving Filter
# dst2 = cv2.edgePreservingFilter(image, flags=2, sigma_s=60, sigma_r=0.4)
# cv2.imshow("Edge Preserving Filter", dst2)
#
# new_image = np.zeros(dst.shape, dst.dtype)

# Gamma Correction
# lookUpTable = np.empty((1, 256), np.uint8)
# gamma = .4
# for i in range(256):
#     lookUpTable[0,1] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
# res = cv2.LUT(new_image, lookUpTable)
#
# alpha = 1.0 # Simple contrast control
# beta = 20 # Simple Brightness control
#
# new_image = cv2.convertScaleAbs(dst, alpha=alpha, beta=beta)
# cv2.imshow('New Image', new_image)

# lookUpTable = np.empty((1, 256), np.uint8)
# gamma = .2
# for i in range(256):
#     lookUpTable[0,1] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
# res = cv2.LUT(new_image, lookUpTable)
# cv2.imshow('Gamma Correction', res)

# grayImg = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
# cv2.imshow('Gray img', grayImg)

# adjust_brightness(croppedImgList[1], 'bright.jpg', 1.7)

# image = cv2.imread('bright.jpg', 0)
# edges = cv2.Canny(image, 100, 200)
#
# plt.subplot(121),plt.imshow(image,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# plt.show()

# cv2.imshow("Target", image)
#
# dst = cv2.fastNlMeansDenoisingColored(image, None, 5, 5, 7, 21)
#
# plt.subplot(121),plt.imshow(img)
# plt.subplot(122),plt.imshow(dst)
# plt.show()

# # Create an SR object
# sr = dnn_superres.DnnSuperResImpl_create()
#
# # # Read image
# image = cv2.imread("bright.jpg")
# # cv2.imshow("img", image)
#
# # Read the desired model
# path = "C:/Users/SYL/Desktop/CPP-AUVSI/img-recog/superres/LapSRN_x4.pb"
# sr.readModel(path)
#
# # Set teh desired model and scale to get correct pre- and post-processing
# sr.setModel("lapsrn", 4)
#
# # Upscale the image
# result = sr.upsample(image)
#
# # Save the image
# cv2.imwrite("./upscaled.png", result)


# avgBlur = cv2.blur(target, (5,5))
# cv2.imshow('Averaging', avgBlur)

# grayImg = cv2.cvtColor(avgBlur, cv2.COLOR_BGR2GRAY)
# cv2.imshow('Gray img', grayImg)
#
# (tresh, bwImg) = cv2.threshold(grayImg, 100, 255, cv2.THRESH_BINARY)
# cv2.imshow('B/W Img', bwImg)

# Guassian Filtering
# target = cv2.imread("upscaled.png")
# gaussianBlur = cv2.GaussianBlur(target, (5,5), 0)
# cv2.imshow("Gasussian", gaussianBlur)
# edges = cv2.Canny(gaussianBlur, 100, 200)
# cv2.imshow("Canny", edges)
# gray_to_black_white(gaussianBlur, 93)

# Median Filtering (great for removing salt and pepper noises)
# median = cv2.medianBlur(target, 5)
# cv2.imshow('Median', median)
# gray_to_black_white(median, 97)

# Bilateral Filtering (Preserves edges)
# bilateralBlur = cv2.bilateralFilter(target, 9,75,75)
# cv2.imshow('Bilateral', bilateralBlur)
# gray_to_black_white(bilateralBlur, 95)

# Box Filter
# boxfilter = cv2.boxFilter(target, ())

# Adaptive Thresholding Gaussian C
# upscaledImg = cv2.imread("upscaled.png")
# grayImg = cv2.cvtColor(upscaledImg, cv2.COLOR_BGR2GRAY)
# # cv2.imshow("Gray", grayImg)
# median = cv2.medianBlur(new_image, 5)
# # cv2.imshow("Median", median)
# grayImg = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
# # cv2.imshow('Gray img', grayImg)
# th = cv2.adaptiveThreshold(grayImg,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11 ,2)
# # cv2.imshow("Adaptive Thresh Gaussain C", th)


# Wait for a key-stroke to close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()


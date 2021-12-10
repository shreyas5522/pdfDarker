from pdf2image import convert_from_path
import cv2
import numpy as np
from PIL import Image, ImageEnhance
from fpdf import FPDF
import os
from alive_progress import alive_bar
from PIL import Image


def invertLight(bgr):
    # Convert to hls
    hls = cv2.cvtColor(bgr, cv2.COLOR_BGR2HLS)

    # Extract hls
    h, l, s = cv2.split(hls)

    # Merger
    new_hls = cv2.merge([h, 255 - l, s])

    # Return bgr
    return cv2.cvtColor(new_hls, cv2.COLOR_HLS2BGR)


def resizing(img, percent):
    width = int(img.shape[1] * percent)
    height = int(img.shape[0] * percent)
    dim = (width, height)

    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


def crop(img, L, R, U, D):
    # Crop image: Left, Right, Up, Down percentages
    row, col, _ = img.shape

    left = int(L * col)
    right = col - int(R * col)
    up = int(U * row)
    down = row - int(D * row)

    return img[up:down, left:right]


def rightBottom(img, rbVer, rbHor):
    # Cover up page numbers
    row, col, _ = img.shape
    img[int((1 - rbVer) * row):, int((1 - rbHor) * col):] = (0, 0, 0)  # 0-255

    return img


def leftBottom(img, lbVer, lbHor):
    # Cover up page numbers
    row, col, _ = img.shape
    img[int((1 - lbVer) * row):, 0:int(lbHor * col)] = (0, 0, 0)

    return img


def rightTop(img, rtVer, rtHor):
    # Cover up logos
    row, col, _ = img.shape
    img[0:int(rtVer * row), int((1 - rtHor) * col):] = (0, 0, 0)

    return img


def black(img):
    # Black space at the bottom
    black_img = img.copy()
    black_img[:, :] = (0, 0, 0)
    new_img = cv2.vconcat([img, black_img])

    return new_img


def dotting(dots, img):
    # Black dots at the bottom
    row, col, _ = dots.shape
    row_img, col_img, _ = img.shape
    row_d = int(row_img * col / col_img)
    small_img = cv2.resize(img, (col, row_d), interpolation=cv2.INTER_AREA)
    row_s, col_s, _ = small_img.shape
    dots[0:row_s, 0:col_s] = small_img

    return dots


##########################################################################################
# MAIN
FILE_NAME = input('Enter file name: ')
FILE_NEW = FILE_NAME[:-4] + 'v1.pdf'
COURSE = FILE_NAME.split('_')[0].lower()

# Open images
images = convert_from_path(FILE_NAME)
blackDots = convert_from_path('./Textures/Dots.pdf')
blackDots = cv2.cvtColor(np.array(blackDots[0]), cv2.COLOR_RGB2BGR)

# Params
testing = False
cropping = True
blacking = True
dotGrid = False
corners = []
rtVer, rtHor, rbVer, rbHor, lbVer, lbHor = 0, 0, 0, 0, 0, 0

# Resizing
smaller = False
SCALE = 0.4

# Crop variables
LEFT = 0
RIGHT = 0
UP = 0
DOWN = 0

if COURSE == 'pe':
    DOWN = 0.12
elif COURSE == 'rss':
    DOWN = 0.12
elif COURSE == 'mcp':
    DOWN = 0.12
elif COURSE == 'ano':
    DOWN = 0.12
elif COURSE == 'nm':
    DOWN = 0.0
    UP = 0.08
elif COURSE == 'srsp':
    DOWN = 0.12
elif COURSE == 'cv':
    LEFT = 0.044
    DOWN = 0.04
    corners = ['rb', 'rt']
    rbVer, rbHor = 0.04, 0.04
    rtVer = 0.09
    rtHor = 0.25

# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

# Testing
if testing:
    ori = images[6]
    ori = cv2.cvtColor(np.array(ori), cv2.COLOR_RGB2BGR)
    # ori = cv2.cvtColor(np.array(ori), cv2.COLOR_RGB2HLS)
    ori = resizing(ori, SCALE)
    blackTst = resizing(blackDots, SCALE)

    tst = ori

    if cropping:
        tst = crop(tst, LEFT, RIGHT, UP, DOWN)

    tst = invertLight(tst)

    if 'rb' in corners:
        tst = rightBottom(tst, rbVer, rbHor)
    if 'rt' in corners:
        tst = rightTop(tst, rtVer, rtHor)
    if 'lb' in corners:
        tst = leftBottom(tst, lbVer, lbHor)

    if blacking:
        tst = black(tst)

    if dotGrid:
        tst = dotting(blackTst, tst)

    cv2.imshow('Original', ori)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imshow('Cropped', tst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Processing
invImages = []
# A4 = 210x297mm
# pdf = FPDF()
height = int(210 * images[0].size[1] / images[0].size[0])
pdf = FPDF(orientation='P', unit='mm', format=(210, height))

if not testing:
    thislist = []

    with alive_bar(len(images), bar='bubbles', spinner='dots_waves2') as bar:

        for i in range(len(images)):
            img = cv2.cvtColor(np.array(images[i]), cv2.COLOR_RGB2BGR)

            if cropping:
                img = crop(img, LEFT, RIGHT, UP, DOWN)

            img = invertLight(img)

            if 'rb' in corners:
                img = rightBottom(img, rbVer, rbHor)
            if 'rt' in corners:
                img = rightTop(img, rtVer, rtHor)
            if 'lb' in corners:
                img = leftBottom(img, lbVer, lbHor)

            if blacking:
                img = black(img)

            if dotGrid:
                img = dotting(blackDots, img)

            if smaller:
                img = resizing(img, SCALE)


            # cv2.imwrite('img{}.png'.format(i), img)
            new_img = Image.fromarray(img)
            thislist.append(new_img)
            # pdf.add_page()
            # pdf.image(new_img, x=0, y=0, w=210)
            # pdf.image('img{}.png'.format(i), x=0, y=0, w=210)
            # os.remove('img{}.png'.format(i))

            # print("Page ", i+1, " of ", len(images), "- Percentage: ", (i+1) * 100 /len(images))
            bar()

    # Convert to PDF
    out_filename = "cumv1.pdf"
    thislist[0].save(out_filename, save_all=True, append_images=thislist[1:])
    print("Saving ", FILE_NEW, ' ...')
    #pdf.output(FILE_NEW, 'F')

print("Done :D")

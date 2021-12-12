import threading
import tkinter.ttk

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

class pdfDark:
    def __init__(self):
        self.file_name = ""
        self.file_name_new = ""
        self.course = ""
        self.images = []
        self.images_invert = []

        # https://a-size.com/a4-paper-size/
        # A4 = 210x297mm = 2480x3508px with 300ppi
        self.width = 2480
        self.height = 3508
        self.resolution = 300

    def open_file(self, filename):
        print(filename)

        self.file_name = filename
        self.file_name_new = self.file_name[:-4] + 'v1.pdf'
        self.course = self.file_name.split('_')[0].lower()

        # Open images
        print("test")
        self.images = convert_from_path(filename)
        print("test2")

    def cum(self, filename):
        print(filename)
        self.images = convert_from_path(filename)

    def convert(self):
        # Processing
        self.height = int(self.width * self.images[0].size[1] / self.images[0].size[0])

        for i in range(len(self.images)):
            # new_img = self.invert_light(self.images[i]).resize((self.width, self.height))
            # self.images_invert.append(new_img)
            img = cv2.cvtColor(np.array(self.images[i]), cv2.COLOR_RGB2BGR)
            new_img = Image.fromarray(invertLight(img))
            self.images_invert.append(new_img)

    def save(self, filename):
        # Convert to PDF
        self.images_invert[0].save(filename, save_all=True, append_images=self.images_invert[1:], resolution=self.resolution)
        print("Saving ", filename, ' ...')

    def invert_light(self, img_rgb):
        # Convert to hls
        # May need to use np.array(img_rgb)
        hls = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HLS)

        # Extract hls
        h, l, s = cv2.split(hls)

        # Merger
        new_hls = cv2.merge([h, 255 - l, s])

        # Return rgb image
        new_rgb = cv2.cvtColor(new_hls, cv2.COLOR_HLS2RGB)

        return Image.fromarray(new_rgb)

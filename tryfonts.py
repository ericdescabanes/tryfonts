#! /usr/bin/env python3

import matplotlib.font_manager as fm
import cv2
from PIL import Image     as PIL_Image
from PIL import ImageDraw as PIL_ImageDraw
from PIL import ImageFont as PIL_ImageFont
import numpy as np
import os
import argparse


parser = argparse.ArgumentParser(description='Display a sample text with all the fonts in default font paths.')
parser.add_argument('--text', help='sample text to use with each font', default='Greetings Professor Falken')
parser.add_argument('--size', help='font size to use (in points)'     , default='14')
parser.add_argument('--verbose', help='list the full path for each font', action=argparse.BooleanOptionalAction)
args = parser.parse_args()


font_paths = sorted(fm.findSystemFonts())


line_height = 2 * int(args.size)
margin = 20
width  = 1400
height = 1000
lines_per_page = int((height - 2 * margin) / line_height)


line_on_page = 0
page = 0

images = []

def convertImageOfPage(page):
    images[page] = cv2.cvtColor(np.array(images[page]), cv2.COLOR_RGB2BGR)

for index, font_path in enumerate(font_paths):
    line_on_page += 1
    if line_on_page > lines_per_page:
        convertImageOfPage(page)
        line_on_page = 1
        page += 1
    if line_on_page == 1:
        images.append(PIL_Image.new(mode="RGB", size=(width, height)))
        draw  = PIL_ImageDraw.Draw(images[page])

    text_X_col1 = margin
    text_X_col2 = int(width * 15 / 100)
    text_X_col3 = int(width * 50 / 100)
    text_Y = margin + line_height * (index % lines_per_page)

    try:
        font = PIL_ImageFont.truetype(font_path, int(args.size))
    except:
        print(f"Warning: failed reading font {font_path}. Skipping it.")
        continue

    draw.text((text_X_col1, text_Y), f"{index:03}"                   , font=font)
    draw.text((text_X_col2, text_Y), f"{str(args.text)}"             , font=font)
    draw.text((text_X_col3, text_Y), f"{os.path.basename(font_path)}", font=font)
    if args.verbose:
        print(f"{index:03}  {font_path}")

convertImageOfPage(page)

alpha_slider_max = page
title_window = 'Font samples'

def on_trackbar(val):
    cv2.imshow(title_window, images[val])

cv2.namedWindow(title_window)
trackbar_name = "Page"
cv2.createTrackbar(trackbar_name, title_window , 0, alpha_slider_max, on_trackbar)
on_trackbar(0)

print("Press Q in the window to Quit")

wait_time_ms = 1000
while cv2.getWindowProperty(title_window, cv2.WND_PROP_VISIBLE) > 0:
    keyCode = cv2.waitKey(wait_time_ms)
    if (keyCode & 0xFF) == ord("q"):
        cv2.destroyAllWindows()
        break


import math

from PIL import Image
import colorsys
import shutil
import cv2
import numpy as np
import pandas as pd

NR_IMAGES = 1892
RES_WIDTH = 512
RES_HEIGHT = 512
BLACK_PIXEL_THRESHOLD = 100
BAD_IMAGE_THRESHOLD = 87000
PATH = "C:\\Users\\Luca\\Desktop\\spaceye\\spaceye\\spaceye"
GOOD_IMAGES_PATH = PATH + "\\good_images"
BAD_IMAGES_PATH = PATH + "\\bad_images"
NON_OCEAN_IMAGES_PATH = PATH + "\\non_ocean_images"
OCEAN_IMAGES_PATH = PATH + "\\ocean_images"
SAVE_IMAGES = True
H_FOV = 53
V_FOV = 41
XC = 204
YC = 230

albedo_list = []
good_images = 0
non_ocean_images = 0

'''
TRAIECTORIA DIN MIJLOC!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''

elev_list = [0] * 1893
ind = 0
with open('/elevations.txt', 'r') as f:
    while True:
        l = f.readline()
        if l == "":
            break
        ind += 1
        elev_list[ind] = int(l)


data = pd.read_csv(r'C:\\Users\\Luca\\Desktop\\spaceye\\spaceye\\spaceye\\data.csv')
df = pd.DataFrame(data, columns= ['Date/time', 'Latitude', 'Longitude', 'ISS_Height'])

latitudes, longitudes, times, heights = [], [], [], []
points = []

def convert_line_to_value(line):
    s = ""
    v = []
    for c in line:
        if c == 'd' or c == 'e' or c == 'g' or c == ' ' or ord(c) == 39 or ord(c) == 34:
            if s != '':
                v.append(float(s))
            s = ""
        else:
            s += c

    value = v[0] + v[1] / 60 + v[2] / 3600
    return value


for i in range(1892):
    line = df.iloc[i]
    times.append(line[0])
    latitudes.append(convert_line_to_value(line[1]))
    longitudes.append(convert_line_to_value(line[2]))
    heights.append(line[3])


def is_good_image(im, img, img_cv):
    black_pixels = 0

    for x in range(0, RES_WIDTH):
        for y in range(0, RES_HEIGHT):
            if (x - XC)**2 + (y - YC)**2 >= 235 * 235:
                continue

            nuance = im[x, y][0] + im[x, y][1] + im[x, y][2]
            black_pixels += (nuance <= BLACK_PIXEL_THRESHOLD)

            if black_pixels >= BAD_IMAGE_THRESHOLD:
                return False

    return True


for i in range(729, NR_IMAGES + 1):
    image_path = PATH + "\\image" + str(i) + ".jpg"
    img = Image.open(image_path)
    im = img.load()
    img_cv = cv2.imread(image_path)

    is_good = is_good_image(im, img, img_cv)

    if i % 50 == 0:
        print("Checking image #", i)

    if is_good:
        good_images += 1
        if SAVE_IMAGES:
            shutil.copy(image_path, GOOD_IMAGES_PATH)

        if elev_list[i] > 0:
            non_ocean_images += 1

            print('xd')

            '''average_albedo = 0
            cnt = 0
            for x in range(0, RES_WIDTH):
                for y in range(0, RES_HEIGHT):
                    if (x - XC) ** 2 + (y - YC) ** 2 >= 235 * 235:
                        continue

                    (h, s, v) = colorsys.rgb_to_hsv(im[x, y][0], im[x, y][1], im[x, y][2])
                    albedo = (im[x, y][0] + im[x, y][1] + im[x, y][2]) // 3

                    h *= 256
                    h = round(h)

                    if albedo >= 190:  # clouds
                        img.putpixel((x, y), (255, 0, 0))
                        continue

                    average_albedo += albedo
                    cnt += 1

            average_albedo /= cnt
            albedo_list.append(average_albedo)'''

            RES = 30
            img = img.resize((RES, RES))
            im = img.load()

            h = heights[i - 1]
            xc = latitudes[i - 1]
            yc = longitudes[i - 1]

            print(xc, yc)

            HALF = RES // 2

            # tan(alpha / 2) = half * d / h
            # tan(beta) = x * d / h

            t1 = math.tan(V_FOV / 2 * 180 / math.pi)
            t2 = math.tan(H_FOV / 2 * 180 / math.pi)

            for x in range(RES):
                for y in range(RES):
                    nuance = im[x, y][0] + im[x, y][1] + im[x, y][2]

                    if nuance <= BLACK_PIXEL_THRESHOLD:
                        continue

                    if nuance // 3 >= 190: #cloud
                        continue

                    t3 = t1 / HALF * (x - HALF)
                    x2 = xc + h * t3 / 111000

                    t4 = t2 / HALF * (y - HALF)
                    y2 = yc + h * t4 / 111000

                    points.append((i, x2, y2, x, y, nuance // 3))

            if SAVE_IMAGES:
                shutil.copy(image_path, NON_OCEAN_IMAGES_PATH)
        elif elev_list[i] <= 0:
            if SAVE_IMAGES:
                shutil.copy(image_path, OCEAN_IMAGES_PATH)

    else:
        if SAVE_IMAGES:
            shutil.copy(image_path, BAD_IMAGES_PATH)

print(100.0 * good_images / NR_IMAGES, "% good images (non pitch-black images)")
print(100.0 * non_ocean_images / good_images, "% non ocean images")

import csv

f = open('data3.csv', 'w', newline='')
writer = csv.writer(f)
header = ['Index', 'X_pixel', 'Y_pixel', 'I', 'J', 'Albedo']

writer.writerow(header)

for i in range(len(points)):
    row = []
    v = points[i]

    for j in range(6):
        row.append(v[j])

    writer.writerow(row)

print(albedo_list)

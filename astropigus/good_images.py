import csv
import glob
from PIL import Image
import colorsys
import matplotlib.pyplot as plt
import pandas as pd
import os

RES_WIDTH = 512
RES_HEIGHT = 512
XC = 204
YC = 230
elev_list_2 = []
lat_list, long_list, time_list = [], [], []
index_list = []
albedo_list = [139.2937731905608, 140.99508072046748, 143.36994063139315, 146.31142475877644, 145.9846647683148, 143.05758914808345, 139.66515636105188, 134.0636943287716, 131.10591626858363, 129.07582308537405, 126.5194933232397, 123.66238502473774, 123.08942434210526, 123.32454830580112, 127.14658491373164, 132.34699935367013, 136.3511311596316, 141.00262390395378, 146.56705872785125, 152.42889278472458, 165.19556532161405, 163.10483582772275, 159.86404603085697, 157.40743739037478, 156.98978805796136, 155.49149758254472, 153.64522161014807, 152.24524828341129, 149.39704287921091, 141.131572690528, 135.16895710960878, 131.09923077643796, 123.80445328105009, 122.33495615686697, 133.33509374976288, 149.3150278542184, 154.06524483876473, 139.4679896408133, 40.13664942914309, 44.07318173722021, 48.45885628792286, 52.97341344526839, 57.971478103923246, 62.79013364523158, 145.29289238617673, 145.94827882775377, 136.41970190229742, 140.162255005503, 152.92687494243935, 142.87692817060437, 137.37288410929528, 141.10518296202238, 142.78715384041203, 146.53134564048577, 149.00670865591357, 148.84127671419293, 148.51563800499392, 146.6661392158391, 146.35302040007923, 145.4989182608426, 144.55878858024693, 143.94292644482022, 142.685030494405, 142.0050330008137, 143.1355498921167, 142.6875324115812, 142.8456775609374, 144.582257939281, 146.34799579291808, 146.684411570386, 146.74609527235663, 148.44224053952792, 149.8084242240749, 150.15008486458564, 149.7358466215441, 150.7126412325752, 151.69509992425566, 151.86956369370947, 152.70590848208184, 153.05762525110688, 153.5199780953512, 151.71812935864094, 148.99522679090552, 145.83751551720943, 141.56949498342323, 136.03099827297137, 130.59567526154495, 125.0872954520825, 115.53847382328175, 105.10335791289663, 94.53366709300201, 86.51854209997595, 79.99873254724295, 74.44662944970212, 69.62842911400287, 65.32936519926277, 61.30529485839194, 56.359769889753686, 51.82029909582584, 48.36196056779525, 44.76673731454931, 41.155763739232135, 38.285981441573014]
elev_list = [0] * 1892
cnt = 0

data = pd.read_csv(r'C:\\Users\\Luca\\Desktop\\spaceye\\spaceye\\spaceye\\data.csv')
df = pd.DataFrame(data, columns= ['Date/time', 'Latitude', 'Longitude'])

latitudes, longitudes, times = [], [], []

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

with open('elevations.txt', 'r') as f:
    while True:
        l = f.readline()
        print(l, cnt)
        if l == "":
            break
        elev_list[cnt] = int(l)
        cnt += 1

id = 0
path = "C:\\Users\\Luca\\Desktop\\spaceye\\spaceye\\spaceye\\non_ocean_images\\"
for image in sorted(os.listdir(path), key=len):
    img = Image.open(path + image)
    im = img.load()

    i = len(image) - 1
    while image[i] != 'e':
        i -= 1

    i += 1

    nr = 0
    while image[i] != '.':
        nr = nr * 10 + int(image[i])
        i += 1

    print(image, nr, id)
    id += 1
    index_list.append(nr)
    elev_list_2.append(elev_list[nr - 1])
    lat_list.append(latitudes[nr - 1])
    long_list.append(longitudes[nr - 1])
    time_list.append(times[nr - 1])

f = open('data2.csv', 'w', newline='')
writer = csv.writer(f)
header = ['Index', 'Time', 'Latitude', 'Longitude', 'Albedo', 'Elevation']

writer.writerow(header)

for i in range(len(albedo_list)):
    row = []
    row.append(index_list[i])
    row.append(time_list[i])
    row.append(lat_list[i])
    row.append(long_list[i])
    row.append(albedo_list[i])
    row.append(elev_list_2[i])
    writer.writerow(row)

print(len(albedo_list))
print(len(elev_list_2))

plt.scatter(albedo_list, elev_list_2)
plt.xlabel("Albedo")
plt.ylabel("Elevation")
plt.show()
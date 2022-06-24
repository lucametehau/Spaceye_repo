import csv
import pandas as pd

cnt = 0
elev_list = [0] * 50823

with open('elevations2.txt', 'r') as f:
    while True:
        l = f.readline()
        print(l, cnt)
        if l == "":
            break
        elev_list[cnt] = int(l)
        cnt += 1


data = pd.read_csv(r'/data3.csv')
df = pd.DataFrame(data, columns= ['Index', 'X_pixel', 'Y_pixel', 'I', 'J', 'Albedo'])

data2 = pd.read_csv(r'C:\\Users\\Luca\\Desktop\\spaceye\\spaceye\\spaceye\\data.csv')
df2 = pd.DataFrame(data2, columns=['Date/time'])

f = open('final_data_water.csv', 'w', newline='')
writer = csv.writer(f)
f2 = open('final_data_land.csv', 'w', newline='')
writer2 = csv.writer(f2)
header = ['Index', 'Date/time', 'Latitude', 'Longitude', 'Albedo', 'Elevation', 'X_in_image', 'Y_in_image']

writer.writerow(header)
writer2.writerow(header)

for i in range(cnt):
    row = []
    l1 = df.iloc[i]
    index = int(l1[0])
    l2 = df2.iloc[index]
    row.append(index)
    row.append(l2[0])
    row.append(l1[1])
    row.append(l1[2])
    row.append(l1[5])
    row.append(elev_list[i])
    row.append(l1[3])
    row.append(l1[4])

    if elev_list[i] <= 0:
        writer.writerow(row)
    else:
        writer2.writerow(row)
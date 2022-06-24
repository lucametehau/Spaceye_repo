import requests
import pandas as pd
import geocoder
import elevation
import threading
import re

from socket import timeout

data = pd.read_csv(r'/data3.csv')
df = pd.DataFrame(data, columns= ['X_pixel', 'Y_pixel'])
print(len(df))

import urllib.request
import json
import random
import math
import matplotlib.pyplot as plt

lock = threading.Lock()

# TESTING
'''P1=[-38.7070167057315, 19.0131651491659]
P2=[25.9253661080903, 179.105414152224]'''

'''P1 = [27.986065, 86.922623]
P2 = [27.986065, 86.922623]'''

#LATITUDE AND LONGITUDE LIST
lat_list = []
lon_list = []

threads = 605
s = int(len(df))

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

# GENERATING POINTS
for i in range(s):
    line = df.iloc[i]

    #lat_step = convert_line_to_value(line[0])
    #lon_step = convert_line_to_value(line[1])
    lat_step = line[0]
    lon_step = line[1]
    #print(str(lat_step) + ' ' + str(lon_step))
    lat_list.append(lat_step)
    lon_list.append(lon_step)

i_list = list(range(0, s))

#print(i_list)


'''#CONSTRUCT JSON
d_ar=[{}]*len(lat_list)
for i in range(len(lat_list)):
    d_ar[i]={"latitude":lat_list[i],"longitude":lon_list[i]}
location={"locations":d_ar}
json_data=json.dumps(location,skipkeys=int).encode('utf8')'''

def get_json_data(left, right):
    lock.acquire()
    #print(str(left) + ' ' + str(right))
    lg = right - left
    d_ar = []
    for j in range(left, right):
        d_ar.append({"latitude": lat_list[j], "longitude": lon_list[j]})
    location = {"locations": d_ar}
    #print(location)
    json_data = json.dumps(location, skipkeys=int).encode('utf8')
    lock.release()
    return json_data

elev_list = [0] * s

batches_done = 0

batch_size = int(s / threads)
nr_batches = threads

solved = [False] * 10000

for i in range(10000):
    solved[i] = False

def pick_random_unfinished(): # find unfinished batch
    unfinished = []

    for i in range(threads):
        if solved[i] == False:
            unfinished.append(i)

    if len(unfinished) == 0:  # all tasks done, exit
        return -1

    id = unfinished[random.randint(0, len(unfinished) - 1)]  # pick random unfinished batch

    return id

# testing if batch size works

'''json_data = get_json_data(batch_size * 0, batch_size * (0 + 1))
#print(json_data)
url = "https://api.open-elevation.com/api/v1/lookup"
response = urllib.request.Request(url,json_data,headers={'Content-Type': 'application/json'})
fp = urllib.request.urlopen(response)'''

# so what this does is:
# it requests elevation for a given list of latitudes and longitudes
# there are limitations to how big the request is, so we split the lists into batches
# using multithreading, we request at the same time for each batch, so chance of
# one request being returned is higher
# improvement: when one thread's batch is finished, pick a random unfinished batch
# and request for it. this way, the chance that that batch gets solved is higher
# after we are done, we plot the data

def make_request(id):

    cnt_request = 0
    thread_id = id
    global batches_done
    while True:

        if solved[id] == True: # if batch was solved by another thread, pick a new one
            id = pick_random_unfinished()

            if id == -1: # no more tasks left
                break

        lock.acquire() # for better printing

        print('SENDING REQUEST ' + str(cnt_request) +
              ' FOR BATCH ' + str(id) +
              ' FOR THREAD ' + str(thread_id))
        cnt_request += 1

        lock.release()

        # try request batch
        try:
            #SEND REQUEST

            json_data = get_json_data(batch_size * id, batch_size * (id + 1))
            #print(json_data)
            url = "https://api.open-elevation.com/api/v1/lookup"
            response = urllib.request.Request(url,json_data,headers={'Content-Type': 'application/json'})
            fp = urllib.request.urlopen(response)
        except:
            continue
        else:

            lock.acquire()

            #RESPONSE PROCESSING
            res_byte=fp.read()
            res_str=res_byte.decode("utf8")
            js_str=json.loads(res_str)
            #print (js_mystr)
            fp.close()

            #GETTING ELEVATION
            response_len=len(js_str['results'])
            print('GOT A RESPONSE FOR BATCH ' + str(id) + ' FROM THREAD ' + str(thread_id) + ' len = ' + str(response_len))

            if solved[id] == False: # 2 threads might finish the same task at the same time
                batches_done += 1

            print(str(batches_done) + ' BATCHES DONE')
            for j in range(response_len):
                elev_list[batch_size * id + j] = js_str['results'][j]['elevation']
                #print(js_str['results'][j]['elevation'])

            cnt = 0
            for i in solved:
                cnt += i

            print(cnt, batches_done)
            if cnt == nr_batches:
                with open('elevations2.txt', 'w') as f:
                    for elev in elev_list:
                        f.write(str(elev))
                        f.write('\n')

                exit(0)

            solved[id] = True

            id = pick_random_unfinished()

            if id == -1: # no more tasks left
                lock.release()
                break

            lock.release()

calc = True

if calc == True:

    t = []

    for i in range(threads):
        t.append(threading.Thread(target=make_request, args=(i,)))

    for i in range(threads):
        t[i].start()

    for i in range(threads):
        t[i].join()

    # write calculated data, might help

    with open('elevations2.txt', 'w') as f:
        for elev in elev_list:
            f.write(str(elev))
            f.write('\n')
else:
    cnt = 0
    with open('elevations2.txt', 'r') as f:
        while True:
            l = f.readline()
            print(l, cnt)
            if l == "":
                break
            elev_list[cnt] = int(l)
            cnt += 1

#BASIC STAT INFORMATION
'''
mean_elev=round((sum(elev_list)/len(elev_list)),3)
min_elev=min(elev_list)
max_elev=max(elev_list)
index=i_list[-1]

#PLOT ELEVATION PROFILE
base_reg=0
plt.figure(figsize=(10,4))
plt.plot(i_list,elev_list)
plt.plot([0,index], [min_elev,min_elev],'--g',label='min: '+str(min_elev)+' m')
plt.plot([0,index], [max_elev,max_elev],'--r',label='max: '+str(max_elev)+' m')
plt.plot([0,index], [mean_elev,mean_elev],'--y',label='ave: '+str(mean_elev)+' m')
plt.fill_between(i_list, elev_list, base_reg,alpha=0.1)
plt.text(i_list[0], elev_list[0],"P1")
plt.text(i_list[-1], elev_list[-1],"P2")
plt.xlabel("Index")
plt.ylabel("Elevation(m)")
plt.grid()
plt.legend(fontsize='small')
plt.show()
'''
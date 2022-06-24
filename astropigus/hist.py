import matplotlib.pyplot as plt
import numpy as np

v = np.array([45613, 0, 7, 108, 464, 7, 3, 1217, 304, 3900, 42, 872, 1991, 494, 570, 2848, 3750, 2509, 4492, 9102, 6829, 20962, 12571, 44329, 66670, 147910, 189166, 223727, 383248, 218499, 222065, 248780, 120654, 33885, 104174, 19961, 89333, 100835, 19475, 18678, 18828, 28697, 20, 263118, 675, 58744, 31513, 27359, 120154, 149865, 269908, 121950, 5944, 86405, 138945, 75987, 1530, 124892, 5621, 21391, 601556, 432267, 8114, 13280, 171352, 85105, 17056, 8967, 149432, 108201, 76701, 572094, 72143, 348398, 116581, 209067, 173496, 22894, 1543090, 198736, 151538, 165299, 550988, 265476, 10, 968823, 0, 14838, 1258749, 89953, 625368, 40929, 104042, 1584225, 4210718, 1850728, 80211, 74359, 1577800, 901446, 6710495, 381869, 2524151, 3981294, 2015422, 9300059, 68437, 2653045, 396859, 3668672, 6341455, 1516482, 497841, 3671411, 10193183, 116956, 1995643, 5657479, 812711, 3785742, 2670861, 3714902, 914878, 3632142, 2292105, 2959508, 2464484, 4093945, 3073479, 3025522, 3269743, 4567435, 3923258, 6768785, 6431757, 10602621, 7353226, 8497238, 5832545, 5643192, 3967305, 2444972, 1126566, 465805, 253826, 92162, 52204, 99553, 53141, 72251, 18528, 45028, 25915, 25207, 14063, 15308, 28857, 2088, 20220, 11970, 6216, 803, 10356, 867, 6036, 3872, 632, 643, 508, 515, 2, 8946, 30, 404, 413, 171, 793, 540, 2077, 2743, 21, 61, 233, 108, 0, 335, 1, 16, 1155, 620, 0, 1, 57, 18, 1, 0, 128, 20, 0, 2115, 1, 256, 46, 0, 6, 0, 477, 2, 97, 12, 0, 0, 0, 692, 0, 0, 4, 0, 26, 0, 11, 0, 970, 0, 0, 22, 3, 2, 357, 3, 0, 0, 131, 45, 0, 3447, 1, 0, 0, 0, 94, 0, 946, 2, 0, 1633, 1, 17, 8, 80, 0, 532, 204, 13, 5, 0])

w = np.array([])

for i in range(256):
    print(i)
    z = np.full(v[i], i)
    print(z)
    w = np.append(w, z)

print(w)

_ = plt.hist(w, bins='auto')

plt.show()
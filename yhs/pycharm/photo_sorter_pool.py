import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread
import multiprocessing
from functools import partial
import timeit

#########################################################################

# 리사이징
def resizer(img):
    h, w, c = img.shape

    if h == 200:
        re_img = img
    else:
        tmp = 200 / h
        re_img = cv.resize(img, dsize=(0, 0), fx=tmp, fy=tmp, interpolation=cv.INTER_LINEAR)

    return re_img

# 사진 분류
def photo_sorter(origin_img, file_name):
    h, w, c = origin_img.shape

    if (h > 2000) or (w > 2000):
        if h < w:
            tmp = round(2000 / w, 3)
        elif h > w:
            tmp = round(2000 / h, 3)
        else:
            tmp = round(2000 / h, 3)

        re_img = cv.resize(origin_img, dsize=(0, 0), fx=tmp, fy=tmp, interpolation=cv.INTER_LINEAR)
    else:
        re_img = origin_img

    gray = cv.cvtColor(re_img, cv.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(50, 50))

    if len(faces) > 0:
        for i in range(len(faces)):
            x, y, w, h = faces[i]
            crop_img = re_img[y:y + h, x:x + w]
            re_crop_img = resizer(crop_img)
            cv.imwrite("../crop/" + file_name + "_" + str(i) + ".png", re_crop_img)
    else:
        pass

# 사진 갯수 판별
def get_count(num, p=4):
    lists = []
    allocate = int(num / p)
    for n in range(p):
        lists.append(allocate)

    lists[p - 1] += num % p
    print("프로세스 할당량 :", lists)
    return lists

# 변환 작업
def work(a, b):
    for i in range(a, b, 1):
        file_name = "img (" + str(i) + ")"
        img = cv.imread("../photo/" + file_name + ".JPG")
        photo_sorter(img, file_name)

    #     if i % 100 == 0:
    #         print(file_name, "까지 완료")
    #     elif i % 3 == 0:
    #         print("-", end="")
    # return 0

#     file_name = "img ("+str(i) + ")"
#     img = cv.imread("photo/"+file_name+".JPG")
#     photo_sorter(img, file_name)

#     if i%100 == 0 :
#         print(file_name, "까지 완료")
#     elif i%3==0 :
#         print("-", end="")

####################################################################
start_time = timeit.default_timer()
print("완료 뜰 때까지 기다리세요")
faceCascade = cv.CascadeClassifier('../data/haarcascade_frontface.xml')

if __name__ == "__main__" :
    start_num = 1
    end_num = 1001


    pool = multiprocessing.Pool(4)
    # pool_prob = partial(work, a=start_num)
    pool.starmap(work, [(start_num, end_num)])


    stop_time = timeit.default_timer()
    total_time = round(stop_time - start_time, 0)
    print("총 걸린시간 : ", total_time, "초")
    print("완료")
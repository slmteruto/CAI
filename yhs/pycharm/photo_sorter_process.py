# 얼굴 인식을 통한 사진 분류 (멀티프로세싱)
# 최초 작성일 : 20/03/04
# 작성자 : 양희승
#
# 작성내용 : 사진 분류기 속도 개선

# 수정내용
#       20/03/06
#           코드 수정  main실행 아닐 경우 추가

import cv2 as cv
import multiprocessing
import timeit

#########################################################################
start_time = timeit.default_timer()
print(start_time)
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

####################################################################
faceCascade = cv.CascadeClassifier('../data/haarcascade_frontface.xml')

if __name__ == "__main__" :
    num = int(30000)
    process_num = 4

    process = []
    start_num = 6511
    end_num = 6511

    for count in get_count(num, process_num):
        end_num += count
        print("실행 범위", start_num, "~", end_num)
        p = multiprocessing.Process(target=work, args=(start_num, end_num))
        start_num += count
        process.append(p)
        p.start()

    for p in process:
        p.join
elif __name__ == "photo_sorter_process" :
    num = int(30000)
    process_num = 4

    process = []
    start_num = 1
    end_num = 1

    for count in get_count(num, process_num):
        end_num += count
        print("실행 범위", start_num, "~", end_num)
        p = multiprocessing.Process(target=work, args=(start_num, end_num))
        start_num += count
        process.append(p)
        p.start()

    for p in process:
        p.join

end_time = timeit.default_timer()
print(end_time)
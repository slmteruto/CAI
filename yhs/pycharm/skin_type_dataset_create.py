# 데이터셋 생성 (멀티프로세싱)
# 최초 작성일 : 20/03/06
# 작성자 : 양희승
#
# 작성내용 : 데이터셋 생성 속도 개선

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append('F:/hs/pythonwork/project/cys')

import numpy as np
from sklearn.cluster import KMeans
import cv2 as cv
from cys import color_classifier   # 예스리 임포트
import color_classifier
import colour
import warnings
import multiprocessing

warnings.filterwarnings(action='ignore')
# warnings.filterwarnings(action='default')
############################################################

def color_ratio(clt) :
    numLabels = np.arange(0, len(np.unique(clt.labels_))+1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)
    hist = hist.astype("float")
    hist /= hist.sum()
    return hist

# k=5이므로 다섯개의 영역에 얼마만큼의 퍼센테이지가 차지되었는지 return된다.

def plot_colors(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype = "uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        endX = startX + (percent * 300)
        cv.rectangle(bar, (int(startX), 0), (int(endX), 50),
            color.astype("uint8").tolist(), -1)
        startX = endX
    return bar


def skin_detector(img, file_name):
    # 피부 검출1
    lower = np.array([0, 48, 80], dtype="uint8")
    upper = np.array([20, 255, 255], dtype="uint8")

    converted = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    skinMask = cv.inRange(converted, lower, upper)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11, 11))
    skinMask = cv.erode(skinMask, kernel, iterations=2)
    skinMask = cv.dilate(skinMask, kernel, iterations=2)

    skinMask = cv.GaussianBlur(skinMask, (3, 3), 0)
    skin = cv.bitwise_and(img, img, mask=skinMask)

    result = skin
    #     plt.imshow(result)
    #     plt.show()

    img = cv.cvtColor(result, cv.COLOR_BGR2HLS)
    skin_img = img
    temp_img = cv.cvtColor(img, cv.COLOR_HLS2RGB)

    h, w, c = img.shape

    for i in range(h):
        for j in range(w):
            H = img[i][j][0]
            L = img[i][j][1]
            S = img[i][j][2]

            R = temp_img[i][j][0]
            G = temp_img[i][j][1]
            B = temp_img[i][j][2]

            LS_ratio = L / S
            skin_pixel = bool((S >= 50) and (LS_ratio > 0.5) and (LS_ratio < 3.0) and ((H <= 25) or (H >= 165)))
            temp_pixel = bool((R == G) and (G == B) and (R >= 220))

            if skin_pixel:
                if temp_pixel:
                    skin_img[i][j][0] = 0
                    skin_img[i][j][1] = 0
                    skin_img[i][j][2] = 0
                else:
                    pass
            else:
                skin_img[i][j][0] = 0
                skin_img[i][j][1] = 0
                skin_img[i][j][2] = 0

    skin_img = cv.cvtColor(skin_img, cv.COLOR_HLS2BGR)
    for i in range(h):
        for j in range(w):
            B = skin_img[i][j][0]
            G = skin_img[i][j][1]
            R = skin_img[i][j][2]

            bg_pixel = bool(B == 0 and G == 0 and R == 0)

            if bg_pixel:
                skin_img[i][j][0] = 255
                skin_img[i][j][1] = 255
                skin_img[i][j][2] = 255
            else:
                pass

    #     plt.imshow(skin_img)
    #     plt.show()

    cvt_img = cv.cvtColor(skin_img, cv.COLOR_BGR2RGB)
    #     plt.imshow(cvt_img)
    #     plt.show()

    cvt_img = cvt_img.reshape((cvt_img.shape[0] * cvt_img.shape[1], 3))
    k = 20
    clt = KMeans(n_clusters=k)
    clt.fit(cvt_img)

    hist = color_ratio(clt)
    temp = np.array(clt.cluster_centers_)

    # hist에서 높은 값 제거, cluster_centers_에서도 제거)
    del_index = hist.argmax()
    hist = np.delete(hist, del_index)
    temp = np.delete(temp, del_index, 0)

    try:

        # hist에서 제일 낮은 값 제거, cluster_centers_ 에서도 제거
        del_index = np.argmin(hist)
        hist = np.delete(hist, del_index)
        temp = np.delete(temp, del_index, 0)

        del_index = np.argmin(hist)
        hist = np.delete(hist, del_index)
        temp = np.delete(temp, del_index, 0)  # 3

        del_index = np.argmin(hist)
        hist = np.delete(hist, del_index)
        temp = np.delete(temp, del_index, 0)  # 4

        del_index = np.argmin(hist)
        hist = np.delete(hist, del_index)
        temp = np.delete(temp, del_index, 0)  # 5

        del_index = np.argmin(hist)
        hist = np.delete(hist, del_index)
        temp = np.delete(temp, del_index, 0)

        del_index = np.argmin(hist)
        hist = np.delete(hist, del_index)
        temp = np.delete(temp, del_index, 0)

        del_index = np.argmin(hist)
        hist = np.delete(hist, del_index)
        temp = np.delete(temp, del_index, 0)

        del_index = np.argmin(hist)
        hist = np.delete(hist, del_index)
        temp = np.delete(temp, del_index, 0)

        del_index = np.argmin(hist)
        hist = np.delete(hist, del_index)
        temp = np.delete(temp, del_index, 0)

        del_index = np.argmin(hist)
        hist = np.delete(hist, del_index)
        temp = np.delete(temp, del_index, 0)

        del_index = np.argmin(hist)
        hist = np.delete(hist, del_index)
        temp = np.delete(temp, del_index, 0)

        del_index = np.argmin(hist)
        hist = np.delete(hist, del_index)
        temp = np.delete(temp, del_index, 0)

        del_index = np.argmin(hist)
        hist = np.delete(hist, del_index)
        temp = np.delete(temp, del_index, 0)
    except ValueError:
        print(file_name, "에러")
        cv.imwrite("../dataset/value_error/"+file_name+".png", img)
        pass

    # 비율 재조정
    hist = hist / hist.sum()
    ####################################

    # 그래프 그리기
    bar = plot_colors(hist, temp)

    #     plt.figure()
    #     plt.axis("off")
    #     plt.imshow(bar)
    #     plt.show()

    # RGB변환 후 저장
    bar = cv.cvtColor(bar, cv.COLOR_BGR2RGB)
    #     cv.imwrite("../img/"+file_name+"_test.jpg", bar)

    return bar


def color_convert(cheek, file_name):
    img = cheek
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    #     plt.imshow(img)
    #     plt.show()

    sum = 0
    R = []
    G = []
    B = []
    for i in img:
        for j in i:
            R.append(j[0])
            G.append(j[1])
            B.append(j[2])

    R_sum = 0
    G_sum = 0
    B_sum = 0

    # 각 R, G, B의 합계 구하기
    for i in range(len(R)):
        R_sum += R[i]
        G_sum += G[i]
        B_sum += B[i]

    R_avg = int(round((R_sum / len(R)), 0))  # R값 평균
    G_avg = int(round((G_sum / len(G)), 0))  # G값 평균
    B_avg = int(round((B_sum / len(B)), 0))  # B값 평균
    RGB_color = [R_avg, G_avg, B_avg]

    # 평균 색만 그래프 그리기 위함 img_avg
    img_avg = img

    for i in img_avg:
        for j in i:
            j[0] = R_avg
            j[1] = G_avg
            j[2] = B_avg

    # 기존
    #     plt.imshow(img)
    #     plt.show()

    # 평균색
    #     plt.imshow(img_avg)
    #     plt.show()
    bgr_img_avg = cv.cvtColor(img_avg, cv.COLOR_RGB2BGR)

    # 저장
    #     cv.imwrite("../img/"+file_name+"_9.jpg", bgr_img_avg)

    arr_RGB_color = np.array(RGB_color)
    float_arr_RGB_color = arr_RGB_color / 255
    float_tp_RGB_color = tuple(float_arr_RGB_color)
    HSV_color = colour.RGB_to_HSV(float_tp_RGB_color)
    HSV_color2 = np.array(
        [round(HSV_color[0] * 359, 3), round(HSV_color[1] * 100, 3) - 4, round(HSV_color[2] * 100, 3) + 8])
    HSV_color2 = list(HSV_color2)
    HSV_color2[0] = round(HSV_color2[0], 2)
    HSV_color2[1] = round(HSV_color2[1], 2)
    HSV_color2[2] = round(HSV_color2[2], 2)
    return HSV_color2


def save_img(img, file_name, skin_type):
    if skin_type == 0:
        cv.imwrite("../dataset/00/" + file_name + ".png", img)
    elif skin_type == 1:
        cv.imwrite("../dataset/01/" + file_name + ".png", img)
    elif skin_type == 2:
        cv.imwrite("../dataset/02/" + file_name + ".png", img)
    elif skin_type == 3:
        cv.imwrite("../dataset/03/" + file_name + ".png", img)
    elif skin_type == 4:
        cv.imwrite("../dataset/04/" + file_name + ".png", img)
    elif skin_type == 5:
        cv.imwrite("../dataset/05/" + file_name + ".png", img)
    elif skin_type == 6:
        cv.imwrite("../dataset/06/" + file_name + ".png", img)
    elif skin_type == 7:
        cv.imwrite("../dataset/07/" + file_name + ".png", img)
    elif skin_type == -1:
        cv.imwrite("../dataset/error/" + file_name + ".png", img)
        print("분류오류 : ", file_name)
    else:
        cv.imwrite("../dataset/value_error/" + file_name + ".png", img)
        print("타입오류 : ", file_name, " 타입번호 : ", skin_type)

def get_count(num, p=4):
    lists = []
    allocate = int(num / p)
    for n in range(p):
        lists.append(allocate)

    lists[p - 1] += num % p
    print("프로세스 할당량 :", lists)
    return lists

def work(start_num, end_num) :
    for i in range(start_num, end_num, 1):
        ## 이미지 로드
        file_name = "img (" + str(i) + ")"
        img = cv.imread("../crop/" + file_name + ".png")

        # 이미지 색 비율 추출
        bar = skin_detector(img, file_name)

        ## 평균색으로 변형
        hsv = color_convert(bar, file_name)

        # 예슬's 피부타입 분류 함수
        color_class = color_classifier.Color()
        skin_type = color_class.color_classifier(hsv)
        save_img(img, file_name, skin_type)

color_type = ["WSB", "WSL", "WAD", "WAM", "CSL", "CSM", "CWB", "CWD"]


if __name__ == "__main__" :

    num = int(1000)
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

from flask import Flask, render_template, request, session, redirect, url_for, jsonify, json
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import pymysql
import cv2 as cv
import colour
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import argparse

import CAIProjectModule

from io import BytesIO

app = Flask(__name__)
app.secret_key = b'caicai123123'


############ function ###################
def musin_rcmnd(facehsv, nick):
    hsv = facehsv
    user_nick = nick
    # database = {"host": "192.168.0.41", "user": "cai", "passwd": "1234", "db": "final"}
    database = {"host":"ec2-13-209-69-114.ap-northeast-2.compute.amazonaws.com", "user":"cai", "passwd":"1234", "db":"final"}
    cursor = CD.connectDB(database)
    HSV = CD.select_prdt_color(cursor)



    ### 얼굴 측색값 기준 팔레트 추출 : 각 6개 색 추출
    hsv_palette_bright = CP.palette_bright(hsv)
    hsv_palette_harmony = CP.palette_harmony(hsv)

    ### 웹용 팔레트 RGB 변환 : 각 6개 색
    rgb_palette_bright = CP.to_rgb(hsv_palette_bright)
    rgb_palette_harmony = CP.to_rgb(hsv_palette_harmony)

    purchase_prdt = CD.getUserPurchase(cursor, user_nick)
    purchase_hsv = CC.greytoneFilter(purchase_prdt)
    purchase_HSV = CC.colorGenerator(purchase_hsv)
    centroid = CC.colorClustering(purchase_HSV)

    prdtCode_bright = CP.matchedPrdt(hsv_palette_bright, HSV)
    prdtCode_harmony = CP.matchedPrdt(hsv_palette_harmony, HSV)
    prdtCode_purchase = CP.matchedPrdt(centroid, HSV)

    imgLink_bright = CD.getPrdtimage(cursor, prdtCode_bright) #6개
    imgLink_harmony = CD.getPrdtimage(cursor, prdtCode_harmony) #6개
    imgLink_purchase = CD.getPrdtimage(cursor, prdtCode_purchase) #6개

    dict_rcmnd = {"bright":imgLink_bright,"harmony":imgLink_harmony,"purchase":imgLink_purchase}
    return dict_rcmnd

def type_classifier(img):
    pass


def connect_db():
    # config = {"host": "192.168.0.41", "user": "cai", "passwd": "1234", "db": "final"}
    config = {"host":"ec2-13-209-69-114.ap-northeast-2.compute.amazonaws.com", "user":"cai", "passwd":"1234", "db":"final"}
    conn = pymysql.connect(**config)
    return conn


def img_db_save(img_binary):
    conn = connect_db()
    cursor = conn.cursor()
    print()
    # sql = "INSERT INTO USER_IMAGE (USER_IMG) VALUES(%s)".format(img_binary)
    cursor.execute("INSERT INTO USER_IMAGE (USER_IMG) VALUES(_binary %s)", img_binary)
    conn.commit()
    cursor.close()
    conn.close()


def img_db_load():
    conn = connect_db()
    cursor = conn.cursor()
    print()
    # sql = "INSERT INTO USER_IMAGE (USER_IMG) VALUES(%s)".format(img_binary)
    cursor.execute("SELECT USER_IMG FROM USER_IMAGE LIMIT 1")
    img_binary = cursor.fetchone()[0]
    img_pil = Image.open(BytesIO(img_binary))
    img_cv = np.array(img_pil)
    img_cv = img_cv[:, :, ::-1].copy()  ## RGB
    return img_cv
    # plt.imshow(img_cv)
    # plt.show()


## 얼굴 인식
def face_detection(img):
    origin_img = img
    print(origin_img.shape)
    faceCascade = cv.CascadeClassifier('data/haarcascade_frontface.xml')

    gray = cv.cvtColor(origin_img, cv.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    face_cropped = None

    # face_detection
    if len(faces) > 1:
        print("한 사람만 찍힌 사진을 올려주세요")
        face_cropped = [0, 0, 0]

    elif len(faces) == 1:
        for (x, y, w, h) in faces:
            cv.rectangle(origin_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #             cv.imshow("Face", origin_img)
            # cv.imwrite("img/" + file_name + "_3.jpg", origin_img)
            face_cropped = origin_img[y:y + h, x:x + w]
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = origin_img[y:y + h, x:x + w]
            # cv.imwrite("img/" + file_name + "_4.jpg", face_cropped)

    elif len(faces) == 0:
        print("정면이거나 정상적인 사진을 올려주세요")
        face_cropped = [0, 0, 0]

    else:
        print("에러")
        face_cropped = [0, 0, 0]

    return face_cropped

############################################################################# Skin

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
#         print("색깔 ",color)
#         print("비율 : ", percent)
        endX = startX + (percent * 300)
        cv.rectangle(bar, (int(startX), 0), (int(endX), 50),
            color.astype("uint8").tolist(), -1)
        startX = endX
    return bar



def skin_extract(img):
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

    cvt_img = cv.cvtColor(skin_img, cv.COLOR_BGR2RGB)
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

    # hist에서 제일 낮은 값 제거, cluster_centers_ 에서도 제거
    for i in range(14) :
        del_index = np.argmin(hist)
        hist = np.delete(hist, del_index)
        temp = np.delete(temp, del_index, 0)

    # 비율 재조정
    hist = hist / hist.sum()

    bar = plot_colors(hist, temp)


    return bar

## color convert
def color_convert(img):
    # img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    # plt.imshow(img)
    # plt.show()
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
    # plt.imshow(img)
    # plt.show()

    # plt.imshow(img_avg)
    # plt.show()
    bgr_img_avg = cv.cvtColor(img_avg, cv.COLOR_RGB2BGR)

    # cv.imwrite("img/" + file_name + "_9.jpg", bgr_img_avg)

    arr_RGB_color = np.array(RGB_color)
    list_rgb_color = arr_RGB_color.tolist()
    float_arr_RGB_color = arr_RGB_color / 255
    float_tp_RGB_color = tuple(float_arr_RGB_color)
    HSV_color = colour.RGB_to_HSV(float_tp_RGB_color)
    HSV_color2 = np.array(
        [round(HSV_color[0] * 359, 3), round(HSV_color[1] * 100, 3) - 4, round(HSV_color[2] * 100, 3) + 8])
    #     print("HSV 값 : ", HSV_color2)
    HSV_color2 = list(HSV_color2)
    HSV_color2[0] = round(HSV_color2[0], 2)
    HSV_color2[1] = round(HSV_color2[1], 2)
    HSV_color2[2] = round(HSV_color2[2], 2)
    return HSV_color2, list_rgb_color


def color_convert_hsv(RGB_color):
    arr_RGB_color = np.array(RGB_color)
    list_rgb_color = arr_RGB_color.tolist()
    float_arr_RGB_color = arr_RGB_color / 255
    float_tp_RGB_color = tuple(float_arr_RGB_color)
    HSV_color = colour.RGB_to_HSV(float_tp_RGB_color)
    HSV_color2 = np.array(
        [round(HSV_color[0] * 359, 3), round(HSV_color[1] * 100, 3) - 4, round(HSV_color[2] * 100, 3) + 8])
    #     print("HSV 값 : ", HSV_color2)
    HSV_color2 = list(HSV_color2)
    HSV_color2[0] = round(HSV_color2[0], 2)
    HSV_color2[1] = round(HSV_color2[1], 2)
    HSV_color2[2] = round(HSV_color2[2], 2)
    return HSV_color2


## color classifier
def color_classifier(person_HSV):
    # 입력값 Hue, Sturation, Value에 따라 변수 지정
    H = float(person_HSV[0])
    S = float(person_HSV[1])
    V = float(person_HSV[2])
    diff = round(V - S, 2)
    color_type = ["WSB", "WSL", "WAD", "WAM", "CSL", "CSM", "CWB", "CWD"]
    if H >= 23 and H <= 203:
        if diff >= 43.15:
            if S >= 32.47:
                ans = 0
            else:
                ans = 1

        elif diff < 43.15:
            if S >= 32.47:
                ans = 2
            else:
                ans = 3

    elif (H >= 0 and H < 23) or (H > 203 and H <= 360):
        if diff >= 47.15:
            if diff >= 60.80:
                ans = 4

            else:
                ans = 5

        elif diff < 47.15:
            if diff >= 23.58:
                ans = 6
            else:
                ans = 7
    else:
        ans = -1
    return ans


color_type = ["Warm Spring Bright", "Warm Spring Light", "Warm Autumn Deep", "Warm Autumn Mute", "Cool Summer Light",
              "Cool Summer Mute", "Cool Winter Bright", "Cool Winter Deep"]
global rgb

CP = CAIProjectModule.ColorPalette()
CD = CAIProjectModule.DatabaseConnetion()
CC = CAIProjectModule.ColorClustering()

############# main ######################
@app.route("/")
def hello():
    return render_template('CAI_main.html')


@app.route("/main/")
def main():
    return render_template('CAI_main.html')


############# menu2
@app.route("/color_recommnd")
def color_recommnd():
    global rgb
    if len(rgb) == 3:
        rgb_value = rgb
        print(rgb_value)
        hsv = color_convert_hsv(rgb_value)
        print(hsv)
        hsv_palette_bright = CP.palette_bright(hsv)
        hsv_palette_harmony = CP.palette_harmony(hsv)

        rgb_palette_bright = CP.to_rgb(hsv_palette_bright)
        rgb_palette_harmony = CP.to_rgb(hsv_palette_harmony)

        data = {"bright": rgb_palette_bright, "harmony": rgb_palette_harmony}
        print(data['bright'][0])
        print(data['harmony'][0])
        return render_template('CAI_palette.html', data=json.dumps(data))
    else:
        print("rgb값 없음")
        return render_template('CAI_palette.html')


############# menu3
@app.route("/musinsa_recommnd")
def musinsa_recommnd():
    return render_template('CAI_recomend.html')


## select nick
@app.route("/selectnick", methods=['GET', 'POST'])
def select_nick():
    global rgb
    if len(rgb) == 3:
        rgb_value = rgb
        print(rgb_value)
        hsv = color_convert_hsv(rgb_value)
    else :
        hsv = [100, 1, 1]
    if 'input_nick' in request.form:
        nick = request.form['input_nick']
        print(nick)
        result = musin_rcmnd(hsv, nick)

        return jsonify(result)
    else:
        print("에러")
        test = {"aa": "error"}
        return jsonify(test)

# def select_nick():
#     if request.method == 'POST':
#         nick = request.form['input_nick']
#         print(nick)
#         test = {"aa": nick}
#         return jsonify(test)
#     else:
#         test = {"aa": "error"}
#         return jsonify(test)


## upload
@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    global rgb
    if request.method == 'POST':
        ##session
        # session['user_photo'] = request.form['file']

        ##image file
        f = request.files['file']
        temp_photo = f
        f.save(f'static/uploads/{secure_filename(f.filename)}')

        img_pil = Image.open(f).convert("RGB")  ## PIL Image
        img_cv = np.array(img_pil)
        img_cv = img_cv[:, :, ::-1].copy()  ## RGB  ## CV Image

        face_img = face_detection(img_cv)
        # img_cv_bgr = cv.cvtColor(img_cv, cv.COLOR_RGB2BGR)
        # face_img = face_detection(img_cv_bgr)
        if np.array_equal(face_img, [0, 0, 0]):
            print(face_img)
            print("에러")
            return jsonify({"pctype": 'error'})
        else:
            success, img_cv_binary = cv.imencode('.jpg', img_cv)  ## Binary Image
            # plt.imshow(img_cv)
            # plt.show()
            print(success)
            if success:
                # img_db_save(img_cv_binary.tostring())
                ext_img = skin_extract(face_img)
                hsv, rgb = color_convert(ext_img)
                result = color_classifier(hsv)  # <<<<<<<<<<<---------------------------algorithm 수정부위


        print(result)
        print(color_type[result])
        result = {"pctype": color_type[result], "rgb_value": rgb}
        return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

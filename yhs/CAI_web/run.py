from flask import Flask, render_template, request, session, redirect, url_for, jsonify, json
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import pymysql
import cv2 as cv
import colour
import matplotlib.pyplot as plt

import sys

sys.path.append("F:\\hs\\pythonwork\\project\\jay")
import CAIProjectModule

from io import BytesIO

app = Flask(__name__)
app.secret_key = b'caicai123123'


############ function ###################
def musin_rcmnd(facehsv, nick):
    hsv = facehsv
    user_nick = nick
    database = {"host": "192.168.0.41", "user": "cai", "passwd": "1234", "db": "final"}
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
    config = {"host": "192.168.0.41", "user": "cai", "passwd": "1234", "db": "final"}
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

    faceCascade = cv.CascadeClassifier('data/haarcascade_frontface.xml')

    gray = cv.cvtColor(origin_img, cv.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

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


## color convert
def color_convert(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
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
                hsv, rgb = color_convert(face_img)
                result = color_classifier(hsv)  # <<<<<<<<<<<---------------------------algorithm 수정부위

        print(result)
        print(color_type[result])
        result = {"pctype": color_type[result], "rgb_value": rgb}
        return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

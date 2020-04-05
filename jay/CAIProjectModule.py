import pandas as pd
import numpy as np
import pymysql
from matplotlib.colors import hsv_to_rgb
import matplotlib.pyplot as plt

from sklearn.cluster import AgglomerativeClustering
from sklearn.utils.testing import ignore_warnings
from sklearn.neighbors.nearest_centroid import NearestCentroid

class ColorPalette:
    person_HSV, personal_palette, prdt_list = list(), list(), list()
    H, S, V = float(), float(), float()
    HSV = None
    
    # 퍼스널컬러 팔레트 매칭 함수
    def palette_bright(self, person_HSV):
        # 입력값 Hue, Sturation, Value에 따라 변수 지정
        self.H = float(person_HSV[0])
        self.S = float(person_HSV[1])
        self.V = float(person_HSV[2])
        diff = round(self.V - self.S, 2)

        # (보색, 삼각보색1, 삼각보색2, 이중보색1, 이중보색2, 이중보색3)
        # hue 변경 값
        h_warm_plus, h_cool_plus = [175, 30, 330, 50, 180, 230], [185, 150, 210, 130, 180, 310]
        # saturation 변경 값
        s_SpringWinter_plus, s_SummerAutumn_plus = [40, 10, 30, 50, 45, 50], [0, -30, -10, 10, 5, 10]
        # Value 변경 값
        v_SpringWinter_plus, v_SummerAutumn_plus = [-40, -15, -30, -40, -15, -40], [-20, 5, -10, -20, 5, -20]
        # 각 보색 값 변수
        h_list, s_list, v_list = [], [], []

        try:
            # 웜톤
            if self.H >= 26 and self.H <= 206 : 
                # 웜톤 HUE 변경
                for hue, i in zip(h_warm_plus, range(6)):
                    if self.H+hue <= 359:
                        h_list.append(self.H+h_warm_plus[i])
                    else:
                        h_list.append(self.H+h_warm_plus[1]-359)

                # 봄
                if diff >= 43.15 :
                    for saturation, value, i in zip(s_SpringWinter_plus, v_SpringWinter_plus, range(6)):
                        # Saturation
                        if saturation >= 0:                    
                            if self.S+saturation <= 100:
                                s_list.append(self.S+s_SpringWinter_plus[i])
                            else:
                                s_list.append(self.S-s_SpringWinter_plus[i])
                        else:
                            if self.S+saturation >= 10:
                                s_list.append(self.S+s_SpringWinter_plus[i])
                            else:
                                s_list.append(self.S-s_SpringWinter_plus[i])
                        # Vlaue
                        if value >= 0:                    
                            if self.V+value <= 100:
                                v_list.append(self.V+v_SpringWinter_plus[i])
                            else:
                                v_list.append(self.V-v_SpringWinter_plus[i])
                        else:
                            if self.V+saturation >= 10:
                                v_list.append(self.V+v_SpringWinter_plus[i])
                            else:
                                v_list.append(self.V-v_SpringWinter_plus[i])                    

                # 가을
                elif diff <= 43.15:
                    for saturation, value, i in zip(s_SummerAutumn_plus, v_SummerAutumn_plus, range(6)):
                        if saturation >= 0:                    
                            if self.S+saturation <= 100:
                                s_list.append(self.S+s_SummerAutumn_plus[i])
                            else:
                                s_list.append(self.S-s_SummerAutumn_plus[i])
                        else:
                            if self.S+saturation >= 10:
                                s_list.append(self.S+s_SummerAutumn_plus[i])
                            else:
                                s_list.append(self.S-s_SummerAutumn_plus[i])

                        if value >= 0:                    
                            if self.V+value <= 100:
                                v_list.append(self.V+v_SummerAutumn_plus[i])
                            else:
                                v_list.append(self.V-v_SummerAutumn_plus[i])
                        else:
                            if self.V+saturation >= 10:
                                v_list.append(self.V+v_SummerAutumn_plus[i])
                            else:
                                v_list.append(self.V-v_SummerAutumn_plus[i])

            # 쿨톤
            elif (self.H >= 0 and self.H < 26) or (self.H > 206 and self.H <= 360) :
                # 쿨톤 HUE 변경
                for hue, i in zip(h_cool_plus, range(6)):
                    if self.H+hue <= 359:
                        h_list.append(self.H+h_cool_plus[i])
                    else:
                        h_list.append(self.H+h_cool_plus[1]-359)

                # 여름
                if diff >= 47.15 :
                    for saturation, value, i in zip(s_SummerAutumn_plus, v_SummerAutumn_plus, range(6)):
                        if saturation >= 0:                    
                            if self.S+saturation <= 100:
                                s_list.append(self.S+s_SummerAutumn_plus[i])
                            else:
                                s_list.append(self.S-s_SummerAutumn_plus[i])
                        else:
                            if self.S+saturation >= 10:
                                s_list.append(self.S+s_SummerAutumn_plus[i])
                            else:
                                s_list.append(self.S-s_SummerAutumn_plus[i])

                        if value >= 0:                    
                            if self.V+value <= 100:
                                v_list.append(self.V+v_SummerAutumn_plus[i])
                            else:
                                v_list.append(self.V-v_SummerAutumn_plus[i])
                        else:
                            if self.V+saturation >= 10:
                                v_list.append(self.V+v_SummerAutumn_plus[i])
                            else:
                                v_list.append(self.V-v_SummerAutumn_plus[i])

                # 겨울
                elif diff <= 47.15:
                    for saturation, value, i in zip(s_SpringWinter_plus, v_SpringWinter_plus, range(6)):
                        # Saturation
                        if saturation >= 0:                    
                            if self.S+saturation <= 100:
                                s_list.append(self.S+s_SpringWinter_plus[i])
                            else:
                                s_list.append(self.S-s_SpringWinter_plus[i])
                        else:
                            if self.S+saturation >= 10:
                                s_list.append(self.S+s_SpringWinter_plus[i])
                            else:
                                s_list.append(self.S-s_SpringWinter_plus[i])
                        # Vlaue
                        if value >= 0:                    
                            if self.V+value <= 100:
                                v_list.append(self.V+v_SpringWinter_plus[i])
                            else:
                                v_list.append(self.V-v_SpringWinter_plus[i])
                        else:
                            if self.V+saturation >= 10:
                                v_list.append(self.V+v_SpringWinter_plus[i])
                            else:
                                v_list.append(self.V-v_SpringWinter_plus[i])                    

            else :
                h_list, s_list, v_list = [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]

        except:
            print('팔레트 매칭에서 오류발생')

        # 팔레트 HSV
        comp_color = [h_list[0], s_list[0], v_list[0]]
        triangle_comp_color_1 = [h_list[1], s_list[1], v_list[1]]
        triangle_comp_color_2 = [h_list[2], s_list[2], v_list[2]]
        doubleness_comp_color_1 = [h_list[3], s_list[3], v_list[3]]
        doubleness_comp_color_2 = [h_list[4], s_list[4], v_list[4]]
        doubleness_comp_color_3 = [h_list[5], s_list[5], v_list[5]]

        personalization_palette = [comp_color, triangle_comp_color_1, triangle_comp_color_2, 
                                  doubleness_comp_color_1, doubleness_comp_color_2, doubleness_comp_color_3]

        return personalization_palette

    
    # 조화색 팔레트 매칭 함수
    def palette_harmony(self, person_HSV):
        # 입력값 Hue, Sturation, Value에 따라 변수 지정
        self.H = float(person_HSV[0])
        self.S = float(person_HSV[1])
        self.V = float(person_HSV[2])
        diff = round(self.V - self.S, 2)

        # (보색, 삼각보색1, 삼각보색2, 이중보색1, 이중보색2, 이중보색3)
        # hue 변경 값
        h_warm_plus, h_cool_plus = [247, 102, 42, 122, 252, 302], [257, 222, 282, 202, 252, 22]
        # saturation 변경 값
        s_SpringWinter_plus, s_SummerAutumn_plus = [40, 10, 30, 50, 45, 50], [0, -30, -10, 10, 5, 10]
        # Value 변경 값
        v_SpringWinter_plus, v_SummerAutumn_plus = [-40, -15, -30, -40, -15, -40], [-20, 5, -10, -20, 5, -20]
        # 각 보색 값 변수
        h_list, s_list, v_list = [], [], []

        try:
            # 웜톤
            if self.H >= 26 and self.H <= 206 : 
                # 웜톤 HUE 변경
                for hue, i in zip(h_warm_plus, range(6)):
                    if self.H+hue <= 359:
                        h_list.append(self.H+h_warm_plus[i])
                    else:
                        h_list.append(self.H+h_warm_plus[1]-359)

                # 봄
                if diff >= 43.15 :
                    for saturation, value, i in zip(s_SpringWinter_plus, v_SpringWinter_plus, range(6)):
                        # Saturation
                        if saturation >= 0:                    
                            if self.S+saturation <= 100:
                                s_list.append(self.S+s_SpringWinter_plus[i])
                            else:
                                s_list.append(self.S-s_SpringWinter_plus[i])
                        else:
                            if self.S+saturation >= 10:
                                s_list.append(self.S+s_SpringWinter_plus[i])
                            else:
                                s_list.append(self.S-s_SpringWinter_plus[i])
                        # Vlaue
                        if value >= 0:                    
                            if self.V+value <= 100:
                                v_list.append(self.V+v_SpringWinter_plus[i])
                            else:
                                v_list.append(self.V-v_SpringWinter_plus[i])
                        else:
                            if self.V+saturation >= 10:
                                v_list.append(self.V+v_SpringWinter_plus[i])
                            else:
                                v_list.append(self.V-v_SpringWinter_plus[i])                    

                # 가을
                elif diff <= 43.15:
                    for saturation, value, i in zip(s_SummerAutumn_plus, v_SummerAutumn_plus, range(6)):
                        if saturation >= 0:                    
                            if self.S+saturation <= 100:
                                s_list.append(self.S+s_SummerAutumn_plus[i])
                            else:
                                s_list.append(self.S-s_SummerAutumn_plus[i])
                        else:
                            if self.S+saturation >= 10:
                                s_list.append(self.S+s_SummerAutumn_plus[i])
                            else:
                                s_list.append(self.S-s_SummerAutumn_plus[i])

                        if value >= 0:                    
                            if self.V+value <= 100:
                                v_list.append(self.V+v_SummerAutumn_plus[i])
                            else:
                                v_list.append(self.V-v_SummerAutumn_plus[i])
                        else:
                            if self.V+saturation >= 10:
                                v_list.append(self.V+v_SummerAutumn_plus[i])
                            else:
                                v_list.append(self.V-v_SummerAutumn_plus[i])

            # 쿨톤
            elif (self.H >= 0 and self.H < 26) or (self.H > 206 and self.H <= 360) :
                # 쿨톤 HUE 변경
                for hue, i in zip(h_cool_plus, range(6)):
                    if self.H+hue <= 359:
                        h_list.append(self.H+h_cool_plus[i])
                    else:
                        h_list.append(self.H+h_cool_plus[1]-359)

                # 여름
                if diff >= 47.15 :
                    for saturation, value, i in zip(s_SummerAutumn_plus, v_SummerAutumn_plus, range(6)):
                        if saturation >= 0:                    
                            if self.S+saturation <= 100:
                                s_list.append(self.S+s_SummerAutumn_plus[i])
                            else:
                                s_list.append(self.S-s_SummerAutumn_plus[i])
                        else:
                            if self.S+saturation >= 10:
                                s_list.append(self.S+s_SummerAutumn_plus[i])
                            else:
                                s_list.append(self.S-s_SummerAutumn_plus[i])

                        if value >= 0:                    
                            if self.V+value <= 100:
                                v_list.append(self.V+v_SummerAutumn_plus[i])
                            else:
                                v_list.append(self.V-v_SummerAutumn_plus[i])
                        else:
                            if self.V+saturation >= 10:
                                v_list.append(self.V+v_SummerAutumn_plus[i])
                            else:
                                v_list.append(self.V-v_SummerAutumn_plus[i])

                # 겨울
                elif diff <= 47.15:
                    for saturation, value, i in zip(s_SpringWinter_plus, v_SpringWinter_plus, range(6)):
                        # Saturation
                        if saturation >= 0:                    
                            if self.S+saturation <= 100:
                                s_list.append(self.S+s_SpringWinter_plus[i])
                            else:
                                s_list.append(self.S-s_SpringWinter_plus[i])
                        else:
                            if self.S+saturation >= 10:
                                s_list.append(self.S+s_SpringWinter_plus[i])
                            else:
                                s_list.append(self.S-s_SpringWinter_plus[i])
                        # Vlaue
                        if value >= 0:                    
                            if self.V+value <= 100:
                                v_list.append(self.V+v_SpringWinter_plus[i])
                            else:
                                v_list.append(self.V-v_SpringWinter_plus[i])
                        else:
                            if self.V+saturation >= 10:
                                v_list.append(self.V+v_SpringWinter_plus[i])
                            else:
                                v_list.append(self.V-v_SpringWinter_plus[i])                    

            else :
                h_list, s_list, v_list = [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]

        except:
            print('팔레트 매칭에서 오류발생')

        # 팔레트 HSV
        comp_color = [h_list[0], s_list[0], v_list[0]]
        triangle_comp_color_1 = [h_list[1], s_list[1], v_list[1]]
        triangle_comp_color_2 = [h_list[2], s_list[2], v_list[2]]
        doubleness_comp_color_1 = [h_list[3], s_list[3], v_list[3]]
        doubleness_comp_color_2 = [h_list[4], s_list[4], v_list[4]]
        doubleness_comp_color_3 = [h_list[5], s_list[5], v_list[5]]

        personalization_palette = [comp_color, triangle_comp_color_1, triangle_comp_color_2, 
                                  doubleness_comp_color_1, doubleness_comp_color_2, doubleness_comp_color_3]

        return personalization_palette
    
    # 팔레트 일괄 rgb로 변환 함수
    def to_rgb(self, personal_palette):
        self.personal_palette = personal_palette
        try:
            rgb_palette = []
            for i in range(len(self.personal_palette)):
                h, s, v = self.personal_palette[i]
                RGB = hsv_to_rgb(np.array([[[h/359, s/100, v/100]]]))
                rgb_palette.append(list(np.round(RGB*255,0).reshape(3)))

        except:
            print('RGB변환에서 오류발생')

        return rgb_palette
    
    # 컬러 시각화 함수
    def show_colors(self, personal_palette):
        self.personal_palette = personal_palette
        try:
            rows, cols, cnt = 1, len(self.personal_palette), 1
            fig = plt.figure(figsize=(12, 3))

            for i in range(len(self.personal_palette)):
                h, s, v = self.personal_palette[i]
                RGB = hsv_to_rgb(np.array([[[h/359, s/100, v/100]]]))

                # 시각화
                ax = fig.add_subplot(rows, cols, cnt)
                ax.imshow(RGB)
                ax.set_title(i)
                ax.set_xticks([]), ax.set_yticks([])
                cnt += 1
            plt.show()

        except:
            print('팔레트 시각화에서 오류발생')
            
    # 팔레트 추출값에 색매칭 상품코드 추출
    def matchedPrdt(self, personal_palette, HSV):
        self.personal_palette, self.HSV = personal_palette, HSV
        
#         try:
        error_range = [5, 5, 5] # 색매칭 오차범위 변수담기
        matched_prdt = [] # 팔레트 총 추천상품 담을 변수

        for i in range(len(self.personal_palette)):
            prdt_codes = [] # 팔레트별 추출 상품코드 담을 변수
            h, s, v = self.personal_palette[i][0], self.personal_palette[i][1], self.personal_palette[i][2]

            # 오차범위 반영 fancy index 변수로 담기
            H_idx = (self.HSV[:, :, 0]<(h+error_range[0]))&(self.HSV[:, :, 0]>(h-error_range[0]))
            S_idx = (self.HSV[:, :, 1]<(s+error_range[1]))&(self.HSV[:, :, 1]>(s-error_range[1]))
            V_idx = (self.HSV[:, :, 2]<(v+error_range[2]))&(self.HSV[:, :, 2]>(v-error_range[2]))

            # 매칭되는 값이 없을경우 예외처리
            if self.HSV[(H_idx&S_idx&V_idx)].shape[0] == 0:
                prdt_codes.append("error:no matched product")
            else:
                # fancy indexing으로 상품코드 찾기
                if len(prdt_codes) <= 6:
                    for j in range(self.HSV[(H_idx&S_idx&V_idx)].shape[0]):
                        prdt_codes.append(self.HSV[(H_idx&S_idx&V_idx)][:,3][j])
                else:
                    break

            matched_prdt.append(prdt_codes)

        ## 리턴할 상품개수 6개로 제한
        self.prdt_list = [] # 상품코드 담을 변수
        cnt = 0
        while len(self.prdt_list) < 6:
                
            if len(self.prdt_list) == 6:
                break
            for i in range(len(matched_prdt)):
                if len(self.prdt_list) == 6:
                    break
                elif matched_prdt[i][0] == "error:no matched product":
                    pass
                elif cnt <= len(matched_prdt[i]):
                    self.prdt_list.append(matched_prdt[i][cnt])
            cnt += 1

#         except:
#             print('상품추출에서 오류발생')

        return self.prdt_list

class DatabaseConnetion:
    
    def connectDB(self, database):
        # DB 연결
        config = database
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        return cursor
    
    
    # DB 상품코드별 색 정보 가져오기
    def select_prdt_color(self, cursor):
        sql = "SELECT H, S, V, PRDT_CODE FROM PRDT_IMAGE WHERE H is NOT NULL;"
        cursor.execute(sql)

        prdt_hsv = pd.DataFrame(cursor, columns=["H", "S", "V", "PRDT_CODE"])

        cols = ["H", "S", "V"]
        for col in cols:
            prdt_hsv[col] = prdt_hsv[col].astype(float)

        HSV = np.array(prdt_hsv).reshape(1, -1, 4)

        return HSV
    
    # DB 상품 이미지링크 갖고오기
    def getPrdtimage(self, cursor, prdt_code):
        self.prdt_code = prdt_code
        
        imgLink_list = []
        for code in self.prdt_code:
            sql = "SELECT PRDT_IMG_LINK FROM PRDT_IMAGE WHERE PRDT_CODE = '{}';"
            cursor.execute(sql.format(str(code)))

            link = str(cursor.fetchone()).replace("('", "").replace("',)", "")
            imgLink_list.append(link)

        return imgLink_list
    
    ## 고객 구매 목록 색정보 가져오기
    def getUserPurchase(self, cursor, user_nick):
        purchase_prdt = [] # 구매상품 담을 목록
        cursor.execute("SELECT USER_NICK FROM PRDT_REVIEW WHERE USER_NICK in ('{}');".format(user_nick))
        
        if cursor.fetchone() == None:
            purchase_prdt.append("해당 닉네임의 구매 목록이 없습니다.")
            
        else:
            sql = "SELECT b.H, b.S, b.V FROM PRDT_REVIEW a, PRDT_IMAGE b WHERE USER_NICK='{}' AND a.PRDT_CODE = b.PRDT_CODE AND b.H is NOT NULL;"
            cursor.execute(sql.format(str(user_nick)))
            
            for i in cursor.fetchall() :
                purchase_prdt.append([float(i[0].replace("'","")), float(i[1].replace("'","")), float(i[2].replace("'",""))])

        return purchase_prdt

class ColorClustering:
    hsv_list = list()
    ctrl, scale = [10, 5], [20, 10] # ctrl = [H조정값, SV조정값] / scale = [H확장규모, SV확장규모]
    
    def colorGenerator(self, hsv):
#         self.hsv_list = hsv_list # hsv_list = [[h1, s1, v1], [h2, s2, v3], ...]

        ## extend color scale
        for (h, s, v), i in zip(hsv, range(len(hsv))):
            ## hsv 제너레이팅 범위 설정 시 색범위를 벗어나지 않도록 방지

            if (h-self.ctrl[0]) < 0:        # h 시작값 (최소 0)
                h_start = 0
            else:
                h_start = (h-self.ctrl[0])
            if (h+self.ctrl[0]) > 359:      # h 종료값 (최대 359)
                h_end = 359
            else:
                h_end = (h+self.ctrl[0])

            if (s-self.ctrl[1]) < 0:        # s 시작값 (최소 0)
                s_start = 0
            else:
                s_start = (s-self.ctrl[1])
            if (s+self.ctrl[1]) > 100:      # s 종료값 (최대 100)
                s_end = 100
            else:
                s_end = (s+self.ctrl[1])

            if (v-self.ctrl[1]) < 0:        # v 시작값 (최소 0)
                v_start = 0
            else:
                v_start = (v-self.ctrl[1])
            if (v+self.ctrl[1]) > 100:      # v 종료값 (최대 100)
                v_end = 100
            else:
                v_end = (v+self.ctrl[1])


            ## 첫번째 hsv 제너레이팅 배열생성
            if i==0:
                V, H = np.mgrid[v_start:v_end:complex(self.scale[1]), h_start:h_end:complex(self.scale[0])]
                S, H = np.mgrid[s_start:s_end:complex(self.scale[1]), h_start:h_end:complex(self.scale[0])]

            ## 첫번째 배열 + 나머지 hsv 제너레이팅 배열 합치기
            else:
                V_n, H_n = np.mgrid[v_start:v_end:complex(self.scale[1]), h_start:h_end:complex(self.scale[0])]
                S_n, H_n = np.mgrid[s_start:s_end:complex(self.scale[1]), h_start:h_end:complex(self.scale[0])]

                H = np.hstack((H, H_n))
                S = np.hstack((S, S_n))
                V = np.hstack((V, V_n))

        HSV = np.dstack((H, S, V))

        return HSV
    
    
    ## Gray tone Filtering : 1. 채도S 명도V 모두 20이하 2, 채도S+(100-명도V)가 20이하 3. (100-채도S)+명도V가 20이하
    ### ## 고객 구매 목록 색정보 받아서 사용 
    def greytoneFilter(self, prdt_hsv_list):
#         hsv_list = [] # 회색조 필터링 hsv 담을 변수
        for h, s, v in prdt_hsv_list:
            if (s<=30 and v<=30) or ((s+(100-v))<=20) or (((100-s)+v)<=20):
                pass
            else:
                self.hsv_list.append([h, s, v])
        return self.hsv_list
    
    
    ## Clustering 구매상품 데이터 적용용
    def colorClustering(self, HSV):
        ## Cluster 개수
        n_hsv, n_ctrl = len(self.hsv_list), 7
        if n_hsv/n_ctrl <= 2:
            if n_hsv < 5:
                n_clusters = n_hsv
            else:
                n_clusters = 5
        else:
            n_clusters = (n_hsv//n_ctrl)+5

        ## Clustering Dataset 생성
        X = HSV[:, :, :3].reshape(HSV.shape[0]*HSV.shape[1], HSV.shape[2])
        ## 알고리즘 선정 : Hierarchical
        algorithm = AgglomerativeClustering(n_clusters=n_clusters, affinity="euclidean")
        ## Clustering 실행
        with ignore_warnings(category=UserWarning):
            algorithm.fit(X)
        if hasattr(algorithm, 'labels_'):
            y_pred = algorithm.labels_.astype(np.int)
        else:
            y_pred = algorithm.predict(X)

        ## centroid(중심점)찾기
        clf = NearestCentroid()
        centroid = clf.fit(X, y_pred).centroids_

        return centroid
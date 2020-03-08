# 퍼스널 컬러 타입 분류
# 최초 작성일 : 20/02/11
# 작성자 : 조예슬
#
# 작성내용 : HSV로 기준 세워 퍼스널 컬러 타입 분류
#
# 수정내용 :
#     20/02/19
#         - 분류기준 먼셀에서 HSV로 변경
#
#     20/02/20
#         - 퍼스널 컬러 타입 결과 숫자로 지정, return 재배치, 타입 기준점(Cool의 Detail) 재조정
#
#     20/02/24
#         - class 형식 추가
#
#     20/02/25
#         - class 형식 return 추가, 불필요한 함수 제거
#
#     20/03/04
#         - pycharm 파일로 작성
#
#     20/03/05
#         - 수학적 오류 수정
#
#     20/03/08
#         - H 범위 수정



# 함수
# 기준값에 따라 분류하기

# Class
# 기준값에 따라 분류하기

class Color:
    person_HSV = []

    def color_classifier(self, person_HSV):
        self.H = float(person_HSV[0])
        self.S = float(person_HSV[1])
        self.V = float(person_HSV[2])
        diff = round(self.V - self.S, 2)

        color_type = ["WSB", "WSL", "WAD", "WAM", "CSL", "CSM", "CWB", "CWD"]

        if self.H >= 23 and self.H <= 203:
            if diff >= 43.15:
                if self.S >= 32.47:
                    self.ans = 0
                    # Warm Spring Bright
                else:
                    self.ans = 1
                    # Warm Spring Light

            elif diff < 43.15:
                if self.S >= 32.47:
                    self.ans = 2
                    # Warm Autumn Deep
                else:
                    self.ans = 3
                    # Warm Autumn Mute

        elif (self.H >= 0 and self.H < 23) or (self.H > 203 and self.H <= 360):
            if diff >= 47.15:
                if diff >= 60.80:
                    self.ans = 4
                    # Cool Summer Light
                else:
                    self.ans = 5
                    # Cool Summer Mute

            elif diff < 47.15:
                if diff >= 23.58:
                    self.ans = 6
                    # Cool Winter Bright
                else:
                    self.ans = 7
                    # Cool Winter Deep

        else:
            self.ans = -1
            # 에러

        return self.ans
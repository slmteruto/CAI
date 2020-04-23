# 퍼스널 컬러 타입 분류(수정파일)
# 최초 작성일 : 20/04/23
# 작성자 : 조예슬
#
# 작성내용 :
#
#         퍼스널컬러 타입 기준점 재조정 후


# 함수
# 기준값에 따라 분류하기

# Class
# 기준값에 따라 분류하기

class Color :
    person_HSV = []
        
    def color_classifier(self, person_HSV) :    
        self.H = float(person_HSV[0])
        self.S = float(person_HSV[1])
        self.V = float(person_HSV[2])
        diff = round(self.V - self.S, 2)
    
        color_type = ["WSB", "WSL", "WAD", "WAM", "CSL", "CSM", "CWB", "CWD"]

        if self.H >= 23 and self.H <= 203 : 
            if diff >= 46.25 :
                if self.S >= 31.00 :
                    self.ans = 0
                    # Warm Spring Bright                            
                else :
                    self.ans = 1
                    # Warm Spring Light

            elif diff < 46.25:
                if self.S >= 46.22 :
                    self.ans = 2
                    # Warm Autumn Deep                
                else :
                    self.ans = 3
                    # Warm Autumn Mute

        elif (self.H >= 0 and self.H < 23) or (self.H > 203 and self.H <= 360) :
            if diff >= 48.75 :
                if diff >= 28.47 :
                    self.ans = 4
                    # Cool Summer Light                
                else :
                    self.ans = 5
                    # Cool Summer Mute

            elif diff < 48.75:
                if diff >= 31.26 :
                    self.ans = 6
                    # Cool Winter Bright                
                else :
                    self.ans = 7
                    # Cool Winter Deep

        else :
            self.ans = -1
            # 에러
            
        return self.ans
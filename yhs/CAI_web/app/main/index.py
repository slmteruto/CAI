from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app


# index라는 파일이 들어갈 때 이름을 어떻게 결정하는지
# url_prefix는 URL 뒤를 어떻게 결정할지
main = Blueprint('main', __name__, url_prefix='/')

# 파일 내부에서 어떤 경로로 나타낼지
@main.route('/main', methods=['GET'])
def index() :
    testData = "testData array"
    #/main/index.html 은 /app/templates/main/index.html을 가리킴
    return render_template('/main/index.html', testDataHtml = testData)




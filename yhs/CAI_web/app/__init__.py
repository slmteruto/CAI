from flask import Flask
app = Flask(__name__)

#파일이름이 index이다.
from app.main.index import main as main

# import를 as main으로 했기 때문에 이렇게 연동해준다.
app.register_blueprint(main)
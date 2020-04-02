from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

app = Flask(__name__)

############ function ###################
def type_classifier(img) :
    pass

def img_db_save(img) :
    pass

############# main ######################
@app.route("/")
def hello():
    return render_template('CAI_main.html')


@app.route("/main/")
def main() :
    return render_template('CAI_main.html')

## menu2
@app.route("/color_recommnd")
def color_recommnd() :
    return render_template('CAI_palette.html')

## menu3
@app.route("/musinsa_recommnd")
def musinsa_recommnd() :
    return render_template('CAI_recomend.html')

## upload
@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f'static/uploads/{secure_filename(f.filename)}')

        img_pil = Image.open(f)
        img_cv = np.array(img_pil)
        img_cv = img_cv[:,:,::-1].copy()  ## RGB
        plt.imshow(img_cv)
        plt.show()
        return render_template('CAI_main.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
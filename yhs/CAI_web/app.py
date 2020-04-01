from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('CAI_main.html')

############# main ######################
@app.route("/main/")
def main() :
    return render_template('CAI_main.html')


## upload
@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f'static/uploads/{secure_filename(f.filename)}')
        return render_template('CAI_main.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
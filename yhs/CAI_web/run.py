from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('main.html')

@app.route("/main/")
def main() :
    return render_template('web_main_test.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
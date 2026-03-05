from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/sign_up")
def signUp():
    return render_template("sign_up.html")
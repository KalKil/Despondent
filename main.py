from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route("/")
def index():
    print("despondent_testing_site")
    return render_template("home.html.jinja")
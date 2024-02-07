from flask import Flask, render_template, request
import os


app = Flask(__name__)

img = os.path.join("static", "images")

@app.route("/")
def index():
    file = os.path.join(img, "img.jpg")
    return render_template(
        "index.html", img=file, content="Let's tackle one problem at a time!")

@app.route("/form_login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        return "success"

@app.route("/fizzbuzz/<int:num>")
def fizzBuzz(num):
    if num % 3 == 0 and num % 5 == 0:
        return "FizzBuzz"
    elif num % 3 == 0:
        return "Fizz"
    elif num % 5 == 0:
        return "Buzz"
    return str(num)

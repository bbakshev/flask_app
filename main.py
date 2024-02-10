from flask import Flask, render_template, request, redirect, url_for
import os


app = Flask(__name__)

img = os.path.join("static", "images")

@app.route("/")
def index():
    file = os.path.join(img, "img.jpg")
    return render_template(
        "index.html", img=file, content="Let's tackle one problem at a time!")

user = "admin"
pwd = "password"

@app.route("/form_login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username != user and password != pwd:
            return {
                "status": "fail",
                "message": "Invalid Inputs",
                "invalid_fields": [
                    { 'id': 'username', 'message': 'Username is not valid' },
                    { 'id': 'pwd', 'message': 'Password is not valid' }
                ]
            }
        elif username != user:
            return {
                "status": "fail",
                "message": "Invalid Inputs",
                "invalid_fields": [
                    { 'id': 'username', 'message': 'Username is not valid' }
                ]
            }
        elif password != pwd:
            return {
                "status": "fail",
                "message": "Invalid Inputs",
                "invalid_fields": [
                    { 'id': 'pwd', 'message': 'Password is not valid' }
                ]
            }
        return redirect(url_for("youCanViewThis"))
    return render_template("login.html")

@app.route("/fizzbuzz/<int:num>")
def fizzBuzz(num):
    if num % 3 == 0 and num % 5 == 0:
        return "FizzBuzz"
    elif num % 3 == 0:
        return "Fizz"
    elif num % 5 == 0:
        return "Buzz"
    return str(num)

@app.route("/success")
def youCanViewThis():
    return render_template("youCanView.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, threaded=True)
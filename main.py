from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    session)
import os


app = Flask(__name__)
# Set secret key
app.secret_key = "thisIsATest"

img = os.path.join("static", "images")
file = os.path.join(img, "img.jpg")

@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template(
        "index.html", img=file, content="Let's tackle one problem at a time!"
    )

user = "admin"
pwd = "password"

@app.route("/form_login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        session["password"] = request.form["password"]
        invalid_fields = []
        if session["username"] != user:
            invalid_fields.append(
                {"id": "username", "message": "Username is not valid"}
            )
        if session["password"] != pwd:
            invalid_fields.append(
                {"id": "password", "message": "Password is not valid"}
            )
        return {
            "status": "success" if len(invalid_fields) == 0 else "fail",
            "invalid_fields": invalid_fields,
        }
    else:
        redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, threaded=True)

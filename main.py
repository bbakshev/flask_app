from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    session)
import os
from models import user
import hashlib


app = Flask(__name__)
# Set secret key
app.secret_key = "thisIsATest"
salt = os.environ.get("SALT")

img = os.path.join("static", "images")
file = os.path.join(img, "img.jpg")

@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template(
        "index.html", img=file, content="Let's tackle one problem at a time!"
    )

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        pass    
    return render_template("signup.html")


@app.route("/form_login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        invalid_fields = []
        user_account = user.getByUsername(request.form["username"])
        if user_account is None:
            invalid_fields.append(
                {"id": "username", "message": "Username does not exist"}
            )
        hashed_string = hashlib.sha256()
        hashed_string.update((salt + request.form["password"]).encode("utf-8"))
        hashed_pass = hashed_string.hexdigest()
        print(hashed_pass)
        if user_account is not None and user_account[3] != hashed_pass:
            invalid_fields.append(
                {"id": "password", "message": "Password is not valid"}
            )
        print(user_account)
        if len(invalid_fields) == 0:
            session["username"] = request.form["username"]
            session["password"] = request.form["password"]
            
        return {
            "status": "success" if len(invalid_fields) == 0 else "fail",
            "invalid_fields": invalid_fields,
        }
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
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

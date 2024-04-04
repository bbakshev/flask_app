from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from models import user
import hashlib, secrets, re
from postmarker.core import PostmarkClient


app = Flask(__name__)

# Set secret key
app.secret_key = "thisIsATest"
salt = os.environ.get("SALT")
token = secrets.token_hex(2)
is_verified = False
postmark = PostmarkClient(server_token=os.environ.get("POSTMARK_TOKEN"))
email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

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
        invalid_fields = []
        username = request.form["username"]
        name = request.form["name"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        email = request.form["email"]
        user_account = user.getByUsername(username)

        if len(username) < 4 or len(username) >= 12:
            invalid_fields.append(
                {
                    "id": "username",
                    "message": "Username must contain characters between 4 and 12",
                }
            )
        if not username.isalnum():
            invalid_fields.append(
                {
                    "id": "username",
                    "message": "Username may only contain letters and numbers",
                }
            )
        if email_pattern == email:
            invalid_fields.append(
                {
                    "id": "email", 
                    "message": "Email is invalid"
                }
            )
        if user_account is not None:
            invalid_fields.append(
                {
                    "id": "username", 
                    "message": "Username already exist"
                }
            )
        if len(password) < 4:
            invalid_fields.append(
                {
                    "id": "password",
                    "message": "Password length should be not be less than four characters",
                }
            )
        if password != confirm_password:
            invalid_fields.append(
                {
                    "id": "confirm_password", 
                    "message": "Passwords must match!"
                }
            )

        hashed_string = hashlib.sha256()
        hashed_string.update((salt + password).encode("utf-8"))
        hashed_pass = hashed_string.hexdigest()

        if len(invalid_fields) == 0:
            user.createUser(name, username, email, hashed_pass, token, is_verified)
            confirm_url = url_for('emailConfirmation', token=token, _external=True)
            html = render_template("confirmation.html", confirm_url=confirm_url)
            flash("A confirmation email has been sent via email.")

            postmark.emails.send(
            From="",
            To=email,
            Subject="Please confirm your email",
            HtmlBody=html,
        )
            return {
                "status": "success",
                "message": "Your account has been successfully created",
            }
        return {
            "status": "fail",
            "invalid_fields": invalid_fields,
        }
    if request.method == "GET":
        return render_template("signup.html")

@app.route("/confirmation/<token>", methods=["GET", "POST"])
def emailConfirmation(token):
    invalid_fields = []
    user_verification = user.getVerificationCode(token)

    if user_verification[4] != token:
        invalid_fields.append(
                {
                    "id": "verification", 
                    "message": "Invalid Code"
                }
            )
    if len(invalid_fields) == 0:
        user.isVerified(token, True)
        flash("You are verified")
        invalid_fields.append(
                {
                    "status": "success",
                    "message": "You are verified",
                }
            )
        return redirect(url_for('login'))
    return render_template("confirmation.html")

@app.route("/verification_code", methods=["GET", "POST"])
def emailVerification():
    if request.method == "POST":
        invalid_field = []
        verification = request.form["verification"]
        user_code = user.getVerificationCode(verification)

        if user_code[4] != verification:
            invalid_field.append(
                {
                    "id": "verification", 
                    "message": "Invalid Code"
                }
            )
        if len(invalid_field) == 0:    
            user.isVerified(user_code[0], True)
            invalid_field.append(
                {
                    "status": "success",
                    "message": "You are verified",
                }
            )
            return redirect(url_for('login'))

    return render_template("verification_code.html")

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

        if len(invalid_fields) == 0:
            session["username"] = request.form["username"]
            session["password"] = request.form["password"]

        return {
            "status": "success" if len(invalid_fields) == 0 else "fail",
            "invalid_fields": invalid_fields,
        }
    return render_template("login.html")


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        print("Post")
    return "Password"


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

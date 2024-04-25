# User Registration

#### By: Bri Bakshev


## Overview
This application is a simple user registration and authentication system built using Python Flask and PostgreSQL. It facilitates the registration of users, handles secure password storage, sends email verifications, and manages user sessions for logged-in states.

![img] (./img.png)

## Features
- **User Registration:** Users can sign up by providing essential information, which is then stored securely in a PostgreSQL database.
- **Email Verification:** Upon registration, users receive an email with a verification link. Clicking this link verifies their account by updating their status in the database.
- **User Login:** After account verification, users can log in to access protected resources. The system checks credentials and grants access only to verified accounts.
- **Session Management:** User sessions are maintained until the user logs out, ensuring that users remain logged in even if they navigate away from the app.
- **Security:** Passwords are securely hashed before being stored in the database. The application also implements basic session management to handle user logins and logouts securely.

## Technical Stack
- **Backend:** Python Flask — Handles HTTP requests, session management, and all backend logic.
- **Database:** PostgreSQL — Used for storing user data, including usernames, hashed passwords, email addresses, and verification status.
- **Frontend:** HTML, CSS, and minimal JavaScript — Provides a basic user interface for registration, login, and session management.
- **Email Service:* Uses an external email service (Postmark) provider to send verification emails to users.

## Getting Started
1. Clone the repository:
`git clone https://github.com/bbakshev/user-authentication-flask-app`
`cd /user-authentication-flask-app`

2. Set up a virtual environment:
`python -m venv venv`

3. Install dependencies:
`pip install -r requirements.txt`

4. Configure the database:
- Ensure PostgreSQL is installed and running.
- Create a database for the application.

5. Run the application:
`pip main.py`

## Usage
- Access the application via http://localhost:5000 in your web browser.
- Register a new account, check your email for the verification link, and proceed to log in.

## License
Enjoy the site! If you have questions or suggestions for fixing the code, please contact me!

[MIT](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt)
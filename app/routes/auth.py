from flask import Flask, redirect

app = Flask(__name__)

COGNITO_SIGNUP_URL = "https://ap-northeast-1mlcv35dkj.auth.ap-northeast-1.amazoncognito.com/signup?client_id=7ln0qbqk35mjv7dp9uuvsav1a&response_type=code&scope=openid&redirect_uri=https%3A%2F%2Fkouden-summary.com%2Foauth2%2Fidpresponse"

@app.route("/signup")
def signup():
    return redirect(COGNITO_SIGNUP_URL)

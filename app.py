from flask import Flask, render_template, redirect, flash, url_for


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/menu/")
def sidebar():
    return render_template('./dashbord/base.html')

@app.route('/user/')
def user():
    return render_template('./users/interface_users.html')

if __name__ == "__main__":
    app.run(debug=True)
    
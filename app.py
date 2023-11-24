from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/interface_users")
def interface_users():
    return render_template("./users/interface_users.html")

if __name__ == "__main__":
    app.run(debug=True)
    
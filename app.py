from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/sidebar/")
def sidebar():
    return render_template('./partials/sidebar.html')

@app.route("/menu/")
def menu():
    return render_template('./dashbord/base.html')
if __name__ == "__main__":
    app.run(debug=True)
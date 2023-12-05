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

@app.route('/test/')
def test():
    return render_template('./users/test/test.html')
@app.route('/register/')
def register():
    return render_template('./register.html')
@app.route('/login/')
def login():
    return render_template('./login.html')

@app.route('/file/')
def file():
    return render_template('./users/file_upload.html')

@app.route("/abonne/")
def abonne():
    return render_template("./admin/view_user.html")
@app.route('/result/')
def result():
    return render_template('./users/test/result.html')

@app.route('/defeat/')
def defeat():
    return render_template("./users/test/defeat.html")

@app.route("/category")
def category():
    return render_template("./category.html")

@app.route("/mode_paiement/")
def mode_paiement():
    return render_template('./users/mode_paiement.html')

@app.route("/view_test/")
def view_test():
    return render_template('./admin/view_test.html')

@app.route("/view_module/")
def view_module():
    return render_template('./admin/view_module.html')

@app.route("/add_module/")
def add_module():
    return render_template('./admin/add_module.html')

@app.route("/add_cours/")
def add_cours():
    return render_template('./admin/add_cours.html')

@app.route("/add_question/")
def add_question():
    return render_template('./admin/add_question.html')
@app.route("/add_test/")
def add_test():
    return render_template('./admin/add_test.html')


if __name__ == "__main__":
    app.run(debug=True, port=5001)
    
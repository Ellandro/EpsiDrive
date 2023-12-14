import os
from datetime import datetime

import pymysql
from flask import Flask, render_template, redirect, flash, url_for, request, session
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from wtforms import FileField, SubmitField
from flask_wtf import FlaskForm
from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
# ? Les informations pour la connexion à ma db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'epsidrive'

app.config['UPLOAD_FOLDER'] = './static/photo_db'
app.config['TEST_FOLDER'] = './static/test_photo'
app.config['QUESTION_FOLDER'] = './static/question_photo'



app.secret_key = '53d79e2d442ce46fe29409f0940345866d6dcc8e25ae10540b125bfadc51553a'
bcrypt = Bcrypt(app)

mail = Mail(app)
s = URLSafeTimedSerializer('Thisisasecret!')
@app.route("/")
def home():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'] ,
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    return render_template("index.html")


app.config['UPLOAD_FOLDER'] = 'static/Images'





class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route('/upload_file/', methods=['GET',"POST"])
def upload_file():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        return "File has been uploaded."
    return render_template('upload_file.html', form=form)

@app.route("/menu/")
def sidebar():
    return render_template('./dashbord/base.html')

@app.route('/user/')
def user():
    return render_template('./users/interface_users.html')

@app.route('/test/')
def test():
    return render_template('./users/test/test.html')
@app.route('/register/', methods=["POST", "GET"])
def register():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    if request.method == "POST":
       if(request.form["prenom"]=="" or
           request.form["nom"]==""or
           request.form["jour"]=="" or
           request.form['mois']=="" or
           request.form["anne"]=="" or
           request.form['tel']==""or
           request.form['mail']=="" or
           request.form['password']=="" or
           request.form['pass']==""):
           # Afficher un message flash
           flash("Veuillez remplir les champs svp", category="success")
       else:
            prenom = request.form["prenom"]
            nom = request.form["nom"]
            jour = request.form["jour"]
            mois = request.form['mois']
            annee = request.form["anne"]
            tel = request.form['tel']
            mail = request.form['mail']
            password = request.form['pass']
            mdp = request.form['password']
            if(mdp!=password):
                flash("Mot de passe non conforme!")
            else:
                date_complete_str = f"{annee}-{mois.zfill(2)}-{jour.zfill(2)}"

                # Convertissez la chaîne en objet datetime
                date_complete = datetime.strptime(date_complete_str, "%Y-%m-%d").date()
                print(date_complete)
                mdp = bcrypt.generate_password_hash(mdp)
                print(mdp)
                select = "SELECT * FROM utilisateurs where Email=%s"
                cursor.execute(select,(mail,))
                user = cursor.fetchone()
                if(user):
                   flash("ce mail existe deja !")
                else:
                    insert = "INSERT INTO utilisateurs (Prenom , Nom, Email,Telephone,Date_naissance, MotDePasse) value(%s,%s, %s, %s, %s, %s)"
                    cursor.execute(insert, (prenom, nom, mail, tel, date_complete, mdp))
                    cursor.connection.commit()
                    session['logged_in'] = True
                    return redirect(url_for('home'))

    return render_template('./register.html')
@app.route('/login/', methods=['POST', 'GET'])
def login():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    if(request.method=="POST"):
        mail = request.form["mail"]
        password = request.form["password"]
        if(mail=="" or password==""):
            flash("Veuillez saisir les champs svp!!")
        else:
            select = "SELECT U.*, R.NomRole FROM utilisateurs U, roles R where U.IDRole=R.IDRole AND Email=%s"
            cursor.execute(select,(mail,))
            user=cursor.fetchone()
            if(user):
                if not bcrypt.check_password_hash(user[ 7], password):
                    # Le mot de passe fourni ne correspond pas au mot de passe haché dans la base de données
                    # Faites quelque chose ici, par exemple, afficher un message d'erreur ou rediriger l'utilisateur
                    flash("Mot de passe ou email incorrect")
                else:
                    session['logged_in'] = True
                    if(user[9]=="user"):
                        session['user']=user
                        return redirect(url_for("user"))
                    else:
                      session["admin"] = user
                      print(user)
            else:
                flash("Mot de passe ou Email inexistant")
    return render_template('./login.html')

@app.route("/profil_user/")
def profil_user():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    if (not (session.get("user"))):
        flash("Vous n'avez pas les droits d'accès à cette page.", "error")
        return redirect(url_for("login"))
    else:
        select = "SELECT * FROM utilisateurs where IDUtilisateur=%s"
        cursor.execute(select,(session["user"][0],))
        profil = cursor.fetchone()
        #print(profil[8])
        return render_template("./users/profil_user.html", profil=profil)
    
    # profil
@app.route("/update_profil/", methods=["POST", "GET"])
def update_profil():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    if request.method=="POST":
        name = request.form["nom"]
        username = request.form["prenom"]
        mail = request.form["mail"]
        id = session["user"][0]
        update = "UPDATE utilisateurs set IDUtilisateur=%s,Prenom=%s, Nom=%s, Email=%s WHERE IDUtilisateur=%s"
        cursor.execute(update, (id, username, name, mail,id))
        cursor.connection.commit()
        select = "SELECT * FROM utilisateurs where IDUtilisateur=%s"
        cursor.execute(select, (session["user"][0],))
        profil = cursor.fetchone()
        print(profil[8])
        return render_template("./users/profil_user.html", profil=profil)

@app.route("/edit_password/", methods=["POST", "GET"])
def edit_password():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    if (request.method=="POST"):
        mdp=request.form["mdp"]
        new = request.form["new"]
        confirm = request.form["confirm"]
        select = "SELECT * FROM utilisateurs where IDUtilisateur=%s AND Email=%s"
        cursor.execute(select, (session["user"][0],session["user"][4]))
        profil = cursor.fetchone()
        if(profil):
            if not bcrypt.check_password_hash(profil[7], mdp):
                flash("Mot de passe ou email incorrect", "errors")
                return redirect(url_for('profil_user')+"#account-change-password")
            else:
                if(new!=confirm):
                    flash("Mot de passe non conforme")
                else:
                    new = bcrypt.generate_password_hash(new)
                    update = "UPDATE utilisateurs SET MotDePasse=%s where IDUtilisateur=%s"
                    cursor.execute(update, (new,session['user'][0]))
                    cursor.connection.commit()
                    return redirect(url_for('profil_user') + "#account-change-password")
    return redirect(url_for('profil_user')+"#account-change-password")
@app.route('/index', methods=['GET', 'POST'])
def index():
     if request.method == 'GET':
        return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'
        email = request.form['email']
        token = s.dumps(email, salt='email-confirm')
        msg = Message('Confirm Email', sender='anthony@prettyprinted.com', recipients=[email])

        link = url_for('confirm_email', token=token, _external=True)

        msg.body = 'Your link is {}'.format(link)

        mail.send(msg)

        return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    return '<h1>The token works!</h1>'
@app.route('/file/')
def file():
    return render_template('./users/file_upload.html')

@app.route("/abonne/")
def abonne():
    if (not (session.get("admin"))):
        flash("Vous n'avez pas les droits d'accès à cette page.", "error")
        return redirect(request.referrer)
    else:
        return render_template("./admin/view_user.html")


@app.route('/add_question/', methods=['GET', 'POST'])
def add_question():
    conn = pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['MYSQL_PASSWORD'],
                           database=app.config['MYSQL_DB'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM testsmodule")
    data = cur.fetchall()
    if request.method == 'POST':
        nom_question = request.form['nom_question']
        Description = request.form['Description']
        Choix1 = request.form['Choix1']
        Choix2 = request.form['Choix2']
        Choix3 = request.form['Choix3']
        Choix4 = request.form['Choix4']
        test = request.form['test']
        reponse = request.form["reponse_correcte"]

        # Traitement de l'image
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['QUESTION_FOLDER'], filename))
        else:
            filename = None

            # Enregistrement dans la base de données
        cur.execute('''
                       INSERT INTO questionstest  VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)
                   ''', (None,test,nom_question, Description, Choix1, Choix2, Choix3, Choix4, filename))
        conn.commit()
        cur.execute("select * FROM questionstest where Nom_question = %s", (nom_question,))

        id_question = cur.fetchone()
        id_question = id_question[0]
        cur.execute("""
                insert into reponsestest values(%s,%s, %s, %s)
        """, (None, test, id_question, reponse))
        print(id_question, nom_question)
        conn.commit()
        conn.close()
        flash("Votre demande a été envoyé!", 'succes')
    return render_template('./admin/add_question.html', data_test=data)


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
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM  modulesenseignes")
    module = cursor.fetchall()
    print(module)
    return render_template('./admin/view_module.html' ,module=module)

@app.route("/add_module/" ,methods=["POST","GET"])
def add_module():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM categoriespermis")
    cat = cursor.fetchall()
    if request.method == 'POST':
        IDModule = request.form.get('IDModule')
        NomModule = request.form.get('NomModule')
        categorie = request.form.getlist("Categorie[]")

        print(categorie)

        # Traitement de l'image
        image = request.files['image']

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        cursor.execute("SELECT * FROM  modulesenseignes WHERE   NomModule= %s", (NomModule,))
        existing_module = cursor.fetchone()
        if (existing_module):
            flash(f"Le module '{NomModule}' existe déjà.", 'warning')
        else:
            insert_query = "INSERT INTO modulesenseignes VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (None, NomModule, filename))
            cursor.connection.commit()
            cursor.execute("SELECT * FROM  modulesenseignes WHERE   NomModule= %s", (NomModule,))
            id_module = cursor.fetchone()[0]
            print(id_module)

            for element in categorie:
                cursor.execute("INSERT INTO modulecategorie value(%s, %s)", (id_module, element))
                cursor.connection.commit()
            flash(f"Le module: {IDModule}: {NomModule} a été ajouté avec succès", 'success')
    return render_template('./admin/add_module.html', title="add_module", categorie=cat)

@app.route("/add_cours/",methods=["POST", "GET"])
def add_cours():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    cursor.execute("select * from modulesenseignes")
    module = cursor.fetchall()
    if(request.method=="POST"):
        if(request.form["titre"]=="" or request.form["module"]=="" or request.form["contenu"]==""):
            flash("Les ne doivent pas etre vide")
        else:
            titre = request.form["titre"]
            modules = request.form["module"]
            contenu = request.form["contenu"]
            print([titre, modules,contenu])
            insert = "INSERT INTO cours values(%s, %s, %s, %s)"
            #cur = connection.cursor()
            cursor.execute(insert,(None,modules,titre,contenu))
            cursor.connection.commit()
            print(cursor)

    return render_template('./admin/add_cours.html', module=module)
@app.route("/view_cours/")
def view_cours():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    cursor.execute("Select * from cours")
    cours = cursor.fetchall()
    return render_template("./admin/view_cours.html", courses = cours)

@app.route("/add_test/", methods=["post", "GET"])
def add_test():
    conn = pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['MYSQL_PASSWORD'],
                           database=app.config['MYSQL_DB'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM modulesenseignes")
    data_module = cur.fetchall()

    if request.method == 'POST':
        nom_test = request.form['nom_test']
        id_module = request.form['module']

        # Traitement de l'image
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['TEST_FOLDER'], filename))
        else:
            filename = None

            # Enregistrement dans la base de données
        cur.execute('''
                       INSERT INTO testsmodule VALUES  (%s,%s, %s, %s)
                   ''', (None, id_module,nom_test, filename))
        conn.commit()
        conn.close()
        flash("Votre demande a été envoyé!", 'succes')
    return render_template('./admin/add_test.html', data_test=data_module)

@app.route("/user_sidbar/")
def user_sidbar():
    return render_template("./users/user_sidbar.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)


import os
import pdfkit
from datetime import datetime

import pymysql
from flask import Flask, render_template, redirect, flash, url_for, request, session,jsonify
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from wtforms import FileField, SubmitField
from flask_wtf import FlaskForm
from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

import paydunya
from paydunya import Store, invoice



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
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM modulesenseignes")
    modle = cursor.fetchall()
    cursor.execute("SELECT * FROM cours")
    nbr_cours = cursor.fetchall()
    nbr_cours = len(nbr_cours)
    cursor.execute("SELECT * FROM progression where Statut='lu'")
    nbr_lu = cursor.fetchall()
    nbr_lu = len(nbr_lu)
    percent = ((nbr_lu*100)/nbr_cours)
    print(percent)
    return render_template('./users/interface_users.html', module=modle, percent=percent)

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
                    if(user[10]=="user"):
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

@app.route('/liste_question/<int:test_id>', methods=['GET'])
def liste_question(test_id):
    conn = pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['MYSQL_PASSWORD'],
                           database=app.config['MYSQL_DB'])
    cur = conn.cursor()

    # Récupérez les questions associées au test_id depuis la base de données
    cur.execute(
        "SELECT question.id_question, test.Nom_test,question.Nom_test, question.Description, question.Choix1, question.Choix2, question.Choix3, question.Choix4, question.image FROM question INNER JOIN test ON question.id_test = test.id_test WHERE question.id_test = %s",
        (test_id,))
    data = cur.fetchall()

    conn.commit()
    conn.close()
    return render_template('liste_question.html', data_question=data)

@app.route('/autoecole/')
def autoecole():
   
    conn = pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['MYSQL_PASSWORD'],
                           database=app.config['MYSQL_DB'])
    cursor = conn.cursor()
    cursor.execute('SELECT * from autoecoles')
    autoecole = cursor.fetchall()
    return render_template('autoecole.html', liste = autoecole)


@app.route('/detail_question/<int:idtest>', methods=['GET', 'POST'])
def detail_question(idtest):
    conn = pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['MYSQL_PASSWORD'],
                           database=app.config['MYSQL_DB'])

    cur = conn.cursor()
    # Récupérez les questions associées au test_id depuis la base de données
    cur.execute(
        "SELECT * from questionstest where IDTest=%s",
        (idtest,))
    data = cur.fetchall()

    conn.commit()
    conn.close()
    return render_template('./admin/detail_question.html', data_detail=data)


@app.route('/ajouter_question', methods=['GET', 'POST'])
def ajouter_question():
    conn = pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['MYSQL_PASSWORD'],
                           database=app.config['MYSQL_DB'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM test")
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
                       INSERT INTO question (Nom_test, Description, Choix1, Choix2, Choix3, Choix4, id_test, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                   ''', (nom_question, Description, Choix1, Choix2, Choix3, Choix4, test, filename))
        conn.commit()
        cur.execute("select * FROM question where Nom_test = %s", (nom_question,))

        id_question = cur.fetchone()
        id_question = id_question[0]
        cur.execute("""
                insert into reponse values(%s,%s, %s, %s)
        """, (None, test, id_question, reponse))
        print(id_question, nom_question)
        conn.commit()
        conn.close()
        flash("Votre question a été ajoutée!", 'succes')
        return redirect(url_for('detail_question'))
    return render_template('ajouter_question.html', data_test=data)


@app.route('/Sup_question/<int:sup_id>', methods=['GET'])
def Sup_question(sup_id):
    sup_id = int(sup_id)
    conn = pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['MYSQL_PASSWORD'],
                           database=app.config['MYSQL_DB'])
    cur = conn.cursor()
    cur.execute('''
                        DELETE FROM questionstest WHERE IDQuestion  = %s''',
                (sup_id,))
    conn.commit()
    conn.close()
    flash("Votre question a été supprimer!", 'warning')
    return redirect(url_for('detail_question'))


@app.route('/Modif_question/<int:mod_id>', methods=['GET', 'POST'])
def Modif_question(mod_id):
    conn = pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['MYSQL_PASSWORD'],
                           database=app.config['MYSQL_DB'])
    cur = conn.cursor()
    if request.method == 'POST':
        nom_question = request.form['nom_question']
        Description = request.form['Description']
        Choix1 = request.form['Choix1']
        Choix2 = request.form['Choix2']
        Choix3 = request.form['Choix3']
        Choix4 = request.form['Choix4']
        test = request.form['test']

        # Traitement de l'image
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['QUESTION_FOLDER'], filename))
        else:
            filename = None

        cur.execute('''
                UPDATE questionstest SET Nom_test=?, Description=?, Choix1=?, Choix2=?, Choix3=?, Choix4=?, image=? WHERE Num_produit =?''',
                    (nom_question, Description, Choix1, Choix2, Choix3, Choix4, test, filename, mod_id))
        conn.commit()
        conn.close()
        flash("Votre question a été Modifiée!", 'succes')
        return redirect(url_for('detail_question'))
    mod_id = int(mod_id)
    conn = pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['MYSQL_PASSWORD'],
                           database=app.config['MYSQL_DB'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM question WHERE id_question  = %s", (mod_id,))
    data = cur.fetchone()
    return render_template(".admin/Modif_question.html", data_question=data)
@app.route('/result/')
def result():
    return render_template('./users/test/result.html')

@app.route('/defeat/')
def defeat():
    return render_template("./users/test/defeat.html")

@app.route("/category")
def category():
    return render_template("./category.html")

@app.route("/mode_paiement/", methods=["GET","POST"])
def mode_paiement():

    return render_template('./users/mode_paiement.html')


@app.route('/update_progression', methods=['POST'])
def update_progression():
    data = request.get_json()
    current_course_id = data['currentCourseId']
    utilisateur_id = session['user'][0]

    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()

    # Mettez à jour la progression pour l'utilisateur et le cours actuel
    cursor.execute("UPDATE progression SET Statut='lu' WHERE utilisateur_id=%s AND cours_id=%s",
                   (utilisateur_id, current_course_id))

    connection.commit()  # N'oubliez pas de valider la transaction

    return jsonify({'status': 'success'})



@app.route("/view_test/")
def view_test():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM  testsmodule")
    test = cursor.fetchall()
    return render_template('./admin/view_test.html',test = test)

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


@app.route("/edit_module/<string:IdModule>", methods=['POST', 'GET'])
def edit_module(IdModule):
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()

    if request.method == 'POST':
        NomModule = request.form.get('NomModule')
        categorie = request.form.getlist("Categorie[]")
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['TEST_FOLDER'], filename))
        else:
            filename = None
        cursor = connection.cursor()
        # Utilisez %s pour les substitutions de paramètres
        cursor.execute("UPDATE modulesenseignes SET NomModule=%s,image=%s WHERE IdModule=%s",
                       (NomModule, filename, IdModule,))
        connection.commit()

        flash(f"Le module n°{IdModule} a été modifié avec succès.")
        return redirect(url_for("view_module"))

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM modulesenseignes WHERE IdModule=%s", (IdModule,))
    data = cursor.fetchone()
    print(data)
    cursor.close()
    connection.close()
    return render_template("./admin/edit_module.html", data=data)

@app.route('/delete_module/<int:id_module>', methods=["GET","POST"])
def delete_module(id_module):
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM modulesenseignes where IDModule=%s",(id_module,))
    module = cursor.fetchone()
    if request.method == "POST":
        cursor.execute("DELETE FROM modulesenseignes WHERE IDModule=%s",(id_module,))
        cursor.connection.commit()
        connection.close()
        flash(f"Le module {module[0]} a bien été supprimé", "succes")
        return redirect(url_for("view_module"))

    return render_template("./admin/delete_module.html",data=module)
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
            titre   = request.form["titre"]
            modules = request.form["module"]
            contenu = request.form["contenu"]
            print([titre, modules,contenu])
            insert = "INSERT INTO cours values(%s, %s, %s, %s)"
            #cur = connection.cursor()
            cursor.execute(insert,(None,modules,titre,contenu))
            cursor.connection.commit()
            print(cursor)

    return render_template('./admin/add_cours.html', module=module)


@app.route("/modifier_add_cours/<string:id_cours>",methods=["POST", "GET"])
def modifier_add_cours(id_cours):
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    cursor.execute("select * from cours WHERE IDCours = %s",(id_cours,))
    data = cursor.fetchone()
    cursor.execute("select* from modulesenseignes")
    cour_modules = cursor.fetchall()
    if request.method == "POST":
            titre   = request.form["titre"]
            modules = request.form["module"]
            contenu = request.form["contenu"]
            print([titre, modules,contenu])
            cursor.execute('''
                    UPDATE cours
                    SET IDCours=%s, IDModule=%s,TitreCours=%s,Contenu=%s
                    WHERE IDCours = %s''',(id_cours,modules,titre,contenu,id_cours))
            cursor.connection.commit() 
            return redirect(url_for('admin_cours'))
    return render_template('./admin/modifier_add_cours.html',data=data, cour_modules=cour_modules)

@app.route("/suprimer_add_cours/<string:id_cours>",methods=["POST", "GET"])
def suprimer_add_cours(id_cours):
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()

    cursor.execute("DELETE FROM cours WHERE IDCours = %s", (id_cours,))
    connection.commit()

    connection.close()

    return redirect(url_for("admin_cours"))
    


# @app.route("/view_cours/")
# def view_cours():

@app.route("/view_cours/<int:module_id>")
def view_cours(module_id):
    if ((not session.get("user"))):
        return redirect(url_for('login'))
    else:
        connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                     user=app.config['MYSQL_USER'],
                                     password=app.config['MYSQL_PASSWORD'],
                                     database=app.config['MYSQL_DB'])
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM modulesenseignes ")
        data = cursor.fetchall()
        cursor.execute("Select * from cours Where IDModule = %s order by IDCours",(module_id,))

        cours = cursor.fetchall()
        cursor.execute("SELECT * FROM progression WHERE module_id=%s", (module_id,))
        nbr=cursor.fetchall()
        nbr = len(nbr)
        cursor.execute("SELECT * FROM progression WHERE module_id=%s and Statut='lu'", (module_id,))
        nb_lu=cursor.fetchall()
        nb_lu = len(nb_lu)
        nbre = ((nb_lu*100)/nbr)
        print(nbre)
        for row in cours:
            # Vérifiez si l'entrée existe déjà dans la table "progression"
            cursor.execute("SELECT * FROM progression WHERE utilisateur_id = %s AND module_id = %s AND cours_id = %s",
                           (session['user'][0], module_id, row[0]))
            existing_entry = cursor.fetchone()

            if not existing_entry:
                # Si l'entrée n'existe pas, insérez-la
                cursor.execute(
                    "INSERT INTO progression (id, utilisateur_id, module_id, cours_id, date_consultation) VALUES (%s, %s, %s, %s, %s)",
                    (None, session['user'][0], module_id, row[0], datetime.now()))

        return render_template("./admin/view_cours.html", courses = cours, nbr=nbre, data=data)


@app.route("/admin_cours/")
def admin_cours():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    cursor.execute("Select * from cours")
    cours = cursor.fetchall()
    return render_template("./admin/admin_cours.html", courses = cours)
@app.route("/modifier_add_cours/<string:id_cours>",methods=["POST", "GET"])
def modifier_add_cours(id_cours):
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    cursor.execute("select * from cours WHERE IDCours = %s", (id_cours,))
    data = cursor.fetchone()
    cursor.execute("select* from modulesenseignes")
    cour_modules = cursor.fetchall()
    if request.method == "POST":
        titre = request.form["titre"]
        modules = request.form["module"]
        contenu = request.form["contenu"]
        print([titre, modules, contenu])
        cursor.execute('''
                       UPDATE cours
                       SET IDCours=%s, IDModule=%s,TitreCours=%s,Contenu=%s
                       WHERE IDCours = %s''', (id_cours, modules, titre, contenu, id_cours))
        cursor.connection.commit()
        return redirect(url_for('admin_cours'))
    return render_template('./admin/modifier_add_cours.html', data=data, cour_modules=cour_modules)
@app.route("/suprimer_add_cours/<string:id_cours>",methods=["POST", "GET"])
def suprimer_add_cours(id_cours):
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()

@app.route("/admin_cours/")
def admin_cours():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    cursor.execute("Select * from cours")
    cours = cursor.fetchall()
    return render_template("./admin/admin_cours.html", courses = cours)


    cursor.execute("DELETE FROM cours WHERE IDCours = %s", (id_cours,))
    connection.commit()

    connection.close()

    return redirect(url_for("admin_cours"))
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
@app.route("/modifier_test/<int:test_id>", methods=["GET", "POST"])
def modifier_test(test_id):
    conn = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    cur = conn.cursor()

    # Récupérer les données du test existant et de son module concerné
    cur.execute("SELECT * FROM testsmodule WHERE IDTest=%s", (test_id,))
    test_data = cur.fetchone()

    # Récupérer les modules pour l'affichage dans le formulaire
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

        # Mettre à jour les données du test
        cur.execute('''
            UPDATE testsmodule 
            SET IDModule=%s, NomTest=%s, image=%s
            WHERE IDTest=%s
        ''', (id_module, nom_test, filename, test_id))

        conn.commit()
        conn.close()
        flash("Le test a été modifié avec succès!", 'success')
        return redirect(url_for('view_test'))

    conn.close()
    return render_template('./admin/modifier_test.html', data_test=data_module, data=test_data)


########################## GESTION DE LA SUPPRESSION D'UN TEST AJOUTE################################

@app.route("/supprimer_test/<int:test_id>", methods=["GET", "POST"])
def supprimer_test(test_id):
    conn = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    cur = conn.cursor()

    # Récupérer les données du test existant
    cur.execute("SELECT * FROM testsmodule WHERE IDTest=%s", (test_id,))
    test_data = cur.fetchone()

    if request.method == 'POST':
        # Supprimer le test de la base de données
        cur.execute("DELETE FROM testsmodule WHERE IDTest=%s", (test_id,))

        conn.commit()
        conn.close()
        flash("Le test a été supprimé avec succès!", 'success')
        return redirect(url_for('view_test'))

    conn.close()
    return render_template('./admin/supprimer_test.html', data=test_data)
@app.route("/add_auto/")
def add_auto():
    return render_template("admin/form_autoecole.html")
@app.route("/view_auto/")
def view_auto():
    return render_template("admin/autoecole.html")
@app.route("/user_sidbar/")
def user_sidbar():
    conn = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    cur = conn.cursor()

    # Récupérer les données du test existant
    cur.execute("SELECT * FROM modules ")
    data = cur.fetchall()
    return render_template("./users/user_sidbar.html", data = data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)


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


conn = pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['MYSQL_PASSWORD'],
                           database=app.config['MYSQL_DB'])
cursor = conn.cursor()
cursor.execute("INSERT INTO autoecoles(NomAutoEcole, Lieu) VALUES (%s, %s)",('ab','cd'))
# autoecole = cursor.fetchall()
# print(autoecole )
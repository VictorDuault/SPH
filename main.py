from flask import Flask, redirect, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from random import randint
from werkzeug.security import generate_password_hash, check_password_hash

#Format de la liste exo:
# [[nom, image(boolean), image(path en string), texte, points, ID(à la toute fin)], ...]
#L'id permettre de rendre la phase de correction beaucoup moins complexe!

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'dev'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods = ["POST", "GET"])
def home():
    return render_template('index.html')

@app.route('/c/projectionvectorielle')
def projvect():
    return render_template('cours/projectionvectorielle.html')

#Méthode pour s'enregistrer
@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        if User.query.filter_by(email=email).first():
            flash("L'Email est déjà enregistré!")
            return redirect('/register')
        id = generate_id()
        username = form.username.data
        password = generate_password_hash(form.password.data, method='sha256')
        user = User(id=id,email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    print(form.errors)
    return render_template('register.html', form = form)

#Méthode login
@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("L'Email ou le mot de passe est erroné")
            return redirect('/login')
        login_user(user, remember=True)
        return redirect('/')
    return render_template('login.html', form=form)

@app.route('/logout', methods=["POST", "GET"])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect('/')
    return redirect(url_for('home'))

@app.route('/profil')
@login_required
def profile():
    return render_template('profile.html', name= current_user.username)

@app.route('/ex/newton') 
def exercices():
    n = request.args.get('id',default=1, type=int)
    print(n)
    return render_template('exercices/newton.html', 
                           exo =  [["Nom", False, "", "Lorem Ipsum", "", 1],
                                ["Nom2", False, "", "Lorem Ipsum2", "", 2],
                                ["Nom3", False, "", "Lorem Ipsum3", "", 3]], 
                           n=n, path="/ex/newton")

#Méthode pour corriger les exercices
#Idée: Attribuer à chaque exercice un ID, le récupérer depuis les arguments.
#Ensuite dans la base de donnée on sauvegarde la réponse avec comme clé l'id de notre exercice puis on compare.
@app.route('/correction', methods=['POST'])
def correction():
    id = request.args.get('id', type=int)
    return redirect(request.referrer)


#Class User (flask-login)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(60), nullable = False)
    username = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(20), nullable = False)

#Générateur d'id
def generate_id():
    id = randint(100000, 999999)
    used = User.query.filter_by(id=id).first()
    if used:
        return generate_id()
    else:
        return id
    

class RegisterForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(max = 60)], render_kw={"placeholder": "Email", "class":"form-control mb-2"})
    username = StringField(validators=[InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder": "Nom d'utilisateur", "class":"form-control mb-2"})
    password = PasswordField(validators=[InputRequired(), Length(min = 4, max = 20), EqualTo('confirm', message='Les mots de passe sont différents!')], render_kw={"placeholder": "Confirmer le mot de passe", "class":"form-control mb-2"})
    confirm = PasswordField(validators=[InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder": "Mot de passe", "class":"form-control mb-2"})
    submit = SubmitField("Valider", render_kw={"class":"btn btn-primary mb-2"})
    
class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(max = 60)], render_kw={"placeholder": "Email", "class":"form-control mb-2"})
    password = PasswordField(validators=[InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder": "Confirmer le mot de passe", "class":"form-control mb-2"})
    submit = SubmitField("Valider", render_kw={"class":"btn btn-primary mb-2"})

if __name__ == '__main__':
    db.create_all()
    app.run()
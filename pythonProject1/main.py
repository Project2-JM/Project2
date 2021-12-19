from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from webforms import UserForm, passwordForm
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

#Create a Flask Instance
app = Flask(__name__)

#add Database
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:password@Localhost/mydb'
app.config["SQLALCHEMY_TRACK_MODIFACTIONS"] = False
#Sercet_key for Form Class
app.config['SECRET_KEY'] = "Hello123"

db = SQLAlchemy(app)

#Create a route decorator (HOME PAGE)
@app.route('/')
def index():
    return render_template('index.html')

#Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            #Hash the password!!! to hide the password
            user = Users(name=form.name.data, email=form.email.data, password_hash=form.password_hash.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        flash("User added")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("sign_up.html", form = form, name=name, our_users=our_users)


#Create Login Page
@app.route('/login', methods=['GET','POST'])
def name():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = passwordForm()
    #Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        #Clear the form
        form.email.data = ''
        form.password_hash.data = ''

    return render_template("login.html")

#Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User Updated Successful")
            return render_template("update.html", form =form, name_to_update=name_to_update)
        except:
            db.session.commit()
            flash("Error! Looks like ther was a problem... Try Again!!")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update)

 ########################MODELS ARE BELOW#######################################

#create Model
class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Do some password stuff!
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('passwors is not a readable')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #Create a string
    def __repr__(self):
        return '<Name %r>' % self.name

db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
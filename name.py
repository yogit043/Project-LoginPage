from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_manager,current_user
from sqlalchemy import text  # Import text from sqlalchemy
'''
In Python, the UserMixin module is typically associated with Flask-Login, a user session management library for Flask applications. The UserMixin module is part of the Flask-Login extension and provides a default implementation of methods required for user authentication.

The UserMixin module is designed to be used as a mixin class, meaning you can inherit from it in your user model class. It includes default implementations for common methods used in user authentication, such as:

is_authenticated: Returns True if the user is authenticated (i.e., they have provided valid credentials).

is_active: Returns True if the user account is active. This is useful for implementing account deactivation or suspension.

is_anonymous: Returns False for regular users, as they are not anonymous.

get_id: Returns a unique identifier for the user. This is usually the user's ID or a unique username.
'''
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,LoginManager,login_required

# first setting up our local server
# my database connection
local_server = True
app = Flask(__name__)
# giving a secret key to our app
app.secret_key = "yogit_034"


# this is for getting unique user access
#Intialize flask login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login view


# app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql://username:password@localhost/database_table_name'
# for xampp server username will be root itself and no password in this case so mysql://root:@localhost/hms
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/hms'
#
#In Flask, the app.config['SQLALCHEMY_DATABASE_URI'] setting is used to configure the connection to a SQL database.

db = SQLAlchemy(app)



# here we will create db models that are tables
# class name should be the same as the database name with the first letter capital
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Adding an 'id' column as the primary key
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50),unique = True)
    password = db.Column(db.String(1000))
    

@login_manager.user_loader
def load_user(user_id):
    # This function is used by Flask-Login to get a user by their ID.
    return User.query.get(int(user_id))


@app.route('/')
def hello():
    # return render_template('index.html')
    try:
        a = Test.query.all()  # when this function runs then only it returns
                              # checking whether the database is connected or not
        print(a)
        # print(a.name)
        # print(a.email)
        return render_template('index.html')
        # return "My database is connected"
    except Exception as e:
        return f"My database is not connected. Error: {str(e)}"

@app.route("/test")
def test():
    return "test"

@app.route("/doctors")
def doctors():
    return render_template("doctors.html")

@app.route("/patients")
@login_required
def patients():
    return render_template("patients.html")

@app.route("/booking")
def booking():
    if not current_user.is_authenticated:#using this we can check if the user is logged in then only go to booking page 
        return render_template('login.html')
    else:
        return render_template("booking.html", username=current_user.username)

@app.route("/signup", methods= ['POST','GET'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first() #left email is the email column in database

        if user:
            flash("Email Already Exists","warning")
            return render_template("signup.html")

        encpassword = generate_password_hash(password)
        
        # Use SQL command to insert values into the 'user' table
        sql = text("INSERT INTO user (username, email, password) VALUES (:username, :email, :encpassword)")
        db.session.execute(sql, {"username": username, "email": email, "encpassword": encpassword})
        db.session.commit()
        '''
        alternate
        newuser = User(username = username , email = email , password = encpassword)
        db.session.add(newuser)
        db.session.commit()
        '''
        flash("Signup Succesful Please Login","success")
        return redirect(url_for('login'))

    return render_template("signup.html")    

@app.route("/login", methods= ['POST','GET'])
def login():
    if request.method == "POST":
        # username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password): # right one represents the password provided by the user during the login attempt.
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for("booking"))
        else:
            flash("Invalid Credentials","danger")
            return render_template("login.html")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("LogOut Success","warning")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
# username = current_user.username
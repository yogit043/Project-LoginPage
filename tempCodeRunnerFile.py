from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

#first detting up our local server
#my database connection
local_server = True
app = Flask(__name__)
#giving a secret key to ourappn
app.secret_key = "yogit_034"

# app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql://username:password@localhost/database_table_name'
#for xampp server username will be root itself and no password in this case so mysql://root:@localhost/hms
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/hms'
db = SQLAlchemy(app)

# here we will create db models that is tables
#class name should be same as the databse name with first letter capital
class Test(db.Model):
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

@app.route('/')
def hello():
    # return render_template('index.html')
    try:
        db.create_all()  # Create tables if they do not exist
        return "My database is connected"
    except Exception as e:
        return f"My database is not connected. Error: {str(e)}"

@app.route("/test")
def test():
    return "test"
   #return render_template('test.html')
   
if __name__ == "__main__":
    app.run(debug = True)
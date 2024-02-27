from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 




db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\adity\\OneDrive\\Desktop\\project\\sqlalchemy_implementation\\app.db'
db.init_app(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    ip_address = db.Column(db.String(100))
    country = db.Column(db.String(100))
with app.app_context():
    db.create_all()
        
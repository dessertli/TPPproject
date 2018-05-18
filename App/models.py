from App.ext import db
from App.models_util import BaseModel


class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    letter = db.Column(db.String(1))



class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regionName = db.Column(db.String(16))
    cityCode = db.Column(db.Integer)
    pinYin = db.Column(db.String(128))
    c_letter = db.Column(db.Integer, db.ForeignKey(Letter.id))

class UserModel(BaseModel, db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        u_name = db.Column(db.String(16), unique=True)
        u_password = db.Column(db.String(256))
        u_email = db.Column(db.String(64), unique=True)
        is_active = db.Column(db.Boolean, default=False)
        is_delete = db.Column(db.Boolean, default=False)
        u_permission = db.Column(db.Integer, default=1)

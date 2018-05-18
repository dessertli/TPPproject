from App.ext import db


class BaseModel():
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return {"msg":"ok"}
        except Exception as e:
            return  {"msg":str(e)}

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return {"msg": "ok"}

        except Exception as e:
            return {"msg": str(e)}
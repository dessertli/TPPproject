import uuid

from flask import render_template
from flask_mail import Message
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_restful.representations import json
from werkzeug.security import generate_password_hash, check_password_hash

from App.ext import mail, cache
from App.models import UserModel

parse = reqparse.RequestParser()

user_fields = {
    "id": fields.Integer,
    "u_name": fields.String,
    "u_email": fields.String
}

result_fields = {
    "msg": fields.String,
    "data": fields.Nested(user_fields)
}
parse.add_argument("username", type=str, required=True, help="请提供用户名")
parse.add_argument("password", type=str, required=True, help="请输入密码")
parse.add_argument("email", type=str, required=True, help="请输入邮箱")

parse_get = reqparse.RequestParser()
parse_get.add_argument("action", type=str, help="请提供必要参数action")
parse_get.add_argument("u_token", type=str, help="用户标识丢失")

class UserResource(Resource):
    def get(self):
        parser = parse_get.parse_args()
        action = parser.get("action")
        u_token = parser.get("u_token")

        if action == "active":
            id = cache.get(u_token)
            if id:
                user = UserModel.query.get(id)
                user.is_active = True
                user.save()
                cache.delete(u_token)
                data = {"msg": "激活成功","my":"gg"}
                ret =  json.dumps(data, ensure_ascii=False)
                print(ret)
                return ret
            else:
                data ={"msg": "激活失败"}
                ret = json.dumps(data, ensure_ascii=False)
                print (ret)
                return ret
        else:
            return {"msg": "功能正在开发中"}

    @marshal_with(result_fields)
    def post(self):
        parser = parse.parse_args()
        username = parser.get("username")
        password = parser.get("password")

        users = UserModel.query.filter(UserModel.u_name.__eq__(username))
        if users.count() > 0:
            user = users.first()
            if check_password_hash(user.u_password, password):
                if user.is_active:
                    return {"msg": "ok", "data": user}
                else:
                    return {"msg": "用户还未激活，请先激活"}
            else:
                return {"msg": "密码错误"}
        else:
            return {"msg": "用户不存在"}
    @marshal_with(result_fields)
    def put(self):
        parser = parse.parse_args()

        username = parser.get("username")
        password = parser.get("password")
        email = parser.get("email")
        user = UserModel()
        user.u_name = username
        user.u_password = generate_password_hash(password=password)
        user.u_email = email
        user.save()
        u_token = str(uuid.uuid4())
        cache.set(u_token, user.id, timeout=60)
        msg = Message(subject="TestTppActive",sender="18020224157@163.com",recipients=["18020224157@163.com"])
        html = render_template("UserActivate.html", username=username, active_url="http://localhost:5000/users/?action=active&u_token=%s"%u_token)

        msg.html = html
        mail.send(msg)

        return {"msg":"ok","data":user}

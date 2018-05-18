from flask_restful import Resource, reqparse, abort

from App.models import UserModel

parse = reqparse.RequestParser()
parse.add_argument("id", type=int, required=True, help="请登录")


def check_permission(permission):
    def receive_permission(func):
        def do_permission(*args, **kwargs):
            parser = parse.parse_args()
            id = parser.get("id")
            user = UserModel.query.get(id)
            if not user:
                abort(401, message="请登录")
            if user.u_permission & permission == permission:
                print("继续做事情")
                return func(*args, **kwargs)
            else:
                abort(403, message="您没有权限，请联系系统管理员进行设置")
        return do_permission
    return receive_permission


READ = 1
WRITE = 2
MANAGE = 4


class OrderResource(Resource):

    @check_permission(WRITE)
    def get(self):
        # parser = parse.parse_args()
        # id = parser.get("id")
        #
        # user = UserModel.query.get(id)
        #
        # if not user:
        #     abort(401, message="请登录")
        #
        # if user.u_permission == 4:
        #     print("我可以阅读帖子")
        #     return {"msg": "读帖子权限"}
        # else:
        #     abort(403, message="你没有权限查看此模块，请联系响应管理员进行设置")
        return {"msg": "ok"}


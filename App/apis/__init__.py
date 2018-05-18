from flask_restful import Api

from App.apis.CityApi import AreaResource
from App.apis.OrderApi import OrderResource
from App.apis.UserApi import UserResource

api = Api()


def init_api(app):
    api.init_app(app=app)



api.add_resource(AreaResource,"/areas/")
api.add_resource(UserResource,"/users/")
api.add_resource(OrderResource, "/orders/")

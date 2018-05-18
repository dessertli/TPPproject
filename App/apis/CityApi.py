from flask import request
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal

from App.ext import cache
from App.models import Letter, City



city_fields = {
    "id": fields.Integer,
    "regionName": fields.String,
    "cityCode": fields.Integer,
    "pinYin": fields.String,
}
letter_city_fields = {
    "A": fields.List(fields.Nested(city_fields)),
    "B": fields.List(fields.Nested(city_fields)),
    "C": fields.List(fields.Nested(city_fields)),
    "D": fields.List(fields.Nested(city_fields)),
    "E": fields.List(fields.Nested(city_fields)),
    "F": fields.List(fields.Nested(city_fields)),
    "G": fields.List(fields.Nested(city_fields)),
    "H": fields.List(fields.Nested(city_fields)),
    "J": fields.List(fields.Nested(city_fields)),
    "K": fields.List(fields.Nested(city_fields)),
    "L": fields.List(fields.Nested(city_fields)),
    "M": fields.List(fields.Nested(city_fields)),
    "N": fields.List(fields.Nested(city_fields)),
    "P": fields.List(fields.Nested(city_fields)),
    "Q": fields.List(fields.Nested(city_fields)),
    "R": fields.List(fields.Nested(city_fields)),
    "S": fields.List(fields.Nested(city_fields)),
    "T": fields.List(fields.Nested(city_fields)),
    "W": fields.List(fields.Nested(city_fields)),
    "X": fields.List(fields.Nested(city_fields)),
    "Y": fields.List(fields.Nested(city_fields)),
    "Z": fields.List(fields.Nested(city_fields))
}

result_fields = {
    "returnCode": fields.String,
    "returnValue": fields.Nested(letter_city_fields)
}

class AreaResource(Resource):
    @cache.cached(timeout=30)
    @marshal_with(result_fields)
    def get(self):
        print("加载数据了")
        returnValues = {}

        letters = Letter.query.all()

        for letter in letters:
            letter_cities = City.query.filter_by(c_letter=letter.id)
            returnValues[letter.letter] = letter_cities

        return {"returnCode": "0", "returnValue": returnValues}

    def post(self):

        returnValues = {}

        letters = Letter.query.all()

        letter_city_fields_dynamic = {}

        for letter in letters:
            letter_city_fields_dynamic[letter.letter] = fields.List(fields.Nested(city_fields))
            letter_cities = City.query.filter_by(c_letter=letter.id)
            returnValues[letter.letter] = letter_cities

        result_fields_dynamic = {
            "returnCode": fields.String,
            "returnValue": fields.Nested(letter_city_fields_dynamic)
        }

        data = {"returnCode": "0", "returnValue": returnValues}
        result = marshal(data=data, fields=result_fields_dynamic)
        return result


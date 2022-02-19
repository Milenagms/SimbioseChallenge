from flask_restful import Resource
from flask import request, jsonify

employees = [
    {'register_number': 1,
     'full_name': 'Milena Ferreira Gomes',
     'CPF': '999.999.999.99'
     },
    {'register_number': 2,
     'full_name': 'Douglas Viana',
     'CPF': '123.999.999.99'
     },
    {'register_number': 4,
     'full_name': 'Roberto Paolo',
     'CPF': '999.123.999.99'
     },
    {'register_number': 3,
     'full_name': 'Bruno Sena',
     'CPF': '123.456.789.45'
     },
]


class Employees(Resource):
    @staticmethod
    def get():
        return {'Employees': employees}

class Employee(Resource):
    def get(self, register_number):
        for employee in employees:
            if employee['register_number'] == register_number:
                return employee

        return {'message': 'Desculpa, esse funcionário não se encontra na nossa base de dados'}

    def post(self, register_number):
        request_data = request.get_json()
        return jsonify(request_data)

    def delete(self, register_number):
        global employees
        employees = [employee for employee in employees if employee['register_number'] != register_number]
        return{'message': 'employee deleted'}
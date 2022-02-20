from flask_restful import Resource
from flask import request, jsonify
from sql_alchemy import project_base


class ModelEmployee(project_base.Model):
    __tablename__ = 'employess'
    register_number = project_base.Column(project_base.Integer, primary_key=True)
    full_name = project_base.Column(project_base.String(80))
    cpf = project_base.Column(project_base.Integer)

    def __init__(self, register_number, full_name, cpf):
        self.register_number = register_number
        self.full_name = full_name
        self.cpf = cpf

    def formatted_data(self):
        return {
            "Número de registro": self.register_number,
            "Nome completo": self.full_name,
            "CPF": self.cpf
        }


class Employees(Resource):
    @staticmethod
    def get():
        return {'Teams da Simbiose cadastrado': [employee.formatted_data() for employee in ModelEmployee.query.all()]}

class Employee(Resource):
    def get(self, register_number):
        for employee in employees:
            if employee['register_number'] == register_number:
                return employee

        return {'message': 'Desculpa, esse funcionário não se encontra na nossa base de dados'}

    def post(self, register_number):
        #  TODO criar uma verificação para quando já estiver criado;
        all_value = [request.json['full_name'], request.json['cpf']]
        print(all_value)
        new_employee = ModelEmployee(register_number, *all_value)
        project_base.session.add(new_employee)
        project_base.session.commit()
        return jsonify(request.json)

    def delete(self, register_number):
        # TODO pensar em um jeito de fazer isso e que funcione da proxima vez
        global employees
        employees = [employee for employee in employees if employee['register_number'] != register_number]
        return{'message': 'employee deleted'}
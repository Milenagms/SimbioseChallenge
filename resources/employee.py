from flask_restful import Resource
from flask import request, jsonify
from sql_alchemy import project_base
from resources.team import ModelTeam


class ModelEmployee(project_base.Model):
    __tablename__ = 'employess'
    register_number = project_base.Column(project_base.Integer, primary_key=True)
    full_name = project_base.Column(project_base.String(80))
    cpf = project_base.Column(project_base.Integer)
    sector_id = project_base.Column(project_base.Integer, project_base.ForeignKey('teams.team_id'))
    sector = project_base.relationship(ModelTeam)

    def __init__(self, register_number, full_name, cpf, sector_id):
        self.register_number = register_number
        self.full_name = full_name
        self.cpf = cpf
        self.sector_id = sector_id

    def formatted_data(self):
        print(self.sector)
        return {
            "Número de registro": self.register_number,
            "Nome completo": self.full_name,
            "CPF": self.cpf,
            "sector": self.sector.formatted_data()
        }


class Employees(Resource):
    @staticmethod
    def get():
        value = [employee.formatted_data() for employee in ModelEmployee.query.all()]
        if not value:
            return {'message': 'Not found'}, 404
        return {'All employess': value}


class Employee(Resource):
    @staticmethod
    def find_employee(register_number):
        return ModelEmployee.query.filter_by(register_number=register_number).first()

    def validate_cpf(self, cpf):
        var = ModelEmployee.query.filter_by(cpf=cpf).first()
        return var

    def get(self, register_number):
        an_employee = Employee.find_employee(register_number)
        if an_employee:
            return an_employee.formatted_data()

        return {'message': 'Desculpa, esse funcionário não se encontra na nossa base de dados'}, 404

    def post(self, register_number):
        an_employee = Employee.find_employee(register_number)
        if an_employee:
            return {"message": f"O funcionário '{register_number}' já existe"}, 400

        all_value = [request.json['full_name'], request.json['cpf'], request.json['sector_id']]
        a_database_cpf = Employee.validate_cpf(self, all_value[1])
        if a_database_cpf:
            return {'message': f'The cpf {a_database_cpf.cpf} already exists in our database'}, 400

        new_employee = ModelEmployee(register_number, *all_value)
        project_base.session.add(new_employee)
        project_base.session.commit()
        return jsonify(request.json)

    def delete(self, register_number):
        an_employee = Employee.find_employee(register_number)
        if an_employee:
            project_base.session.delete(an_employee)
            project_base.session.commit()
            return {'message': 'Funcionário deletado'}

        return {'message': 'Funcionário não encontrado'}, 404

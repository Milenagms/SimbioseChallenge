from flask_restful import Resource
from flask import request, jsonify
from sql_alchemy import project_base
from resources.team import ModelTeam


class ModelEmployee(project_base.Model):
    __tablename__ = 'employess'
    id = project_base.Column(project_base.Integer, primary_key=True)
    full_name = project_base.Column(project_base.String(80))
    cpf = project_base.Column(project_base.Integer)
    sector_id = project_base.Column(project_base.Integer, project_base.ForeignKey('teams.id'))
    sector = project_base.relationship(ModelTeam)

    def __init__(self, full_name, cpf, sector_id):
        self.full_name = full_name
        self.cpf = cpf
        self.sector_id = sector_id

    def serialize_json(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "CPF": self.cpf,
            "sector": self.sector.serialize_json()
        }


class Employees(Resource):
    @staticmethod
    def get():
        value = [employee.serialize_json() for employee in ModelEmployee.query.all()]
        if not value:
            return {'message': 'Not found in our dataset'}, 404
        return {'employees': value}

    def find_by_Documenty(self, cpf):
        employee_document = ModelEmployee.query.filter_by(cpf=cpf).first()
        return employee_document

    def post(self):
        employee = [request.json['full_name'], request.json['cpf'], request.json['sector_id']]
        cpf_already_exists = Employees.find_by_Documenty(self, request.json['cpf'])
        if cpf_already_exists:
            return {'message': f'The cpf {cpf_already_exists.cpf} already exists in our database'}, 400

        new_employee = ModelEmployee(*employee)
        project_base.session.add(new_employee)
        project_base.session.commit()
        return jsonify(new_employee.serialize_json())


class Employee(Resource):
    @staticmethod
    def find_employee(id):
        return ModelEmployee.query.filter_by(id=id).first()

    def get(self, id):
        employee = Employee.find_employee(id)
        if not employee:
            return {'message': 'Sorry, this employee is not registered in our database.'}, 404

        return employee.serialize_json()

    def delete(self, id):
        employee_already_exists = Employee.find_employee(id)
        if not employee_already_exists:
            return {'message': 'Employee not found'}, 404

        project_base.session.delete(employee_already_exists)
        project_base.session.commit()
        return {'message': 'Excluded employee'}


from flask_restful import Resource
from flask import request, jsonify
from sql_alchemy import project_base
from resources.team import ModelTeam


class ModelEmployee(project_base.Model):
    __tablename__ = 'employess'
    id = project_base.Column(project_base.Integer, primary_key=True)
    full_name = project_base.Column(project_base.String(80))
    cpf = project_base.Column(project_base.Integer)
    sector_id = project_base.Column(project_base.Integer, project_base.ForeignKey('teams.team_id'))
    sector = project_base.relationship(ModelTeam)

    def __init__(self, full_name, cpf, sector_id):
        self.full_name = full_name
        self.cpf = cpf
        self.sector_id = sector_id

    # TODO retornar as chaves do objeto da mesma maneira que está no banco de dados
    def serialize_json(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "CPF": self.cpf,
            "sector": self.sector.formatted_data()
        }


class Employees(Resource):
    @staticmethod
    def get():
        value = [employee.serialize_json() for employee in ModelEmployee.query.all()]
        if not value:
            return {'message': 'Not found'}, 404
        return {'employees': value}


class Employee(Resource):
    @staticmethod
    def find_employee(id):
        return ModelEmployee.query.filter_by(id=id).first()

    #TODO acho que nao precisa mais disso aqui.
    # TODO tirar os first() daqui quando o banco não estiver com os dados duplicados

    def find_by_Documenty(self, cpf):
        var = ModelEmployee.query.filter_by(cpf=cpf).first()
        return var

    def get(self, id):
        an_employee = Employee.find_employee(id)
        if an_employee:
            return an_employee.serialize_json()

        return {'message': 'Desculpa, esse funcionário não se encontra na nossa base de dados'}, 404

    # TODO não precisa passar o register_number, o banco pode ser um autoincrement
    def post(self, id):
        employee_already_exists = Employee.find_employee(id)
        if employee_already_exists:
            return {"message": f"O funcionário '{id}' já existe"}, 400

        # TODO passar o valor do cpf diretamente para a função
        # TODO alterar o nome das variaveis all_value e a_database_cpf
        all_value = [request.json['full_name'], request.json['cpf'], request.json['sector_id']]
        a_database_cpf = Employee.find_by_Documenty(self, all_value[1])
        if a_database_cpf:
            return {'message': f'The cpf {a_database_cpf.cpf} already exists in our database'}, 400

        new_employee = ModelEmployee(id, *all_value)
        project_base.session.add(new_employee)
        project_base.session.commit()
        return jsonify(new_employee.serialize_json())

    def delete(self, id):
        employee_already_exists = Employee.find_employee(id)
        if employee_already_exists:
            project_base.session.delete(employee_already_exists)
            project_base.session.commit()
            return {'message': 'Funcionário deletado'}

        return {'message': 'Funcionário não encontrado'}, 404

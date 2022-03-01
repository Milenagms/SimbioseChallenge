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

    # TODO retornar as chaves do objeto da mesma maneira que está no banco de dados
    # TODO modificar nome para serializeJSON -> acho que faz mais sentido
    def formatted_data(self):
        return {
            "id": self.register_number,
            "full_name": self.full_name,
            "CPF": self.cpf,
            "sector": self.sector.formatted_data()
        }


class Employees(Resource):
    @staticmethod
    def get():
        value = [employee.formatted_data() for employee in ModelEmployee.query.all()]
        if not value:
            return {'message': 'Not found'}, 404
        return {'employees': value}


class Employee(Resource):
    @staticmethod
    def find_employee(register_number):
        return ModelEmployee.query.filter_by(register_number=register_number).first()
    # TODO tirar os first() daqui quando o banco não estiver com os dados duplicados

    def validate_cpf(self, cpf):
        var = ModelEmployee.query.filter_by(cpf=cpf).first()
        return var

    def get(self, register_number):
        an_employee = Employee.find_employee(register_number)
        if an_employee:
            return an_employee.formatted_data()

        return {'message': 'Desculpa, esse funcionário não se encontra na nossa base de dados'}, 404

    # TODO não precisa passar o register_number, o banco pode ser um autoincrement
    def post(self, register_number):
        # TODO modificar a variavel, elas normalmente ficam genẽricas com o que está para ser buscado, ex: employee, employeeAlreadyExists
        an_employee = Employee.find_employee(register_number)
        if an_employee:
            return {"message": f"O funcionário '{register_number}' já existe"}, 400

        # TODO passar o valor do cpf diretamente para a função
        # TODO alterar o nome das variaveis all_value e a_database_cpf
        all_value = [request.json['full_name'], request.json['cpf'], request.json['sector_id']]
        # TODO mudar o nome da funçao para findByCPF
        a_database_cpf = Employee.validate_cpf(self, all_value[1])
        if a_database_cpf:
            return {'message': f'The cpf {a_database_cpf.cpf} already exists in our database'}, 400

        new_employee = ModelEmployee(register_number, *all_value)
        project_base.session.add(new_employee)
        project_base.session.commit()
        return jsonify(request.json)

    def delete(self, register_number):
        # TODO modificar a variavel, elas normalmente ficam genẽricas com o que está para ser buscado, ex: employee, employeeAlreadyExists
        # TODO modificar o nome do metodo para findById
        an_employee = Employee.find_employee(register_number)
        if an_employee:
            project_base.session.delete(an_employee)
            project_base.session.commit()
            return {'message': 'Funcionário deletado'}

        return {'message': 'Funcionário não encontrado'}, 404

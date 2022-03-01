from flask_restful import Resource
from flask import request, jsonify
from sql_alchemy import project_base
from resources.employee import ModelEmployee


class ModelRecommend(project_base.Model):
    __tablename__ = 'recommendations'
    # TODO colocar o nome da chave primaria como id
    recommendation_id = project_base.Column(project_base.Integer, primary_key=True)
    email = project_base.Column(project_base.String(20))
    full_name = project_base.Column(project_base.String(50))
    curriculum = project_base.Column(project_base.String(100))
    phone_number = project_base.Column(project_base.Integer)
    sector = project_base.Column(project_base.String(50))
    employee_id = project_base.Column(project_base.Integer, project_base.ForeignKey('employess.register_number'))
    employee = project_base.relationship(ModelEmployee)

    def __init__(self, email, full_name, curriculum, phone_number, sector, employee_id):
        self.email = email
        self.full_name = full_name
        self.curriculum = curriculum
        self.phone_number = phone_number
        self.sector = sector
        self.employee_id = employee_id

    def formatted_data(self):
        # TODO retornar os dados conforme o que retorna na tabela
        return {
            "id": self.recommendation_id,
            "E-mail": self.email,
            "Full name": self.full_name,
            "Curriculum": self.curriculum,
            "Phone number": self.phone_number,
            "Sector": self.sector,
            "funcionário": self.employee_id
        }


class Recommendations(Resource):
    @staticmethod
    def get():
        return {'Dados de todos os indicados': [recommend.formatted_data() for recommend in ModelRecommend.query.all()]}


class Recommendation(Resource):
    # TODO Fazer tratativa para quando aquele funcionário já estiver no banco de dados
    # TODO verificar se o id do empregado é um id valido
    @staticmethod
    def post():
        all_value = [request.json['email'], request.json['full_name'], request.json['curriculum'],
                     request.json['phone_number'], request.json['sector'], request.json['employee_id']]
        new_recommendation = ModelRecommend(*all_value)
        project_base.session.add(new_recommendation)
        project_base.session.commit()
        return jsonify(new_recommendation)


# class EmployeeRecommendation(ModelRecommend):
#     def gete(self):
#         print(self.employee_id)
#         return {'Dados de todos os indicados': [recommende.formatted_data() for recommende in ModelRecommend.query.all()]}


from flask_restful import Resource
from flask import request, jsonify, send_from_directory
from sql_alchemy import project_base

class ModelRecommend(project_base.Model):
    __tablename__ = 'recommendations'
    recommendation_id = project_base.Column(project_base.Integer, primary_key=True)
    email = project_base.Column(project_base.String(20))
    full_name = project_base.Column(project_base.String(50))
    curriculum = project_base.Column(project_base.String(100))
    phone_number = project_base.Column(project_base.Integer)
    sector = project_base.Column(project_base.String(50))

    def __init__(self, recommendation_id, email, full_name, curriculum, phone_number, sector):
        self.recommendation_id = recommendation_id
        self.email = email
        self.full_name = full_name
        self.curriculum = curriculum
        self.phone_number = phone_number
        self.sector = sector

    def formatted_data(self):
        return {
            "Identificação": self.recommendation_id,
            "E-mail": self.email,
            "Nome completo": self.full_name,
            "Adicione informações do indicado": self.curriculum,
            "Número de telefone": self.phone_number,
            "Para qual área a indicação?": self.sector
        }

class Recommendations(Resource):
    @staticmethod
    def get():
        return {'Dados de todos os indicados': [recommend.formatted_data() for recommend in ModelRecommend.query.all()]}

class Recommendation(Resource):
    def post(self, recommendation_id):
        all_value = [request.json['full_name'], request.json['email'], request.json['curriculum'],
                     request.json['phone_number'], request.json['sector']]
        new_recommendation = ModelRecommend(recommendation_id, *all_value)
        print(new_recommendation)
        project_base.session.add(new_recommendation)
        project_base.session.commit()
        return jsonify(request.json)


from flask_restful import Resource
from flask import request, jsonify
from sql_alchemy import project_base
from resources.employee import ModelEmployee


class ModelRecommend(project_base.Model):
    __tablename__ = 'recommendations'
    id = project_base.Column(project_base.Integer, primary_key=True)
    email = project_base.Column(project_base.String(20))
    full_name = project_base.Column(project_base.String(50))
    curriculum = project_base.Column(project_base.String(100))
    phone_number = project_base.Column(project_base.Integer)
    sector = project_base.Column(project_base.String(50))
    employee_id = project_base.Column(project_base.Integer, project_base.ForeignKey('employess.id'))
    employee = project_base.relationship(ModelEmployee)

    def __init__(self, email, full_name, curriculum, phone_number, sector, employee_id):
        self.email = email
        self.full_name = full_name
        self.curriculum = curriculum
        self.phone_number = phone_number
        self.sector = sector
        self.employee_id = employee_id

    def serialize_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "curriculum": self.curriculum,
            "phone_number": self.phone_number,
            "Sector": self.sector,
            "employee": self.employee.serialize_json()
        }


class Recommendations(Resource):
    def find_employee(self, employee_id):
        if ModelEmployee.query.filter_by(id=employee_id).first():
            return True

    def existing_recomendation(self, email, phone_number):
        if (ModelRecommend.query.filter_by(email=email).first()) or\
                (ModelRecommend.query.filter_by(phone_number=phone_number).first()):
            return True

    @staticmethod
    def get():
        return {'Dados de todos os indicados': [recommend.serialize_json() for recommend in ModelRecommend.query.all()]}

    def post(self):
        recommendation = [request.json['email'], request.json['full_name'], request.json['curriculum'],
                          request.json['phone_number'], request.json['sector'], request.json['employee_id']]

        if not Recommendations.find_employee(self, request.json['employee_id']):
            return {'message': 'invalid employee'}, 404
        if Recommendations.existing_recomendation(self, request.json['email'], request.json['phone_number']):
            return {'message': 'data like email and phone number already exists in the database'}, 404

        new_recommendation = ModelRecommend(*recommendation)
        project_base.session.add(new_recommendation)
        project_base.session.commit()
        return jsonify(new_recommendation.serialize_json())


class RecommendationsEmployees(Resource):
    def get(self):
        employees_made_recommendations = project_base.session.query(ModelRecommend, ModelEmployee)\
            .join(ModelEmployee).all()

        for recommed, employee in employees_made_recommendations:
            recommendations_employee = [recommed.full_name, employee.serialize_json()]
            return recommendations_employee

from flask_restful import Resource
from flask import request, jsonify
from sql_alchemy import project_base

class ModelRecommendation(project_base.Model):
    __tablename__ = 'recommendations'
    recommendation_id = project_base.Column(project_base.Integer, primary_key=True)
    full_name = project_base.Column(project_base.String(80))

    def __init__(self, full_name, recommendation_id):
        self.full_name = full_name
        self.recommendation_id = recommendation_id

    def formatted_data(self):
        return {
            "identificação": self.recommendation_id,
            "Nome completo": self.full_name,
        }

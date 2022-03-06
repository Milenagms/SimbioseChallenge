from flask_restful import Resource
from flask import request, jsonify
from sql_alchemy import project_base


class ModelTeam(project_base.Model):
    __tablename__ = 'teams'
    id = project_base.Column(project_base.Integer, primary_key=True)
    team_name = project_base.Column(project_base.String)

    def __init__(self, team_name):
        self.team_name = team_name

    def serialize_json(self):
        return {
            'id': self.id,
            'team_name': self.team_name
        }


class Teams(Resource):
    @staticmethod
    def get():
        value = [team.serialize_json() for team in ModelTeam.query.all()]
        if not value:
            return {'message': 'Not found in the dataset'}, 404
        return {'All employess': value}

    def post(self):
        team_name = request.json['team_name']

        team_already_exists = list(filter(lambda value_name: value_name.team_name == team_name, ModelTeam.query.all()))
        if team_already_exists:
            return {'message': 'team already registered'}, 404

        new_team = ModelTeam(team_name)
        project_base.session.add(new_team)
        project_base.session.commit()
        return jsonify(new_team.serialize_json())


class Team(Resource):
    def get(self, id):
        existing_team = ModelTeam.query.filter_by(id=id).first()
        if existing_team:
            return existing_team.serialize_json()
        return {'message': 'This team does not exist in our database'}

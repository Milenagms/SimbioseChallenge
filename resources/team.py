from flask_restful import Resource
from flask import request, jsonify
from sql_alchemy import project_base


class ModelTeam(project_base.Model):
    __tablename__ = 'teams'
    team_id = project_base.Column(project_base.Integer, primary_key=True)
    team_name = project_base.Column(project_base.String)

    def __init__(self, team_id, team_name):
        self.team_id = team_id
        self.team_name = team_name

    def formatted_data(self):
        return {
            'Registro do time': self.team_id,
            'Nome da equipe': self.team_name
        }


class Teams(Resource):
    @staticmethod
    def get():
        value = [team.formatted_data() for team in ModelTeam.query.all()]
        if not value:
            return {'message': 'Not found'}, 404
        return {'All employess': value}


class Team(Resource):
    def post(self, team_id):
        team_already_exists = list(filter(lambda value_id: value_id.team_id == team_id, ModelTeam.query.all()))
        if team_already_exists:
            return {'message': 'team já cadastrado'}, 404

        team_name = request.json['team_name']
        # TODO retirar o team_name=team_name
        new_team = ModelTeam(team_id, team_name=team_name)
        project_base.session.add(new_team)
        project_base.session.commit()
        return jsonify(new_team.formatted_data())

    def get(self, team_id):
        # TODO retirar o team_id=team_id
        # TODO mudar o nome da funçao para ser mais explicita findById
        variavel = ModelTeam.query.filter_by(team_id=team_id).first()
        if variavel:
            return variavel.formatted_data()
        return {'message': 'esse team não existe na nossa base de dados'}

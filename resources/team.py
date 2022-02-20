from flask_restful import Resource
from flask import request, jsonify
from sql_alchemy import project_base

class Teams(Resource):
    @staticmethod
    def get():
        return {'Teams da Simbiose cadastrado': [team.json() for team in ModelTeam.query.all()]} # SELECT * FROM teams


class Team(Resource):
    def post(self, team_id):

        new = list(filter(lambda number: number.team_id == team_id, ModelTeam.query.all()))
        print(new)
        if not new:
            print('entrou')
            team_name = request.json['team_name']
            new_team = ModelTeam(team_id, team_name=team_name)
            project_base.session.add(new_team)
            project_base.session.commit()
            return jsonify(request.json)
        else:
            return {'message': 'team já cadastrado'}

    def get(self, team_id):
       pass


class ModelTeam(project_base.Model):
    __tablename__ = 'teams'
    team_id = project_base.Column(project_base.Integer, primary_key=True)
    team_name = project_base.Column(project_base.String)

    def __init__(self, team_id, team_name):
        self.team_id = team_id
        self.team_name = team_name

    def json(self):
        return {
            'Registro do time': self.team_id,
            'Nome da equipe': self.team_name
        }
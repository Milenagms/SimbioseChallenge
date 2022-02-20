from flask_restful import Resource
from flask import request, jsonify
from sql_alchemy import project_base

teams = [
    {'id_team': 1,
     'nome': 'Guaravi',
     'atvidades': 'tests manuais e automatizados',
     'trabalho': 1
     },
    {'id_team': 2,
     'nome': 'FastCrud backend',
     'atvidades': 'Trabalha com manutenção do site',
     'trabalho': 2
     },
    {'id_team': 1,
     'nome': 'FastCrud backend 2',
     'atvidades': 'Trabalha com funcionalidades novas',
     'trabalho': 2
     },
    {'id_team': 1,
     'nome': 'Guaravi back',
     'atvidades': 'tests de tabelas',
     'trabalho': 1
     }
]


class Teams(Resource):
    @staticmethod
    def get():
        return {'Teams': teams}


class Team(Resource):

    def post(self, team_id):
        team_name = request.json['team_name']

        new_team = ModelTeam(team_name=team_name)

        project_base.session.add(new_team)
        project_base.session.commit()

        return jsonify(request.json)

    def get(self, team_id):
        for team in ModelTeam.query.all():
            print(team.team_id, team.team_name)


class ModelTeam(project_base.Model):
    __tablename__ = 'teams'
    team_id = project_base.Column(project_base.Integer, primary_key=True)
    team_name = project_base.Column(project_base.String)


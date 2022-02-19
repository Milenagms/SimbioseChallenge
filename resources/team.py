from flask_restful import Resource
from flask import request, jsonify


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
    def post(self):
        request_data = request.get_json()
        return jsonify(request_data)
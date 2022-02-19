from flask import Flask, jsonify, request

app = Flask(__name__)

team = [
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

@app.route('/teams', methods=['POST'])
def register_teams():
    # Get data from the POST body
    request_data = request.get_json()

    return_dict = {"example": team}

    return jsonify(return_dict)


if __name__ == "__main__":
    app.run(debug=True)

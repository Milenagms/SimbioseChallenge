from flask import Flask
from resources.team import Teams, Team
from resources.employee import Employee, Employees
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

api.add_resource(Teams, '/teams')
api.add_resource(Team, '/team')

api.add_resource(Employees, '/employees')
api.add_resource(Employee, '/employees/<int:register_number>')

if __name__ == "__main__":
    app.run(debug=True)

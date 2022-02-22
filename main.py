from flask import Flask
from resources.team import Teams, Team
from resources.employee import Employee, Employees
from resources.recommendation import Recommendation, Recommendations
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teste.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_project_base():
    project_base.create_all()


api.add_resource(Teams, '/teams')
api.add_resource(Team, '/teams/<int:team_id>')

api.add_resource(Recommendations, '/recommendations')
api.add_resource(Recommendation, '/recommendations/<int:recommendation_id>')

api.add_resource(Employees, '/employees')
api.add_resource(Employee, '/employees/<int:register_number>')

if __name__ == "__main__":
    from sql_alchemy import project_base

    project_base.init_app(app)
    app.run(debug=True)

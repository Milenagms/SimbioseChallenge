from flask import Flask
from resources.team import Teams, Team
from resources.employee import Employee, Employees
from resources.recommendation import Recommendations, RecommendationsEmployees
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simbiose_recommendations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_project_base():
    project_base.create_all()


api.add_resource(Teams, '/teams')
api.add_resource(Team, '/teams/<int:id>')

api.add_resource(Recommendations, '/recommendations')
api.add_resource(RecommendationsEmployees, '/recommendations/employees')

api.add_resource(Employees, '/employees')
api.add_resource(Employee, '/employees/<int:id>')

if __name__ == "__main__":
    from sql_alchemy import project_base

    project_base.init_app(app)
    app.run(debug=True)

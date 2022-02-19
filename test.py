from flask import Flask

ap = Flask(__name__)

@ap.route('/')
def hello() -> str:
    return 'Hello world'
ap.run()
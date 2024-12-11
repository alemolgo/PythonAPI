from flask import Flask
from swagger.blueprint import api_blueprint
from config import configure
# from flask_cors import CORS


app = Flask(__name__)

# CORS(app, resources={"*": {"origins": "http://localhost:9300"}})

def page_not_found(error):
    """Page No fouth method"""
    return "<h1>Not found page...Soquete!!</h1>", 404

if __name__ == '__main__':
    app.config.from_object(configure['development'])

    # Error Hanlders
    app.register_error_handler(404, page_not_found)

    # Register the blueprint in the Flask app
    app.register_blueprint(api_blueprint, url_prefix="/api")

    app.run(port=8000)
    





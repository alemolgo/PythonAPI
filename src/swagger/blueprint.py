# api/__init__.py
from flask import Blueprint
from flask_restx import Api

# Crea el blueprint
api_blueprint = Blueprint("api", __name__)

# Crea la instancia de Api
api = Api(api_blueprint, version="2.0", title="Molina Firts API", description="Documentación Swagger para mi API")

# Importa el módulo de rutas para registrar los endpoints
from routes.Course import ns as items_namespace

# Añade el namespace a la instancia de Api
api.add_namespace(items_namespace, path="/courses")

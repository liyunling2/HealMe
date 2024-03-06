from flask import Blueprint

routes = Blueprint("schedule", __name__)

@routes.route("/")
def home():
    return {
        "code": 200,
        "message": "Hello from schedule service"
    }
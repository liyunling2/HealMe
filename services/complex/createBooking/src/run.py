from flask import Flask
from routes import routes
from db import db
import os

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.register_blueprint(routes)
    
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()

    PORT = os.environ.get("PORT", 5000)
    app.run(host='0.0.0.0', port=PORT, debug=True)

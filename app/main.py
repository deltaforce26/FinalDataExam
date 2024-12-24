from flask import Flask
from app.controllers.stat_blueprint import stat_bp
from app.db.mongo_db import init_db

app = Flask(__name__)

app.register_blueprint(stat_bp)


with app.app_context():
    init_db()


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=5000)
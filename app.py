from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from api import initRoute
from core.setup_app import setup_onstart
from database import mongodb
from database.models import init_collections
from utils.file import UPLOAD_FOLDER
from utils.logger import configure

load_dotenv()
setup_onstart()
configure("FLASK_SERVER", "logs")
mongodb.connect()
init_collections()
mongodb.get_collections()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024
CORS(app)

initRoute(app)

if __name__ == "__main__":
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.run("0.0.0.0", port=8000, debug=False)

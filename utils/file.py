import os
import uuid
from datetime import datetime

from constants import ALLOWED_EXTENSIONS

UPLOAD_FOLDER = "uploads"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def getUniqueFileName(root_folder):
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    folder_name = f"{timestamp}_{unique_id}"

    full_path = os.path.join(root_folder, folder_name)

    return full_path

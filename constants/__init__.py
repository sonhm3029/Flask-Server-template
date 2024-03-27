from .api import API

ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
UPLOAD_FOLDER = "uploads"
MAX_FILE_LENGTH = 300  # 200MB


__all__ = ["API", "ALLOWED_EXTENSIONS", "UPLOAD_FOLDER", "MAX_FILE_LENGTH"]

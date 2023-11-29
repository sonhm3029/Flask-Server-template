from .user_api import user_bp
from flask import send_from_directory

def initRoute(app):
    
    @app.route("/", methods=["GET"])
    def hello():
        return "<div style='width:100%;height:100vh;display:flex;justify-content:center;align-items:center;position:fixed;'>Ivirse AAD Chatbot!</div>"
    
    @app.route("/uploads/<subfolder>/<filename>")
    def download_file(subfolder,filename):
        return send_from_directory(f'uploads/{subfolder}', filename)
    
    app.register_blueprint(user_bp, url_prefix="/user")
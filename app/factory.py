from flask import Flask
import os

from flask_cors import CORS, cross_origin
import logging

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

def create_app(app_name=PKG_NAME, **kwargs):
    """Initialize the core application."""
    # global is_mongo_connected
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    # gunicorn_logger = logging.getLogger('gunicorn.error')
    # app.logger.handlers = gunicorn_logger.handlers
    # app.logger.setLevel(gunicorn_logger.level)
    
    # Later replace this logger with gunicorn
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)  # Set the log level to INFO
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)  # Set the app logger level
    
    # Initialize Plugins
    # from app.model import db
    # try:
    #     db.init_app(app)
    #     app.logger.info("CONNECTED TO MONGODB")
    #     is_mongo_connected = True
    # except Exception as e:
    #     app.logger.error("MONGODB CONNECTION ERROR : " + str(e))
    #     is_mongo_connected = False



    cors = CORS(app)

    with app.app_context():
        # Include our Routes

        # from app.resources.embedding_models import embedding_model
        # from app.resources.vector_indices import table_index
        from app.views import bad_request, forbidden_error, not_found, method_not_allowed, internal_server_error, query_gen_bp

        app.register_blueprint(query_gen_bp)
        
        app.register_error_handler(400, bad_request)
        app.register_error_handler(403, forbidden_error)
        app.register_error_handler(404, not_found)
        app.register_error_handler(405, method_not_allowed)
        app.register_error_handler(500, internal_server_error)
        return app
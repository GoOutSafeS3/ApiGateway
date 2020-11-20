import connexion
import logging

def create_app():
    logging.basicConfig(level=logging.INFO)
    app = connexion.App(__name__)
    app.add_api('swagger.yaml')
    application = app.app
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=80)

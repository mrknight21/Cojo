import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
import firebase_admin
from flask_mail import Mail
from flask import Flask, request, current_app
from config import Config

mail = Mail()


def create_app(config_class=Config):
    firebase_cred = firebase_admin.credentials.Certificate(Config.FIREBASE_CRED_PATH)
    firebase_app = firebase_admin.initialize_app(firebase_cred)
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.news_api import bp as news_api_bp
    app.register_blueprint(news_api_bp, url_prefix='/news_api')

    if not app.debug and not app.testing:
        # if app.config['MAIL_SERVER']:
        #     auth = None
        #     if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        #         auth = (app.config['MAIL_USERNAME'],
        #                 app.config['MAIL_PASSWORD'])
        #     secure = None
        #     if app.config['MAIL_USE_TLS']:
        #         secure = ()
        #     mail_handler = SMTPHandler(
        #         mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        #         fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        #         toaddrs=app.config['ADMINS'], subject='Microblog Failure',
        #         credentials=auth, secure=secure)
        #     mail_handler.setLevel(logging.ERROR)
        #     app.logger.addHandler(mail_handler)

        # if app.config['LOG_TO_STDOUT']:
        #     stream_handler = logging.StreamHandler()
        #     stream_handler.setLevel(logging.INFO)
        #     app.logger.addHandler(stream_handler)
        # else:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/cojo_applog',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('cojo_app startup')

    return app
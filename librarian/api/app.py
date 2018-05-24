import os
from injector import Module, Injector, singleton, inject
from flask import Flask, jsonify
from flask_injector import FlaskInjector
from sqlalchemy.engine import Connection
from sqlalchemy.orm import sessionmaker, Session
from librarian.models import Base, Kitty
from librarian.utils.db import get_db_engine, get_db_session_factory, create_tables
from uuid import uuid4


class AppModule(Module):
    def __init__(self, app, connection=None, session_factory=None):
        self.app = app
        self.connection=connection
        self.session_factory = session_factory

    def configure(self, binder):
        engine = get_db_engine(self.app.config['SQLALCHEMY_URL'])
        connection = self.connection or engine.connect()
        session_factory = get_db_session_factory(connection)
        session = self.session_factory or session_factory()
        Base.metadata.bind = session
        create_tables(engine)
        binder.bind(Connection, to=connection, scope=singleton)
        binder.bind(sessionmaker, to=session_factory, scope=singleton)
        binder.bind(Session, to=session, scope=singleton)

        @self.app.teardown_appcontext
        def close_db_session(error):
            if session:
                try:
                    if error:
                        self.app.logger.info("Session rollback")
                        session.rollback()
                finally:
                    self.app.logger.info("Removing session")
                    session.close()
            self.app.logger.info("Closing db connection...")
            connection.close()
            self.app.logger.info("Closed db connection")


def configure_app(app):
    app.config.update(
        DEBUG=os.environ.get('DEBUG', True),
        TESTING=os.environ.get('TESTING', False),
        SECRET_KEY=os.environ['API_SECRET_KEY'],
        SERVER_NAME=os.environ.get('SERVER_NAME', 'localhost'),
        SQLALCHEMY_URL=os.environ['SQLALCHEMY_URL']
    )


def configure_views(app):
    @app.route('/list', methods=['GET'])
    def list(session: Session):

        res = []
        kitties = session.query(Kitty).all()
        for k in kitties:
            res.append({'id': k.id, 'name': k.name})
        return jsonify(res)

    @app.route('/make', methods=['POST'])
    def make(session: Session):
        kitty = Kitty(name=uuid4())
        session.add(kitty)
        session.commit()
        return jsonify({'id': kitty.id, 'name': kitty.name})


def create_app(connection=None, session_factory=None):
    app = Flask(__name__)
    configure_app(app)
    configure_views(app=app)
    injector = Injector([AppModule(app, connection=connection, session_factory=session_factory)])
    FlaskInjector(app=app, injector=injector)
    return app

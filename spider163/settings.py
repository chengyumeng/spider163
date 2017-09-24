# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from spider163.utils import config


def configure_orm():
    global engine
    global Session
    engine_args = {}
    engine = create_engine(config.get_db(), **engine_args)
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine))


configure_orm()

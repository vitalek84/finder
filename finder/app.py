import logging
import sys
import falcon
from .db import DB
from .hnsw import Finder
from .resources import Ident
from .resources import Look2Camera
from .resources import MaskOnHead
from .resources import TestDataGeneration

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
#Enter you database connect here
CON_STR ='postgresql://login:password@localhost/database'

def create_app():
    db_handler = DB(CON_STR)
    finder = Finder(db_handler.persons_numpy)
    ident = Ident(db_handler, finder)
    look = Look2Camera(db_handler)
    mask = MaskOnHead(db_handler)
    testdata =  TestDataGeneration(db_handler)
    api = falcon.API()
    api.add_route('/ident', ident)
    api.add_route('/mask', mask)
    api.add_route('/look2camer', look)
    api.add_route('/datagen', testdata)
    #api.add_route('/reindex', ident)
    return api


def get_app():
    return create_app()


application = get_app()

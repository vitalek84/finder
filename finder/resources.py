import json
import numpy
import falcon
import logging
import pprint
from .hnsw import Finder
import requests

WEB = 'http://localhost:8080/dosomething'
PAYLOAD = {'shop_id': '2'}

class TestDataGeneration(object):
    def __init__(self, db = None, finder = None ):
        if db == None :
            raise ValueError("Need database connect")
        self.db = db

    def on_post(self, req, resp):
        query = req.media
        shop_id = query['data']['shop']
        p_id = self.db.insert_person(shop_id, query['data'])
        doc = {"message": "Create new user with id {}".format(p_id)}
        logging.warning("Create new user with id {}".format(p_id))
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200

class Ident(object):

    def __init__(self, db = None, finder = None ):
        if db == None or finder == None:
            raise ValueError("Need database connect and hnsw object instance")
        self.finder = finder
        self.db = db



    def on_post(self, req, resp):
        #TODO VALIDATE QUERY
        query = req.media
        #pprint.pprint(query['data']['face'])
        #ident = [];
        #ident.append()
        shop_id = query['data']['shop']
        candidate = self.finder.find(query['data']['ident'], self.db.persons_id)
        #For log
        cand_idx = None
        cand_id = None
        if candidate != None:
            cand_idx = candidate
            cand_id = self.db.persons_id[candidate]
        else:
            cand_idx = 'None'
            cand_id = 'None'
        print(candidate)
        logging.warning("find person with index: {} id: {}".format(cand_idx, cand_id))
        doc = None
        state = self.db.current_state(shop_id)
        #logging.warning("current state is: ")
        if  state != 'found' and state != 'manual':

            if candidate:
                self.db.state_find(shop_id, self.db.persons_id[candidate], query['data']['face'])
                doc = {"message": "find person with index: {} and id: {}".format(candidate, self.db.persons_id[candidate])}
                requests.get(WEB, params=PAYLOAD)
                resp.status = falcon.HTTP_200

            else:
                p_id = self.db.insert_person(shop_id, query['data'])
                self.db.state_find(shop_id, p_id, query['data']['face'])
                requests.get(WEB, params=PAYLOAD)
                self.db.load_persons()
                self.finder = Finder(self.db.persons_numpy)
                doc = {"message": "User not find create new user with id {}".format(p_id)}
                logging.warning("User not find create new user with id {}".format(p_id))
                resp.body = json.dumps(doc, ensure_ascii=False)
                resp.status = falcon.HTTP_404

        else:
            logging.warning("State Found. Do nothing")
            doc = {"message": "State Found. Do nothing"}
            resp.body = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_423

class Look2Camera(object):

    def __init__(self, db = None ):
        if db == None:
            raise ValueError("Need database connect")
        self.db = db

    def on_post (self, req, resp):
        query = req.media
        shop_id = query['data']['shop']
        state =self.db.current_state(shop_id)
        if state != 'found' and state != 'manual':
            self.db.state_wrong_pos(shop_id, query['data']['face'])
            doc = {"message": "Wrong head position"}
            logging.warning("Wrong head position")
            resp.body = json.dumps(doc, ensure_ascii=False)
            requests.get(WEB, params=PAYLOAD)
            resp.status = falcon.HTTP_200
        else:
            logging.warning("IN wrong head position")
            logging.warning("State found. Do nothing")
            doc = {"message": "State found. Do nothing"}
            resp.body = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_423

class MaskOnHead(object):

    def __init__(self, db = None ):
        if db == None:
            raise ValueError("Need database connect")
        self.db = db

    def on_post (self, req, resp):
        query = req.media
        shop_id = query['data']['shop']
        state =self.db.current_state(shop_id)
        if state != 'found' and state != 'manual':
            self.db.state_mask(shop_id, query['data']['face'])
            doc = {"message": "Mask on head"}
            logging.warning("Mask on head")
            resp.body = json.dumps(doc, ensure_ascii=False)
            requests.get(WEB, params=PAYLOAD)
            resp.status = falcon.HTTP_200
        else:
            logging.warning("IN mask on head")
            logging.warning("State found. Do nothing")
            doc = {"message": "State found. Do nothing"}
            resp.body = json.dumps(doc, ensure_ascii=False)
            resp.status = falcon.HTTP_423

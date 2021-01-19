import numpy
import logging
from random import randint
from sqlalchemy import create_engine


IDENT_LEN =256

class DB:

    def __init__(self, con_str):
        self.con_str = con_str
        self.engine = create_engine(con_str)
        self.load_persons()

    def current_state(self, shop_id):
        result = self.engine.execute("SELECT state FROM loyalty_states where shop_id = {}".format( shop_id)).fetchone()
        key, value = (result.items())[0]
        return value
#TODO Load all DB need load for one company only!
    def load_persons(self):

        result_set = self.engine.execute("SELECT id, ident FROM loyalty_person where ident is not NULL")
        i = 0
        persons_idx =[]
        persons_id = []

        for r in result_set:
            if len(r.ident) != IDENT_LEN:
                raise ValueError("Length of ident vectory not eq {} for id {}. Please fix it".format(IDENT_LEN, r.id))
            persons_idx.append(r.ident)
            persons_id.append(r.id)

        self.persons_id = persons_id
        self.persons_numpy =numpy.array(persons_idx)




    def select_person(self, person):
        pass

    def insert_person(self, shop_id, person):
        arr_str = "'{"
        for el in person['ident']:
            arr_str += str(el) + ','
        arr_str = arr_str[:-1]
        arr_str += "}'"
        name = 'Name' + str(randint(1, 10000000))
        self.engine.execute("INSERT INTO loyalty_person (firstname, ident, age, gender, last_shop_id, phone, photo ) values ('{}', {}, {}, '{}', {}, 0, '{}')"\
        .format(name, arr_str, person['age'], person['gender'], shop_id, person['face']))
        result = self.engine.execute("select id from loyalty_person where firstname = '{}' and photo = '{}'".format(name, person['face'])).fetchone()
        key, value = (result.items())[0]
        return value

    def update_person(self, person):
        pass


    def state_wrong_pos(self, shop_id, photo = ''):

        self.engine.execute("UPDATE loyalty_states set state='wrong_head_position', buyer_id = NULL, photo ='{}' where shop_id = {}".format(photo, shop_id))

    def state_mask(self, shop_id, photo=''):

        self.engine.execute("UPDATE loyalty_states set state='mask_on_head', buyer_id = NULL, photo='{}'  where shop_id = {}".format(photo, shop_id))

    def state_find(self, shop_id, person_id, photo=''):

        self.engine.execute("UPDATE loyalty_states set state='found', buyer_id = {}, photo ='{}'  where shop_id = {}".format(person_id, photo, shop_id))


    def state_ready(self, shop_id):

        self.engine.execute("UPDATE loyalty_states set state='ready', buyer_id = NULL, photo = NULL  where shop_id = {}".format(shop_id))

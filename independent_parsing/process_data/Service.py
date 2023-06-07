#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import process_data.Model as Model
from process_data.Repository import Repository
from project_setup.logger_setup import logger

class Service:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.users_repo = Repository()#(cls.context_db)
            cls.instance = super(Service, cls).__new__(cls)
        return cls.instance
            
    def add_userstats(cls, obj_data):
        model_userstats = Model.UserStats(obj_data)
        model_userstats.parsedate = datetime.utcnow() # utc
        modeluser = Model.Users(obj_data)
        
        if modeluser:
            print(modeluser)
            res = cls.users_repo.create_user(modeluser) # create user if it doesnt exist
            if res == 1:
                print('NEW USER CREATED.')
            elif res == 0:
                print('USER EXISTS.')
            else:
                logger.error('Problem with creating user.')
                return 'Problem with creating user.'
               #w_repo.select_data()
        if model_userstats:
            res = cls.users_repo.create_userstats(model_userstats)  # create corresponding data
            if res == 1:
                return 'Statistics added.'
            elif res == 0:
                return 'Statistics was already parsed within last 12 hours.'
            else:
                logger.error('Problem with creating user statistics.')
                return 'Problem with creating user statistics.'

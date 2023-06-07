#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker  # v 2.0
import process_data.Model as Model
from project_setup.context_setup import AlchemyContext
from project_setup.logger_setup import logger

class Repository:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.__repo = AlchemyContext()
            Session = sessionmaker(bind = cls.__repo.Engine)
            cls.__repo.session = Session()
            cls.instance = super(Repository, cls).__new__(cls)
        return cls.instance

    def create_user(cls, obj):        
        if obj is None:    # and other checkings
            logger.error('create_user: object is none')
            return
        try:            
            dupl = cls.__repo.session.query(cls.__repo.table_Users).filter(Model.Users.userId == obj.userId).first()
            if dupl is None:
                cls.__repo.session.add(obj)
                cls.__repo.session.commit()
                logger.info(f'Added user {obj.userId} with name: {obj.userName}')
            else:
                logger.warning(f'User {obj.userId} exists.')
                return 0
        except Exception as e:
            cls.__repo.session.rollback()
            logger.error(f'create_user: {e}')
            return
        return 1

    def create_userstats(cls, obj):        
        if obj is None:    # and other checkings
            return
        try:
            corr_user = cls.__repo.session.query(cls.__repo.table_Users).filter(Model.Users.userId == obj.userId).first()
            if corr_user is not None:
                # check the last time of user stats parse. It should be more than 12 hours
                last_userstats = cls.__repo.session.query(cls.__repo.table_UserStats).filter(Model.UserStats.userId == corr_user.id).filter(Model.UserStats.parsedate > (datetime.utcnow() - timedelta(hours=12))).first()
                if last_userstats:
                    logger.info(f'Last time of user {corr_user.userId} stats parse: {last_userstats.parsedate}, id: {last_userstats.statsid}') 
                    return 0
                else:
                    obj.userId = corr_user.id
                    cls.__repo.session.add(obj)
                    cls.__repo.session.commit()
                    logger.info(f'Added stats {obj.userId}')
                    
                    statsid = obj.statsid            
                    if obj.competitionsSummary:
                        obj.competitionsSummary.userstatsid = statsid
                        cls.__repo.session.add(obj.competitionsSummary)
                        cls.__repo.session.commit()
                    if obj.scriptsSummary:
                        obj.scriptsSummary.userstatsid = statsid
                        cls.__repo.session.add(obj.scriptsSummary)
                        cls.__repo.session.commit()
                    if obj.datasetsSummary:
                        obj.datasetsSummary.userstatsid = statsid
                        cls.__repo.session.add(obj.datasetsSummary)
                        cls.__repo.session.commit()
                    if obj.discussionsSummary:
                        obj.discussionsSummary.userstatsid = statsid
                        cls.__repo.session.add(obj.discussionsSummary)
                        cls.__repo.session.commit()
                    return 1
        except Exception as e:
            cls.__repo.session.rollback()
            logger.error(f'create_userstats: {e}')
            return 
        finally:
            cls.__repo.session.close()
            cls.__repo.Engine.dispose()            
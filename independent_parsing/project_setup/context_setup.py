#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sqlalchemy.orm import registry
from process_data.Model import UserStats, Stats, Users

class AlchemyContext:
    __provider = 'sqlite:///userstats.db'  # database connection
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AlchemyContext, cls).__new__(cls)
            AlchemyContext.Engine = sa.create_engine(AlchemyContext.__provider)
            metadata = sa.MetaData()
             
            AlchemyContext.table_Users = sa.Table('Users', metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('userId', sa.Integer, nullable=False),  ## alt key
            sa.Column('userName', sa.String(100), nullable=False), 
            sa.Column('userJoinDate', sa.DateTime, nullable=False))
            
            AlchemyContext.table_UserStats = sa.Table('UserStats', metadata,
            sa.Column('statsid', sa.Integer, primary_key=True),
            sa.Column('userId', sa.Integer, sa.ForeignKey('Users.id'), nullable=False),  ## fk
            sa.Column('displayName', sa.String(100), nullable=False), 
            sa.Column('country', sa.String(100)), 
            sa.Column('city', sa.String(100)), 
            sa.Column('region', sa.String(100)), 
            sa.Column('bio', sa.String(1000)),
            sa.Column('userLastActive', sa.DateTime, nullable=False),
            sa.Column('performanceTier', sa.String(50)), 
            sa.Column('followers', sa.Integer, nullable=False), 
            sa.Column('following', sa.Integer, nullable=False),
            sa.Column('parsedate', sa.DateTime, nullable=False))
            
            AlchemyContext.table_Stats = sa.Table('Stats', metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('userstatsid', sa.Integer, sa.ForeignKey('UserStats.statsid'), nullable=False),  ## foreign key
            sa.Column('statstype', sa.String(40), nullable=False), # 'competitionsSummary', 'scriptsSummary', 'datasetsSummary'
            sa.Column('tier', sa.String(50)), 
            sa.Column('totalResults', sa.Integer), 
            sa.Column('rankPercentage', sa.Float, nullable=False), 
            sa.Column('rankOutOf', sa.Integer, nullable=False), 
            sa.Column('rankCurrent', sa.Integer), 
            sa.Column('rankHighest', sa.Integer), 
            sa.Column('totalGoldMedals', sa.Integer), 
            sa.Column('totalSilverMedals', sa.Integer), 
            sa.Column('totalBronzeMedals', sa.Integer))
        
        metadata.create_all(AlchemyContext.Engine)
        mapper_reg = registry() # 2.0
        
        mapper_reg.map_imperatively(Users, AlchemyContext.table_Users)
        mapper_reg.map_imperatively(UserStats, AlchemyContext.table_UserStats)
        mapper_reg.map_imperatively(Stats, AlchemyContext.table_Stats)
        
        return cls.instance
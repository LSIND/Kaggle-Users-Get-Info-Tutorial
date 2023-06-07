#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

class UserStats:
    def __init__(self, kwargs):
        valid_keys = ('userId', 'displayName','country', 'city', 'region', 'bio', 'userLastActive', 'performanceTier', 'competitionsSummary', 'scriptsSummary', 'datasetsSummary', 'discussionsSummary', 'followers', 'following', 'parsedate')
        for key in valid_keys:
            val = kwargs.get(key)
            
            if key == 'userLastActive':
                try:
                    dt = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S.%fZ') # Z represents the GMT/UTC
                except:
                    dt = None
                finally:
                   setattr(self, key, dt)
            
            elif key in ('competitionsSummary', 'scriptsSummary', 'datasetsSummary', 'discussionsSummary'): # 1 - oo
                st = Stats(val, key)
                setattr(self, key, st)
            elif key in ('followers', 'following'):  # key count
                if 'count' in kwargs[key]:
                    #print(key, kwargs.get(key).get('count'))
                    try:
                        num = int(val.get('count'))
                    except:
                        num = 0
                    finally:
                        setattr(self, key, num)
                else:
                    setattr(self, key, 0)
            else:
                setattr(self, key, kwargs.get(key))

class Stats:
    def __init__(self, kwargs, statstype):
        valid_keys = ('tier', 'totalResults', 'rankPercentage', 'rankOutOf', 'rankCurrent', 'rankHighest', 'totalGoldMedals', 'totalSilverMedals', 'totalBronzeMedals')
        self.statstype = statstype
        for key in valid_keys:
            val = kwargs.get(key)  # integer fields
            if key in ('totalResults', 'rankOutOf', 'rankCurrent', 'rankHighest', 'totalGoldMedals', 'totalSilverMedals', 'totalBronzeMedals'):
                try:
                    val = int(val)
                except:
                    val = None
                finally:
                    setattr(self, key, val)
            elif key == 'rankPercentage': # float fields
                try:
                    val = float(val)
                except:
                    val = None
                finally:
                    setattr(self, key, val)
            else:
                setattr(self, key, val)
            
class Users:
    def __init__(self, kwargs):
        valid_keys = ('userId', 'userName', 'userJoinDate')
        for key in valid_keys:
            val = kwargs.get(key)
            if key == 'userJoinDate':
                try:
                    dt = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S.%fZ') # Z represents the GMT/UTC
                except:
                    dt = None
                finally:
                   setattr(self, key, dt)
            else:
                setattr(self, key, val)
                
    def __str__(self):
        return f'--> ID {self.userId}, {self.userName}. Joined at {self.userJoinDate}'
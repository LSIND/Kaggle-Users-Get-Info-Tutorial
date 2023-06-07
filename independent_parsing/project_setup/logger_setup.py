#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('logger')
log_format = '%(asctime)s -%(levelname)s \t %(filename)s(%(lineno)d) \t -%(message)s'
logname = os.path.join(os.path.dirname(__file__), 'logs', 'log.log')

handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)

# add a suffix which you want
handler.suffix = "%Y%m%d"

# finally add handler to logger    
logger.addHandler(handler)
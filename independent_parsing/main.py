#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import requests
from bs4 import BeautifulSoup
from process_data.Service import Service
from project_setup.logger_setup import logger

def parse_data(link):
    if link:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
        content = requests.get(link, headers = headers)
        if content.status_code == 200:
            logger.info(f'Start reading {link}')
            try:
                content = content.text
                soup = BeautifulSoup(content, 'html.parser')                
                info = soup.find('script', {'class': 'kaggle-component'})
                info = info.text
                s = re.search(r'"userId"(.*?)}\);', info).group(0)[0:-2]
                s = '{'+s
                ser_data = json.loads(s)
                #print(ser_data)
            except Exception as e:
                print('Error parsing data')
                logger.error(f'Cannot parse data for {link}; {e}')
                return None
            else:
                return ser_data # dictionary
        else:
            print(content.status_code)
            logger.error(f'Page {link} returns {content.status_code}')
            return None
    else:
        logger.error('Invalid link')
        return None

if __name__ == '__main__':
    #usernames = ('lsind18', 'binaicrai', 'vikasukani')

    filename = os.path.join(os.path.dirname(__file__),'usernames.txt')
    if os.path.exists(filename):
        controller = Service()
        with open(filename, encoding = 'utf-8') as infile:
            for username in infile:
                if username is None or username.isspace():
                    continue
                username = username.strip()
                link = f'https://www.kaggle.com/{username}'
                print(link)

                dict_data = parse_data(link)
                if dict_data:
                    res = controller.add_userstats(dict_data)
                    print(res)
                else:
                    logger.error(f'Cannot parse data for {username}')
                print(20*'-', end='\n')
    else:
        logger.error(f'File with usernames not found.')
        print('File doesnt exist.')
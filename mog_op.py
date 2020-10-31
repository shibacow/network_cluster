#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pymongo
import re,os
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import logging
logging.basicConfig(level=logging.INFO)
from dotenv import load_dotenv
envpath=os.path.expanduser("~/.ssh/.env")
load_dotenv(envpath)
MONGO_HOST=os.environ.get("MONGO_HOST")
MONGO_USER=os.environ.get("MONGO_USER")
PASSWORD=os.environ.get("PASSWORD")
AUTHSOURCE=os.environ.get("AUTHSOURCE")

class MongoOp(object):
    def __init__(self,host,db='twitter'):
        self.con = pymongo.MongoClient(MONGO_HOST,
                                       27017,
                                       username=MONGO_USER,
                                       password=PASSWORD,
                                       authSource=AUTHSOURCE,
                                       authMechanism='SCRAM-SHA-1')
        
        self.db=self.con[db]
    def __del__(self):
        if self.con:
            self.con.close()
            self.con=None
    def close(self):
        if self.con:
            self.con.close()
            self.con=None
    def get_col(self,col):
        return self.db[col]
def test():
    mp=MongoOp('localhost')
    print(mp)
if __name__=='__main__':test()


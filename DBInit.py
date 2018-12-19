# -*- coding:utf-8 -*-
import sys
sys.dont_write_bytecode = True
from ddl.make_db_tables import executeDBInit
import logging

logging.basicConfig(level=logging.DEBUG)

executeDBInit(rebuild_tables=True)
#executeDBInit()

#[EOF]
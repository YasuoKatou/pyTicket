# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import psycopg2
import json
from logging import getLogger, DEBUG

from dao.ticket_dao_manager import TicketDaoManager
from config.db_config import DBConfig

_Log = getLogger(__name__)

def _dropTable(cur, ddl):
    try:
        cur.execute(ddl)
    except Exception as ex:
        _Log.debug(ex)

def _createTable(cur, ddl):
    try:
        cur.execute(ddl)
    except Exception as ex:
        raise ex

def _createTables():
    _DDL_XML_PATH = 'ddl/DBInitDao.xml'

    ddl_insert = {}
    ddl_delete = {}

    tree = ET.parse(_DDL_XML_PATH)
    root = tree.getroot()
    for child in root:
        if 'insert' == child.tag:
            ddl_insert[child.attrib['id']] = child.text.strip()
        elif 'delete' == child.tag:
            ddl_delete[child.attrib['id']] = child.text.strip()

    #DBに接続
    with psycopg2.connect(DBConfig.getConnectUrl()) as conn:
        #トランザクション制御を行わない
        conn.autocommit = True
        #DDLを実行するカーソルを開く
        with conn.cursor() as cur:
            _Log.info('--- start delete')
            for id, ddl in ddl_delete.items():
                _Log.info(id)
                _dropTable(cur, ddl)
            _Log.info('--- start create')
            for id, ddl in ddl_insert.items():
                _Log.info(id)
                _createTable(cur, ddl)

def _setInitData():
    _JSON_PATH = 'ddl/ap_init_data.json'
    with open(_JSON_PATH, 'r', encoding='utf-8') as jf:
        init_data = json.load(jf)
    dao_manager = TicketDaoManager.get_instance()
    #DBに接続
    with psycopg2.connect(DBConfig.getConnectUrl()) as conn:
        #DDLを実行するカーソルを開く
        with conn.cursor() as cur:
            for tbl in init_data['initDataList']:
                _Log.info('--- table : ' + tbl['title'])
                dao = dao_manager.get_dao(tbl['dao'])
                if dao:
                    for rec in tbl['values']:
                        if tbl['method'] == 'insert':
                            dao.insert(cur, rec)
                        elif tbl['method'] == 'appendItem':
                            dao.appendItem(cur, rec)
                        else:
                            raise Exception('no such method (' + tbl['method'] + ')')
                else:
                    _Log.debug('no DAO : ' + tbl['dao'])
        #コミット
        conn.commit()

def executeDBInit(rebuild_tables=False):
    #テーブルを作成する
    if rebuild_tables:
        _createTables()
    #初期データの登録を行う
    _setInitData()
#[EOF]
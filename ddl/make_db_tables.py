# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
#import psycopg2
import json
import re
from logging import getLogger, DEBUG

import util.DBAccess as DBA
from dao.ticket_dao_manager import TicketDaoManager
#from config.db_config import DBConfig

_Log = getLogger(__name__)

# drop table {テーブル名} からテーブル名を抽出する正規表現
_re_01 = re.compile(r'\s*drop\s+table\s+(?P<name>\S+)', re.IGNORECASE)
_find_table = 'select case count(1) when 1 then TRUE else FALSE end ' \
              'from pg_stat_user_tables where lower(relname) = lower(%s)'

def _hasTable(cur, ddl):
    # todo DDL('drop table m_user')からテーブル名を取り出す
    m = _re_01.search(ddl)
    tblName = m.group('name')
    cur.execute(_find_table, (tblName,))
    (found,) = cur.fetchone()
    if not found:
        _Log.debug("'" + tblName + "' not found" )

    return True if found else False

def _dropTable(cur, ddl):
    if not _hasTable(cur, ddl):
        return
    try:
        cur.execute(ddl)
    except Exception as ex:
        _Log.debug(ex)

def _createTable(cur, ddl):
    try:
        cur.execute(ddl)
    except Exception as ex:
        raise ex

@DBA.Transactional
def _createTables(**kwargs):
    _Log.debug('start create Tables')
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
    #with psycopg2.connect(DBConfig.getConnectUrl()) as conn:
        #トランザクション制御を行わない
        #conn.autocommit = True
        #DDLを実行するカーソルを開く
        #with conn.cursor() as cur:
    cur = kwargs['cursor']
    _Log.info('--- start delete')
    for id, ddl in ddl_delete.items():
        _Log.info(id)
        _dropTable(cur, ddl)
    _Log.info('--- start create')
    for id, ddl in ddl_insert.items():
        _Log.info(id)
        _createTable(cur, ddl)

@DBA.Transactional
def _setInitData(**kwargs):
    _Log.debug('start Data Init')
    _JSON_PATH = 'ddl/ap_init_data.json'
    with open(_JSON_PATH, 'r', encoding='utf-8') as jf:
        init_data = json.load(jf)
    dao_manager = TicketDaoManager.get_instance()
    #DBに接続
    #with psycopg2.connect(DBConfig.getConnectUrl()) as conn:
        #DDLを実行するカーソルを開く
        #with conn.cursor() as cur:
    cur = kwargs['cursor']
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
        #conn.commit()

def executeDBInit(rebuild_tables=False):
    #テーブルを作成する
    if rebuild_tables:
        _createTables()
    #初期データの登録を行う
    _setInitData()
#[EOF]
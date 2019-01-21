# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
from logging import getLogger
from inspect import stack
import re

from util.syntactic_ana import TestTagExp
from util.pg_sql_editor import SqlEditor as SQL_EDITOR

_Log = getLogger(__name__)

#Dao呼び出しパターン(xxDao.insert(param))
FN_RE = re.compile(r'.+\.(?P<name>\w+).+')

def addFuncName(func):
    def wrapper(self, *args):
        #呼び出し元のソースから呼び出す関数名を取り出す
        stk = stack()
        fn = stk[1].code_context
        m = re.match(FN_RE, fn[0])
        r = list(m.groups('mame'))[0]
 
        #呼び出し関数名を引数に追加して呼び出す
        return func(self, r, *args)
    return wrapper

class DaoBase:
    def __init__(self, xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        self._namespace = root.attrib['namespace']
        self._dml_select = {}
        self._dml_insert = {}
        self._dml_update = {}
        self._dml_delete = {}
        for child in root:
            tag = child.tag.lower()
            if 'resultmap' == tag:
                _Log.debug('[{}] tag not use ...'.format(child.tag))
            elif 'select' == tag:
                self._dml_select[child.attrib['id']] = child
            elif 'insert' == tag:
                self._dml_insert[child.attrib['id']] = child
            elif 'update' == tag:
                self._dml_update[child.attrib['id']] = child
            elif 'delete' == tag:
                self._dml_delete[child.attrib['id']] = child
            else:
                _Log.error('[{}] tag is not supported'.format(tag))

    @property
    def dao_name(self):
        wk = self._namespace.split('.')
        return wk[len(wk) - 1].lower()

    def _edit_if_tag(self, source, values):
        '''
        クエリー内の「if」タグを編集する
        '''
        query = source.text.split('\n')
        for elm in list(source):
            if 'if' == elm.tag:
                condStr = elm.attrib['test']
                if TestTagExp.doTest(condStr, values):
                    query.append(elm.text)
            query.extend(elm.tail.split('\n'))
        return  '\n'.join(query)

    def _make_column_list(self, desc):
        '''
        カラム名一覧を作成
        '''
        return [col.name for col in desc]

    def _make_dict_rec(self, name_list, rec):
        '''
        辞書型のレコードを作成
        @param name_list カラム名一覧
        @param rec レコードの配列
        '''
        r = {}
        for i in range(0, len(name_list)):
            r[name_list[i]] = rec[i]
        return r

    def _execSql(self, cur, source, values, isSelect):
        #_Log.debug(ET.tostring(source))
        #_Log.debug(values)
        query = self._edit_if_tag(source, values)
        #_Log.debug('sql :', query)
        q, v = SQL_EDITOR.edit_valiables(query, values)
        #_Log.debug('dml : ' + q)
        #_Log.debug('value : ' + str(v))
        #_Log.debug('cursor closed : ' + str(cur.closed))
        cur.execute(q, v)
        #_Log.debug('dml : ' + str(cur.query))
        #_Log.debug('status message : ' + cur.statusmessage)
        #_Log.debug('cursor name : ' + str(cur.name))
        if not isSelect:
            return None
        #_Log.debug('description : ' + str(len(cur.description)))
        recs = cur.fetchall()
        #_Log.debug('rownumber : ' + str(cur.rownumber))
        #_Log.debug('rows : ' + str(recs))
        if cur.rownumber == 0:
            return None
        else:
            nml = self._make_column_list(cur.description)
            if cur.rownumber == 1:
                return self._make_dict_rec(nml, recs[0])
            else:
                dict_recs = []
                for i in range(0, len(recs)):
                    dict_recs.append(self._make_dict_rec(nml, recs[i]))
                return dict_recs

    @addFuncName
    def _execute(self, name, cur, argv):
        if name in self._dml_select:
            return self._execSql(cur, self._dml_select[name], argv, True)
        elif name in self._dml_insert:
            return self._execSql(cur, self._dml_insert[name], argv, False)
        elif name in self._dml_update:
            return self._execSql(cur, self._dml_update[name], argv, False)
        elif name in self._dml_delete:
            return self._execSql(cur, self._dml_delete[name], argv, False)
        else:
            raise NotImplementedError('no such method (' + name + ')')

    def __getattr__(self, name):
        #print('call', name)
        return self._execute

def get_dao(xml_path):
    return DaoBase(xml_path)

#[EOF]
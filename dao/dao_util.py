# -*- coding:utf-8 -*-
import re
import xml.etree.ElementTree as ET
from logging import getLogger, DEBUG

from util.syntactic_ana import TestTagExp
from util.pg_sql_editor import SqlEditor as SQL_EDITOR

_Log = getLogger(__name__)

class DaoBase:
    def __init__(self, xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        self._namespace = root.attrib['namespace']
        self._dml = {}
        for child in root:
            tag = child.tag.lower()
            if 'resultmap' == tag:
                _Log.debug('[{}] tag not use ...'.format(child.tag))
            elif 'select' == tag:
                self._dml[child.attrib['id']] = child
            elif 'insert' == tag:
                self._dml[child.attrib['id']] = child
            elif 'update' == tag:
                self._dml[child.attrib['id']] = child
            elif 'delete' == tag:
                self._dml[child.attrib['id']] = child
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

    def _execSql(self, cur, source, values):
        #_Log.debug(ET.tostring(source))
        #_Log.debug(values)
        query = self._edit_if_tag(source, values)
        #_Log.debug(query)
        q, v = SQL_EDITOR.edit_valiables(query, values)
        #_Log.debug('query : ' + q)
        #_Log.debug('value : ' + str(v))
        cur.execute(q, v)
    def execute(self, cur, name, argv):
        if name in self._dml:
            self._execSql(cur, self._dml[name], argv)
        else:
            NotImplementedError('no such method (' + name + ')')

def get_dao(xml_path):
    return DaoBase(xml_path)

#[EOF]
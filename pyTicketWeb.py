# -*- coding:utf-8 -*-
import sys
sys.dont_write_bytecode = True

import json
import logging
from bottle import post, request, response, run, HTTPResponse, hook, route

from dao.ticket_dao_manager import TicketDaoManager

#Log level
logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=logging.INFO)

#サービスクラスのルートパス
_SERVICE_ROOT = 'service'

#コントローラの一覧
_controller_map = {}
_CONTROLLER_ROOT = 'controller'

def make_service_map():
    '''
    サービスの一覧を作成する.
    '''
    from pathlib import Path
    import importlib

    dao_manager = TicketDaoManager.get_instance()

    svc_map = {}
    p = Path(__file__).parent / _SERVICE_ROOT
    for f in p.glob('*.py'):
        cn = Path(f).stem
        if cn == 'BaseService':
            continue
        im = '{0}.{1}'.format(_SERVICE_ROOT, cn)
        m = importlib.import_module(im)
        inst = getattr(m, cn)()
        print(inst.service_name, '->', im)
        svc_map[inst.service_name] = inst
        inst.dao_manager = dao_manager
    return svc_map

def make_controller_map(servicMap):
    '''
    コントローラの一覧を作成する.
    '''
    from pathlib import Path
    import importlib
    global _controller_map

    p = Path(__file__).parent / _CONTROLLER_ROOT
    for f in p.glob('*.py'):
        cn = Path(f).stem
        if cn == 'BaseController':
            continue
        im = '{0}.{1}'.format(_CONTROLLER_ROOT, cn)
        m = importlib.import_module(im)
        inst = getattr(m, cn)()
        print(inst.controller_name, '->', im)
        _controller_map[inst.controller_name] = inst
        inst.set_service_map(servicMap)

def get_controller(path):
    '''
    POST時のパスからコントローラを取得する.
    '''
    global _controller_map
    for name, inst in _controller_map.items():
        method = inst.hasMapping(path)
        if method:
            return inst, method
    return None, None

def edit_response(body):
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

@hook('after_request')
def enable_cors():
	if not 'Origin' in request.headers.keys():
		return
	response.headers['Access-Control-Allow-Origin']  = request.headers['Origin']
	#response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
	response.headers['Access-Control-Allow-Methods'] = 'POST'
	response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Authorization'

@route('<any:path>', method='OPTIONS')
def response_for_options(**kwargs):
	return {}

@post('/login')
@post('/login/prepare')
@post('/logout')
@post('/new_project')
@post('/edit_project')
@post('/project_list')
def login_out():
    '''
    '''
    c, m = get_controller(request.path)
    result = getattr(c, m)(request)
    return edit_response(json.dumps(result))

if __name__ == '__main__':
    #サービスの一覧を作成
    svc_map = make_service_map()

    #コントローラの一覧を作成
    make_controller_map(svc_map)

    #開始
    #run(host='localhost', port=8080)
    run(host='0.0.0.0', port=8080)

#[EOF]
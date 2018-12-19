# -*- coding:utf-8 -*-
import sys
sys.dont_write_bytecode = True

import json
from bottle import post, request, run, HTTPResponse

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

    svc_map = {}
    p = Path(__file__).parent / _SERVICE_ROOT
    for f in p.glob('*.py'):
        cn = Path(f).stem
        if cn == 'BaseService':
            continue
        im = '{0}.{1}'.format(_SERVICE_ROOT, cn)
        m = importlib.import_module(im)
        inst = getattr(m, cn)()
        print(inst.mapper_name, '->', im)
        svc_map[inst.mapper_name] = inst
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
        print(inst.mapper_name, '->', im)
        _controller_map[inst.mapper_name] = inst
        inst.set_service_map(servicMap)

def get_controller(path):
    '''
    POST時のパスからコントローラを取得する.
    '''
    global _controller_map
    return _controller_map[path]

@post('/login')
def login():
    '''
    $ curl -H "Content-Type: application/json" -X POST -d '{ "user_id" : "yasuo katou" }' http://localhost:8080/login
    {"message": "hello yasuo katou"}
    '''
    c = get_controller(request.path)
    return c.execute_post(request)

#サービスの一覧を作成
svc_map = make_service_map()

#コントローラの一覧を作成
make_controller_map(svc_map)

#開始
run(host='localhost', port=8080)

#[EOF]
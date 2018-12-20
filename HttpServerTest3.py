# -*- coding:utf-8 -*-
from bottle import post, request, run

@post('/hello/json')
def helloJson():
    key = 'hoge'
    data = request.json[key]
    print(key, ":", data)
run(host='localhost', port=8080)

#[EOF]
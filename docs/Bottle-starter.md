Bottleを使ってみる

インストール
    https://raw.githubusercontent.com/bottlepy/bottle/master/bottle.py
    をプロジェクトのルートにＤＬする。
    vertion:0.13-dev

    参考：https://qiita.com/Gen6/items/949babb51d0cc000dcfb


POSTリクエストをJSON形式で受信する
    参考：http://shuzo-kino.hateblo.jp/entry/2016/11/09/234840

    注意：BaseHTTPRequestHandlerを使ったサンプルでは、リクエストの
         Content-Typeが曖昧（指定しなくてもエラーにならなかったが）
         Bottleでは、「-H "Content-Type: application/json"」の
         指定が必要
         curlコマンドは、以下の通り
         $ curl -H "Content-Type: application/json" -X POST -d '{ "hoge" : 1, "bar" : "bar" }' http://localhost:8080/hello/json

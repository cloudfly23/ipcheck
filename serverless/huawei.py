# -*- coding:utf-8 -*-
from wsgiref.simple_server import make_server
import json
import socket
import os
import base64


def check_tcp_port(kw, timeout=3):
    try:
       #socket.AF_INET 服务器之间网络通信
       #socket.SOCK_STREAM  流式socket , 当使用TCP时选择此参数
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (str(kw["host"]), int(kw["port"]))
        cs.settimeout(timeout)
        #s.connect_ex(adddress)功能与connect(address)相同，但是成功返回0，失败返回error的值。
        status = cs.connect_ex(address)
    except Exception as e:
        return {"status": "fail", "message": str(e), "info": "tcp check"}
    else:
        if status != 0:
            return {"status": "fail", "message": "Connection %s:%s failed" % (kw["host"], kw["port"]),
                    "info": "tcp check"}
        else:
            return {"status": "success", "message": "OK", "info": "tcp check"}

def check_ping(ip):
    ip_address = ip
    ret=os.system('ping -c 2 -W 1 '+ip_address+' &> /dev/null')
    if ret:
        return {"status": "fail", "message": "icmp fail",
                    "info": "icmp check"}
    else:
        return {"status": "success", "message": "OK", "info": "icmp check"}
    

def handler (event, context):
    ip_info = event
    body = str(base64.b64decode(ip_info["body"]), "utf-8")
    body = json.loads(body)
    ip = body["ip"]
    port = body["port"]
    kw = {'host': ip, 'port': port}
    tcp_check = check_tcp_port(kw)
    ping_check = check_ping(ip)
    dic = {"tcp":tcp_check["status"],"icmp":ping_check["status"]}

    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "body": json.dumps(dic),
        "headers": {
            "Content-Type": "application/json"
        }
    }

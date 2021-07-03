import pymysql
import requests
import json
import telebot
from telebot import types

# tg设置相关
BOT_TOKEN=""
user=""

# 设置国内外检测节点
gn_urls = [
          ]
gw_urls = [
          ]

# MySQL数据库相关
db_host = "localhost"
db_user = ""
db_passwd = ""
db_name = ""


conn = pymysql.connect(host=db_host ,user = db_user ,passwd = db_passwd ,db = db_name)
cursor=conn.cursor()

cursor.execute("select * from ip;")

bot = telebot.TeleBot(BOT_TOKEN)

result = cursor.fetchall()
for res in result:
    name = res[0]
    print(name+"开始检测")
    ip = res[1]
    port = res[2]
    gn_tcp = res[3]
    gn_icmp = res[4]
    gw_tcp = res[5]
    gw_icmp = res[6]
    gn={}
    gw={}
    gn["tcp"] = "fail"
    gn["icmp"] = "fail"
    gw["tcp"] = "fail"
    gw["icmp"] = "fail"
    data = {'ip':ip,'port':port}
    for gn_url in gn_urls:
        re = json.loads(requests.post(gn_url,json=data).text)
        if(gn["tcp"]=="fail" and re["tcp"]=="fail"):
            gn["tcp"] = "fail"
        else:
            gn["tcp"] = "success"
        if(gn["icmp"]=="fail" and re["icmp"]=="fail"):
            gn["icmp"] = "fail"
        else:
            gn["icmp"] = "success"
    
    for gw_url in gw_urls:
        re = json.loads(requests.post(gw_url,json=data).text)
        if(gw["tcp"]=="fail" and re["tcp"]=="fail"):
            gw["tcp"] = "fail"
        else:
            gw["tcp"] = "success"
        if(gw["icmp"]=="fail" and re["icmp"]=="fail"):
            gw["icmp"] = "fail"
        else:
            gw["icmp"] = "success"
        



    if(gw["tcp"]==gw_tcp and gn["tcp"]==gn_tcp):
        1
    else:
        if(gw["tcp"]=="success"):
            if(gn["tcp"]=="fail"):
                if(gn["icmp"]=="fail"):
                    bot.send_message(
                        text=f'{name}被墙',
                        chat_id=user,
                        parse_mode='HTML'
                    )
                else:
                    bot.send_message(
                        text=f'{name}端口被墙,端口为{port}',
                        chat_id=user,
                        parse_mode='HTML'
                    )
            else:
                bot.send_message(
                    text=f'{name}恢复,端口为{port}',
                    chat_id=user,
                    parse_mode='HTML'
                )
        else:
            if(gn["icmp"]=="fail" and gn["tcp"]=="fail"):
                bot.send_message(
                    text=f'{name}翻车',
                    chat_id=user,
                    parse_mode='HTML'
                )
            else:
                if(gn["tcp"]=="success"):
                    bot.send_message(
                        text=f'{name}被反向墙',
                        chat_id=user,
                        parse_mode='HTML'
                    )
                else:
                    1

    if(gw["tcp"]==gw_tcp and gn["tcp"]==gn_tcp and gw["icmp"]==gw_icmp and gn["icmp"]==gn_icmp):
        1
    else:
        sql = "update ip set last_tcp=%s,last_icmp=%s,gw_tcp=%s,gw_icmp=%s where name=%s;"
        cursor.execute(sql, [gn["tcp"], gn["icmp"], gw["tcp"], gw["icmp"], name])
        conn.commit()
    
    print("结果国外tcp:"+gw["tcp"]+",icmp:"+gw["icmp"]+"  国内tcp:"+gn["tcp"]+",国内icmp:"+gn["icmp"])
    
cursor.close ()
conn.close ()


import telebot
from telebot import types
import pymysql
import requests
import json
# tg设置相关
BOT_ADMINS = []  # 直接填id无需引号
BOT_TOKEN=""

# MySQL 数据库相关
db_host = "localhost"
db_user = ""
db_passwd = ""
db_name = ""

#国内外检测节点设置
gn_url = ("")
gw_url = ("")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['add'])
def add_jd(call):
    if call.from_user.id not in BOT_ADMINS:
        return
    msg = bot.send_message(
        text='请输入节点名称 不能重复:',
        chat_id=call.from_user.id,
        parse_mode='HTML'
    )
    bot.register_next_step_handler(msg, get_name)

def get_name(m):
    name = m.text
    msg = bot.send_message(
            text='名称获取成功\n'
                 '输入节点ip或域名:',
            chat_id=m.from_user.id,
            parse_mode='HTML'
        )
    bot.register_next_step_handler(msg, get_ip,name)

def get_ip(m,name):
    ip=m.text
    msg = bot.send_message(
            text='ip获取成功\n'
                 '输入tcp端口:',
            chat_id=m.from_user.id,
            parse_mode='HTML'
        )
    bot.register_next_step_handler(msg, save_jd,name,ip)


def save_jd(m,name,ip):
    port=m.text
    conn = pymysql.connect(host=db_host ,user = db_user ,passwd = db_passwd ,db = db_name)
    #获取游标
    cursor=conn.cursor()
    try:
        sql="insert into ip(name,ip,port) values(%s,%s,%s)"
        cursor.execute(sql,(name,ip,port))
        conn.commit()
        bot.send_message(
            text='添加成功',
            chat_id=m.from_user.id,
            parse_mode='HTML'
        )
    except Exception as e:
    # 如果发生错误则回滚
        conn.rollback()
        bot.send_message(
            text=str(e),
            chat_id=m.from_user.id,
            parse_mode='HTML'
        )
        
    cursor.close()
    conn.close()

    



@bot.message_handler(commands=[ 'del'])
def send_jd(call):
    if call.from_user.id not in BOT_ADMINS:
        return
    list_jd(call)
    
    msg = bot.send_message(
        text='请输入需要删除的节点名称:',
        chat_id=call.from_user.id,
        parse_mode='HTML'
    )
    bot.register_next_step_handler(msg, del_jd)

def del_jd(msg):
    name = msg.text
    conn = pymysql.connect(host=db_host ,user = db_user ,passwd = db_passwd ,db = db_name)
    cursor=conn.cursor()
    delete = "delete from ip where name=%s"
    try: 
        cursor.execute(delete,name) 
        conn.commit() 
        bot.send_message(
            text='删除成功',
            chat_id=msg.from_user.id,
            parse_mode='HTML'
        )
        list_jd(msg)
    except Exception as e: 
        conn.rollback()
        bot.send_message(
            text='删除失败'+str(e),
            chat_id=msg.from_user.id,
            parse_mode='HTML'
        )




@bot.message_handler(commands=[ 'list'])
def list_jd(call):
    if call.from_user.id not in BOT_ADMINS:
        return
    conn = pymysql.connect(host=db_host ,user = db_user ,passwd = db_passwd ,db = db_name)
    #获取游标
    cursor=conn.cursor()
    select = "select * from ip"
    cursor.execute(select)
    text='节点      ip     port\n'

    result = cursor.fetchall()
    for res in result:
        name = res[0]
        ip = res[1]
        port = res[2]
        text=text +f'{name}   {ip}  {port}    \n'
    print(text)
    cursor.close()
    conn.commit()
    conn.close()

    bot.send_message(
        text=text,
        chat_id=call.from_user.id,
        parse_mode='HTML'
    )


@bot.message_handler(commands=[ 'check'])
def check(m):
    if m.from_user.id not in BOT_ADMINS:
        return
    msg = bot.send_message(
            text='输入要检测的节点ip或域名:',
            chat_id=m.from_user.id,
            parse_mode='HTML'
        )
    bot.register_next_step_handler(msg, get_check_ip)

def get_check_ip(m):
    if m.from_user.id not in BOT_ADMINS:
        return
    ip=m.text
    msg = bot.send_message(
            text='ip获取成功\n'
                 '输入tcp端口:',
            chat_id=m.from_user.id,
            parse_mode='HTML'
        )
    bot.register_next_step_handler(msg, check_ip,ip)

def check_ip(m,ip):
    try:
        msg=bot.send_message(text='正在检测...',
                chat_id=m.from_user.id,
                parse_mode='HTML'
            )
        port=m.text
        data = {'ip':ip,'port':port}
        gn =json.loads(requests.post(gn_url,json=data).text)
        gw =json.loads(requests.post(gw_url,json=data).text)
        bot.send_message(
                text=f'ip:{ip}\n'
                    f'端口:{port}\n'
                    f'国内tcp:<code>{gn["tcp"]}</code>,icmp:<code>{gn["icmp"]}</code>\n'
                    f'国外tcp:<code>{gw["tcp"]}</code>,icmp:<code>{gw["icmp"]}</code>',
                chat_id=m.from_user.id,
                parse_mode='HTML'
            )
    except Exception as e: 
        bot.send_message(
                text=f'错误:{e}\n',
                chat_id=m.from_user.id,
                parse_mode='HTML'
            )


bot.polling()


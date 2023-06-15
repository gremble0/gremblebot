#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Accidentally deleted the other project files so this is what i have left
# Also this code is ancient and a lot of it is very bad.

import re
import requests
import random
import socket
import sys
import datetime
import os
import os.path
import ast
import wolframalpha
import mysql.connector
import pymysql
from dotenv import load_dotenv
from subprocess import Popen
from commands import rtrihard, rkkona, rbanger
from formatters import time_format, cdate_format
# ------------------------------------------------- Global Variables -----------------------------------------------
prefix = '='
admin = 'qremble'
regex = re.compile(r"(?:_|(?:(?:\/[\\()[\]]\/|\|\\\||Ʌ\/|\/IJ|\/\|\/|rı|VI|[\|l][\\\/][\|l]|[Ѝпᴺ內几Ոꝴ∏ꖦN∏Й刀ղꞐᏁӅΠИ𝐧𝑛𝒏𝓃𝓷𝔫𝕟𝖓𝗇𝗻𝘯𝙣𝚗ոռＮℕ𝐍𝑁𝑵𝒩𝓝𝔑𝕹𝖭𝗡𝘕𝙉𝙽Ν𝚴𝛮𝜨𝝢𝞜ꓠŃŅŇŋƝǸȠΝṄꓠṆṈṊ₦ἠἡἢἣἤἥἦἧὴήᾐᾑᾒᾓᾔᾕᾖᾗῂῃῄῆῇñńņňŉŊƞǹȵɲɳɴᵰᶇṅṇṉṋꝴπ])[-\\x{0336}\\x{0332}+_¤\s\.=\\x{00AD}:;\/=\"\\x{0027}\?#$%&*]*)+)(?:[\]гЇᴵ工ꝉÎᏉเﾉíꟾỈyi1|ꝉlj!\/\\ｉł¡ⅰℹ↕ⅈ𝐢𝑖𝒊𝒾𝓲𝔦𝕚𝖎𝗂𝗶𝘪𝙞𝚒ı𝚤ɪɩιιͺ𝛊𝜄𝜾𝝸𝞲іⒾꙇӏꭵᎥɣᶌｙ𝐲𝑦𝒚𝓎𝔂𝔶𝕪𝖞𝗒𝘆𝘺𝙮𝚢ʏỿꭚγℽ𝛄𝛾𝜸𝝲𝞬уүყＹ𝐘𝑌𝒀𝒴𝓨𝔜𝕐𝖄𝚼𝛶𝜰𝝪𝞤ⲨУҮᎩᎽꓬŶŸƳȲɎʏẎỲỴỶỸＹÌÍÎÏĨĪĬĮİƖƗǏȈȊɪΊΐΙΪІЍИЙӢӤḬḮỈỊῘῙⅠＩェエｪｴìíîïĩīĭįıǐȉȋɨ¦ɩͥίϊийіѝӣӥḭḯỉịἰἱἲἳἴἵἶἷὶίιῐῑῒΐῖῗｉᶅḷḹḻḽýÿŷƴȳɏʎʸẏẙỳỵỷỹｙłꞲỉ][-\\x{0336}\\x{0332}+_¤\s\.\\x{00AD}:;\/=\"\\x{0027}\?#$%&*]*)+c?[бƃЭᴳp∂ճǤᘜ₲Ɡ@Ⴘkgq469ğ൫ｇℊ𝐠𝑔𝒈𝓰𝔤𝕘𝖌𝗀𝗴𝘨𝙜𝚐ɡᶃƍց𝐆么𝐺𝑮𝒢𝓖𝔊𝔾𝕲𝖦𝗚𝘎𝙂𝙶ԌᏀᏳꓖĜĞĠĢƓǤꞡǦǴʛΓГḠＧᎶĝğġģ][-\\x{0336}\\x{0332}+_¤\s\.\\x{00AD}:;\/=\"\\x{0027}\?#$%&*]*(?:[бƃЭᴳ∂ճǤᘜ₲Ɡ@Ⴘkgq469ğ൫ｇℊ𝐠𝑔𝒈𝓰𝔤𝕘𝖌𝗀𝗴𝘨𝙜𝚐ɡᶃƍց𝐆么𝐺𝑮𝒢𝓖𝔊𝔾𝕲𝖦𝗚𝘎𝙂𝙶ԌᏀᏳꓖĜĞĠĢƓǤꞡǦǴʛΓГḠＧᎶĝğġģǥǧǵɠɡɢꬶ]([-\\x{0336}\\x{0332}+_¤\s\.\\x{00AD}:;\/=\"\\x{0027}\?#$%&*]*)+[-\\x{0336}\\x{0332}+_¤\s\.\\x{00AD}:;\/=\"\\x{0027}\?#$%&*]*((?:[aAаA𝔞𝖆𝓪卂𝒶𝕒ａᴀɐa⃣a⃞🄰ɒₐᵃⓐคαǟᏗąค𝐚𝘢𝙖𝚊Λαå₳卂ﾑa҉ąᗩᗩa̶a̴a̷a̲a̳a̾aa͎a͓̽])|(?:[ᴱԐ巨ꬳ€Ėㅌ乇ҽЄᏋỀΣΞe3u𝑒𝒆𝓮𝔢𝕖𝖊𝖾𝗲𝘦𝙚𝚎ꬲеҽ⋿Ｅℰ𝐄𝐸𝑬𝓔𝔈𝔼𝕰𝖤𝗘𝘌𝙀𝙴Ε𝚬𝛦𝜠𝝚𝞔ЕⴹᎬꓰÈÉÊËĒĔΈĖĘĚƎƐȄȆȨɆΈЭӬḔḖḘḚḜẸẺẼẾỀỂỄỆἘἙἚἛἜἝῈΈèéêëēĕėęěƏȅȇȩɇɘɛɜɝɞͤέεеэӭḕḗḙḛḝẹẻẽếềểễệἐἑἒἓἔἕὲέꬴ3][-\\x{0336}\\x{0332}+_¤\s\.\\x{00AD}}:;\/=\"\\x{0027}\?#$%&*]*)+[ᴿԻꭆ尺ɾЃЯr𝐫𝑟𝒓𝓇𝓻𝔯𝕣𝖗𝗋𝗿𝘳𝙧𝚛ꭇꭈᴦⲅгꮁℛℜℝ𝐑𝑅𝑹𝓡ꭆ𝕽𝖱𝗥𝘙𝙍𝚁ƦᎡᏒ𐒴ᖇꓣŔŖŘȐȒɌʀʁṘṚṜṞⱤＲᎡŕŗřȑȓɍɹɺɻɼɽᚱᡵᵲᵳᶉṙṛꞦꝵѓ]+))")

HOST = "irc.twitch.tv"
PORT = 6667
CHAN = ''
CHANNELS = ['#gremble','#qremble','#y5or','#duskdarker','#downgrade']
NICK = "epicswagbot"
CLIENTID = os.getenv("CLIENTID")
OAUTH = os.getenv("OAUTH")

load_dotenv(".env")
HEADERS = {
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Client-ID': CLIENTID,
    'Authorization': OAUTH
}

connection = mysql.connector.connect(host = "localhost", user = "root", passwd = "", database = "gremblebot")
cursor = connection.cursor(dictionary = True, buffered = True)

# --------------------------------------------- Start Functions ----------------------------------------------------
def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))
 
message_counter = 2
def send_message(chan, msg):
    sql_check_towards_database = "SELECT banphrase, banphrasetype FROM gremblebot.banphrases"
    cursor.execute(sql_check_towards_database)
    for row in cursor:
        banphrase = row["banphrase"]
        banphrasetype = row["banphrasetype"]
        compile_banphrase = re.compile(banphrase)
        sensored = compile_banphrase.sub("SENSORED", msg)
    global message_counter
    if message_counter % 2 == 0:
        message_counter += 1
        con.send(bytes("PRIVMSG %s :%s\r\n" % (chan, sensored), 'UTF-8'))
    else:
        message_counter += 1
        sensored = sensored + ' 󠀀'
        con.send(bytes("PRIVMSG %s :%s\r\n" % (chan, sensored), 'UTF-8'))

def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))
 
def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))

def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))
 
def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))
# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result

def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.replace(':', '', 1) 
    return result

def get_target(msg):
    split_message = msg.split(' ')
    if len(split_message) >= 3:
        result = split_message[1]
        return result
    else:
        result = sender
        return result

def get_level(sender):
    sql_level = "SELECT userlevel FROM gremblebot.users WHERE username = '{}'".format(sender)
    cursor.execute(sql_level)
    for row in cursor:
        level = row["userlevel"]
        return level

def get_userid(user):
    req = requests.get("https://api.twitch.tv/kraken/users?login=%s" % (user), headers = HEADERS)
    userid = req.json()["users"][0]["_id"]
    return userid

def insert_into_db(user):
    req = requests.get("https://api.twitch.tv/kraken/users?login=%s" % (user), headers = HEADERS)
    userid = req.json()["users"][0]["_id"]
    usercdate = req.json()["users"][0]["created_at"]
    usercdate_replaced = cdate_format(usercdate)

    sql_insert_user_into_database = "INSERT IGNORE INTO users(user_id, username, usercdate) VALUES({}, '{}', '{}')".format(userid, user, usercdate_replaced)
    cursor.execute(sql_insert_user_into_database)

def log_message(chan, user, msg):
    sql_log = "INSERT INTO gremblebot.chatlogs(channel, sender, message, datethen) VALUES('{}', '{}', '{}', '{}')".format(chan, user, pymysql.escape_string(msg), datetime.datetime.today())
    cursor.execute(sql_log)

def check_notif(user):
    sql_check_notif = "SELECT * FROM gremblebot.pending WHERE notif_target = '{}'".format(sender)
    for row in cursor:
        notif_target = row["notif_target"]
        notif_sender = row["notif_sender"]
        notif_time = row["pend_date"]
        pend_message = row["message"]
        timedelta = time_format(notif_time, datetime.datetime.today())
        send_message(CHAN, '@{}, notification from {} {}: {}'.format(pymysql.escape_string(notif_target), notif_sender, timedelta, pend_message))
    sql_delete = "DELETE FROM gremblebot.pending WHERE notif_target ='{}'".format(sender)
    cursor.execute(sql_delete)

def parse_message(msg):
    if len(msg) >= 1:
        msg = msg.split(' ')
        options = {
            (prefix + 'quit'): command_quit,
            (prefix + 'ping'): command_ping,
            (prefix + 'afk'): command_afk,
            (prefix + 'gn'): command_gn,
            (prefix + 'say'): command_say,
            (prefix + 'eval'): command_eval,
            (prefix + 'suggest'): command_suggest,
            (prefix + 'query'): command_query,
            (prefix + 'rtrihard'): command_rtrihard,
            (prefix + 'randomtrihard'): command_rtrihard,
            (prefix + 'rkkona'): command_rkkona,
            (prefix + 'randomkkona'): command_rkkona,
            (prefix + 'rbanger'): command_rbanger,
            (prefix + 'randombanger'): command_rbanger,
            (prefix + 'rsong'): command_rsong,
            (prefix + 'randomsong'): command_rsong,
            (prefix + 'rsongs'): command_rsongs,
            (prefix + 'randomsongs'): command_rsongs,
            (prefix + 'followage'): command_followage,
            (prefix + 'hbl'): command_hbl,
            (prefix + 'hbn'): command_hbn,
            (prefix + 'evalfile'): command_evalfile,
            (prefix + 'haxk'): command_haxk,
            (prefix + 'notify'): command_notify,
            (prefix + 'remind'): command_notify,
            (prefix + 'bingo'): command_bingo,
            (prefix + 'rkanye'): command_rkanye,
            (prefix + 'rkq'): command_rkanye,
            (prefix + 'randomkanyequote'): command_rkanye,
            (prefix + 'hug'): command_hug,
            (prefix + 'commands'): command_commands,
            (prefix + 'userid'): command_userid,
            (prefix + 'uid'): command_userid,
            (prefix + 'cdate'): command_cdate,
            (prefix + 'creationdate'): command_cdate,
            (prefix + 'addbanphrase'): command_addbanphrase,
            (prefix + 'rclip'): command_rclip,
            (prefix + 'rq'): command_rq,
            (prefix + 'rl'): command_rq,
            (prefix + 'fq'): command_fq,
            (prefix + 'fl'): command_fq,
            (prefix + 'setlevel'): command_setlevel
            #(prefix + 'translate'): command_translate
        }

    if msg[0] in options:
        options[msg[0]]()

# --------------------------------------------- Commands --------------------------------------------------
def command_quit():
    if get_level(sender) >= 1000:
        send_message(CHAN, 'Shutting down... FeelsBadMan')
        os.execl(sys.executable, sys.executable, *sys.argv)

def command_ping():
    if CHAN == '#college_boi':
        send_message(CHAN, 'pong pepoDank')
    if CHAN == '#y5or' or CHAN == '#gremble':
        send_message(CHAN, 'pong JamesB')
    if CHAN == '#pajlada':
        send_message(CHAN, 'pong peepoSadDank')
    else:
        send_message(CHAN, 'pong TriHard')

def command_afk():
    afk_message = message[5:]
        # sql = "INSERT INTO gremblebot.pending(notif_sender, notif_target, pend_date, message) VALUES('%s', '%s', '%s', '%s')" % (sender, target, datetime.datetime.today(), notification)
        # cursor.execute(sql)
        # send_message(CHAN, '@%s, i will notify %s' %(sender, target))
    if len(split_message) >= 3:
        sql_afk = "INSERT INTO gremblebot.pending(notif_sender, pend_date, message, isafk) VALUES('%s', '%s', '%s', '1')" % (sender, datetime.datetime.today(), afk_message)
        cursor.execute(sql_afk)
        send_message(CHAN, '{} is now afk - {}'.format(sender, afk_message))
    else:
        sql_afk = "INSERT INTO gremblebot.pending(notif_sender, pend_date, message, isafk) VALUES('%s', '%s', 'no message', '1')" % (sender, datetime.datetime.today())
        cursor.execute(sql_afk)
        send_message(CHAN, '{} is now afk - no message'.format(sender))

def command_hug():
    target = get_target(message)
    if target == sender:
        send_message(CHAN, '%s hugs himself FeelsBadMan' % (sender))
    else:    
        send_message(CHAN, '%s hugs %s 🤗 ' % (sender, split_message[1]))

def command_gn():
    send_message(CHAN, '%s is now sleeping - %s' % (sender, message[3:]))

def command_say():
    if get_level(sender) >= 500:
        send_message(CHAN, message[4:])

def command_eval():
    if get_level(sender) >= 500:
        evalu = message[5:]
        eval(evalu)
        if 'send_message' not in message:
            send_message(CHAN, evalu)

def command_evalfile():
    if get_level(sender) >= 1000:
        evalfrom = (message[10:])
        evalprint = exec(open(evalfrom).read())

def command_suggest():
    suggestion = (sender + ' suggested: ' + message[9:])
    with open('suggest.txt', 'a') as writer: 
        writer.write(suggestion + '\n')
        send_message(CHAN, '@' + sender + ', Added your suggestion, thanks for suggesting :)')

def command_query():
    if get_level(sender) >= 200:
        userinput = message[6:]
        client = wolframalpha.Client(os.getenv("WOLFRAMALPHAKEY"))
        res = client.query(userinput)
        answer = next(res.results).text
        send_message(CHAN, answer)

def command_sub():
    if sender == admin:
        data = (requests.get('http://api.wolframalpha.com/v2/query.jsp').json())
        send_message(CHAN, data)

def command_rtrihard():
    send_message(CHAN, 'TriHard 👉 ' + random.choice(rtrihard))

def command_rkkona():
    send_message(CHAN, 'KKona 👉 ' + random.choice(rkkona))

def command_rbanger():
    send_message(CHAN, 'SourPls 👉 ' + random.choice(rbanger))

def command_rsong():
    rsong_genre = random.randint(1,3)

    if rsong_genre == 1:
        send_message(CHAN, random.choice(rtrihard))
    elif rsong_genre == 2:
        send_message(CHAN, random.choice(rkkona))
    else:
        send_message(CHAN, random.choice(rbanger))

def command_rsongs():
    send_message(CHAN, 'All rsongs are listed here: https://pastebin.com/Lxhgu44s :)')

def command_followage():
    if len(message) in range(10, 11):
        url = 'https://beta.decapi.me/twitch/followage/%s/%s' % (CHAN[1:], sender)
        followed = requests.get(url) 

        if followed.text == 'Follow not found' or 'No user with the name' in followed.text:
            send_message(CHAN, '%s is not following %s' % (sender, CHAN[1:]))
        else:
            send_message(CHAN, '%s followed %s ' % (sender, CHAN[1:]) + followed.text + ' ago')
    
    if len(message) > 11:
        url = 'https://beta.decapi.me/twitch/followage/%s/%s' % (split_message[2], split_message[1])
        followed =  requests.get(url)
        
        if len(split_message) > 3:
            if followed.text == 'Follow not found' or 'No user with the name' in followed.text:
                send_message(CHAN, '%s is not following %s' % (split_message[1], split_message[2]))
            else:
                send_message(CHAN, '%s followed %s ' % (split_message[1], split_message[2]) + followed.text + ' ago')
        
        if len(split_message) <= 3:
            url = 'https://beta.decapi.me/twitch/followage/%s/%s' % (CHAN[1:], split_message[1]) 
            followed = requests.get(url)

            if followed.text == 'Follow not found' or 'No user with the name' in followed.text:
                send_message(CHAN, '%s is not following %s' % (split_message[1], CHAN[1:]))
            else:
                send_message(CHAN, '%s followed %s ' % (split_message[1], CHAN[1:]) + followed.text + ' ago')

def command_hbl():
    send_message(CHAN, 'Happy birthday leeba! FeelsBirthdayMan')

def command_hbn():
    send_message(CHAN, 'Happy birthday nuuls! FeelsBirthdayMan')

def command_haxk():
    send_message(CHAN, 'https://i.imgur.com/Ey2EGjU.png monkaS')

def command_notify():
    target = split_message[1]
    notification = message[2 + len(split_message[0]) + len(split_message[1]):]

    if len(split_message) >= 3:
        sql_notif = "INSERT INTO gremblebot.pending(notif_sender, notif_target, pend_date, message) VALUES('%s', '%s', '%s', '%s')" % (sender, target, datetime.datetime.today(), notification)
        cursor.execute(sql_notif)
        send_message(CHAN, '@%s, i will notify %s' %(sender, target))
    else:
        send_message(CHAN, '@%s, please type a target and a message for your notifaction :)' % (sender))

def command_rq():
    sql_rq = "SELECT * FROM gremblebot.chatlogs WHERE sender = '{}' AND channel = '{}' ORDER BY RAND() LIMIT 1;"
    if len(split_message) == 3:
        sql_rq = sql_rq.format(split_message[1], CHAN)
    if len(split_message) >= 4:
        sql_rq = sql_rq.format(split_message[1], split_message[2])
    else:
        sql_rq = sql_rq.format(sender, CHAN)
    cursor.execute(sql_rq)
    for row in cursor:
        rq_message = row["message"]
        rq_sender = row["sender"]
        rq_datethen = row["datethen"]
        rq_timedelta = time_format(rq_datethen, datetime.datetime.today())
        send_message(CHAN, "({}) {}: {}".format(rq_timedelta, rq_sender, rq_message))

def command_fq():
    if len(split_message) >= 3:
        sql_fq = "SELECT * FROM gremblebot.chatlogs WHERE sender = '{}' AND channel = '{}' ORDER BY datethen ASC LIMIT 1;".format(split_message[1], CHAN)
    else:
        sql_fq = "SELECT * FROM gremblebot.chatlogs WHERE sender = '{}' AND channel = '{}' ORDER BY datethen ASC LIMIT 1;".format(sender, CHAN)
    cursor.execute(sql_fq)
    for row in cursor:
        fq_message = row["message"]
        fq_sender = row["sender"]
        fq_datethen = row["datethen"]
        fq_timedelta = time_format(fq_datethen, datetime.datetime.today())
        send_message(CHAN, "({}) {}: {}".format(fq_timedelta, fq_sender, fq_message))

def command_bingo():
    if sender == admin: 
        emotes = [
            'WeirdChamp', 'JUICER', 'OMEGALUL', 'PainsChamp', 'WeebsOut', '4Weirder', 'StareHard', 'gachiGASM',
            'forsenCD', 'LULW', '4HEadInLULWSpyingOutOfOMEGALUL', 'pepeLaugh', 'PagChomp', 'POGGERS', 'monkaOMEGA',
            'ZULUL', 'FeelsDankMan', 'ZULOL', 'eShrug', '4Weird', 'FeelsWeirdMan', 'PagShake', 'peepoPOGGERS', 
            'downieFortnite', 'JamesB'
            ]
        emote = random.choice(emotes)
        send_message(CHAN, 'Bingo minigame started PogChamp guess the FFZ or BTTV emote, one emote per message.')
        while emote not in get_message(line):
            if get_message(line) == emote:
                send_message(CHAN, get_sender(line[0]) + ' got it right PogChamp the emote was ' + emote)

def command_rkanye():
    url = requests.get('https://api.kanye.rest/')
    stringToDict = ast.literal_eval(url.text)
    send_message(CHAN, '"' + stringToDict['quote'] + '" -Kanye West')

def command_commands():
    send_message(CHAN, '@%s, commands are listed here: https://pastebin.com/9fdJ0aLY :)' % (sender))

# def command_translate():
    #key = ''
    #text = split_message[1:]

def command_userid():
    target = get_target(message)
    url = "https://api.twitch.tv/helix/users?login=%s" % (target)
    req = requests.get(url, headers = HEADERS)
    try:
        userid = req.json()["users"][0]["_id"]
        send_message(CHAN, '@{}, that users userid is {}'.format(sender, userid))
    except: # ! ! DÅRLIG ! !
        send_message(CHAN, 'Could not find that user FeelsBadMan')

def command_cdate():
    target = get_target(message)
    url = "https://api.twitch.tv/kraken/users?login=%s" % (target)
    req = requests.get(url, headers = HEADERS)
    try:
        cdate = req.json()["users"][0]["created_at"]
        cdate_replaced = cdate_format(cdate)
        cdate_formatted = time_format(datetime.datetime.strptime(cdate_replaced, '%Y-%M-%d'), datetime.datetime.today())
        send_message(CHAN, '@{}, that user was created {} ({})'.format(sender, cdate_formatted, cdate_replaced))
    except:
        send_message(CHAN, 'Could not find that user FeelsBadMan')

def command_addbanphrase():
    if get_level(sender) >= 500:
        if len(split_message) >= 3:
            banphrasetype = split_message[1]
            banphrase = message[len(split_message[0]) + len(split_message[1]) + 2:]
            sql_banphrase = "INSERT INTO gremblebot.banphrases(banphrase, banphrasetype) VALUES('{}', '{}')".format(banphrase, banphrasetype)
            cursor.execute(sql_banphrase)
            send_message(CHAN, '@{}, successfully added your banphrase'.format(sender))
        else:
            send_message(CHAN, '@{}, please provide a valid banphrase type(regex or plain) and banphrase'.format(sender))

def command_rclip():
    target = get_target(message)
    try:
        userid = get_userid(target)
        url = 'https://api.twitch.tv/helix/clips?broadcaster_id=%s' % (userid)
        req = requests.get(url, headers = HEADERS)
        rand_num = random.randint(0, len(req.json()["data"]))
        rclip = req.json()["data"][rand_num - 1]["url"]
        if target == sender:
            send_message(CHAN, "@{}, here is a random clip from your channel: {}".format(sender, rclip))
        else:
            send_message(CHAN, "@{}, here is a random clip from {}'s channel: {}".format(sender, target, rclip))
    except:
        send_message(CHAN, "Could not find any clips from that user FeelsBadMan")

def command_setlevel():
    if get_level(sender) >= 1000:
        sql_setlevel = "UPDATE gremblebot.users SET userlevel = {} WHERE username = '{}'".format(split_message[2], split_message[1])
        cursor.execute(sql_setlevel)
        send_message(CHAN, "{} is now level {} :D".format(split_message[1], split_message[2]))

# --------------------------------------------- Running the program ----------------------------------------------

con = socket.socket()
con.connect((HOST, PORT))

send_pass(OAUTH)
send_nick(NICK)
for channel in CHANNELS: join_channel(channel)

data = ""

while True:
    try:
        data = data + con.recv(1024).decode('UTF-8', 'ignore')
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop()

        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)
 
            if len(line) >= 1:
                if line[0] == 'PING':
                    send_pong(line[1])
 
                if line[1] == 'PRIVMSG':
                    sender = get_sender(line[0])
                    message = get_message(line)
                    split_message = message.split(' ')
                    CHAN = line[2]
                    parse_message(message)

                    sql_check_notif_afk = "SELECT * FROM gremblebot.pending WHERE notif_target = '{}' OR isafk = 1".format(sender)
                    cursor.execute(sql_check_notif_afk)
                    for row in cursor:
                        notif_target = row["notif_target"]
                        notif_sender = row["notif_sender"]
                        notif_time = row["pend_date"]
                        pend_message = row["message"]
                        isafk = row["isafk"]
                        timedelta = time_format(notif_time, datetime.datetime.today())
                        if isafk == "0":
                            send_message(CHAN, '@{}, notification from {} {}: {}'.format(pymysql.escape_string(notif_target), notif_sender, timedelta, pend_message))
                            sql_delete = "DELETE FROM gremblebot.pending WHERE notif_target ='{}' OR isafk = 1".format(sender)
                            cursor.execute(sql_delete)
                        elif isafk == "1":
                            send_message(CHAN, '{} is no longer afk: {} {}'.format(sender, pend_message, timedelta))
                            sql_delete = "DELETE FROM gremblebot.pending WHERE notif_target ='{}' OR isafk = 1".format(sender)
                            cursor.execute(sql_delete)

                    # insert_into_db(sender)
                    # log_message(CHAN, sender, message)
                    # check_notif(sender)

                    today = datetime.datetime.today().strftime("%Y/%m/%d %H:%M")
                    print("[{}] {}, {}: {}".format(today, CHAN, sender, message))

    # sketchy
    except:
        p = Popen("python" + sys.argv[0], shell = True)
        p.wait()

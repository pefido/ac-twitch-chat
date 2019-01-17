import os
import sys
import urllib
import platform
import ac
import json
import time 
from threading import Thread
from threading import Timer

PATH_APP = os.path.dirname(__file__)
path_stdlib=''
if platform.architecture()[0] == "64bit":
    path_stdlib = os.path.join(PATH_APP, 'stdlib64')
else:
    path_stdlib = os.path.join(PATH_APP, 'stdlib')
sys.path.insert(0, path_stdlib)
sys.path.insert(0, os.path.join(PATH_APP, 'third_party'))

os.environ['PATH'] = os.environ['PATH'] + ";."

import socket
import re
import configparser

configfile = os.path.join(PATH_APP, 'twitch.ini')
config = configparser.ConfigParser()
config.read(configfile)

HOST = config['MAIN']['host']
PORT = int(config['MAIN']['port'])
NICK = config['MAIN']['nick']
PASS = config['MAIN']['pass']
CHAN = config['MAIN']['chan']


CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
LOGGUED_MSG=re.compile(r"^:.*?001.*?:Welcome.*")
LOGGUEDFAIL_MSG=re.compile(r"^:.*?Login authentication failed")
APP_NAME = 'Twitch chat'
messageLabel = []
messageList = ['','','','','','','']
backupMessageList = ['','','','','','','']
lastMessageTime = time.time()
hidingMessages = False
colors = (
            (255, 0, 0),
            (255, 128, 0),
            (255, 255, 0),
            (128, 255, 0),
            (0, 255, 0),
            (0, 255, 128),
            (0, 255, 255),
            (0, 128, 255),
            (0, 0, 255),
            (128, 0, 255),
            (255, 0, 255),
            (255, 0, 128),
            (128, 128, 128),
            (255, 255, 255),
        )
linkColorNick = [('',0)]
curr_color = 0 
offsetMessage = 0
elsaped_time = 0
viewers = 'offline'
logged = 0
call = 0
running = True
fetching = False
def acMain(ac_version):
    global appWindow,messageLabel,messageList,s,next,prev,end
    appWindow=ac.newApp(APP_NAME)
    ac.setSize(appWindow,600,160)
    ac.drawBorder(appWindow,0)
    ac.setIconPosition(appWindow, 0, -10000)
    ac.setBackgroundOpacity(appWindow,0)
    s = socket.socket()
    s.connect((HOST.format(PASS).encode("utf-8"), PORT))
    s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
    s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
    s.setblocking(False)
    for i in range(0,7):
        messageLabel.append(ac.addLabel(appWindow,messageList[i]))
        ac.setPosition(messageLabel[i],15,(i*20)+30)
    # input_text = ac.addTextInput(appWindow,"")
    # ac.setPosition(input_text,15,(11*20)+30)
    # ac.setSize(input_text,555,20)
    # ac.addOnValidateListener(input_text,onSendMessage)
    #prevButton = ac.addButton(appWindow,'ᐃ')
    # ac.setSize(prevButton,20,20)
    # ac.setFontSize(prevButton,12)
    # ac.setPosition(prevButton,570,30)
    # ac.addOnClickedListener(prevButton,onClickPrev)
    # nextButton = ac.addButton(appWindow,'ᐁ')
    # ac.setSize(nextButton,20,20)
    # ac.setFontSize(nextButton,12)
    # ac.setPosition(nextButton,570,210)
    # ac.addOnClickedListener(nextButton,onClickNext)
    # endButton = ac.addButton(appWindow,'ꓪ')
    # ac.setSize(endButton,20,20)
    # ac.setFontSize(endButton,12)
    # ac.setPosition(endButton,570,230)
    # ac.addOnClickedListener(endButton,onClickEnd)
    checkTimer()
    displayRefresh()
    ac.console('Twitch app init done')
    return APP_NAME
def onClickPrev(v1,v2):
    global offsetMessage,messageList
    if (len(messageList) > 7) and (offsetMessage < (len(messageList)-7)):
        offsetMessage += 1
        displayRefresh()
def onClickNext(v1,v2):
    global offsetMessage,messageList
    if offsetMessage > 0:
        offsetMessage -= 1
        displayRefresh()
def onClickEnd(v1,v2):
    global offsetMessage
    offsetMessage = 0
    displayRefresh()
def onSendMessage(message):
    global s,messageList
    s.send("PRIVMSG {} :{}\r\n".format(CHAN, message).encode("utf-8"))
    colorIndex = getUsernameColor(NICK)
    messageList.append((NICK+": "+message,colorIndex))
    displayRefresh()
def splitMessage(mess,user):
    userlen = len(user)+2
    splitted = []
    length_sup = True
    first = True
    rest_mess = mess
    while length_sup == True:
        if len(rest_mess) > (64-userlen):
            split_mess = rest_mess[0:64]
            rest_mess = rest_mess[64:]
            if first == True:
                splitted.append(user+': '+split_mess)
                first = False
            else:
                splitted.append(split_mess)
        else:
            if rest_mess.strip() != "":
                if first == True:
                    splitted.append(user+': '+rest_mess)
                    first = False
                else:
                    splitted.append(rest_mess)
            length_sup = False
    return splitted
def rangeColor(value):
    OldRange = (255 - 0)  
    NewRange = (1 - 0)  
    NewValue = (((value - 0) * NewRange) / OldRange) + 0
    return NewValue
def displayRefresh():
    global messageList,messageLabel,offsetMessage
    lenList = len(messageList)
    for i in range(0,7):
        curr_mess = messageList[i+(lenList-7)-offsetMessage]
        if isinstance(curr_mess, tuple):
            message = curr_mess[0]
            ColorIndex = curr_mess[1]
            ac.setText(messageLabel[i], "{}".format(message))
            R = rangeColor(colors[ColorIndex][0])
            G = rangeColor(colors[ColorIndex][1])
            B = rangeColor(colors[ColorIndex][2])
            ac.setFontColor(messageLabel[i],R,G,B,1)
        else:
            ac.setText(messageLabel[i], "{}".format(curr_mess))
def getUsernameColor(nick):
    global curr_color,linkColorNick
    color = None
    for i in linkColorNick:
        if i[0] == nick:
            color = i[1]
    if color == None:
        linkColorNick.append((nick,curr_color))
        color = curr_color
        curr_color += 1
        if curr_color > (len(colors)-1):
            curr_color = 0
    return color
def getActualFollow():
    global viewers,CHAN,PASS,fetching
    fetching = True
    try:
        headers = {'Accept': 'application/vnd.twitchtv.v3+json'}
        r = urllib.get('https://api.twitch.tv/kraken/streams/'+CHAN[1:]+'?oauth_token='+PASS[6:], headers=headers)
        jsonData = r.json()
        ac.console('json {}'.format(jsonData))
        if jsonData['stream'] != None:
            viewers = str(jsonData['stream']['viewers'])
        else:
            viewers = 'offline'
    except:
        pass
    fetching = False
    
def acUpdate(deltaT):
    global messageList,messageLabel,s,appWindow,elsaped_time,viewers,CHAN,logged,hidingMessages,backupMessageList,messageList,lastMessageTime
    elsaped_time += deltaT
    if elsaped_time > 5 and logged == 1:
        if fetching == False:
            Thread(target=getActualFollow).start()
        ac.setTitle(appWindow,'')
        elsaped_time = 0
        ac.setBackgroundOpacity(appWindow,0)
    try:
        response = s.recv(512).decode("utf-8")
        if logged == 0:
            res = re.search(LOGGUED_MSG, response)
            if res != None:
                logged = 1
                #messageList.append('logged in success')
                displayRefresh()
            res = re.search(LOGGUEDFAIL_MSG, response)
            if res != None:
                logged = 1
                messageList.append('login fail please check you\'re credential information')
                displayRefresh()
        else:
            if response == "PING :tmi.twitch.tv\r\n":
                s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            elif response != None:
                result = re.search(CHAT_MSG, response)
                if result != None:
                    if hidingMessages == True:
                        tmpArray = backupMessageList
                        backupMessageList = messageList
                        messageList = tmpArray
                        hidingMessages = False
                    result = result.group(0)
                    username = re.search(r"\w+", response).group(0) # return the entire match
                    colorIndex = getUsernameColor(username)
                    message = CHAT_MSG.sub("", response)
                    message_ready = splitMessage(message,username)
                    lastMessageTime = time.time()
                    for i in message_ready:
                        messageList.append((i,colorIndex))
                    displayRefresh()

    except:
        pass
def checkTimer():
    global lastMessageTime,hidingMessages,messageList,backupMessageList,running
    currentTime = time.time()
    if currentTime - lastMessageTime > 120 and hidingMessages == False:
        tmpArray = messageList
        messageList = backupMessageList
        backupMessageList = tmpArray
        hidingMessages = True
    displayRefresh()
    if running:
        Timer(2, checkTimer).start()
def acShutdown():
    global s,running
    running = False
    s.close()
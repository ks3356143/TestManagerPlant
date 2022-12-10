# -*- coding:utf-8 -*-
import time
import zmq
import PySimpleGUI as sg
#界面简单设计
sg.theme("SystemDefault")
layout = [
    [sg.B('接收消息-主线程',key='-bu-')],
    [sg.In(key='-message-')],
    [sg.ML(reroute_cprint=True,size=(70,20),key='-ml-')]
]
window = sg.Window('服务器收到消息记录',layout)
#zmq连接
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:51011")
socket.bind("tcp://*:51013")
while True:
    event, values = window.read()
    if event == None:
        break
    if event == '-bu-' :
        message = socket.recv()
        message1 = message.decode('UTF-8')
        print(message1)
        socket.send('服务端一体化返回消息'.encode('UTF-8'),zmq.NOBLOCK)
        sg.cprint('收到消息：', message1)



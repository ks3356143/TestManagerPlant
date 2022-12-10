# -*- coding:utf-8 -*-
import time
import zmq
import PySimpleGUI as sg
context = zmq.Context()
socket = context.socket(zmq.SUB)
# 这里设置的是过滤条件，不然无法收到消息
socket.setsockopt_string(zmq.SUBSCRIBE,'')
socket.connect("tcp://localhost:51012")

while True:
    message = socket.recv_string()
    print('订阅者收到消息，计数',message)
    sg.PopupAnnoying(message,location=(100,100),grab_anywhere=True,non_blocking = True)

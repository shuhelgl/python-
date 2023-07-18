#!/usr/bin/python

from socket import *
import threading
import time
import os
HOST = 'localhost'
PORT = 22332
BUFSIZ = 1024
ADDR = (HOST, PORT)

flag = True

try:
    cliSock = socket(AF_INET, SOCK_STREAM)
    cliSock.connect(ADDR)  # 连接服务端
except:
    print('连接失败')
    flag = False


def heart_bit(cliSock):
    while True:
        try:
            # 发送心跳消息
            cliSock.send('heartbeat'.encode())

        except:
            print('连接已断开:')
            os._exit(0)
            break
        time.sleep(1)

def recv_message(cliSock):
    while True:
        try:
            data = cliSock.recv(BUFSIZ).decode()
            if data == 'over':
                    cliSock.close()
                    break
            elif data == 'ok':
                continue
            elif 'lose' in data:
                    print('')
                    print('你输了，有人答对了，开始下一轮')
            elif 'win' in data:
                    print('')
                    print('你赢了，开始下一轮')
            else:
                    print('')
                    print( data)  #输出服务端给自己的内容
        except:
            break
    



recv_thread = threading.Thread(target=recv_message, args=(cliSock,))
recv_thread.start()

bit_thread = threading.Thread(target=heart_bit, args=(cliSock,))
bit_thread.start()

while flag:
    data = input('输入over结束>')
    if data == 'over':
        cliSock.close()
        break
    cliSock.send(data.encode())  # 把键盘输入发送给服务端
    # data = cliSock.recv(BUFSIZ).decode()  # 接收服务端给自己的内容





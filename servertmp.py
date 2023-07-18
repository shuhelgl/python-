# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 16:40:02 2023

@author: wb.liguangliang
"""

#!/usr/bin/python

from socket import *

import random
import threading
import time
from guess import A_count,B_count,check

HOST = ''  # 代表本机
PORT = 22332  # 端口
BUFSIZ = 1024  # 缓存大小 1KB
a = (HOST, PORT)  # 生成一个字典，用来bind套接字

app_list = list()  # 连接池

# 初始化函数


def init():
    """
    初始化服务端
    """
    global tcpSock
    tcpSock = socket(AF_INET, SOCK_STREAM)  # 生成对象
    tcpSock.bind(a)  # 绑定套接字
    tcpSock.listen(5)  # 最大监听客户端数量


# 生成随机数
number = str(random.randint(0, 9)) + str(random.randint(0, 9)) + \
    str(random.randint(0, 9)) + str(random.randint(0, 9))


# 检查输入的合法性以及其他查看答案等功能



'''计算A的数量，需要输入两个字符串一个是用户输入的，一个是随机生成的，他对
输入的连个字符串一样比对相应位置，找出A的个数并且会记录每一个A的位置（以数组形式存储）-数组长度，因为在后边会将
A对应位置的字符从两个字符串中

'''



'''计算B的数量，需要输入两个字符串，这两个字符串是剔除了A所在位置的字符的字符串
然后循环比对两个字符串，当发现当前位置用户答案在该位置与系统中随机数相同则B数量加1
'''


# 子进程主程序，用于主要的答案计算，发送信息等等功能


def message_handle(cliSock, tcp_client_ip):
    # client_type = ""  # 用于标记该客户端的身份
    print(app_list)
    while True:

        data = cliSock.recv(BUFSIZ).decode()  # 连接成功后，把客户端的输入存到自己的buffer
        print('data:', data)
        ch = check(data)
        global number
        global one_win
        global who_win
        

        
        if ch == 'answer':
            cliSock.send(number.encode())
        elif ch == 'heartbeat':
            cliSock.send('ok'.encode())
        elif ch == 'next':
            number = str(random.randint(0, 9)) + str(random.randint(0, 9)) + \
                str(random.randint(0, 9)) + str(random.randint(0, 9))
            cliSock.send('进入下一轮'.encode())
            print(number)
            continue
        elif ch == 'over':
            cliSock.send('over'.encode())
            break
        elif ch == True:
            cliSock.send('输入不合法重新输入,请重新输入'.encode())
            continue
        else:
            string_number = str(number)
            string_answer = str(data)

            # 调用A_count函数，计算A个数和要删除的序列right_opt
            A, right_opt = A_count(string_number, string_answer)
            # 遍历right_count循环删除A的位置
            for i in right_opt:
                string_answer = string_answer[:i]+string_answer[i+1:]
                string_number = string_number[:i]+string_number[i+1:]

            B = B_count(string_number, string_answer)
            # 判断是否回答正确，胜者将会收到胜利信息进入下一轮，广播输者信息同样进入下一轮
            if A != 4:
                cliSock.send((str(A)+'A'+str(B)+'B').encode())
            elif A == 4:
                cliSock.send('你win,开始下一轮'.encode())
                number = str(random.randint(0, 9)) + str(random.randint(0, 9)) + \
                    str(random.randint(0, 9)) + str(random.randint(0, 9))
                notify_lose(cliSock)
            print(str(A)+'A'+str(B)+'B')


# 广播函数，接受胜利者，然后遍历连接池向胜者以外的人发送输了的信息
def notify_lose(winner):
    lose_message = "lose"
    global app_list
    for client in app_list:
        if client != winner:
            client.sendall(lose_message.encode())

# 链接函数用于监听客户端连接，当有链接时创建一个线程用于服务，并将该客户端加入连接池
def accept_client():
    """
    接收新连接
    """
    while True:

        cliSock, addr = tcpSock.accept()  # 监听客户端套接字等
        global app_list
        app_list.append(cliSock)
        print(str(cliSock) + "接入")
        # 给每个客户端创建一个独立的线程进行管理
        thread = threading.Thread(target=message_handle, args=(cliSock, addr))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()


if __name__ == '__main__':
    init()
    print("waiting for connection:...")
    thread = threading.Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    while True:
        time.sleep(0.1)

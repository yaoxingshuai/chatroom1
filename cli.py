#udp客户端
#usage: python3 UDP_cli.py

#注册方法
#登录方法
#发送消息

#待改进的地方：
# 不管是不是好友，都可以发消息
from socket import *
import sys
import threading


addr=('stardan.cn',12310)
sockfd=socket(AF_INET,SOCK_DGRAM)
BUFSIZE=1024

sockfd.sendto(b'login none none',addr)

name_from=None
#name_from_tmp=None  #可能登录成功的名字
name_to=None

def send_msg():
    global name_from,name_to
    while True:
        #print('thread_____send')
        #print('fd1',sockfd)
        data=sys.stdin.readline().encode().strip()

        try:
            #登录 login user passwd
            if data.startswith(b'#login'):
                name_from=data.split()[1]
                print('你请求登录账号：',name_from)
                sockfd.sendto(data,addr)
            #注册 regist user passwd
            elif data.startswith(b'#regist'):
                print('尝试注册用户...')
                sockfd.sendto(data,addr)
            #设置聊天对象 to user
            elif data.startswith(b'#to'):
                name_to=data.split()[1]
                print('您设置聊天对象为：',name_to)
            #如果已经登录，且设置好聊天对象，可以直接输入内容
            else:
                if name_from!=None and name_to!=None:
                    from_to_data=name_from+b' '+name_to+b' '+data
                    sockfd.sendto(from_to_data,addr)
        except Exception as e:
            print('exception...',e)
        #print('______发送出去了_______',data)




def recv_msg():
    while True:
        #print('thread_____recv')
        #print('fd2',sockfd)
        data,addr=sockfd.recvfrom(BUFSIZE)
        print('_________新消息______',data)
t2=threading.Thread(target=recv_msg)
t1=threading.Thread(target=send_msg)

t1.start()
t2.start()

t1.join()
t2.join()
print('end___')

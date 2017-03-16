#ser:  udp服务器
#usage:  python3 ser1.py

from socket import *
from mySolution import Solution


#记录已注册的用户的用户名和密码
user_dic={
    b'sky':b'39sky',
    b'dan':b'1d'
}

#记录在线的用户的用户名和addr
addr_dic={}

HOST=''
PORT=12310
BUFSIZE=1024

serAddr=(HOST,PORT)
udpSerSock=socket(AF_INET,SOCK_DGRAM)
udpSerSock.bind(serAddr)

sov=Solution(udpSerSock,user_dic,addr_dic)


sov.hello()

while True:
    try:
        print("---------------waitint for message...")
        data,addr=udpSerSock.recvfrom(BUFSIZE)
        data=data.strip()

        dataTup=data.split(maxsplit=2)  #最多分为三段
        if len(dataTup)<3:
            print('data too short, ignore it')
            continue
        #如果用户想登录 数据包内容为 login user passwd
        if(dataTup[0].lower()==b'#login'):
            sov.onLoginOk(dataTup[1],dataTup[2],addr)

        # 如果用户想登录 数据包内容为 regist user passwd
        elif(dataTup[0].lower()==b'#regist'):
            sov.onRegist(dataTup[1],dataTup[2],addr)


        #如果用户在聊天,服务器转发到目的地
        else:
            sov.recruSend(data,addr)


    except Exception as e:
        print("catch exception:",e)



udpSerSock.close()




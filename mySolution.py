#from ser1 import user_dic,udpSerSock


class Solution:
    def __init__(self,sersock,user_dic_,addr_dic_):
        self.udpSerSock=sersock
        self.user_dic=user_dic_
        self.addr_dic=addr_dic_

    def hello(self):
        print('hello,world')

    #如果用户登录，处理之
    def onLoginOk(self, user, passwd, addr):
        if user in self.user_dic and self.user_dic[user]==passwd:
            retData='login_ok'  #登录成功
            self.addr_dic[user]=addr
        elif user not in self.user_dic:
            retData='login_userErr' #用户名不存在
        else:
            retData='login_passwdErr'   #密码错误

        #显示用户登录的信息，并且返回给用户
        print(user,passwd,addr,retData)
        self.udpSerSock.sendto(retData.encode('utf8'),addr)


    # 如果用户需要注册，处理之
    def onRegist(self, user, passwd, addr):
        #用户名已存在
        if user in self.user_dic:
            print('user:', user, 'Exist')
            self.udpSerSock.sendto(b'user_exits',addr)
        #注册成功
        else:
            self.user_dic[user]=passwd
            print('user:',user, 'regist OK')
            self.udpSerSock.sendto(b'regist_OK',addr)

    #如果用户在聊天，服务器中转信息
    def recruSend(self,data,sourceAddr):
        try:
            name_from,name_to,content=data.split(maxsplit=2)

            #输入的源或目的  用户名错误
            if (name_from not in self.addr_dic) or \
                    (name_to not in self.addr_dic) :
                print('name not in addr_dic')
                self.udpSerSock.sendto(data+b' destination not online',sourceAddr)
            #假装别人发送数据
            if self.addr_dic[name_from]!=sourceAddr:
                print('you did not login as:',name_from)
                self.udpSerSock.sendto('you did not login as: '+name_from,sourceAddr)

            else:
                toAddr=self.addr_dic[name_to]
                print('转发消息',data,toAddr)
                self.udpSerSock.sendto(data,toAddr)

        except Exception as e:
            print('solution exception:',e)



if __name__=='__main__':
    print('this is solution')
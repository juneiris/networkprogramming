
BLOCK_TIME=60
FAILURE_TIME=3


#open the list of username and password to autheticate
f=open('/Users/xuchuwen/Documents/python/user_pass.txt','r')

result=list()
for line in f.readlines():
    line=line.strip()
    result.append(line)
#import neccessary modules
import socket
import time
import datetime
import select
import threading
import sys


#set server address
host='localhost'
port=int(sys.argv[1])

#create lists
clientnum=0
clientlist=list()
usernameused=[' ']*10000

logintime=list()
loginname=[' ']*10000

logininfo=list()
whoelseinfo=list()
whoelsetime=list()
whoelsename=list()


logoutname=list()
logoutconn=list()


blockname=list()
blocktime=[' ']*10000

#function to splite sentence by space
def splitbyspace(inmessage):

       outmessage=inmessage.split(' ')
       return outmessage

#function to get the connection of a given username
def getuserconn(username):
       ino=usernameused.index(username)
       print ino
       for c in clientlist:
              if c.fileno()==ino:
                     return c

#function deals with private talk between users
def privatetalk(fromwhoconn,fromwhoname,towhoname,inmessage):
       print fromwhoname,towhoname
       try:
           # myconn=getuserconn(fromwho)
           userconn=getuserconn(towhoname)
           space=' '
           message=space.join(inmessage)
           print message
           userconn.send('\n'+fromwhoname+':'+message+'\n'+'>>')
           #towho.send('\n'+fromwho+':'+message+'\n'+'>>')
       except ValueError:
            fromwhoconn.send('\n'+towhoname+' is not online. Please change a receiver'+'\n'+'>>')


       except AttributeError:
           fromwhoconn.send('\n'+'Some error occured because other users suddenly logout. Please logout and login again'+'\n'+'>>')
            # myconn=getuserconn(fromwho)
            # myconn.send('\n'+towho+' is not online. Please change a receiver'+'\n'+'>>')
            # pass

#function deals with broadcast to all users
def broadcasttoall(fromwhoconn,fromwhoname,inmessage):
    try:
       space=' '
       message=space.join(inmessage)
       print fromwhoname,message
       for c in clientlist:
              if usernameused[c.fileno()]!=fromwhoname:
                     c.send('\n'+fromwhoname+':'+message+'\n'+'>>')
              else:
                     pass
    except AttributeError:
           fromwhoconn.send('\n'+'Some error occured because other users suddenly logout. Please logout and login again'+'\n'+'>>')


#function deals with broadcast to some users
def broadcasttosome(fromwhoconn,fromwhoname,towho,inmessage):
       #myconn=getuserconn(fromwhoname)
       print towho
       i=0
       space=(' ')
       message=space.join(inmessage)
       print message
       while i<len(towho):
           try:
               userconn=getuserconn(towho[i])
               userconn.send('\n'+fromwhoname+':'+message+'\n'+'>>')
               i+=1
           except ValueError:

               fromwhoconn.send('\n'+towho[i]+' is not online. Please change a receiver'+'\n'+'>>')
               i+=1
           except AttributeError:
               fromwhoconn.send('\n'+'Some error occured because other users suddenly logout. Please logout and login again'+'\n'+'>>')
               i+=1

#thread deals with one client connection, including login authetication, message recv and send
def client_process(conn,addr):
        ftry=1
        getunpw=True

        #login authetication
        while getunpw==True:
            x = conn.recv(1024)
            xunpw=splitbyspace(x)
            xusername=xunpw[0]
            print xusername
            #check if the username is blocked before
            if (xusername in blockname):
                print blockname
                bt=blocktime[blockname.index(xusername)]
                print bt
                btime=datetime.datetime.strptime(bt, "%a %b %d %H:%M:%S %Y")
                ct=time.ctime()
                curtime=datetime.datetime.strptime(ct, "%a %b %d %H:%M:%S %Y")
                if (curtime-btime).seconds<(datetime.timedelta(0,BLOCK_TIME)).seconds:
                    conn.send('\n'+'You are blocked')

                    print btime
                else:
                    blockname.remove(xusername)
                    blocktime.remove(bt)
                    conn.send('You are removed from block list, please login again')
                    continue
            else:
                #check if the username is in the txt file and haven't been used before
                if (x in result) == True:
                    if (xusername in usernameused)==False:
                        conn.send('success')
                        print 'connected by',xusername,addr


                        usernameused[conn.fileno()]=xusername
                        clientlist.append(conn)
                                          #print usernameused

                        mylogintime=time.ctime()
                        logintime.append(mylogintime)
                        timeindex=logintime.index(mylogintime)
                        #print timeindex
                        loginname[timeindex]=xusername
                        #print loginname

                        mylogininfo=mylogintime+': '+xusername
                        logininfo.append(mylogininfo)
                                          #print logininfo
                        ftry=1
                        getunpw=False
                    else:
                        conn.send('The user has already logged in, please use another username')
                else:

                    # check if failed thress times and block

                    if ftry<FAILURE_TIME:
                        conn.send ('Wrong username or password, please try again')
                        print ftry
                        ftry+=1
                    else:
                        ftry=1
                        blockname.append(xusername)
                        blockindex=blockname.index(xusername)
                        blocktime[blockindex]=time.ctime()
                        print 'block time:'+blocktime[blockindex]
                        conn.send('Sorry, connection failed. You are blocked')
                        conn.close()
                        return

        #recv and send message
        while 1:
              try:

                     data=conn.recv(1024)


                     datasplit=splitbyspace(data)
                     print datasplit

                     #command recognition
                     #whoelse
                     if data=='whoelse':

                            myinfoindex=logininfo.index(mylogininfo)
                            whoelseinfo=logininfo[:myinfoindex]+logininfo[(myinfoindex+1):]

                            conn.send('else:%s'%(whoelseinfo))
                     #logout
                     elif data=='logout':
                         try:
                            logininfo.remove(mylogininfo)
                            usernameused.remove(xusername)
                            clientlist.remove(conn)

                            conn.send('Good bye!you have been logout')
                            conn.close()
                            return
                         except ValueError:
                             continue

                    #wholast
                     elif datasplit[0]=='wholast':
                            try:
                                   lastsec=float(datasplit[1])*60
                                   print lastsec
                                   tself=datetime.datetime.strptime(mylogintime, "%a %b %d %H:%M:%S %Y")

                                   i=0
                                   while i<len(logintime):
                                          tother=datetime.datetime.strptime(logintime[i], "%a %b %d %H:%M:%S %Y")
                                          print tother
                                          if (tself-tother).seconds<(datetime.timedelta(0,lastsec)).seconds:
                                                 if loginname[i]!=xusername:
                                                        conn.send('\n'+loginname[i]+'\n'+'>>')
                                          i+=1
                            except ValueError:
                                   conn.send('Wrong format,please try again! Input should be wholast+number'+'\n'+'>>')
                            except IndexError:
                                   conn.send('Wrong format,please try again! Input should be wholast+number'+'\n'+'>>')


                    #private talk
                     elif datasplit[0]=='message':
                         try:
                             myconn=conn
                             #userconn=getuserconn(datasplit[1])
                             privatetalk(myconn,xusername,datasplit[1],datasplit[2:])
                             #privatetalk(xusername,datasplit[1],datasplit[2:])
                         except IndexError:
                             conn.send('Wrong format,please try again! Input should be message+username+your words'+'\n'+'>>')
                    #broadcast
                     elif datasplit[0]=='broadcast':
                            if('message' in datasplit)== True:
                                   if datasplit[1]=='message':
                            #if messageindex==1:
                                          broadcasttoall(conn,xusername,datasplit[2:])
                            #elif messageindex!=1:
                                   elif datasplit[1]!='message':
                                          messageindex=datasplit.index('message')

                                          broadcasttosome(conn,xusername,datasplit[1:messageindex],datasplit[(messageindex+1):])
                            else:
                                   conn.send('wrong message format, please try again'+'\n'+'>>')
                    #if user input command not on the table
                     else:
                         conn.send('Cannot recognize the input command! Please try again'+'\n'+'>>')


              except KeyboardInterrupt:

                    conn.send('Good bye!You have been logout')
                    conn.close()
                    return




#main thread, only deals with listen and accept connections
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)
while 1:
    try:
       r,w,e=select.select([s],[],[])
       for s in r:
              if s in r:

                     connection,address = s.accept()
                     clientnum+=1
                     print 'client number:',clientnum


                     clientthread=threading.Thread(target=client_process,name='server process thread'+str(clientnum),args=(connection,address))
                     clientthread.daemon=True
                     clientthread.start()

    #gracefully exit when ctrl+c
    except KeyboardInterrupt:
        for c in clientlist:
            c.send('Good bye!you have been logout')
            c.close()
        break




s.close()
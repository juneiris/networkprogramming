TIME_OUT=1

import socket
import threading
import sys

host=sys.argv[1]
port=int(sys.argv[2])
#host='localhost'
#port=8001


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

i=1

flag=1

#input information to login
def loginFunc():

    username=raw_input('please enter your username >>')
    password=raw_input('please enter your password >>')
    unpw=username+' '+password
    s.send(unpw)


#thread that keeps receiving message, indepent from keybroad input
def recvFunc():
     global flag
     while 1:
         try:
            serverdata=s.recv(1024)
            print serverdata
            if serverdata=='Good bye!you have been logout':
                print 'Please press Enter'
                flag=0
                break
         except socket.timeout:
             print ('\n'+'Timeout')
             s.send('logout')




while 1:
    try:
        #set timeout to logout automatically
        s.settimeout((TIME_OUT*60))

        if flag==0:
            break
        loginFunc()
        serverdata=s.recv(1024)
        print serverdata
        if serverdata=='Sorry, connection failed. You are blocked':
            s.close()
            break
        if serverdata=='success':
            print 'Welcome to server!'


            tr=threading.Thread(target=recvFunc)
            tr.setDaemon(True)
            tr.start()

            while 1:
                # tr=threading.Thread(target=recvFunc)
                # tr.setDaemon(True)
                # tr.start()
                #print tr.is_alive()
                inp=raw_input('>>')

                if inp=='whoelse':
                    print 'wait a sec...'
                s.send(inp)



                if flag==0:
                    break

    except socket.timeout:
        print 'timeout'
    except KeyboardInterrupt:
        s.send('logout')
        break



s.close()
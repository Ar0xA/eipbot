#replacing eip

import socket, random, time, string, requests, select
from urllib import urlencode
from urllib2 import urlopen, Request

NICKNAME='eip[bot]'
CHANNEL='#inforekt'
network = 'adams.freenode.net'
port = 6667

def connect():
    irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    irc.connect ( ( network, port ) )
    print irc.recv ( 4096 )
    irc.send('NICK %s \r\n' % NICKNAME)
    irc.send ( 'USER Foo foo foo : eip replacement\r\n' )
    irc.send('JOIN %s \r\n' % CHANNEL)
    return irc

def sendmsg(irc, message):
    irc.send(message)

def url_generator(size=5, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == "__main__":
    irc = connect()
    timer=0
    while True:
        irc.setblocking(0)
        ready = select.select([irc],[],[], 5)
        if ready[0]:
            data = irc.recv ( 4096 )
        if data.find ( 'PING' ) != -1:
            irc.send('PONG '+ data.split() [ 1 ] + '\r\n')
        #did 5 minutes pass yet?
        if (timer <= 300):
            timer += 1
	    time.sleep(1)
	    print ("- Pretending to work as hard as Eip")
        else:
            print "getting info"
            timer = 0
            rndurl=url_generator()
            #check if url exists
            checkurl = "http://imgur.com/%s" % (rndurl)
            result= requests.get(checkurl)
            if result.status_code == 404:
                print "url does not exist :("
            else:
                what_to_say = "omg lol kek: %s" % (checkurl)
                sendmsg(irc,'PRIVMSG '+ CHANNEL + ' :%s\r\n' % (what_to_say))

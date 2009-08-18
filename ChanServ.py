# -*- coding: utf-8 -*-
#This is just to not brake lobby chanserv support, the server wors also without that
import time
import thread
import threading
import traceback
import pickle
from Channel import *
from ServicesClient import *
ist = ServicesClient()
tl = threading.Lock()
debug = False
def onlogin(data):
  cid = unpack("H",data[:2])[0]
  username = parsetag(data[2:])[1]
  ist.forgemsg(cid,"ADDUSER ChanServ ?? 0\nCLIENTSTATUS ChanServ 64\n")
  
def onjoinchannel(data):
  cid = unpack("H",data[:2])[0]
  channametag = parsetag(data[2:])
  ist.forgemsg(cid,"CLIENTS %s ChanServ\n"%channametag[1])
def clientsent(data):
  try:
    tl.acquire()
    cid = unpack("H",data[:2])[0]
    cmd = parsetag(data[2:])[1]
    
    #print username
    a = cmd.strip("\r\n").split(" ")
    if len(a) >= 2:
      if a[0].upper() == "SAY":
	username = ist.getclientattr(cid,"username")
	code = ""
	code += "if \"%s\" in self.main.channels and \"%s\" in self.main.channels[\"%s\"].users:\n" % (a[1],username,a[1])
	code += "\tself.sendpacket(OP_RESULT,forgetag(\"result\",\"True\"))\n"
	code += "else:\n"
	code += "\tself.sendpacket(OP_RESULT,forgetag(\"result\",\"False\"))\n"
	#print code
	ist.execpython(code)
	#print "Executed"
	res = ist.getresult()
	if res == "True":
	  if a[2] == "!info":
	    code = ""
	    code += "self.sendpacket(OP_RESULT,forgetag(\"res\",str(self.main.channels[\"%s\"].confirmed)))" % a[1]
	    ist.execpython(code)
	    res = ist.getresult()
	    if res == "True":
	      ops = []
	      code = ""
	      code += "self.sendpacket(OP_RESULT,forgetag(\"res\",pickle.dumps(self.main.channels[\"%s\"])))" % a[1]
	      ist.execpython(code)
	      res = ist.getresult()
	      channelobj = pickle.loads(res) #Epic python rocks
	      for op in channelobj.operators:
		ops.append(ist.getaccountnamebyid(int(op)))
		
	      founder = ist.getaccountnamebyid(int(channelobj.founder))
	      ist.broadcastchannel(a[1],"SAID %s ChanServ %s: Channel #%s info: Founder is <%s>, Operators are %s\n" % (a[1],username,a[1],founder,str(ops)))
	    else:
	      ist.broadcastchannel(a[1],"SAID %s ChanServ %s: Channel #%s Is not registered\n" % (a[1],username,a[1]))
	  if a[2] == "!mute":
	    if len(a[2:]) >= 2:
	      code = ""
	      code += "self.sendpacket(OP_RESULT,forgetag(\"res\",pickle.dumps(self.main.channels[\"%s\"])))" % a[1]
	      ist.execpython(code)
	      res = ist.getresult()
	      channelobj = pickle.loads(res) #Epic python rocks
	      userid = ist.getaccountid(username)
	      print channelobj.founder,userid
	      if int(userid) == int(channelobj.founder) or userid in channelobj.operators:
		code = ""
		code += "self.main.accmute(\"%s\",\"%s\",\"%s\",%i)" % (a[1],"Channel Services Emulator",a[3],int(a[4]))
		ist.execpython(code)
	      else:
		ist.broadcastchannel(a[1],"SAID %s ChanServ %s: Not enough rights to use that command\n" % (a[1],username))
  except:
    print traceback.format_exc()
  tl.release()
  #print username,a
def onclientsent(data):
  thread.start_new_thread(clientsent,(data,))
ist.callbacks[OP_CLIENTLOGGEDIN] = onlogin
ist.callbacks[OP_CLIENTSENT] = onclientsent
ist.callbacks[OP_CLIENTJOINEDCHANNEL] = onjoinchannel
while 1:
  time.sleep(100)

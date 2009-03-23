import socket,string,thread,time
import sys,traceback,pdb,re,os
import base64,md5,commands,ip2country
import select,os
from utilities import *
from colors import *
class Battle:
  def __init__(self,typ,nattype,password,port,maxplayers,hashcode,minrank,maphash,mapname,title,modname,founder,hostip,id):
    self.type = typ
    self.nattype = nattype
    self.password = password
    self.port = port
    self.maxplayers = maxplayers
    self.hashcode = hashcode
    self.minrank = minrank
    self.maphash = maphash
    self.mapname = mapname
    self.title = title
    self.modname = modname
    self.players = []
    self.hostip = hostip
    self.founder = founder
    self.players.append(founder)
    self.id = id
    if password == "*":
      self.passworded = 0
    else:
      self.passworded = 1
  def forgebattleopened(self):
    s = "BATTLEOPENED %i %s %s %s %s %s %s %s %s %s %s\n" % ( self.id,self.type,self.nattype,self.founder,self.hostip,self.port,self.maxplayers,self.passworded,self.minrank,self.maphash,'\t'.join([self.mapname,self.title,self.modname]))
    return s
class ssock:
  def __init__(self,sock):
    self.buf = []
    self.sck = sock
  def send(self,data):
    self.buf.append(data)
    #print buf
class BattleStatus:
  def __init__(self,status):
    st =  int(status)
    self.b0 = 0
    self.ready = getready(st)
    self.teamno = getteam(st)
    self.allyno = getally(st)
    self.mode = getspec(st)
    self.handicap = gethand(st)
    self.b1821 = 0
    self.sync = getsync(st)
    self.side = getside(st)
    self._28_ = 0
  def update(self,status):
    st =  int(status)
    #print status
    #for e in dir(self):
    #  exec("g = self.%s" % e)
    #  print "self.%s = %s" % (e,str(g))
    self.b0 = 0
    self.ready = getready(st)
    self.teamno = getteam(st)
    self.allyno = getally(st)
    self.mode = getspec(st)
    self.handicap = gethand(st)
    self.b1821 = 0
    self.sync = getsync(st)
    self.side = getside(st)
    self._28_ = 0
  def calc(self):
    bstr = "0%i%s%s%i%s0000%s%s0000" % (int(self.ready),dec2bin(self.teamno,4),dec2bin(self.allyno,4),int(self.mode),dec2bin(self.handicap,7),dec2bin(self.sync,2),dec2bin(self.side,4))
    print bstr+" = "+str(bin2dec(bstr))
    return str(bin2dec(bstr))
class Client:
  
  
  def __init__(self,ip,sock):
    #self.lastping = time.time()
    self.accountid = 0
    self.ip = ip
    self.lgstatus = 0 # 0 Just connected,1: Logged in
    self.username = ""
    self.afk = 0
    self.rank = 0
    self.bs = 0
    self.lastbsreset = time.time()
    self.battlestatus = "0"
    self.mod = 0
    self.country = ip2country.lookup(self.ip[0])
    self.bot = 0
    self.admin = 0
    self.sso = ssock(sock)
    self.ingame = 0
    self.ptime = 0
    self.teamcolor = "0"
    self.password = ""
    self.battlestatus = BattleStatus(0)
    self.inbuf = ""
    self.lastping = time.time()
    self.cpu = 0
    self.battle = 0
  def getstatus(self):
      self.rank = 0
      if self.ptime >= 300:
	self.rank = 1
      if self.ptime >= 900:
	self.rank = 2
      if self.ptime >= 1800:
	self.rank = 3
      if self.ptime >= 6000:
	self.rank = 4
      if self.ptime >= 20000:
	self.rank = 5
      if self.ptime >= 60000:
	self.rank = 6
      bstr= "%s%s%s%s%s" % (int(self.ingame),int(self.afk),dec2bin(self.rank,3),int(self.mod),int(self.bot))
      #print "GetStatus() = "+bstr+" = "+str(bin2dec(bstr))
      return bin2dec(bstr)
  def setbattlestatus(self,status):
      self.battlestatus.update(status)
  def getbattlestatus(self):
      return self.battlestatus.calc()
    
class Handler:
  commands = dict()
  clients = dict()
  clientsusernames = dict()
  main = 0
  id = 0
  #pendingclients = []
  accesstable = dict()
  def __init__(self,main,id):
    self.id = id
    self.clients = dict()
    
    self.main = main
    for f in os.listdir("cmds/"):
     # print f.split(".")
      if f.split(".")[2] == 'py':
	g = open("cmds/"+f,"r")
	self.commands.update([(f.split(".")[0].lower(),g.read())])
	self.accesstable.update([(f.split(".")[0].lower(),int(f.split(".")[1]))])
      
	g.close()
  def reloadcommands(self):
    self.commands = dict()
    self.accesstable = dict()
    for f in os.listdir("cmds/"):
     # print f.split(".")
      if f.split(".")[2] == 'py':
	g = open("cmds/"+f,"r")
	self.commands.update([(f.split(".")[0].lower(),g.read())])
	self.accesstable.update([(f.split(".")[0].lower(),int(f.split(".")[1]))])
    good("Handler %i: Commands reloaded succesful :)" % self.id)
  def remove(self,c,reason):
    
    try:
      
      if c in self.clients:
	if self.clients[c].lgstatus > 0:  
	  try:
	    for ch in list(self.main.channels):
	      if self.clients[c].username in self.main.channels[ch].users:
		self.main.broadcastchannel(ch,"LEFT %s %s %s\n" % (ch,self.clients[c].username,reason))
		self.main.channels[ch].users.remove(self.clients[c].username)
		if len(self.main.channels[ch].users) == 0:
		  del self.main.channels[ch]
	  except:
	    print '-'*60
	    traceback.print_exc(file=sys.stdout)
	    print '-'*60
	  for b in dict(self.main.battles):
	    try:
	      if b in self.main.battles and self.clients[c].username in self.main.battles[b].players:
		if b in self.main.battles and self.main.battles[b].founder == self.clients[c].username:
		  self.main.broadcast("BATTLECLOSED %i\n" % b)
		  if b in self.main.battles:
		    del self.main.battles[b]
		else:
		  self.main.battles[b].players.remove(self.clients[c].username)
		  self.main.broadcast("LEFTBATTLE %i %s\n" % (b,self.clients[c].username))
	    except:
	      pass
	  self.main.broadcast("REMOVEUSER %s\n" % self.clients[c].username)
	try:
	  c.close()
	except:
	  pass
	notice("Disconnected %s from handler %i , reason: %s" % (str(self.clients[c].ip),self.id,reason))
	if self.clients[c].lgstatus > 0:  
	  if self.clients[c].username in self.main.clientsusernames:
	    del self.main.clientsusernames[self.clients[c].username]
	  if self.clients[c].accountid in self.main.clientsaccid:
	    del self.main.clientsaccid[self.clients[c].accountid]
	if c in self.main.allclients:
	  del self.main.allclients[c]
	del self.clients[c]
    except:
      print '-'*60
      traceback.print_exc(file=sys.stdout)
      print '-'*60
  def ml(self):
    self.clients = dict()
    self.clientsusernames = dict()
    try:
      while 1:
	#time.sleep(0.02)
	iR,oR,eR = select.select(self.clients.keys(),self.clients.keys(),[],0.5)
	if len(iR) == 0:
	  time.sleep(0.5)
	chsafe = dict(self.main.channels)
	for ch in chsafe:
	  for muted in list(chsafe[ch].mutes):
	    if chsafe[ch].mutes[muted] < time.time():
	      try:
		del self.main.channels[ch].mutes[muted]
		self.main.broadcastchannel(ch,"CHANNELMESSAGE %s %s has been unmuted(mute expired)\n" % ( ch,muted))
	      except:
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60
	for co in iR:
	  cl = self.clients[co]
	  c = cl.sso
	  try:
	      while not cl.inbuf.endswith("\n"):
		d = co.recv(1024)
		if len(d) == 0:
		  break
		cl.inbuf += d
	  except socket.error:
		se = sys.exc_value[0]
		if not sys.exc_value[1] == "Resource temporarily unavailable":
		  self.remove(co,"Error %i: %s" % (int(se),str(sys.exc_value[1])))
	  except:
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60
	  cl.bs += len(cl.inbuf)
	  #print cl.lastbsreset+" "+time.time()
	
	  if time.time() - cl.lastbsreset > float(self.main.conf["floodlimitseconds"]) :
	    
	    if cl.bs > int(self.main.conf["floodlimitbw"])*float(self.main.conf["floodlimitseconds"]):
	      if co in self.clients:
		self.remove(self.clients[co],"Disconnected for flooding")
	    else:
	      cl.lastbsreset = time.time()
	  if cl.inbuf.endswith("\n"):
	    cmds = cl.inbuf.split("\n")
	    cl.inbuf = ""
	    for cm in cmds:
	      args = cm.strip("\r ").split(" ")
	      #print "Handler %i: " % (self.id) + str(args)
	      if len(args) > 0 and args[0].lower() in self.commands and args[0].lower() in self.accesstable and cl.lgstatus >= self.accesstable[args[0].lower()]:
		try:
		  exec self.commands[args[0].lower()]
		except:
		  error(args[0])
		  print '-'*60
		  traceback.print_exc(file=sys.stdout)
		  print '-'*60
	for co in dict(self.clients):
	  cl = self.clients[co]
	  c = cl.sso
	  
	  if time.time() - cl.lastping > 30.0:
	    self.remove(co,"Ping Timeout")
	  
	  for s in oR:
	    if s in self.clients:
	      try:
		for x in list(self.clients[s].sso.buf):
		  try:
		    z = x
		    self.clients[s].sso.buf.remove(x)
		    s.send(z)
		  except:
		    pass
		#s.send(self.clients[s].sso.buf)
		#self.clients[s].sso.buf = ""
	      #except socket.error:
		#se = sys.exc_value[0]
		#if not sys.exc_value[1] == "Resource temporarily unavailable":
		 # self.remove(co,"Error %i: %s" % (int(se),str(sys.exc_value[1])))
	      except:
		  pass
    except:
      print "---------------------FATAL ERROR-----------------------"
      print '-'*60
      traceback.print_exc(file=sys.stdout)
      print '-'*60
	
	  
	

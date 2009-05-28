# -*- coding: utf-8 -*-
import socket,string,thread,time
import sys,traceback,pdb,re,os
import base64,md5,commands,ip2country
import select,os
from utilities import *
from colors import *
class StartRect:
  def __init__(self,allyno,left,top,right,bottom):
    self.allyno = int(allyno)
    self.left = float(left)
    self.top = float(top)
    self.right = float(right)
    self.bottom = float(bottom)  
  def forgeaddstartrect(self):
    s = "ADDSTARTRECT %i %f %f %f %f\n" % (self.allyno,self.left,self.top,self.right,self.bottom)
    return s
class Bot:
  def __init__(self,owner,name,battlestatus,teamcolor,aidll=""):
    self.owner = owner
    self.name = name
    self.battlestatus = battlestatus
    self.teamcolor = teamcolor
    self.aidll = aidll
  def update(self,battlestatus,teamcolor):
    self.battlestatus = battlestatus
    self.teamcolor = teamcolor
  def forgeupdatebot(self,bid):
    s = "UPDATEBOT %i %s %s %s\n" % (int(bid),self.name,self.battlestatus,self.teamcolor)
    return s
  def forgeaddbot(self,bid):
    s = "ADDBOT %i %s %s %s %s %s\n" % (int(bid),self.name,self.owner,self.battlestatus,self.teamcolor,self.aidll)
    return s
class Battle:
  def __del__(self):
    debug("Battle %i destroyed" % self.id)
  def __init__(self,typ,nattype,password,port,maxplayers,hashcode,minrank,maphash,mapname,title,modname,founder,hostip,id):
    self.type = typ
    self.nattype = nattype
    self.password = password
    self.port = port
    self.scripttags = dict()
    self.speccount = 0
    self.startrects = dict()
    self.bots = dict()
    self.locked = 0
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
    self.disabledunits = []
    self.id = id
    if password == "*":
      self.passworded = 0
    else:
      self.passworded = 1
  def forgebattleopened(self):
    s = "BATTLEOPENED %i %s %s %s %s %s %s %s %s %s %s\n" % ( self.id,self.type,self.nattype,self.founder,self.hostip,self.port,self.maxplayers,self.passworded,self.minrank,self.maphash,'\t'.join([self.mapname,self.title,self.modname]))
    return s
  def forgeupdatebattleinfo(self):
    s = "UPDATEBATTLEINFO %i %i %i %s %s\n" % (self.id,self.speccount,self.locked,self.maphash,self.mapname)
    return s
class ssock:
  def __init__(self,sock,ist):
    self.buf = []
    self.ist = ist
    self.sck = sock
  def send(self,data):
    self.buf.append(data)
  def close(self):
    self.sck.close()
  def Flush(self,Final=False):
    if Final:
      try:
	for x in list(self.buf):
	  z = str(x)
	  self.sck.send(z)
	  if self.ist.main.debug:#and z.strip("\n") != "PING":
	    debug("%s Sent:%s" % (cl.username,z.replace("\n",red+"\\n"+blue).replace("\r",red+"\\r"+blue)))
	  self.buf.remove(x)
      except:
	pass
    else:
      try:
	for x in list(self.buf):
	  z = str(x)
	  self.sck.send(z)
	  if self.ist.main.debug:#and z.strip("\n") != "PING":
	    debug("%s Sent:%s" % (cl.username,z.replace("\n",red+"\\n"+blue).replace("\r",red+"\\r"+blue)))
	  self.buf.remove(x)
      except socket.error:
	se = sys.exc_value[0]
	if not sys.exc_value[1] == "Resource temporarily unavailable":
	  self.ist.remove(self.sck,"Write Error %i: %s" % (int(se),str(sys.exc_value[1])))
      except:
	print traceback.format_exc()
	self.ist.remove(self.sck,"Critical Error While flushing buffer, See stdout for details")
	
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
    print status
    for e in dir(self):
      exec("g = self.%s" % e)
      #debug( "self.%s = %s" % (e,str(g)))
  def calc(self):
    bstr = "0%i%s%s%i%s0000%s%s0000" % (int(self.ready),dec2bin(self.teamno,4),dec2bin(self.allyno,4),int(self.mode),dec2bin(self.handicap,7),dec2bin(self.sync,2),dec2bin(self.side,4))
    #print bstr+" = "+str(bin2dec(bstr))
    return str(bin2dec(bstr))
class Client:
  
  
  def __init__(self,ip,sock,ist):
    #self.lastping = time.time()
    self.accountid = 0
    self.supportedfeatures = [] 
    # FEATURES: CLIENTCHANNELSTATUS, ZIPSTREAM, 250PLAYERS
    #
    #
    #
    
    self.ip = ip
    self.sql = False
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
    self.ist = ist
    self.sso = ssock(sock,self.ist)
    self.ingame = 0
    self.ptime = 0
    self.teamcolor = "0"
    self.password = ""
    self.battlestatus = BattleStatus(0)
    self.inbuf = ""
    self.lastping = time.time()
    self.cpu = 0
    self.battle = -1
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
      if self.ptime >= 18000:
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
  def sync(self,db):
    if self.username == "":
      error("Sync() : Trying to sync a player with empty name!")
      return
    if not self.sql:
      error("Sync() : Player <%s> is not an sql user!" % self.username)
      return
    debug("Saving user <%s> in database..." % self.username)
    al = 1
    if self.mod == 1:
      al = 2
    if self.admin == 1:
      al = 3
    db.query("UPDATE users SET name = '%s', password = '%s', playtime = %i, accesslevel = %i, bot = %i, banned = %i, casename = '%s' WHERE id = %i" % (self.username.lower().replace("'","\\'"),self.password,self.ptime,al,self.bot,0,self.username.replace("'","\\'"),self.accountid),False)
    
    
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
    self.pollobj = select.poll()
    self.main = main
    for f in os.listdir("cmds/"):
      #print f.split(".")
      if len(f.split(".")) != 3:
	bad("Failed to load command %s" % f)
      
      elif f.split(".")[2] == 'py':
	g = open("cmds/"+f,"r")
	self.commands.update([(f.split(".")[0].lower(),g.read())])
	self.accesstable.update([(f.split(".")[0].lower(),int(f.split(".")[1]))])
	#debug("Loaded command %s" % f.split(".")[0].lower() )
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
	self.clients[c].sso.Flush(True)
	if self.clients[c].lgstatus > 0:  
	  try:
	    for ch in list(self.main.channels):
	      if self.clients[c].username in self.main.channels[ch].users:
		self.main.broadcastchannel(ch,"LEFT %s %s %s\n" % (ch,self.clients[c].username,reason))
		self.main.channels[ch].users.remove(self.clients[c].username)
		if len(self.main.channels[ch].users) == 0 and not self.main.channels[ch].confirmed:
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
	  if self.clients[c].username.lower() in self.main.clientsusernames:
	    del self.main.clientsusernames[self.clients[c].username.lower()]
	  if self.clients[c].accountid in self.main.clientsaccid:
	    del self.main.clientsaccid[self.clients[c].accountid]
	if c in self.main.allclients:
	  del self.main.allclients[c]
	try:
	  self.pollobj.unregister(c.fileno())
	except:
	  pass # it got destroyed by itself
	if self.clients[c].lgstatus > 0 and self.clients[c].sql:
	  try:
	    self.clients[c].sync(self.main.database)
	  except:
	    error("Cannot sync player <%s> to database" % self.clients[c].username)
	del self.clients[c]
    except:
      print '-'*60
      traceback.print_exc(file=sys.stdout)
      print '-'*60
  def processcommand(self,args,cl,co,c):
    pass
  def ml(self):
    self.clients = dict()
    self.clientsusernames = dict()
    
    try:
      while 1:
	#debug("Handler %i: %f" % (self.id,time.time()))
	#time.sleep(0.02)
	#iR,oR,eR = select.select(self.clients.keys(),self.clients.keys(),[],0.5)
	iR = []
	oR = list(self.clients.keys())
	pl = self.pollobj.poll(0.1)
	for fd in pl:
	  pollin = bool((fd[1] >> 0) & 1)
	  pollpri = bool((fd[1] >> 1) & 1)
	  pollout = bool((fd[1] >> 2) & 1)
	  pollerr = bool((fd[1] >> 3) & 1)
	  pollhup = bool((fd[1] >> 4) & 1)
	  pollnval = bool((fd[1] >> 5) & 1)
	  if pollin or pollpri:
	    #print " %s ready to receive data" % str(fd)
	    for s in list(self.clients.keys()):
	      if s.fileno() == fd[0]:
		newsocket = s
	    iR.append(newsocket)
	  if pollerr or pollhup or pollnval:
	    #print "Removing %s , socket error" % str(fd)
	    for s in list(self.clients.keys()):
		if fd[0] == s.fileno(): #TODO: Very slow , needs optimization
		  if pollhup:
		    self.remove(s,"Poll Error: Connection reset by peer")
		  elif pollnval:
		    self.remove(s,"Poll Error: Bad file descriptor")
		  elif pollerr:
		    self.remove(s,"Poll Error: Socket Exception")
	#print iR
	if len(iR) == 0:
	  time.sleep(0.5)
	chsafe = dict(self.main.channels)
	for ch in chsafe:
	  for muted in list(chsafe[ch].mutes):
	    if chsafe[ch].mutes[muted] > 0.0 and chsafe[ch].mutes[muted] < time.time():
	      try:
		del self.main.channels[ch].mutes[muted]
		if self.main.sql:
		  muted_ = self.main.getaccountbyid(muted)
		else:
		  muted_ = muted
		self.main.channels[ch].sync(self.main.database)
		#print "CHANNELMESSAGE %s %s has been unmuted(mute expired) " % (ch,muted_)
		self.main.broadcastchannel(ch,"CHANNELMESSAGE %s %s has been unmuted(mute expired)\n" % ( ch,muted_))
	      except:
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60
	for co in iR:
	  if co in self.clients:
	    cl = self.clients[co]
	    c = cl.sso
	    
	    try:
		while not cl.inbuf.endswith("\n"):
		  d = co.recv(1024)
		  if len(d) == 0:
		    self.remove(co,"Read Error: Connection reset by peer")
		    break
		  cl.inbuf += d
	    except socket.error:
		  se = sys.exc_value[0]
		  if not sys.exc_value[1] == "Resource temporarily unavailable":
		    self.remove(co,"Read Error %i: %s" % (int(se),str(sys.exc_value[1])))
	    except IOError:
		  self.remove(co,"IOError")
	    except:
		  se = sys.exc_value[0]
		  self.remove(co,str(se))

	    cl.bs += len(cl.inbuf)
	    if time.time() - cl.lastbsreset > float(self.main.conf["floodlimitseconds"]) :
	      cl.bs = 0
	      cl.lastbsreset = time.time()
	    #print "cl.bs > "+str(int(self.main.conf["floodlimitbw"])*float(self.main.conf["floodlimitseconds"]))+" = "+str(cl.bs > int(self.main.conf["floodlimitbw"])*float(self.main.conf["floodlimitseconds"]))
	    if cl.bs > int(self.main.conf["floodlimitbw"])*float(self.main.conf["floodlimitseconds"]):
	      self.remove(co,"Flood limit exceeded , Max flood is %i bytes/%fseconds, current flood was %i" % (int(self.main.conf["floodlimitbw"]),float(self.main.conf["floodlimitseconds"]),int(float(cl.bs)/float(self.main.conf["floodlimitseconds"]))))

		
	    if cl.inbuf.endswith("\n"):
	      cmds = cl.inbuf.split("\n")
	      cl.inbuf = ""
	      for cm in cmds:
		if self.main.debug and cm != "":
		  debug("%s Received:%s" % (cl.username,cm+red+"\n"+blue))
		args = cm.strip("\r ").split(" ")
		#print "Handler %i: " % (self.id) + str(args)
		if len(args) > 0 and args[0].lower() in self.commands and args[0].lower() in self.accesstable and cl.lgstatus >= self.accesstable[args[0].lower()]:
		  try:
		    if self.main.climit:
		      self.main.cmdlimit.oncommand(cl.username,self,co,args[0].upper())
		    exec self.commands[args[0].lower()].strip(" \t\n\r")
		  except:
		    error(args[0])
		    print '-'*60
		    tb = traceback.format_exc()
		    print tb
		    print '-'*60
		    self.main.broadcastadmins("SERVERMSG Broadcast to all admins - Command issued was '%s' by '%s'\n" % (args[0].upper(),cl.username))
		    self.main.broadcastadmins("SERVERMSG %s\n" % ("-"*60))
		    for l in tb.split("\n"):
		      self.main.broadcastadmins("SERVERMSG %s\n" % l)
		    self.main.broadcastadmins("SERVERMSG %s\n" % ("-"*60))  
	for co in dict(self.clients):
	  if co in self.clients:
	    cl = self.clients[co]
	    c = cl.sso
	    
	    if time.time() - cl.lastping > 30.0:
	      self.remove(co,"Ping Timeout")
	    
	    for s in oR:
	      if s in self.clients:
		  self.clients[s].sso.Flush()


		    
		  #s.send(self.clients[s].sso.buf)
		  #self.clients[s].sso.buf = ""
		#except socket.error:
		  #se = sys.exc_value[0]
		  #if not sys.exc_value[1] == "Resource temporarily unavailable":
		  # self.remove(co,"Error %i: %s" % (int(se),str(sys.exc_value[1])))
		
		    
    except:
      print "---------------------FATAL ERROR-----------------------"
      print '-'*60
      traceback.print_exc(file=sys.stdout)
      print '-'*60
	
	  
	

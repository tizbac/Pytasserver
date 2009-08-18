# -*- coding: utf-8 -*-
"""
Copyright (C) 2009  Tiziano Bacocco
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/
    """
  
import socket,string,thread,time,threading
import sys,traceback,pdb,re,os
import base64,md5,commands,ip2country
import select,os
from utilities import *
from colors import *
class CommandError(Exception):
  def __init__(self,value):
    self.value = value
  def __str__(self):
    return repr(self.value)
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
  def __init__(self,typ,nattype,password,port,maxplayers,hashcode,minrank,maphash,mapname,title,modname,founder,hostip,id,lanip):
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
    self.lanip = lanip
    self.founder = founder
    self.players.append(founder)
    self.disabledunits = []
    self.id = id
    if password == "*":
      self.passworded = 0
    else:
      self.passworded = 1
  def forgebattleopened(self,client=None):
    ip = ""
    if client and self.lanip != "*" and client.ip[0] == self.hostip:
      ip = self.lanip
    else:
      ip = self.hostip
	
    s = "BATTLEOPENED %i %s %s %s %s %s %s %s %s %s %s\n" % ( self.id,self.type,self.nattype,self.founder,ip,self.port,self.maxplayers,self.passworded,self.minrank,self.maphash,'\t'.join([self.mapname,self.title,self.modname]))
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
    self.ist.needflush = True
  def close(self):
    self.sck.close()
  def Flush(self,Final=False):
    i = 0
    bufsafe = list(self.buf)
    if str(self.sck).startswith("<__main__.compressedsocket"):
        self.sck.flush()
    if Final:
      try:
	for x in list(self.buf):
	  z = str(x)
	  self.sck.send(z)
	 # if self.ist.main.debug:#and z.strip("\n") != "PING":
	   # debug("%s Sent:%s" % (cl.username,z.replace("\n",red+"\\n"+blue).replace("\r",red+"\\r"+blue))) NOTE: Temporarily broken
	  self.buf.remove(x)
      except:
	pass
    else:
      try:
	for x in bufsafe:
	  z = str(x)
	  bytestosend = len(z)
          bytessent = self.sck.send(z)
	  if bytessent == bytestosend:
	    try:
	        self.buf.remove(x)
	    except:
	        pass
	  else:
	     #print "Sent incomplete data"
	    self.buf.remove(x)
	    self.buf.insert(0,z[bytessent:])
	    break
	  i += 1
	    #print "bytessent != len(z)"
	  #if self.ist.main.debug:#and z.strip("\n") != "PING":
	    #debug("%s Sent:%s" % (cl.username,z.replace("\n",red+"\\n"+blue).replace("\r",red+"\\r"+blue)))
	  
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
    #print status
    #for e in dir(self):
    #  exec("g = self.%s" % e)
      #debug( "self.%s = %s" % (e,str(g)))
  def calc(self):
    bstr = "0%i%s%s%i%s0000%s%s0000" % (int(self.ready),dec2bin(self.teamno,4),dec2bin(self.allyno,4),int(self.mode),dec2bin(self.handicap,7),dec2bin(self.sync,2),dec2bin(self.side,4))
    #print bstr+" = "+str(bin2dec(bstr))
    return str(bin2dec(bstr))
class Client:
  def checkaccess(self,flags):
    r = True
    x = "OK"
    i = 0
    s = dec2bin(flags,6)
    s2 = dec2bin(self.getaccessflags(),6)
    for b in s:
      if bool(int(b)):
	
	r = i < len(s2) and r and ( bool(int(s2[i])))
	if r == False:
	  x = "You haven't '%s' flag" % self.privtable[i]
	  break
      i += 1
    return [r,x]
  def getaccessflags(self):# b0 Logged in , b1 Bot , b2 Moderator , b3 Administator, b4 In battle, b5 Not in battle, b6 Battle founder
    al = 0
    al  = self.lgstatus*pow(2,0) + self.bot*pow(2,1) + self.mod*pow(2,2) + self.admin*pow(2,3)+ int(self.battle != -1)*pow(2,4)+ int(self.battle == -1)*pow(2,5)+int(self.battle != -1 and self.battle in self.ist.main.battles and self.ist.main.battles[self.battle].founder == self.username)*pow(2,6)
    return al
  def __init__(self,ip,sock,ist,mainist):
    #self.lastping = time.time()
    self.privtable = { 0 : "Logged in" , 1 : "Bot" , 2 : "Moderator", 3 : "Server administrator" , 4 : "In battle" , 5 : "Not in battle", 6 : "Battlefounder"}
    #		     { 1 : "Logged in" , 2 : "Bot" , 4 : "Moderator", 8 : "Server administrator" , 16 : "In battle" , 32 : "Not in battle" , 64 : "Battlefounder"}
    self.accountid = 0
    self.supportedfeatures = [] 
    # FEATURES: CLIENTCHANNELSTATUS, ZIPSTREAM, 250PLAYERS
    #
    #
    #
    self.lanip = "*"
    self.main = mainist
    self.loginlock = threading.Lock()
    self.loggingin = False
    self.ip = [ip[0],ip[1]]
    
    self.sql = False
    self.lgstatus = 0 # 0 Just connected,1: Logged in
    self.username = ""
    self.afk = 0
    self.rank = 0
    self.oldname = ""
    self.bs = 0
    self.lastlogin = 0.0
    self.lastbsreset = time.time()
    self.battlestatus = "0"
    self.mod = 0
    if ip[0] == "127.0.0.1" or ip[0].startswith("192.168.1"):
      self.ip[0] = self.main.externip
    self.country = ip2country.lookup(self.ip[0])
      
    self.bot = 0
    self.admin = 0
    self.ist = ist
    self.sso = ssock(sock,self.ist)
    self.ingame = 0
    self.ptimecounter = None
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
    db.query("UPDATE users SET name = '%s', password = '%s', playtime = %i, accesslevel = %i, bot = %i, banned = %i, casename = '%s', lastlogin = %i, lastip = '%s' WHERE id = %i" % (self.main.database.escape(self.username).lower(),self.password,self.ptime,al,self.bot,0,self.main.database.escape(self.username),int(self.lastlogin),self.ip[0],self.accountid),False)
    
    
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
    
    self.needflush = False
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
      if self.main.services and c in self.clients:
	self.main.services.onclientremoved(self.clients[c],reason)
    except:
      error("Failed to send the client removed event to services interface:%s" % str(sys.exc_value))
      
    try:
      
      if c in self.clients:
	self.clients[c].loginlock.acquire()
	self.clients[c].sso.Flush(True)
	if self.clients[c].lgstatus > 0:  
	  try:
	    for ch in list(self.main.channels):
	      if self.clients[c].oldname in self.main.channels[ch].users:
		self.main.broadcastchannel(ch,"LEFT %s %s %s\n" % (ch,self.clients[c].oldname,reason))
		self.main.channels[ch].users.remove(self.clients[c].oldname)
		if len(self.main.channels[ch].users) == 0 and not self.main.channels[ch].confirmed:
		  del self.main.channels[ch]
	  except:
	    print '-'*60
	    traceback.print_exc(file=sys.stdout)
	    print '-'*60
	  for b in dict(self.main.battles):
	    try:
	      if b in self.main.battles and self.clients[c].oldname in self.main.battles[b].players:
		
		if b in self.main.battles and self.main.battles[b].founder == self.clients[c].oldname:
		  self.main.broadcast("BATTLECLOSED %i\n" % b)
		  
		  if b in self.main.battles:
		    for p in self.main.battles[b].players:
		    	if p.lower() in self.main.clientsusernames:
		    		self.main.getuserist(p).battle = -1
		   
		    del self.main.battles[b]
		    
		else:
		  self.main.battles[b].players.remove(self.clients[c].oldname)
		  self.main.broadcast("LEFTBATTLE %i %s\n" % (b,self.clients[c].oldname))
	    except:
	      pass
	  self.main.broadcast("REMOVEUSER %s\n" % self.clients[c].oldname)
	
	notice("Disconnected %s from handler %i , reason: %s" % (str(self.clients[c].ip),self.id,reason))
	if self.clients[c].lgstatus > 0:
	  #print self.main.clientsusernames
	  if self.clients[c].oldname.lower() in self.main.clientsusernames:
	    del self.main.clientsusernames[self.clients[c].oldname.lower()]
	  #print self.main.clientsusernames
	  if self.clients[c].accountid in self.main.clientsaccid:
	    del self.main.clientsaccid[self.clients[c].accountid]
	if c in self.main.allclients:
	  del self.main.allclients[c]
	try:
	  self.pollobj.unregister(c.fileno())
	except:
	  pass
	try:
	  c.close()
	except:
	  pass
	if self.clients[c].lgstatus > 0 and self.clients[c].sql:
	  try:
	    self.clients[c].sync(self.main.database)
	  except:
	    error("Cannot sync player <%s> to database: %s" % (self.clients[c].username,traceback.format_exc()))
	self.clients[c].loginlock.release()
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
    lastexpirecheck = time.time()#It limits ban & mute expire checks so they gets checked every sec also with a lot of load
    try:
      while 1:
	#debug("Handler %i: %f %s" % (self.id,time.time(),str(self.needflush)))
	#time.sleep(0.02)
	#iR,oR,eR = select.select(self.clients.keys(),self.clients.keys(),[],0.5)
	iR = []
	oR = list(self.clients.keys())
	
	pl = self.pollobj.poll(1 if self.needflush else 700)
	#print pl
	for fd in pl:
	  pollin = bool((fd[1] >> 0) & 1)
	  pollpri = bool((fd[1] >> 1) & 1)
	  pollout = bool((fd[1] >> 2) & 1)
	  pollerr = bool((fd[1] >> 3) & 1)
	  pollhup = bool((fd[1] >> 4) & 1)
	  pollnval = bool((fd[1] >> 5) & 1)
	 # print pollin,pollpri,pollout,pollerr,pollhup,pollnval
	  if pollin or pollpri:
	    #print " %s ready to receive data" % str(fd)
	    for s in list(self.clients.keys()):
	      if s.fileno() == fd[0]:
		newsocket = s
	    iR.append(newsocket)
	  if pollerr or pollhup or pollnval:
	    print "Removing %s , socket error" % str(fd)
	    
	    for s in list(self.clients.keys()):
	      try:
		print "%i == %i = %s" % (fd[0],s.fileno(),str(fd[0] == s.fileno()))
		if fd[0] == s.fileno(): #TODO: Very slow , needs optimization
		  if pollhup:
		    self.remove(s,"Poll Error: Connection reset by peer")
		  elif pollnval:
		    self.remove(s,"Poll Error: Bad file descriptor")
		  elif pollerr:
		    self.remove(s,"Poll Error: Socket Exception")
	      except:
		pass
	    try:
	      self.pollobj.unregister(fd[0])
	    except:
	      pass
	#print iR
	#if not self.needflush:
	#  print "Sleep: ",self.needflush
	#  time.sleep(0.5)
	#debug("id = %i"%self.id)
	if self.id == 1 and time.time() - lastexpirecheck > 1.0:#Only run that on one handler
		#debug("Check mutes & bans expire")
		chsafe = dict(self.main.channels)
		for ch in chsafe:
		  for muted in list(chsafe[ch].mutes):
		    if chsafe[ch].mutes[muted] >= 0.0 and chsafe[ch].mutes[muted] < time.time():
		      try:
			del self.main.channels[ch].mutes[muted]
			if self.main.sql:
			  muted_ = self.main.getaccountbyid(muted)
			else:
			  muted_ = muted
			if not muted_:
			  muted_ = muted
			self.main.channels[ch].sync(self.main.database)
			#print "CHANNELMESSAGE %s %s has been unmuted(mute expired) " % (ch,muted_)
			self.main.broadcastchannel(ch,"CHANNELMESSAGE %s %s has been unmuted(Account mute expired)\n" % ( ch,muted_))
		      except:
			print '-'*60
			traceback.print_exc(file=sys.stdout)
			print '-'*60
		  for muted in list(chsafe[ch].ipmutes):
		    if chsafe[ch].ipmutes[muted] >= 0.0 and chsafe[ch].ipmutes[muted] < time.time():
		      try:
			del self.main.channels[ch].ipmutes[muted]
			mutedip = muted
			self.main.channels[ch].sync(self.main.database)
			#print "CHANNELMESSAGE %s %s has been unmuted(mute expired) " % (ch,muted_)
			self.main.broadcastchannel(ch,"CHANNELMESSAGE %s %s has been unmuted(IP-mute expired)\n" % ( ch,str(mutedip)))
		      except:
			print '-'*60
			traceback.print_exc(file=sys.stdout)
			print '-'*60
		  for banned in list(chsafe[ch].accountbans):
		    if chsafe[ch].accountbans[banned] >= 0.0 and chsafe[ch].accountbans[banned] < time.time():
		      try:
			del chsafe[ch].accountbans[banned]
			if self.main.sql:
			  banned_ = self.main.getaccountbyid(banned)
			else:
			  banned_ = banned
			if not muted_:
			  banned_ = banned
			self.main.channels[ch].sync(self.main.database)
			#print "CHANNELMESSAGE %s %s has been unmuted(mute expired) " % (ch,muted_)
			self.main.broadcastchannel(ch,"CHANNELMESSAGE %s %s has been unbanned from channel(Account ban expired)\n" % ( ch,banned_))
		      except:
			print '-'*60
			traceback.print_exc(file=sys.stdout)
			print '-'*60
		  for banned in list(chsafe[ch].ipbans):
		    if chsafe[ch].ipbans[banned] >= 0.0 and chsafe[ch].ipbans[banned] < time.time():
		      try:
			del chsafe[ch].ipbans[banned]
			self.main.channels[ch].sync(self.main.database)
			#print "CHANNELMESSAGE %s %s has been unmuted(mute expired) " % (ch,muted_)
			self.main.broadcastchannel(ch,"CHANNELMESSAGE %s %s has been unbanned from channel(IP ban expired)\n" % ( ch,str(banned)))
		      except:
			print '-'*60
			traceback.print_exc(file=sys.stdout)
			print '-'*60
		lastexpirecheck = time.time()
	for co in iR:
	  if co in self.clients:
	    cl = self.clients[co]
	    c = cl.sso
	    
	    try:
		while not cl.inbuf.endswith("\n"):
		  d = co.recv(1024)
		  if len(d) == 0:
		    self.remove(co,"Read Error 104: Connection reset by peer")
		    break
		  cl.inbuf += d
		  if len(cl.inbuf) > int(self.main.conf["maxrecvbuffersize"]):
		    break
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
	    if cl.admin != 1:
	      if cl.bot != 1:
		if time.time() - cl.lastbsreset > float(self.main.conf["floodlimitseconds"]) :
		  cl.bs = 0
		  cl.lastbsreset = time.time()
		#print "cl.bs > "+str(int(self.main.conf["floodlimitbw"])*float(self.main.conf["floodlimitseconds"]))+" = "+str(cl.bs > int(self.main.conf["floodlimitbw"])*float(self.main.conf["floodlimitseconds"]))
		if cl.bs > int(self.main.conf["floodlimitbw"])*float(self.main.conf["floodlimitseconds"]):
		  self.remove(co,"Flood limit exceeded , Max flood is %i bytes/ %f seconds, current flood was %i bytes/sec" % (int(self.main.conf["floodlimitbw"])*float(self.main.conf["floodlimitseconds"]),float(self.main.conf["floodlimitseconds"]),int(float(cl.bs)/float(self.main.conf["floodlimitseconds"]))))
	      else:
		if time.time() - cl.lastbsreset > float(self.main.conf["botfloodlimitseconds"]) :
		  cl.bs = 0
		  cl.lastbsreset = time.time()
		#print "cl.bs > "+str(int(self.main.conf["floodlimitbw"])*float(self.main.conf["floodlimitseconds"]))+" = "+str(cl.bs > int(self.main.conf["floodlimitbw"])*float(self.main.conf["floodlimitseconds"]))
		if cl.bs > int(self.main.conf["botfloodlimitbw"])*float(self.main.conf["botfloodlimitseconds"]):
		  self.remove(co,"BOT Flood limit exceeded , Max flood is %i bytes/%fseconds, current flood was %i bytes/sec" % (int(self.main.conf["botfloodlimitbw"])*float(self.main.conf["botfloodlimitseconds"]),float(self.main.conf["botfloodlimitseconds"]),int(float(cl.bs)/float(self.main.conf["botfloodlimitseconds"]))))

		
	    if cl.inbuf.endswith("\n"):
	      cmds = cl.inbuf.split("\n")
	      cl.inbuf = ""
	      for cm in cmds:
		if self.main.debug and cm != "":
		  debug("%s Received:%s" % (cl.username,cm+red+"\n"+blue))
		args = cm.strip("\r ").split(" ")
		#print "Handler %i: " % (self.id) + str(args)
		if len(args) > 0 and args[0].lower() in self.commands and args[0].lower() in self.accesstable:
		  access = cl.checkaccess(self.accesstable[args[0].lower()])
		  if access[0]:
		    try:
		      if self.main.climit and cl.admin == 0:
			self.main.cmdlimit.oncommand(cl.username,self,co,args[0].upper())
		      try:
			exec self.commands[args[0].lower()].strip(" \t\n\r")
		      except CommandError:
			c.send("SERVERMSG Command %s failed:%s\n"%(args[0],str(sys.exc_value)))
		    except:
		      error(args[0])
		      print '-'*60
		      tb = traceback.format_exc()
		      print tb
		      print '-'*60
		      self.main.broadcastadmins("SERVERMSG Broadcast to all admins - Command issued was '%s' by '%s', args: %s\n" % (args[0].upper(),cl.username,str(args[1:]) if len(args) > 1 else "no args"))
		      self.main.broadcastadmins("SERVERMSG %s\n" % ("-"*60))
		      for l in tb.split("\n"):
			self.main.broadcastadmins("SERVERMSG %s\n" % l)
		      self.main.broadcastadmins("SERVERMSG %s\n" % ("-"*60))
		  else:
		    c.send("SERVERMSG Not enough privileges to use '%s' : %s\n"%( args[0].upper(),access[1]))
		    
		    
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
		
	self.needflush = False	    
    except:
      print "---------------------FATAL ERROR-----------------------"
      print '-'*60
      traceback.print_exc(file=sys.stdout)
      print '-'*60
	
	  
	

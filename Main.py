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
import socket
import string
import thread
import signal
import time
import sys
import traceback
import pdb
import os
import pickle
import re
import select
from ClassDump import *
import base64
from cStringIO import StringIO
import md5
from Channel import *
import commands
from ParseConfig import *
from colors import *
from utilities import *
import _mysql as mysql
import Handler
import zlib
import urllib
from BanClient import *
import threading
from ServicesInterface import *
from CommandLimit import *
'''class Battle:
  def __init__(self,typ,nattype,password,port,maxplayers,hashcode,minrank,maphash,mapname,title,modname):
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
    self.players = []'''


class compressedsocket:
  def __init__(self,sock):
    self.sock = sock
    self.datatosend = ""
    self.co = zlib.compressobj(9)
    self.sock.send(self.co.flush(zlib.Z_SYNC_FLUSH))
    self.dc = zlib.decompressobj()
  def close(self):
    self.sock.close()
  def flush(self):
    self.send("")#Will cause flush
  def send(self,data):
    if len(self.datatosend) > 0 or len(data) > 0:
            self.co.compress(data)
            dts = self.datatosend + self.co.flush(zlib.Z_SYNC_FLUSH)
            bs = self.sock.send(dts)
            self.datatosend = ""
            if bs != len(dts):
                self.datatosend = dts[bs-1:]
    return len(data)
  def recv(self,sz):
    data = self.sock.recv(sz)
    #debug("Compressed: "+data.replace("\n",red+"\\n"+blue).replace("\r",red+"\\r"+blue))
    if data == "":
	return ""
    data = self.dc.decompress(data)
    debug("UNCompressed: "+data.replace("\n",red+"\\n"+blue).replace("\r",red+"\\r"+blue))
    if data == "":
	data = "\n"
    return data
  def fileno(self):
    return self.sock.fileno()

def listengzip(self):
  good("Listening for compressed connections on port %i" % (int(self.conf["listenportgzip"])))
  while 1:
      cs,ip = self.msGZ.accept()
      good("New gzipped connection from %s" %  str(ip))
      try:
	cs.setblocking(0)
	cs = compressedsocket(cs)
	cs.send("TASServer 0.35 0.79.0 8201 0\n")
	hln = dict()
	l = 900000
	for h in self.handlers:
	  hln.update([(len(h.clients.keys()),h)])
	for k in hln:
	  if k < l:
	    lh = hln[k]
	    l = k
	ist = Handler.Client(ip,cs,lh,self)
	lh.clients.update([(cs,ist)])
	lh.pollobj.register(cs.sock,select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR | select.POLLNVAL | select.POLLNVAL)
	self.allclients.update([(cs,ist)])
	#print "Handler %i: %s" % (lh.id,str(lh.clients))
	good("New connection accepted from %s on handler %i" % ( str(ip),lh.id))
	
      except:
	error(traceback.format_exc())

class sd: #Makes mysql module threadsafe
  def __init__(self,host,username,password,database,debug=False):
    self.uname = username
    self.pw = password
    self.debug = debug
    #self.Locked = False
    self.host = host
    self.db = database
    self.lasterror = False
    self.lock = threading.Lock()
    self.database = mysql.connect("localhost",self.uname,self.pw,self.db)
  def escape(self,s):
    return mysql.escape_string(s)
  def query(self,q,Lock=True):
    i = 0
    self.lock.acquire()
    try:
      if self.debug: debug("MYSQL Query: %s" % q)
      self.database.query(q)
      self.lasterror = False
    except:
      error("Critical mysql query error Query was \"%s\": " % q + traceback.format_exc())
      self.lasterror = True
    if not Lock:
    	self.lock.release()
    #except:
    #  self.database = mysql.connect("localhost",self.uname,self.pw,self.db)
    #  self.database.query(q)
  def store_result(self):
    try:
      if not self.lasterror:
	res = self.database.store_result()
      else:
	return None
      self.lock.release()
      return res
    except:
      self.lock.release()
      #self.database = mysql.connect("localhost",self.uname,self.pw,self.db)
  def ping(self):
    try:
      self.database.ping()
    except:
      self.database = mysql.connect("localhost",self.uname,self.pw,self.db)
      self.database.ping()
class Main:
  
  handlers = []
  channels = dict()
  battles = dict()
  cid = 0
  def __del__(self):
    debug("Main instance destroyed")
  def __init__(self,flags):
    self.externip = "127.0.0.1"
    self.signaldict = dict()
    for s in dir(signal):
      if s.startswith("SIG"):
	exec "self.signaldict[signal.%s] = \"%s\"" % ( s,s)
    #print self.signaldict
    self.clientsusernames = dict()
    self.clientsaccid = dict()
    self.allclients = dict()
    self.dynamicsettings = ["springversion","serverversion","natport"]
    self.battles = dict()
    self.starttime = time.time()
    self.ms = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.msGZ = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.debug = "d" in flags
    self.ipregex = re.compile("\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b")
  def ipmute(self,channame,src,username,secs):
    chan = self.channels[channame]
    targetclient = self.getuserist(username)
    chan.ipmutes.update([(targetclient.ip[0],time.time()+secs)])
    self.broadcastchannel(channame,"CHANNELMESSAGE %s <%s> has ip-muted <%s>\n"%(channame,src,username))
    chan.sync(selfmain.database)
  def accmute(self,channame,src,username,secs):
    chan = self.channels[channame]
    targetclient = self.getuserist(username)
    self.broadcastchannel(channame,"CHANNELMESSAGE %s <%s> has account-muted <%s>\n"%(channame,src,username))
    chan.mutes.update([(int(targetclient.accountid),time.time()+secs)])
    chan.sync(self.database)
  def updateexternipthread(self):
    while 1:
      try:
	  u = urllib.urlopen("http://tiztracker.altervista.org/ip.php")
	  ip = u.read()
	  u.close()
	  ip2 = ip.strip(" \r\n\t")
	  if self.ipregex.match(ip2):
	    self.externip = ip2
	  else:
	    error("Got invalid ip: "+ip2)
      except:
	  error("Failed to get ip")
      time.sleep(240.0)
      
    
  def syncallthread(self):
    if self.sql:
      while 1:
	notice("Saving all users logged in...")
	for h in self.handlers:
	  for cll in dict(h.clients):
	    cl = h.clients[cll]
	    cl.sync(self.database)
	good("Done saving logged in users")
	time.sleep(float(self.conf["syncallinterval"]))
	
  def connectionpingthread(self):
    while 1:
      try:
	#notice("Pinging mysql conection")
	self.database.ping()
	#notice("Ping done")
      except:
	pass
      time.sleep(30)
  def addchannel(self,name,fnd):
    self.channels.update([(name,Channel(fnd,name))])
  def settopic(self,channame,by,topic):
    self.channels[channame].topic = topic
    self.channels[channame].topicsetby =by
    self.channels[channame].topichangedtime = time.time()
    self.broadcastchannel(channame,"CHANNELTOPIC %s %s %i %s\n" % (channame,self.channels[channame].topicsetby,int(self.channels[channame].topichangedtime*1000),self.channels[channame].topic))
    if self.sql:
      self.channels[channame].sync(self.database)
  def reloadcommandtable(self):
    for h in self.handlers:
      h.reloadcommands()
  def broadcastEX(self,func,exc=None):
    for h in self.handlers:
      for c in dict(h.clients):
	try:
	  if c in h.clients and h.clients[c].lgstatus > 0 and c != exc:
	    try:
	      h.clients[c].sso.send(func(h.clients[c]))
	    except:
	      pass
	except:
	  pass
  def broadcast(self,cmd,exc=None):
    for h in self.handlers:
      for c in dict(h.clients):
	try:
	  if c in h.clients and h.clients[c].lgstatus > 0 and c != exc:
	    try:
	      h.clients[c].sso.send(cmd)
	    except:
	      pass
	except:
	  pass
  def broadcastadmins(self,cmd,exc=None):
    for h in self.handlers:
      for c in dict(h.clients):
	try:
	  if c in h.clients and h.clients[c].lgstatus > 0 and c != exc and h.clients[c].admin == 1:
	    try:
	      h.clients[c].sso.send(cmd)
	    except:
	      pass
	except:
	  pass
  def broadcastchannel(self,ch,cmd,exc=None):
    for h in self.handlers:
      for c in dict(h.clients):
	try:
	  if c in h.clients and h.clients[c].username in self.channels[ch].users and c != exc:
	    try:
	      h.clients[c].sso.send(cmd)
	    except:
	      pass
	except:
	  pass
  def broadcastbattle(self,bid,cmd,exc=None):
    for h in self.handlers:
      for c in dict(h.clients):
	try:
	  if c in h.clients and h.clients[c].username in self.battles[bid].players and c != exc:
	    try:
	      h.clients[c].sso.send(cmd)
	    except:
	      pass
	except:
	  pass
  def getuserist(self,username):
    ul = username.lower()
    for u in self.clientsusernames:
      if ul == u.lower():
	for h in self.handlers:
	  if self.clientsusernames[u].sck in h.clients:
	    ist = h.clients[self.clientsusernames[u].sck]
	    return ist
    return None
  def getaccountid(self,username):
    if self.sql:
      self.database.query("SELECT id,name FROM users WHERE name = '%s'" % username.replace("'","\\'").replace("\\","\\\\"))
      res = self.database.store_result()
      if res.num_rows() >= 1:
	r2 = res.fetch_row()[0]
	accid = int(r2[0])
      else:
	error("getaccountid(%s) : User doesn't exist in database" % username)
	return None
    else:
      error("getaccountid(%s) : MYSQL is not enabled" % username)
      return None
    return accid
  def writesettings(self):
    writeconfigfile("Server.conf",self.conf)
    good("Wrote current config to file")
  def loadaccountfromdatabase(self,username):
    if self.sql:
      notice("Loading <%s> account..." % username )
      self.database.query("SELECT id,name,password,playtime,accesslevel,bot,banned,casename,lastlogin,registrationdate,lastip FROM users WHERE name = '%s'" % self.database.escape(username))
      res = self.database.store_result()
      if res.num_rows() >= 1:
	r2 = res.fetch_row()[0]
	cl = Handler.Client("0.0.0.0",None,None)
	cl.accountid = int(r2[0])
	cl.name = r2[1]
	cl.password = r2[2]
	cl.ptime = int(r2[3])
	accesslevel = int(r2[4])
	if accesslevel >= 3:
	  cl.admin = 1
	if accesslevel > 1:
	  cl.mod = 1
	cl.bot = int(r2[5])
	cl.banned = int(r2[6])
	cl.username = r2[7]
	cl.lastlogin = int(r2[8])
	cl.registrationdate = int(r2[9])
	cl.ip = (r2[10],0)
	good("Account <%s> loaded succesful" % username)
	return cl
      else:
	bad("Account <%s> doesn't exist" % username)
	return None
    else:
      return None
  def getaccountbyid(self,id):
    accname = None
    if self.sql:
      self.database.query("SELECT id,casename FROM users WHERE id = '%s'" % self.database.escape(str(id)))
      res = self.database.store_result()
      if res.num_rows() >= 1:
	r2 = res.fetch_row()[0]
	accname = r2[1]
      else:
	error("getaccountbyid(%s) : User doesn't exist in database" % str(id))
    else:
      error("getaccountbyid(%s) : MYSQL is not enabled" %str(id))
    return accname
  def onsignal(self,sig,stk):
    notice("Shutting down on %s..."% str(self.signaldict[sig]))
    self.broadcast("SERVERMSGBOX Server received singnal %s, Exiting\n" % str(self.signaldict[sig]))
    if sig == signal.SIGSEGV:
      ans = raw_input(red+"************** WARNING: RECEIVED SIGSEGV, SYNCING USERS MAY CAUSE CORRUPTION, CONTINUE ( any other answer than 'yes' will mean NO) ? [yes/no] "+normal)
      if ans.lower().strip() != "yes":
	raise SystemExit(-2)
    for h in self.handlers:
      for c in h.clients:
	s = h.clients[c].sso.sck
	try:
	  for x in list(h.clients[c].sso.buf):
	    z = x
	    
	    s.send(z)
	    if self.main.debug:#and z.strip("\n") != "PING":
	      debug("%s Sent:%s" % (cl.username,z.replace("\n",red+"\\n"+blue).replace("\r",red+"\\r"+blue)))
	      
	    self.clients[s].sso.buf.remove(x)
	except:
	  pass
	if h.clients[c].sql:
	  try:
	    h.clients[c].sync(self.database)
	  except:
	    error("Cannot sync player <%s>" % h.clients[c].username)
	    error(traceback.format_exc())
    del self.database
    if sig == signal.SIGSEGV or sig == signal.SIGABRT:
	    self.dump()
    good("Server shutdown complete.")
    
    #self.exitcode = 1 #Server has been terminated / killed and must not restart
  def validateusername(self,uname):
    if len(uname) <= self.maxunamelen:
      if bool(self.unamer.match(uname)):
        if "bannednames" in self.conf:
           d = str2dict(self.conf["bannednames"])
        else:
           d = dict()
        if uname.lower() not in d:
          return (True,"OK")
        else:
          return (False,d[uname.lower()])
       
	
      else:
	return (False,"Username must match regex %s" % self.unamers)
    else:
      return (False,"Max username length is %i characters" % self.maxunamelen)
  def dump(self):
    filename = "ServerState.%s.dump"%(str(time.time()))
    notice("Dumping server state...")
    f = file(filename,"w")
    inst = Dumper()
    data = inst.dump("self",self)
    f.write(data)
    f.close()
    good("Server dump complete")
    return filename
  def run(self):
    signal.signal(signal.SIGINT,self.onsignal)
    signal.signal(signal.SIGTERM,self.onsignal)
    signal.signal(signal.SIGHUP,self.onsignal)
    signal.signal(signal.SIGSEGV,self.onsignal)
    signal.signal(signal.SIGABRT,self.onsignal)
    #signal.signal(signal.SIGFLT,self.onsignal)
    self.conf = readconfigfile("Server.conf")
    self.sql = False
    self.au = False
    
    thread.start_new_thread(self.updateexternipthread,())
    try:
	u = urllib.urlopen("http://tiztracker.altervista.org/ip.php")
	ip = u.read()
	u.close()
	ip2 = ip.strip(" \r\n\t")
	if self.ipregex.match(ip2):
	  self.externip = ip2
	  good("External IP: "+ip2)
	else:
	  error("Got invalid ip: "+ip2)
    except:
	error("Failed to get ip")
    if "servicesport" in self.conf:
      sport = int(self.conf["servicesport"])
      notice("Starting services interface on port %i" % sport)
      self.services = Services(sport,self)
    else:
      self.services = None
    self.unamers = "\A[a-zA-Z-0-9-\[-\]-_]+?\Z"
    self.unamer = re.compile("\A[a-zA-Z-0-9-\[-\]-_]+?\Z")
    self.climit = "commandlimit" in self.conf and self.conf["commandlimit"] == "1"
    self.bcl = "banlistserverenabled" in self.conf and self.conf["banlistserverenabled"] == "1"
    if "usernameregex" in self.conf:
    	try:
    		self.unamer = re.compile(self.conf["usernameregex"])
		self.unamers = self.conf["usernameregex"]
    	except:
		error("Username regex %s failed to compile, using \A[a-zA-Z-0-9]+?\Z !!!" % self.conf["usernameregex"])
		self.unamer = re.compile("\A[a-zA-Z-0-9]+?\Z")
    
    if self.bcl:
      self.banlistserv = BanClient(self.conf["banlistserverhost"],int(self.conf["banlistserverport"]))
    self.maxunamelen = 32
    if "maxusernamelen" in self.conf:
      if self.conf["maxusernamelen"].isdigit():
	self.maxunamelen = int(self.conf["maxusernamelen"])
    if self.climit:
      self.cmdlimit = CommandsLimitHandler(self)
    else:
      self.cmdlimit = None
    if self.conf["sql"] == "1":
      if bool(int(self.conf["allowunregisteredusers"])):
	notice("Users can login without registering!")
      self.au = bool(int(self.conf["allowunregisteredusers"]))
      self.sql = True
      notice("MYSQL Enabled!, Connecting to database...")
      self.database = sd("localhost",self.conf["mysqlusername"],self.conf["mysqlpassword"],self.conf["mysqldatabase"],self.debug)
      thread.start_new_thread(self.connectionpingthread,())
      good("Done")
      notice("Loading channels...")
      self.database.query("SELECT name,founder,operators,accountmutes,topic,password,id,ipmutes,accountbans,ipbans FROM channels")
      res = self.database.store_result()
      for i in range(res.num_rows()):
	
	r = res.fetch_row()[0]
	#print r
	"""self.getaccountid(r[1].lower())
	self.database.query("SELECT id,casename FROM users WHERE id = %i LIMIT 1" % int(r[1]))
	res2 = self.database.store_result()
	if res2.num_rows() > 0:
	  r3 = res2.fetch_row()[0]
	  #print r3
	  founder = r3[1]
	else:
	  error("FATAL: Channel \"%s\" founder does not exist, database damaged, exiting..." % r[0])
	  return"""
	
	name = r[0]
	if r[2] and len(r[2]) > 0:
	  operators = r[2].split(" ")
	else:
	  operators = []
	mutes = str2dict(r[3],int,float)
	topic = r[4]
	self.channels.update([(name,Channel(r[1],name,mutes,topic,operators,int(r[6]),r[5],str2dict(r[7],str,float),str2dict(r[8],int,float),str2dict(r[9],str,float)))])
	self.channels[r[0]].confirmed = True
	good("Added channel %s from database" % r[0])

    i = 0
    while i < int(self.conf["handlers"]):
      self.handlers.append(Handler.Handler(self,i+1))
      i += 1
    thread.start_new_thread(self.syncallthread,())
    for h in self.handlers:
      thread.start_new_thread(h.ml,())
      
    good("Started %i handlers" % len(self.handlers))
    
    self.ms.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR,self.ms.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1 )
    self.msGZ.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR,self.ms.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1 )
    self.ms.bind((self.conf["listenaddr"],int(self.conf["listenport"])))
    self.ms.listen(int(self.conf["listenqlen"]) if "listenqlen" in self.conf else 5)
    good("Listening for connections on port %i" % (int(self.conf["listenport"])))
    self.msGZ.bind((self.conf["listenaddr"],int(self.conf["listenportgzip"])))
    self.msGZ.listen(int(self.conf["listenqlen"]) if "listenqlen" in self.conf else 5)
    
    thread.start_new_thread(listengzip,(self,))
    try:
      while 1:
	cs,ip = self.ms.accept()
	good("New connection from %s" %  str(ip))
	rej = False
	if self.bcl:
	  if self.banlistserv.ipisbanned(ip[0]):
	    notice("IP %s rejected by ban list server, killing connection" % ip[0])
	    cs.setblocking(0)
	    try:
	      cs.close()
	    except:
	      pass
	    rej = True
	if not rej:
	  try:
	    cs.setblocking(0)
	    cs.send("TASServer %s %s %s 0\n" % (self.conf["serverversion"],self.conf["springversion"],self.conf["natport"]))
	    hln = dict()
	    l = 900000
	    for h in self.handlers:
	      hln.update([(len(h.clients.keys()),h)])
	    for k in hln:
	      if k < l:
		lh = hln[k]
		l = k
	    ist = Handler.Client(ip,cs,lh,self)
	    lh.clients.update([(cs,ist)])
	    lh.pollobj.register(cs,select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR | select.POLLNVAL )
	    self.allclients.update([(cs,ist)])
	    try:
	      if self.services:
		self.services.onclientcreated(ist)
	    except:
	      error("Failed to send the client created event to services interface:%s" % str(sys.exc_value))
	    #print "Handler %i: %s" % (lh.id,str(lh.clients))
	    good("New connection accepted from %s on handler %i" % ( str(ip),lh.id))
	    
	  except:
	    error(traceback.format_exc())
    except:
      error(traceback.format_exc())
      raise SystemExit(0)
if len(sys.argv) > 1: 
  ist = Main(sys.argv[1])
else:
  ist = Main("")

ret = ist.run()

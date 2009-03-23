import socket
import string
import thread
import time
import sys
import traceback
import pdb
import os
import re
import base64
import md5
import commands
from ParseConfig import *
from colors import *
import _mysql as mysql
import Handler
class Battle:
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
    self.players = []

class Channel:
  operators = []
  founder = ""
  topic = ""
  users = []
  topichangedtime = 0.0
  mutes = dict()
  topicsetby = "Nobody"
  def __init__(self,founder,name,mutes=dict(),topic="",operators=[],dbid=0):
    self.name = name

    self.dbid = dbid
    self.topicsetby = "Nobody"
    self.topichangedtime = 0.0
    self.founder = founder
    self.users = []
    self.confirmed = False
    self.mutes = mutes
    self.operators = operators
    if topic == "":
      self.topic = "*"
    else:
      self.topic = topic
  def sync(self,db):
    mutesstr = ""
    for m in self.mutes:
      mutesstr += "%s:%s " % (str(m),str(self.mutes[m]))
    ops = ' '.join(self.operators)
    db.query("SELECT id,casename FROM users WHERE casename = '%s' LIMIT 1" % self.founder)
    res = db.store_result()
    if res.num_rows() >= 1:
      r2 = res.fetch_row()[0]
    else:
      error("Founder of channel %s does not exist in database !!!!!!!!!!" % self.name)
      return
    db.query("UPDATE channels SET name = '%s',founder = '%s',mutes = '%s',operators = '%s', topic = '%s' WHERE id = %i" %
    (self.name.replace("'",""),str(r2[0]),mutesstr.replace("'",""),ops.replace("'",""),self.topic.replace("'","\\'").replace("\\n","\\\\n",self.dbid),False)
class sd:
  def __init__(self,host,username,password,database):
    self.uname = username
    self.pw = password
    self.Locked = False
    self.host = host
    self.db = database
    self.database = mysql.connect("localhost",self.uname,self.pw,self.db)
  def query(self,q,Lock=True):
    i = 0
    while self.Locked:
      i += 1
      time.sleep(0.01)
      if i >= 10000: break
    try:
      self.Locked = True
      print "Query: "+q
      self.database.query(q)
      if not Lock:
	self.Locked = False
    except:
      self.database = mysql.connect("localhost",self.uname,self.pw,self.db)
      self.database.query(q)
  def store_result(self):
    try:
      res = self.database.store_result()
      self.Locked = False
      return res
    except:
      self.Locked = False
      self.database = mysql.connect("localhost",self.uname,self.pw,self.db)
  def ping(self):
    try:
      self.database.ping()
    except:
      self.database = mysql.connect("localhost",self.uname,self.pw,self.db)
      self.database.ping()
class Main:
  ms = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  handlers = []
  channels = dict()
  battles = dict()
  cid = 0
  def __init__(self):
    self.clientsusernames = dict()
    self.clientsaccid = dict()
    self.allclients = dict()
  def connectionpingthread(self):
    while 1:
      try:
	notice("Pinging mysql conection")
	self.database.ping()
	notice("Ping done")
      except:
	pass
      time.sleep(30)
  def addchannel(self,name,fnd):
    self.channels.update([(name,Channel(fnd,name))])
  def reloadcommandtable(self):
    for h in self.handlers:
      h.reloadcommands()
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
  def run(self):
    self.conf = readconfigfile("Server.conf")
    self.sql = False
    if self.conf["sql"] == "1":
      self.sql = True
      notice("MYSQL Enabled!, Connecting to database...")
      self.database = sd("localhost",self.conf["mysqlusername"],self.conf["mysqlpassword"],self.conf["mysqldatabase"])
      thread.start_new_thread(self.connectionpingthread,())
      good("Done")
      notice("Loading channels...")
      self.database.query("SELECT name,founder,operators,mutes,topic,id FROM channels")
      res = self.database.store_result()
      for i in range(res.num_rows()):
	r = res.fetch_row()[0]
	self.database.query("SELECT id,casename FROM users WHERE id = %i LIMIT 1" % int(r[1]))
	res2 = self.database.store_result()
	if res2.num_rows() > 0:
	  r3 = res2.fetch_row()[0]
	  #print r3
	  founder = r3[1]
	else:
	  error("FATAL: Channel \"%s\" founder does not exist, database damaged, exiting..." % r[0])
	  return
	
	name = r[0]
	if r[2] and len(r[2]) > 0:
	  operators = r[2].split(" ")
	else:
	  operators = []
	mutes = dict()
	topic = r[4]
	if r[3] and len(r[3]) > 0:
	  for v in r[3].split(" "):
	    if v.count(":") > 0:
	      z = v.split(":")
	      mutes.update([(int(z[0]),float(z[1]))])
	self.channels.update([(name,Channel(founder,name,mutes,topic,operators,int(r[5])))])
	self.channels[r[0]].confirmed = True
	good("Added channel %s from database" % r[0])

    i = 0
    while i < int(self.conf["handlers"]):
      self.handlers.append(Handler.Handler(self,i+1))
      i += 1
    
    for h in self.handlers:
      thread.start_new_thread(h.ml,())
    good("Started %i handlers" % len(self.handlers))
    
    self.ms.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR,self.ms.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1 )
    self.ms.bind((self.conf["listenaddr"],int(self.conf["listenport"])))
    self.ms.listen(5)
    good("Listening for connections on port %i" % (int(self.conf["listenport"])))
    while 1:
      cs,ip = self.ms.accept()
      good("New connection from %s" %  str(ip))
      try:
	cs.setblocking(0)
	cs.send("TASServer 0.35 0.78.2 8201 0\n")
	hln = dict()
	l = 900000
	for h in self.handlers:
	  hln.update([(len(h.clients.keys()),h)])
	for k in hln:
	  if k < l:
	    lh = hln[k]
	    l = k
	ist = Handler.Client(ip,cs)
	lh.clients.update([(cs,ist)])
	self.allclients.update([(cs,ist)])
	#print "Handler %i: %s" % (lh.id,str(lh.clients))
	good("New connection accepted from %s on handler %i" % ( str(ip),lh.id))
	
      except:
	error(traceback.format_exc())
ist = Main()
ist.run()

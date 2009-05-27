# -*- coding: utf-8 -*-
import time
from ParseConfig import *
from colors import *
import thread
import string
"""class CommandLimit:
  def __init__(self,cmdname,n,secs,usermult=1.0):
    self.name = cmdname.upper()
    self.n = n
    self.secs = secs
    self.usermult = usermult"""
class CommandsLimitHandler:
  def __init__(self,mainist,configfile="CommandsLimit.cfg"):
    self.main = mainist
    self.f = readconfigfile(configfile)
    self.limits = dict()
    self.userlimits = dict() # { username : [[command,times,resettime,handler,client],...]
    for l in self.f:
      d = parselist(self.f[l],",") # maxn,secs,usermult(for example in channels),datamult
      self.limits.update([(l.upper(),[int(d[0]),float(d[1]),float(d[2]),float(d[3])])])
      debug("Command %s: Limit is %i times in %f seconds, usermult = %f, datamult = %f" % (l.upper(),int(d[0]),float(d[1]),float(d[2]),float(d[3])))
    thread.start_new_thread(self.limitthread,())
  def limitthread(self):
    good("Command antiflood thread started")
    while 1:
      time.sleep(0.05)
      for l in dict(self.userlimits):
	for ul in list(self.userlimits[l]):
	  if time.time() > ul[2]:
	    self.userlimits[l].remove(ul)
	  else:
	    if ul[1] > self.limits[ul[0]][0]:
	      ul[3].remove(ul[4],"%s command abuse: frequency is too high, max is %i times in %f seconds" % (ul[0],self.limits[ul[0]][0],self.limits[ul[0]][1]))
  def oncommand(self,user,handler,client,command):
    if command.upper() in self.limits:
      if user not in self.userlimits:
	self.userlimits.update([(user,[[command,1,time.time()+self.limits[command.upper()][1],handler,client]])])
      else:
	added = False
	for j in self.userlimits[user]:
	  if j[0] == command.upper():
	    j[1] += 1
	    added = True
	    break
	if not added:
	  self.userlimits[user].append([command,1,time.time()+self.limits[command.upper()][1],handler,client])
      #debug(str(self.userlimits))
	
      
	  
    
    
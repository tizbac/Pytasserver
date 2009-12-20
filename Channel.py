# -*- coding: utf-8 -*-
from utilities import *
from colors import *
#import _mysql as mysql
class Channel:
  operators = []
  founder = ""
  topic = ""
  users = []
  topichangedtime = 0.0
  mutes = dict()
  topicsetby = "Nobody"
  def __del__(self):
    debug("Channel %s unloaded from memory" % self.name)
  def __init__(self,founder,name,mutes=dict(),topic="",operators=[],dbid=0,key="*",ipmutes=dict(),accountbans=dict(),ipbans=dict()):
    self.name = name
    self.key = key
    self.dbid = dbid
    self.topicsetby = "Nobody"
    self.topichangedtime = 0.0
    self.founder = founder
    self.users = []
    self.confirmed = False
    self.mutes = mutes
    self.ipmutes = dict()
    self.operators = operators
    self.accountbans = accountbans
    self.ipbans = ipbans
    if topic == "":
      self.topic = "*"
    else:
      self.topic = topic
  def checkbanned(self,cl):
    if int(cl.accountid) in self.accountbans:
    	return (True,"Account banned on channel")
    if cl.ip[0] in self.ipbans:
    	return (True,"IP-Banned on channel")
    return (False,"OK")
  def checkmuted(self,cl):
    if int(cl.accountid) in self.mutes:
    	return (True,"Account muted on channel")
    if cl.ip[0] in self.ipmutes:
    	return (True,"IP-Muted on channel")
    return (False,"OK")
  def confirm(self,db):
    if not db:
      return
    db.query("SELECT name FROM channels WHERE name = '%s' LIMIT 1" % self.name.replace("'","\\'"))
    res = db.store_result()
    if res.num_rows() == 0:
      """mutesstr = ""
      for m in self.mutes:
	mutesstr += "%s:%s " % (str(m),str(self.mutes[m]))"""
      ops = ' '.join(self.operators)
      """db.query("SELECT id,casename FROM users WHERE casename = '%s' LIMIT 1" % self.founder)
      res = db.store_result()
      if res.num_rows() >= 1:
	r2 = res.fetch_row()[0]
      else:
	error("Founder of channel %s does not exist in database !!!!!!!!!!" % self.name)
	return"""
      db.query("INSERT INTO channels (name,founder,accountmutes,operators,topic,password,ipmutes,accountbans,ipbans) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %
      (mysql.escape_string(self.name),mysql.escape_string(str(self.founder)),mysql.escape_string(dict2str(self.mutes)),mysql.escape_string(ops),mysql.escape_string(self.topic),mysql.escape_string(self.key),mysql.escape_string(dict2str(self.ipmutes)),mysql.escape_string(dict2str(self.accountbans)),mysql.escape_string(dict2str(self.ipbans))),False)
      db.query("SELECT id,name FROM channels WHERE name = '%s' LIMIT 1" % db.escape(self.name))
      res = db.store_result()
      if res.num_rows() > 0:
	self.dbid = int(res.fetch_row()[0][0])
    self.confirmed = True
  def sync(self,db):
    if not db:
      return
    debug("Saving channel #%s in database" % self.name)
    mutesstr = ""
    for m in self.mutes:
      mutesstr += "%s:%s " % (str(m),str(self.mutes[m]))
    ops = ' '.join(self.operators)
    db.query("UPDATE channels SET name = '%s',founder = '%s',accountmutes = '%s',operators = '%s', topic = '%s', password = '%s', accountmutes= '%s', ipmutes='%s', accountbans='%s', ipbans='%s' WHERE id = %i" %
    (db.escape_string(self.name),str(self.founder),db.escape_string(mutesstr),db.escape_string(ops),db.escape_string(self.topic),db.escape_string(self.key),db.escape_string(dict2str(self.mutes)),db.escape_string(dict2str(self.ipmutes)),db.escape_string(dict2str(self.accountbans)),db.escape_string(dict2str(self.ipbans)),self.dbid),False)
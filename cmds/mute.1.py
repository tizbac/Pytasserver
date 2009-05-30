# -*- coding: utf-8 -*-
####MUTE channame username minutes mode
###Description
##Forbids an user from talking in a channel for some time, only channel operators, founder, or a moderator can use it
if len(args) >= 3:
  if len(args) >= 4:
    mutetime = float(args[3])*60.0
  else:
    mutetime = -1
  if self.main.sql:
    tid = self.main.getaccountid(args[2].lower())
    if not tid and not self.main.au:
      c.send("SERVERMSG MUTE Error: user <%s> does not exist in database\n")
    elif self.main.au and args[2].lower() in self.main.clientsusernames:
      for h in self.main.handlers:
	if self.main.clientsusernames[args[2].lower()] in h.clients:
	  tid = h.clients[self.main.clientsusernames[args[2].lower()]].accountid
    else:
      c.send("SERVERMSG MUTE Error: user <%s> does not exist\n")
      tid = None
    #print tid
    #print self.main.channels[args[1]].mutes
    if tid:
      if args[1] in self.main.channels:
	#print self.main.channels[args[1]].founder, cl.username
	if str(cl.accountid) in self.main.channels[args[1]].operators or cl.accountid == self.main.channels[args[1]].founder or cl.mod == 1:
	  self.main.broadcastchannel(args[1],"CHANNELMESSAGE %s <%s> has muted <%s> for %f seconds\n" % ( args[1] , cl.username , args[2],mutetime))
	  self.main.channels[args[1]].mutes.update([(tid,time.time()+mutetime)])
	  if bool(self.main.channels[args[1]].confirmed):
	    self.main.channels[args[1]].sync(self.main.database)	
      else:
	c.send("SERVERMSG MUTE Error: channel #%s does not exist\n")
  else:
      self.main.channels[args[1]].mutes.update([(args[2],time.time()+mutetime)])

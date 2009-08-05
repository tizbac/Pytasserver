# -*- coding: utf-8 -*-

if len(args) >= 3:
  if self.main.sql and args[2].lower() in self.main.clientsusernames:
    tsck = self.main.clientsusernames[args[2].lower()].sck
    for h in self.main.handlers:
      if tsck in h.clients:
	tid = h.clients[tsck].accountid
    #print tid
    #print self.main.channels[args[1]].mutes
    if args[1] in self.main.channels:
      if (str(cl.accountid) in self.main.channels[args[1]].operators or cl.accountid == int(self.main.channels[args[1]].founder) or cl.mod == 1) and tid in self.main.channels[args[1]].mutes:
	self.main.broadcastchannel(args[1],"CHANNELMESSAGE %s <%s> has account-unmuted <%s>\n" % ( args[1] , cl.username , args[2]))
	del self.main.channels[args[1]].mutes[tid]
	self.main.channels[args[1]].sync(self.main.database)
  else:
      del self.main.channels[args[1]].mutes[args[2]]
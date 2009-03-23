print args
if len(args) >= 3:
  if len(args) >= 4:
    mutetime = float(args[3])*60.0
  else:
    mutetime = -1
  if self.main.sql and args[2] in self.main.clientsusernames:
    tsck = self.main.clientsusernames[args[2]].sck
    for h in self.main.handlers:
      if tsck in h.clients:
	tid = h.clients[tsck].accountid
    #print tid
    #print self.main.channels[args[1]].mutes
    if args[1] in self.main.channels:
      if str(cl.accountid) in self.main.channels[args[1]].operators or cl.username == self.main.channels[args[1]].founder or cl.mod == 1:
	self.main.broadcastchannel(args[1],"CHANNELMESSAGE %s <%s> has muted <%s>\n" % ( args[1] , cl.username , args[2]))
	self.main.channels[args[1]].mutes.update([(tid,time.time()+mutetime)])
	self.main.channels[args[1]].sync(self.main.database)
  else:
      self.main.channels[args[1]].mutes.update([(args[2],time.time()+mutetime)])
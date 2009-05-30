# -*- coding: utf-8 -*-
####JOIN channame [key]
###Description
##Sent by client trying to join a channel.

##key: If channel is locked, then client must supply a correct key to join the channel (clients with access >= Account.ADMIN_ACCESS can join locked channels withouth supplying the key - needed for ChanServ bot).

###Examples
##JOIN main
##JOIN myprivatechannel mypassword
if len(args) >= 2 and args[1] in self.main.channels:
  if not cl.username in self.main.channels[args[1]].users:
    self.main.channels[args[1]].users.append(cl.username)
    c.send("JOIN %s\n" % args[1])
    #print self.main.channels[args[1]].users
    c.send("CLIENTS %s %s\n" % ( args[1], ' '.join(self.main.channels[args[1]].users)))
    if "CLIENTCHANNELSTATUS" in cl.supportedfeatures:
      for u in list(self.main.channels[args[1]].users):
	cli = self.main.allclients[self.main.clientsusernames[cl.username.lower()].sck]
	bstr = "%i%i%i" % (int(int(cli.accountid) in self.main.channels[args[1]].operators),int(int(cli.accountid) in self.main.channels[args[1]].mutes),int(cli.username == self.main.channels[args[1]].founder))
	c.send("CLIENTCHANNELSTATUS %s %s %i\n" % (args[1],cli.username,bin2dec(bstr)))   #CLIENTCHANNELSTATUS channel user status
    self.main.broadcastchannel(args[1],"JOINED %s %s\n" % (args[1],cl.username),co)
    c.send("CHANNELTOPIC %s %s %f %s\n" % (args[1],self.main.channels[args[1]].topicsetby,self.main.channels[args[1]].topichangedtime,self.main.channels[args[1]].topic))
  else:
    c.send("SERVERMSG *** Error: cannot join #%s, already in the channel\n" % args[1])
  
    #bad("%s tried to join more times %s" % (cl.username,args[1]))
  
else:
  self.main.addchannel(args[1],cl.accountid)
  notice("Created new channel #%s with founder <%s>" % (args[1],cl.username))
  c.send("JOIN %s\n" % args[1])
  self.main.channels[args[1]].users.append(cl.username)
  c.send("CLIENTS %s %s\n" % ( args[1], ' '.join(self.main.channels[args[1]].users)))
  c.send("CHANNELTOPIC %s %s %f %s\n" % (args[1],self.main.channels[args[1]].topicsetby,self.main.channels[args[1]].topichangedtime,self.main.channels[args[1]].topic))#self.main.broadcastchannel(args[1],"JOINED %s %s\n" % (args[1],cl.username),c)

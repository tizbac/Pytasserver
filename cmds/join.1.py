if args[1] in self.main.channels:
  if not cl.username in self.main.channels[args[1]].users:
    self.main.channels[args[1]].users.append(cl.username)
    c.send("JOIN %s\n" % args[1])
    #print self.main.channels[args[1]].users
    c.send("CLIENTS %s %s\n" % ( args[1], ' '.join(self.main.channels[args[1]].users)))
    self.main.broadcastchannel(args[1],"JOINED %s %s\n" % (args[1],cl.username),co)
    c.send("CHANNELTOPIC %s %s %f %s\n" % (args[1],self.main.channels[args[1]].topicsetby,self.main.channels[args[1]].topichangedtime,self.main.channels[args[1]].topic))
  else:
    c.send("SERVERMSG *** Error: cannot join #%s, already in the channel\n" % args[1])
  
    #bad("%s tried to join more times %s" % (cl.username,args[1]))
  
else:
  self.main.addchannel(args[1],cl.username)
  notice("Created new channel #%s with founder <%s>" % (args[1],cl.username))
  c.send("JOIN %s\n" % args[1])
  self.main.channels[args[1]].users.append(cl.username)
  c.send("CLIENTS %s %s\n" % ( args[1], ' '.join(self.main.channels[args[1]].users)))
  c.send("CHANNELTOPIC %s %s %f %s\n" % (args[1],self.main.channels[args[1]].topicsetby,self.main.channels[args[1]].topichangedtime,self.main.channels[args[1]].topic))#self.main.broadcastchannel(args[1],"JOINED %s %s\n" % (args[1],cl.username),c)

if len(args) == 2:
  if args[1] not in self.main.channels:
    c.send("SERVERMSG %s\n" % "This channel does not exist")
  elif cl.mod != 1:
    c.send("SERVERMSG %s\n" % "Not enough  access level to register this channel")  #cl.username != self.main.channels[args[1]].founder --- should i enable registering channel to anyone? 
  else:
    self.main.channels[args[1]].confirm(self.main.database)
    self.main.broadcastchannel(args[1],"CHANNELMESSAGE %s %s\n" % (args[1],"This channel has just been saved to database")
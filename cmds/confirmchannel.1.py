if len(args) == 2:
  if args[1] in self.main.channels:
    if cl.username == self.main.channels[args[1]].founder:
      self.main.broadcastchannel(args[1],"CHANNELMESSAGE %s Channel permanently registered to %s\n" % (args[1],cl.username))
      self.main.channels[args[1]].confirmed = True
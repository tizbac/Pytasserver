if self.main.sql:
  if len(args) >= 3 and args[1] in self.main.channels and cl.username in self.main.channels[args[1]].users and not cl.accountid in self.main.channels[args[1]].mutes:
    self.main.broadcastchannel(args[1],"SAID %s %s %s\n" % (args[1],cl.username,' '.join(args[2:])))
else:
  if len(args) >= 3 and args[1] in self.main.channels and cl.username in self.main.channels[args[1]].users and not cl.username in self.main.channels[args[1]].mutes:
    self.main.broadcastchannel(args[1],"SAID %s %s %s\n" % (args[1],cl.username,' '.join(args[2:])))
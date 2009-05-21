# -*- coding: utf-8 -*-
if len(args) == 2:
  if args[1] in self.main.channels:
    if cl.accountid == self.main.channels[args[1]].founder or cl.mod == 1:
      self.main.broadcastchannel(args[1],"CHANNELMESSAGE %s Channel permanently registered to %s\n" % (args[1],cl.username))
      self.main.channels[args[1]].confirmed = True
      self.main.channels[args[1]].confirm(self.main.database)
      self.main.channels[args[1]].sync(self.main.database)
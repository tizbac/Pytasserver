# -*- coding: utf-8 -*-
####SETCHANNELKEY channel key
##Sets the channel key, can be only used by a moderator or the channel founder, to disable it , set it to *
if len(args) >= 3 and args[1] in self.main.channels:
  if cl.accountid == self.main.channels[args[1]].founder or cl.mod == 1:
    self.main.channels[args[1]].key = args[2]
    if self.main.sql:
      self.main.channels[args[1]].sync(self.main.database)
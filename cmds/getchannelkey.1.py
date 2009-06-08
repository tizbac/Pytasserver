# -*- coding: utf-8 -*-
####GETCHANNELKEY channel
##Retrieves the channel key, can be only used by a moderator or the channel founder
if len(args) >= 2 and args[1] in self.main.channels:
  if cl.accountid == self.main.channels[args[1]].founder or cl.mod == 1:
    c.send("SERVERMSG Channel #%s key is %s\n" %(args[1],self.main.channels[args[1]].key ))
  else:
    c.send("SERVERMSG Not enough privileges\n")
    
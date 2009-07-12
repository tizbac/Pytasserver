# -*- coding: utf-8 -*-
if cl.mod == 1:
  if len(args) == 2:
    if args[1].lower() in self.main.clientsusernames:
      c.send("SERVERMSG %s's ip is %s\n"  % (args[1],self.main.allclients[self.main.clientsusernames[args[1].lower()].sck].ip[0]))
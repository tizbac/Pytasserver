# -*- coding: utf-8 -*-
if cl.admin == 1:
  if len(args) == 2:
    if args[1].lower() in self.main.clientsusernames:
      target = self.main.clientsusernames[args[1]].sck
      for h in self.main.handlers:
	if target in h.clients:
	  h.remove(target,"Quit")
	  break
    else:
      c.send("SERVERMSG No player with name \"%s\" is currently logged on\n" % args[1])
  else:
    c.send("SERVERMSG Wrong number of arguments\n")
else:
  c.send("SERVERMSG Not enough rights to use that command\n")
  #c.send("SERVERMSG 0wned\n")
  #self.remove(co,"Quit")
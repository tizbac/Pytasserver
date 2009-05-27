# -*- coding: utf-8 -*-
if len(args) == 2 and cl.admin == 1:
  uist = self.main.getuserist(args[1])
  if uist:
    if uist.sql:
      uist.mod = 1
      uist.admin = 1
      self.main.broadcast("CLIENTSTATUS %s %i\n" % (uist.username,uist.getstatus()))
      uist.sync(self.main.database)
    else:
      uist.mod = 1
      uist.admin = 1
      self.main.broadcast("CLIENTSTATUS %s %i\n" % (uist.username,uist.getstatus()))
  else:
    c.send("SERVERMSG Error: Clients needs to be logged in actually\n")
if cl.admin == 0:
  c.send("SERVERMSG Error: Needs admin privilege\n")
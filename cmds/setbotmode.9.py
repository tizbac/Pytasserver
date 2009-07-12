# -*- coding: utf-8 -*-
####SETBOTMODE username 0-1
###Description
##Sets or unsets the bot flag on the account, only admins can use that command
if len(args) == 3 and cl.admin == 1:
  uist = self.main.getuserist(args[1])
  if uist:
    if uist.sql:
      uist.bot = min(1,int(args[2]))
      self.main.broadcast("CLIENTSTATUS %s %i\n" % (uist.username,uist.getstatus()))
      uist.sync(self.main.database)
    else:
      uist.bot = min(1,int(args[2]))
      self.main.broadcast("CLIENTSTATUS %s %i\n" % (uist.username,uist.getstatus()))
  else:
    c.send("SERVERMSG Error: Clients needs to be logged in actually\n")
if cl.admin == 0:
  c.send("SERVERMSG Error: Needs admin privilege\n")

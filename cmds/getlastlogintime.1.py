# -*- coding: utf-8 -*-
if cl.mod == 1:
  if len(args) == 2:
    fromsql = False
    if not args[1].lower() in self.main.clientsusernames:
      acc = self.main.loadaccountfromdatabase(args[1].lower())
      fromsql = True
      c.send("SERVERMSG Loading <%s> account from database...\n" % args[1])
    else:
      c.send("SERVERMSG Retrieving account info from memory...\n")
      acc = self.main.allclients[self.main.clientsusernames[args[1].lower()].sck]
      fromsql = False
    if not acc:
      c.send("SERVERMSG Error: Cannot load <%s> account\n" % args[1])
    else:
      c.send("SERVERMSG %s's last login was on %s\n" % (args[1],time.ctime(acc.lastlogin)))
      if fromsql:
	del acc
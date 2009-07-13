# -*- coding: utf-8 -*-

if len(args) == 3:
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
      acc.username = args[2]
      acc.sync(self.main.database)
      if not fromsql:
	c.send("SERVERMSG Disconnecting client\n")
	acc.sso.send("SERVERMSG Your account has been renamed by %s to %s, you will now get disconnected\n" % (cl.username,acc.username))
	for h in self.main.handlers:
	  if acc.sso.sck in h.clients:
	    h.remove(acc.sso.sck,"Renamed by <%s> to '%s'" % (cl.username,acc.username))
	#self.remove(acc.sso.sck,"Renamed by <%s> to '%s'" % (cl.username,acc.username))
	c.send("SERVERMSG Done.\n")
	
	

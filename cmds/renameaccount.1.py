# -*- coding: utf-8 -*-
if self.main.sql and cl.sql:
  if len(args) == 2:
    if not self.main.getaccountid(args[1].lower()):
      if not args[1].lower() in self.main.clientsusernames:
	cl.username = args[1]
	c.send("SERVERMSG Account name changed succesfully\n")
	cl.sync(self.main.database)
	self.remove(co,"Renaming account")
      else:
	c.send("SERVERMSG Error, an user with that name is already logged in\n")
    else:
      c.send("SERVERMSG Error, an user with that name already exists\n")
else:
  c.send("SERVERMSG Error: Cannot change name while in LAN mode\n")
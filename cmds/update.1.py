if cl.admin == 1:
  s,t = commands.getstatusoutput("git-pull")
  if s != 0:
	c.send("SERVERMSG git-pull failed\n")
	for l in t.split("\n"):
		c.send("SERVERMSG %s\n" % l)
  else:
	for l in t.split("\n"):
		c.send("SERVERMSG %s\n" % l)

	self.main.reloadcommandtable()
	c.send("SERVERMSG Commands reloaded\n")
  

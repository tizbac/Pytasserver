if len(args) == 2:
  if int(args[1]) in self.main.battles and self.main.battles[int(args[1])].passworded == 0:
    self.main.battles[int(args[1])].players.append(cl.username)
    self.main.broadcast("JOINEDBATTLE %i %s\n" % (self.main.battles[int(args[1])].id,cl.username))
    c.send("JOINBATTLE %i %s" % (self.main.battles[int(args[1])].id,self.main.battles[int(args[1])].hashcode))
    cl.battle = self.main.battles[int(args[1])].id
    
    c.send("REQUESTBATTLESTATUS\n")
    
    for b in dict(self.main.battles):
      try:
	for bot in list(self.main.battles[b].bots):
	  c.send(bot.forgeaddbot(int(b)))
	for rect in dict(self.main.battles[b].startrects):
	  r = self.main.battles[b].startrects[rect]
	  c.send(r.forgeaddstartrect())
	sts = ""
	stl = []
	for tag in self.main.battles[b].scripttags:
	  stl.append(tag+"="+self.main.battles[b].scripttags[tag])
	sts = '\t'.join(stl)
	c.send("SETSCRIPTTAGS %s\n" % sts)
	for p in self.main.battles[b].players:
	  try:
	    GT = self.clients[self.clientsusernames[p]]
	    c.send("CLIENTBATTLESTATUS %s %s\n" % (GT.getbattlestatus(),GT.teamcolor))
	  except:
	    pass
      except:
	pass
	    
  elif int(args[1]) in self.main.battles and self.main.battles[int(args[1])].passworded == 1 and len(args) == 3 and self.main.battles[int(args[1])].password == args[2]:
    self.main.battles[int(args[1])].players.append(cl.username)
    self.main.broadcast("JOINEDBATTLE %i %s\n" % (self.main.battles[int(args[1])].id,cl.username))
    c.send("JOINBATTLE %i %s" % (self.main.battles[int(args[1])].id,self.main.battles[int(args[1])].hashcode))
    cl.battle = self.main.battles[int(args[1])].id
    for b in dict(self.main.battles):
      try:
	for p in self.main.battles[b].players:
	  try:
	    GT = self.clients[self.clientsusernames[p]]
	    c.send("CLIENTBATTLESTATUS %s %s\n" % (GT.getbattlestatus(),GT.teamcolor))
	  except:
	    pass
      except:
	pass
    c.send("REQUESTBATTLESTATUS\n")
  elif int(args[1]) in self.main.battles and self.main.battles[int(args[1])].passworded == 1 and len(args) == 3 and self.main.battles[int(args[1])].password != args[2]:
    c.send("SERVERMSG *** Error: cannot join the battle, invalid password!\n" % args[1])
  else:
    c.send("SERVERMSG *** Error: cannot join the battle, battle does not exist!\n" % args[1])
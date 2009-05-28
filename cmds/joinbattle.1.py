# -*- coding: utf-8 -*-
if len(args) == 2:
  if cl.battle == -1:
    if int(args[1]) in self.main.battles and self.main.battles[int(args[1])].locked == 0:
      if int(args[1]) in self.main.battles and self.main.battles[int(args[1])].passworded == 0:
	self.main.battles[int(args[1])].players.append(cl.username)
	self.main.broadcast("JOINEDBATTLE %i %s\n" % (self.main.battles[int(args[1])].id,cl.username))
	c.send("JOINBATTLE %i %s\n" % (self.main.battles[int(args[1])].id,self.main.battles[int(args[1])].hashcode))
	cl.battle = self.main.battles[int(args[1])].id
	
	
	
	b = int(args[1])
	try:
	  for p in self.main.battles[b].players:
	    if p != cl.username:
	      try:
		GT = self.main.allclients[self.main.clientsusernames[p.lower()].sck]
		c.send("CLIENTBATTLESTATUS %s %s %s\n" % (p,GT.getbattlestatus(),GT.teamcolor))
	      except:
		if self.main.debug:
		  debug("Error sending CLIENTBATTLESTATUS: \n"+yellow+traceback.format_exc()+blue+"\n")
	  c.send("REQUESTBATTLESTATUS\n")
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
	  debug("SENT BATTLEINFO")
	except:
	  debug("JOINBATTLE Error"+red+" "+traceback.format_exc())
		
      elif int(args[1]) in self.main.battles and self.main.battles[int(args[1])].passworded == 1 and len(args) >= 3 and self.main.battles[int(args[1])].password == ' '.join(args[2:]):
	self.main.battles[int(args[1])].players.append(cl.username)
	self.main.broadcast("JOINEDBATTLE %i %s\n" % (self.main.battles[int(args[1])].id,cl.username))
	c.send("JOINBATTLE %i %s\n" % (self.main.battles[int(args[1])].id,self.main.battles[int(args[1])].hashcode))
	cl.battle = self.main.battles[int(args[1])].id
	for b in dict(self.main.battles):
	  try:
	    for p in self.main.battles[b].players:
	      try:
		GT = self.clients[self.clientsusernames[p.lower()]]
		c.send("CLIENTBATTLESTATUS %s %s\n" % (GT.getbattlestatus(),GT.teamcolor))
	      except:
		pass
	  except:
	    pass
	c.send("REQUESTBATTLESTATUS\n")
      elif int(args[1]) in self.main.battles and self.main.battles[int(args[1])].passworded == 1 and len(args) == 3 and self.main.battles[int(args[1])].password != args[2]:
	c.send("JOINBATTLEFAILED Error: cannot join the battle, invalid password!\n" )
      else:
	c.send("JOINBATTLEFAILED Error: cannot join the battle, battle does not exist!\n")
    else:
      c.send("JOINBATTLEFAILED Error: cannot join the battle, battle is locked\n")
  else:
    c.send("JOINBATTLEFAILED Error: cannot join the battle,you are already in another one\n" )
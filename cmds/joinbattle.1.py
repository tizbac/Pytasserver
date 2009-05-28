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
	  botsaf = dict(self.main.battles[b].bots)
	  uts = []
	  for u in self.main.battles[b].disabledunits:
	    uts.append(u)
	    if len(uts) >= 30:
	      c.send("DISABLEUNITS %s\n" % (' '.join(uts)))
	  if len(uts) > 0:
	    c.send("DISABLEUNITS %s\n" % (' '.join(uts)))
	  uts = []
	  for bot_ in botsaf:
	    bot = botsaf[bot_]
	    c.send(bot.forgeaddbot(int(b)))
	  del botsaf
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
	  botsaf = dict(self.main.battles[b].bots)
	  for bot_ in botsaf:
	    bot = botsaf[bot_]
	    c.send(bot.forgeaddbot(int(b)))
	  del botsaf

	  uts = []
	  for u in self.main.battles[b].disabledunits:
	    uts.append(u)
	    if len(uts) >= 30:
	      c.send("DISABLEUNITS %s\n" % (' '.join(uts)))
	  if len(uts) > 0:
	    c.send("DISABLEUNITS %s\n" % (' '.join(uts)))
	  uts = []
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
      elif int(args[1]) in self.main.battles and self.main.battles[int(args[1])].passworded == 1 and len(args) == 3 and self.main.battles[int(args[1])].password != args[2]:
	c.send("JOINBATTLEFAILED Error: cannot join the battle, invalid password!\n" )
      else:
	c.send("JOINBATTLEFAILED Error: cannot join the battle, battle does not exist!\n")
    else:
      c.send("JOINBATTLEFAILED Error: cannot join the battle, battle is locked\n")
  else:
    c.send("JOINBATTLEFAILED Error: cannot join the battle,you are already in another one\n" )
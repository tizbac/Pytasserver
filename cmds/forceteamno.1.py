# -*- coding: utf-8 -*-
if len(args) == 3:
  if cl.battle in self.main.battles and self.main.battles[cl.battle].founder == cl.username:
    if args[1] in self.main.battles[cl.battle].players:
      if args[2].isdigit() and int(args[2]) < 17:
	tu = self.main.allclients[self.main.clientsusernames[args[1]].sck]
	tu.battlestatus.teamno = int(args[2])
	bs = tu.getbattlestatus()
	self.main.broadcastbattle(cl.battle,"CLIENTBATTLESTATUS %s %s\n" % (tu.username,bs))
elif cl.battle in self.main.battles and self.main.battles[cl.battle].founder != cl.username:
  c.send("SERVERMSG Error: Only the battle founder can use that command\n")
else:
  c.send("SERVERMSG Error: You are not hosting\n")
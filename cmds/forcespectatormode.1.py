# -*- coding: utf-8 -*-
if len(args) == 2:
  if cl.battle in self.main.battles and self.main.battles[cl.battle].founder == cl.username:
    if args[1] in self.main.battles[cl.battle].players:
      tu = self.main.allclients[self.main.clientsusernames[args[1].lower()].sck]
      tu.battlestatus.mode = 0
      bs = tu.getbattlestatus()
      self.main.broadcastbattle(cl.battle,"CLIENTBATTLESTATUS %s %s\n" % (tu.username,bs))
elif cl.battle in self.main.battles and self.main.battles[cl.battle].founder != cl.username:
  c.send("SERVERMSG Error: Only the battle founder can use that command\n")
else:
  c.send("SERVERMSG Error: You are not hosting\n")
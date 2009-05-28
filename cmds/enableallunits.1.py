# -*- coding: utf-8 -*-
if cl.battle in self.main.battles and self.main.battles[cl.battle].founder == cl.username:
  self.main.broadcastbattle(cl.battle,"ENABLEALLUNITS\n",c)
  self.main.battles[cl.battle].disabledunits = []
elif cl.battle in self.main.battles and self.main.battles[cl.battle].founder != cl.username:
  c.send("SERVERMSG Error: Only the battle founder can use that command\n")
else:
  c.send("SERVERMSG Error: You are not hosting\n")
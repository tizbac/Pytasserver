# -*- coding: utf-8 -*-
####ENABLEUNITS unitname1 unitname2 ...
###Description
##Sent by founder of the battle to server telling him he enabled one or more previous disabled units. At least one unit name must be passed as an argument.

##unitname1: Multiple units may follow, but at least one must be present in the arguments list.

if cl.battle in self.main.battles and self.main.battles[cl.battle].founder == cl.username:
  self.main.broadcastbattle(cl.battle,"ENABLEALLUNITS\n",c)
  self.main.battles[cl.battle].disabledunits = []
elif cl.battle in self.main.battles and self.main.battles[cl.battle].founder != cl.username:
  c.send("SERVERMSG Error: Only the battle founder can use that command\n")
else:
  c.send("SERVERMSG Error: You are not hosting\n")
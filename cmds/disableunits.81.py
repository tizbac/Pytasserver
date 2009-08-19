# -*- coding: utf-8 -*-
####DISABLEUNITS unitname1 unitname2 ...
###Description
##Sent by founder of the battle to server telling him he disabled one or more units. At least one unit name must be passed as an argument.

##unitname1: Multiple units may follow, but at least one must be present in the arguments list. 
if len(args) > 1:
  if cl.battle in self.main.battles and self.main.battles[cl.battle].founder == cl.username:
    ue = []
    #self.main.battles[cl.battle].disabledunits = []
    for un in args[1:]:
      if un not in self.main.battles[cl.battle].disabledunits:
	ue.append(un)
	self.main.battles[cl.battle].disabledunits.append(un)
    self.main.broadcastbattle(cl.battle,"DISABLEUNITS %s\n" % (' '.join(ue)),co)
  elif cl.battle in self.main.battles and self.main.battles[cl.battle].founder != cl.username:
    c.send("SERVERMSG Error: Only the battle founder can use that command\n")
  else:
    c.send("SERVERMSG Error: You are not hosting\n")
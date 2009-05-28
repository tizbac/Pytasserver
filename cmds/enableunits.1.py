# -*- coding: utf-8 -*-
if len(args) > 1:
if cl.battle in self.main.battles and self.main.battles[cl.battle].founder == cl.username:
  ue = []
  for un in args[1:]:
    if un in self.main.battles[cl.battle].disabledunits:
      ue.append(un)
      self.main.battles[cl.battle].disabledunits.remove(un)
  self.main.broadcastbattle(cl.battle,"ENABLEUNITS %s\n" % (' '.join(ue)),c)
elif cl.battle in self.main.battles and self.main.battles[cl.battle].founder != cl.username:
  c.send("SERVERMSG Error: Only the battle founder can use that command\n")
else:
  c.send("SERVERMSG Error: You are not hosting\n")
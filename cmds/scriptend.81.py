# -*- coding: utf-8 -*-
if len(self.main.battles[cl.battleid].replayscript) == 0:
  raise CommandError("No Script Sent")
self.main.broadcastbattle(cl.battle,"SCRIPTSTART\n",co)
for l in self.main.battles[cl.battleid].replayscript:
  self.main.broadcastbattle(cl.battle,"SCRIPT %s\n" % l,co)

self.main.broadcastbattle(cl.battle,"SCRIPTEND\n",co)
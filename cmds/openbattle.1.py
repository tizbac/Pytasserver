# -*- coding: utf-8 -*-
# len(args)
if len(args) >= 10:
  args2 = ' '.join(args[9:]).split("\t")
  if len(args2) == 3:
    self.main.cid += 1
    if self.main.cid > 65536:
      self.main.cid = 0
    cl.battle = int(self.main.cid)
    self.main.battles.update([(cl.battle,Battle(args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8],args2[0],args2[1],args2[2],cl.username,cl.ip[0],cl.battle))])
    self.main.broadcast(self.main.battles[cl.battle].forgebattleopened())
    c.send("OPENBATTLE %i\n" % cl.battle)
    c.send("REQUESTBATTLESTATUS\n")
    

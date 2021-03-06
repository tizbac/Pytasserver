# -*- coding: utf-8 -*-
####UPDATEBATTLEINFO SpectatorCount locked maphash {mapname}	 Source: client
###Description
##Sent by the founder of the battle telling the server some of the "outside" parameters of the battle changed.

##locked: A boolean (0 or 1). Note that when client creates a battle, server assumes it is unlocked (by default). Client must make sure it actually is.

##maphash: A signed 32-bit integer. See OPENBATTLE command for more info.

##mapname: Must NOT contain file extension! 
if len(args) >= 4:
  for b in list(self.main.battles.keys()):
    if cl.username == self.main.battles[b].founder:
      self.main.battles[b].speccount = int(args[1])
      self.main.battles[b].locked = int(args[2])
      self.main.battles[b].maphash = args[3]
      if len(args) == 5:
	self.main.battles[b].mapname= ' '.join(args[4:])
      self.main.broadcast(self.main.battles[b].forgeupdatebattleinfo())
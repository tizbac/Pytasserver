# -*- coding: utf-8 -*-
####OPENBATTLE type natType password port maxplayers hashcode rank maphash {map} {title} {modname}
###Description
##Sent by client when he is trying to open a new battle. The client becomes a founder of this battle, if command is successful (see Response section).

##type: Can be 0 or 1 (0 = normal battle, 1 = battle replay)

##natType: NAT traversal method used by the host. Must be a number (0 means no NAT traversal technique should be applied).

##password: Must be "*" if founder does not wish to have password-protected game.

##hashcode: A signed 32-bit integer (acquired via unitsync.dll).

##maphash: A signed 32-bit integer as returned from unitsync.dll.

###Response
##Client is notified about this command's success via OPENBATTLE/OPENBATTLEFAILED commands. 
if cl.battle == -1:
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
else:
  c.send("OPENBATTLEFAILED Error: you are already hosting or you are already in another battle!\n")
    

# -*- coding: utf-8 -*-
for b in dict(self.main.battles):
  if b in self.main.battles:
    ba = self.main.battles[b]
    if cl.username == ba.founder:
      self.main.broadcast("BATTLECLOSED %i\n" % ba.id)
      for p in ba.players:
	if p.lower() in self.main.clientsusernames:
	  tu = self.main.allclients[self.main.clientsusernames[p.lower()].sck]
	  tu.battle = -1
      del self.main.battles[b]
    elif cl.username in ba.players:
      ba.players.remove(cl.username)
      self.main.broadcast("LEFTBATTLE %i %s\n" % (ba.id,cl.username))
      cl.battle = -1
    cl.battlestatus = BattleStatus("0")
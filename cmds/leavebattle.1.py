for b in list(self.main.battles.keys()):
  ba = self.main.battles[b]
  if cl.username == ba.founder:
    self.main.broadcast("BATTLECLOSED %i\n" % ba.id)
    del self.main.battles[b]
  elif cl.username in ba.players:
    ba.players.remove(cl.username)
    self.main.broadcast("LEFTBATTLE %i %s\n" % (ba.id,cl.username))
  cl.battlestatus = BattleStatus("0")
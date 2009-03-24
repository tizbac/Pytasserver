if len(args) >= 4:
  for b in list(self.main.battles.keys()):
    if cl.username == self.main.battles[b].founder:
      self.main.battles[b].speccount = int(args[1])
      self.main.battles[b].locked = int(args[2])
      self.main.battles[b].maphash = args[3]
      if len(args) == 5:
	self.main.battles[b].mapname= ' '.join(args[4:])
      self.main.broadcast(self.main.battles[b].forgeupdatebattleinfo())
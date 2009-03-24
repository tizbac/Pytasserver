if len(args) >= 2:
  for b in list(self.main.battles.keys()):
    if cl.username in self.main.battles[b].players:
      self.main.broadcastbattle(b,"SAIDBATTLEEX %s %s\n" % ( cl.username, ' '.join(args[1:])))
print args
if len(args) == 2: #Needs more check, it may be used to crash failclient
    for b in list(self.main.battles.keys()):
      if cl.username == self.main.battles[b].founder:
	if int(args[1]) in self.main.battles[b].startrects:
	  del self.main.battles[b].startrects[int(args[1])]
	  self.main.broadcastbattle(b,"REMOVESTARTRECT %i\n" % int(args[1]))
	  debug("Removed startrect %i" % int(args[1]))

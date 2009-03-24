print args
if len(args) == 6: #Needs more check, it may be used to crash failclient
  for b in list(self.main.battles.keys()):
    if cl.username == self.main.battles[b].founder:
      if int(args[1]) in self.main.battles[b].startrects:
	del self.main.battles[b].startrects[int(args[1])]
	self.main.broadcastbattle(b,"REMOVESTARTRECT %i\n" % int(args[1]))
	debug("Startrect %i on battle %i already exists, removed it!" % (int(args[1]),int(b)))
      self.main.battles[b].startrects.update([(int(args[1]),StartRect(int(args[1]),args[2],args[3],args[4],args[5]))])
      self.main.broadcastbattle(b,self.main.battles[b].startrects[int(args[1])].forgeaddstartrect())
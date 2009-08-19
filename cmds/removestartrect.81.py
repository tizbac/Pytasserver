# -*- coding: utf-8 -*-
####REMOVESTARTRECT allyno
###Description
##Sent by host of the battle removing a start rectangle for 'allyno' ally team. See client implementation and Spring docs for more info on this one.

if len(args) == 2: #Needs more check, it may be used to crash failclient
    for b in list(self.main.battles.keys()):
      if cl.username == self.main.battles[b].founder:
	if int(args[1]) in self.main.battles[b].startrects:
	  del self.main.battles[b].startrects[int(args[1])]
	  self.main.broadcastbattle(b,"REMOVESTARTRECT %i\n" % int(args[1]),co)
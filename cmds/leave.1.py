# -*- coding: utf-8 -*-
####LEAVE channame
###Description
##Sent by client when he is trying to leave a channel. When client is disconnected, he is automatically removed from all channels. 
if args[1] in self.main.channels:
	#print "%s is leaving %s"%(cl.username,args[1])
	if cl.username in self.main.channels[args[1]].users:
		#print "broadcasting"
		self.main.broadcastchannel(args[1],"LEFT %s %s %s\n" % (args[1],cl.username,""))
		self.main.channels[args[1]].users.remove(cl.username)
		if self.main.services:
		  self.main.services.onclientleftchannel(cl,args[1])
		if len(self.main.channels[args[1]].users) == 0 and not self.main.channels[args[1]].confirmed:
		  del self.main.channels[args[1]]
	else:
	  raise CommandError("You weren't on #%s"%args[1])

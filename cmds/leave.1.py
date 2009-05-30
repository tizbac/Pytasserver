# -*- coding: utf-8 -*-
####LEAVE channame
###Description
##Sent by client when he is trying to leave a channel. When client is disconnected, he is automatically removed from all channels. 
if args[1] in self.main.channels:
	if cl.username in self.main.channels[args[1]].users:
		self.main.broadcastchannel(ch,"LEFT %s %s %s\n" % (args[1],cl.username,""))
		self.main.channels[args[1]].users.remove(cl.username)
		if len(self.main.channels[args[1]].users) == 0 and not self.main.channels[args[1]].confirmed:
		  del self.main.channels[args[1]]

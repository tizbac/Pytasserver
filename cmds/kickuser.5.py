# -*- coding: utf-8 -*-
####KICKUSER username {reason}
###Description
##Kicks the user from the server, only a moderator can use it
if len(args) >= 2 and cl.mod == 1:
	if len(args) >= 3:
		reason = ' '.join(args[2:])
	else:
		reason = "Not given"
	print "Kicking "+args[1]
	
	if args[1].lower() in dict(self.main.clientsusernames):
		for cha in dict(self.main.channels):
		  if args[1] in self.main.channels[cha].users:
		    self.main.broadcastchannel(cha,"CHANNELMESSAGE %s <%s> has kicked <%s> from server (Reason: %s)\n" % (cha,cl.username,args[1],reason))
	for h in self.main.handlers:
		for cli in dict(h.clients):
			if h.clients[cli].username == args[1]:
				h.remove(cli,"Kicked from server by %s" % cl.username)

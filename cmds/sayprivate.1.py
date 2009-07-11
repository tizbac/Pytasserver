# -*- coding: utf-8 -*-
####SAYPRIVATE username {message}
###Description
##Sent by client when he is trying to send a private message to some other client.

###Response
##Server will respond with a SAYPRIVATE command.

#print self.main.clientsusernames[args[1].lower()],self.clients
if len(args) >= 3 and args[1].lower() in self.main.clientsusernames :
  for h in self.main.handlers:
	if self.main.clientsusernames[args[1].lower()].sck in h.clients:
  		self.main.clientsusernames[args[1].lower()].send("SAIDPRIVATE %s %s\n" % (cl.username,' '.join(args[2:])))
  c.send("SAYPRIVATE %s %s\n" % (args[1],' '.join(args[2:])))
else:
  c.send("SERVERMSG %s\n" % (("No such user :%s" % args[1]) if len(args) > 2 else "Missing argument, your command was %s, syntax is SAYPRIVATE username message" % (' '.join(args))))

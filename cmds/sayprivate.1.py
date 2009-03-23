print args
print self.main.clientsusernames[args[1]],self.clients
if len(args) >= 3 and args[1] in self.main.clientsusernames :
  for h in self.main.handlers:
	if self.main.clientsusernames[args[1]].sck in h.clients:
  		self.main.clientsusernames[args[1]].send("SAIDPRIVATE %s %s\n" % (cl.username,' '.join(args[2:])))
  c.send("SAYPRIVATE %s %s\n" % (args[1],' '.join(args[2:])))

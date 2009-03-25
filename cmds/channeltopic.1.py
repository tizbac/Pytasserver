if len(args) >= 3 and args[1] in self.main.channels:
	if cl.accountid in self.main.channels[args[1]].operators or cl.username == self.main.channels[args[1]].founder or cl.mod == 1:
		self.main.channels[args[1]].topic = ' '.join(args[2:])
		self.main.channels[args[1]].topicsetby = cl.username
		self.main.channels[args[1]].topichangedtime = time.time()
		self.main.broadcastchannel(args[1],"CHANNELTOPIC %s %s %f %s\n" % (args[1],self.main.channels[args[1]].topicsetby,self.main.channels[args[1]].topichangedtime,self.main.channels[args[1]].topic))
		self.main.channels[args[1]].sync(self.main.database)

# -*- coding: utf-8 -*-
####CHANNELTOPIC channame {topic}
###Description
##Sent by privileged user who is trying to change channel's topic. Use * as topic if you wish to disable it. 
if len(args) >= 3 and args[1] in self.main.channels:
	if str(cl.accountid) in self.main.channels[args[1]].operators or cl.accountid == self.main.channels[args[1]].founder or cl.mod == 1:
		self.main.channels[args[1]].topic = ' '.join(args[2:])
		self.main.channels[args[1]].topicsetby = cl.username
		self.main.channels[args[1]].topichangedtime = time.time()
		self.main.broadcastchannel(args[1],"CHANNELTOPIC %s %s %i %s\n" % (args[1],self.main.channels[args[1]].topicsetby,int(self.main.channels[args[1]].topichangedtime*1000),self.main.channels[args[1]].topic))
		if self.main.sql:
		  self.main.channels[args[1]].sync(self.main.database)

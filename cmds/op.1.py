# -*- coding: utf-8 -*-
if len(args) == 3:
  if args[2].lower() in self.main.clientsusernames and args[1] in self.main.channels:
    cli = self.main.allclients[self.main.clientsusernames[args[2].lower()].sck]
    cha = self.main.channels[args[1]]
    if cl.accountid == cha.founder or cl.mod == 1:
      if str(cli.accountid) not in cha.operators:
	cha.operators.append(str(cli.accountid))
	cha.sync(self.main.database)
	self.main.broadcastchannel(args[1],"CHANNELMESSAGE %s <%s> has just been added to channel's operator list by <%s>\n" % (args[1],cli.username,cl.username))
    

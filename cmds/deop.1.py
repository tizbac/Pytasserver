# -*- coding: utf-8 -*-
####DEOP channame user
###Description
##Remove the user from channel operator list, only the founder or a moderator can use it
if len(args) == 3:
  if args[2].lower() in self.main.clientsusernames and args[1] in self.main.channels:
    cli = self.main.allclients[self.main.clientsusernames[args[2].lower()].sck]
    cha = self.main.channels[args[1]]
    if cl.username == cha.founder or cl.mod == 1:
      if str(cli.accountid) in cha.operators:
	cha.operators.remove(str(cli.accountid))
	cha.sync(self.main.database)
	self.main.broadcastchannel(args[1],"CHANNELMESSAGE %s <%s> has just been removed from channel's operator list by <%s>\n" % (args[1],cli.username,cl.username))

# -*- coding: utf-8 -*-
#### UNMUTEIP channel ip
if args[1] not in self.main.channels:
  raise CommandError("No such channel: "+args[1])
chan = self.main.channels[args[1]]
if not ( cl.accountid in chan.operators or cl.accountid == chan.founder or cl.mod == 1):
  raise CommandError("Not enough privileges")
if not self.main.ipregex.match(args[2]):
  raise CommandError("Invalid IP")
ip = args[2]
if not ip in chan.ipmutes:
  raise CommandError("IP %s is not muted" % ip )
del chan.ipmutes[ip]
self.main.broadcastchannel(args[1],"CHANNELMESSAGE %s <%s> has been ip-unmuted by <%s>\n" % (cl.username,args[1],ip))
chan.sync(self.main.database)
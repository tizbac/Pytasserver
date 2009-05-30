####CHANNELFOUNDER channame newfounder
###Description
##Changes the founder of the channel
##Only the current founder or a moderator can use it
if len(args) == 3 and self.main.sql and args[1] in self.main.channels and self.main.channels[args[1]].confirmed and ( cl.mod == 1 or cl.username == self.main.channels[args[1]].founder ):
  self.main.channels[args[1]].founder = args[2]
  self.main.channels[args[1]].sync(self.main.database)
  self.main.broadcastchannel(args[1],"CHANNELMESSAGE %s <%s> is the new founder of this channel\n" % (args[1],args[2]))

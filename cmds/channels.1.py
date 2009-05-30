# -*- coding: utf-8 -*-
####CHANNELS
###Description
##Sent by client when requesting channels list

###Response
##Server will respond with a series of CHANNEL command, ending it with ENDOFCHANNELS command.

###Examples
##JOIN main

for cha in self.main.channels:
  c.send("CHANNEL %s %i\n" % (cha,len(self.main.channels[cha].users)))
c.send("ENDOFCHANNELS\n")
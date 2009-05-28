# -*- coding: utf-8 -*-
for cha in self.main.channels:
  c.send("CHANNEL %s %i\n" % (cha,len(self.main.channels[cha].users)))
c.send("ENDOFCHANNELS\n")
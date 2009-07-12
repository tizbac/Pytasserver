# -*- coding: utf-8 -*-
if cl.admin == 1:
  for C in self.main.conf:
    c.send("SERVERMSG %s = %s\n" % (C,self.main.conf[C]))
else:
  c.send("SERVERMSG Needs admin privileges\n")
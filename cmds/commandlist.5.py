# -*- coding: utf-8 -*-
c.send("SERVERMSG Commands avaible to you in current context:\n")
for comm in self.commands:
  if cl.checkaccess(self.accesstable[comm])[0]:
    c.send("SERVERMSG %s\n" % comm.upper())
  
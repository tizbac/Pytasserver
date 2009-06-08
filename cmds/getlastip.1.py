# -*- coding: utf-8 -*-
if cl.mod == 1:
  if len(args) == 2:
    acc = self.main.loadaccountfromdatabase(args[1].lower())
    if not acc:
      c.send("SERVERMSG Error: Cannot load <%s> account\n" % args[1])
    else:
      c.send("SERVERMSG Account <%s> last ip is %s\n" % (args[1],acc.ip[0]))
      del acc
      
# -*- coding: utf-8 -*-
if cl.mod == 1:
  if len(args) == 2:
    acc = self.main.loadaccountfromdatabase(args[1].lower())
    c.send("SERVERMSG Loading <%s> account from database...\n" % args[1])
    if not acc:
      c.send("SERVERMSG Error: Cannot load <%s> account\n" % args[1])
    else:
      c.send("SERVERMSG %s's registration date is %s\n" % (args[1],time.ctime(acc.registrationdate)))
      del acc
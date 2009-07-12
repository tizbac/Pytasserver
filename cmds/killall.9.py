# -*- coding: utf-8 -*-
uname = str(cl.username)
for h in self.main.handlers:
  for kl in dict(h.clients):
    h.remove(kl,"KILLALL Command issued by %s" % uname)
      
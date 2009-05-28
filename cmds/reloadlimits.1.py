# -*- coding: utf-8 -*-
if cl.admin == 1:
  c.send("SERVERMSG Reloading command rate limits...\n")
  if self.main.cmdlimit:
    self.main.cmdlimit.reloadlimits()
  else:
    c.send("SERVERMSG Error: command rate limits are disabled\n")
  c.send("SERVERMSG Done\n")
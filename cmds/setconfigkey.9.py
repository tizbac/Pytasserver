# -*- coding: utf-8 -*-
####SETCONFIGKEY keyname {value}
if cl.admin == 1:
  if len(args) >= 3:
    if args[1].lower() in self.main.conf:
      if args[1].lower() in self.main.dynamicsettings:
	self.main.conf[args[1].lower()] = ' '.join(args[2:])
	self.main.writesettings()
	c.send("SERVERMSG Config updated successfully\n")
      else:
	c.send("SERVERMSG Error, that setting cannot be changed without restart\n")
    else:
      c.send("SERVERMSG That key doesn't exist\n")
  else:
    c.send("SERVERMSG Not enough parameters\n")
else:
  c.send("SERVERMSG Needs admin privileges\n")
  
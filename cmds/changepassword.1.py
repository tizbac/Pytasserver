# -*- coding: utf-8 -*-
####CHANGEPASSWORD oldPassword newPassword	 Source: client
###Description
##Will change password of client's account (which he is currently using).

###Response
##No response is prescribed, although server may reply with some SERVERMSG command.

if self.main.sql and cl.sql:
  if len(args) == 3 and args[1] == cl.password:
    cl.password = args[2]
    c.send("SERVERMSG Password changed succesfully\n")
    cl.sync(self.main.database)
  elif len(args) == 3 and args[1] != cl.password:
    c.send("SERVERMSG Invalid Old Password\n")
else:
  c.send("SERVERMSG Error: Cannot change password while in LAN mode\n")
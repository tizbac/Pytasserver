# -*- coding: utf-8 -*-
####HANDICAP username value
###Description
##Sent by founder of the battle changing username's handicap value (of his battle status). Only founder can change other users handicap values (even they themselves can't change it).

##value: Must be in range [0, 100] (inclusive).

if len(args) == 3:
  if cl.battle in self.main.battles and self.main.battles[cl.battle].founder == cl.username:
    if args[1] in self.main.battles[cl.battle].players:
      if args[2].isdigit() and int(args[2]) < 101 and int(args[2]) > -1:
	tu = self.main.allclients[self.main.clientsusernames[args[1].lower()].sck]
	tu.battlestatus.teamcolor = str(args[2])
	bs = tu.getbattlestatus()
	self.main.broadcastbattle(cl.battle,"CLIENTBATTLESTATUS %s %s\n" % (tu.username,bs))
elif cl.battle in self.main.battles and self.main.battles[cl.battle].founder != cl.username:
  c.send("SERVERMSG Error: Only the battle founder can use that command\n")
else:
  c.send("SERVERMSG Error: You are not hosting\n")
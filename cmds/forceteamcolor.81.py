# -*- coding: utf-8 -*-
####FORCETEAMCOLOR username color
###Description
##Sent by founder of the battle when he is trying to force some other client's team color to 'color'. Server will update client's battle status automatically.

##color: Should be a 32-bit signed integer in decimal form (e.g. 255 and not FF) where each color channel should occupy 1 byte (e.g. in hexdecimal: $00BBGGRR, B = blue, G = green, R = red). Example: 255 stands for $000000FF.
if len(args) == 3:
  if cl.battle in self.main.battles and self.main.battles[cl.battle].founder == cl.username:
    if args[1] in self.main.battles[cl.battle].players:
      if args[2].isdigit():
	tu = self.main.allclients[self.main.clientsusernames[args[1].lower()].sck]
	tu.battlestatus.teamcolor = str(args[2])
	bs = tu.getbattlestatus()
	self.main.broadcastbattle(cl.battle,"CLIENTBATTLESTATUS %s %s\n" % (tu.username,bs))
elif cl.battle in self.main.battles and self.main.battles[cl.battle].founder != cl.username:
  c.send("SERVERMSG Error: Only the battle founder can use that command\n")
else:
  c.send("SERVERMSG Error: You are not hosting\n")
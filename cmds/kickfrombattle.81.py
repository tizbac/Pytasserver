# -*- coding: utf-8 -*-
####KICKFROMBATTLE username
###Description
##Sent by founder of the battle when he kicks the client out of the battle. Server remove client from the battle and notify him about it via FORCEQUITBATTLE command.

if len(args) == 2:
  if cl.battle in self.main.battles and self.main.battles[cl.battle].founder == cl.username:
    if args[1] in self.main.battles[cl.battle].players:
     
	tu = self.main.allclients[self.main.clientsusernames[args[1].lower()].sck]
	tu.sso.send("FORCEQUITBATTLE\n")
	#debug("Broadcasting LEFTBATTLE")
	self.main.broadcast("LEFTBATTLE %i %s\n" % (cl.battle,tu.username))
	#debug("Broadcasting LEFTBATTLE - Done")
	tu.battle = -1
elif cl.battle in self.main.battles and self.main.battles[cl.battle].founder != cl.username:
  c.send("SERVERMSG Error: Only the battle founder can use that command\n")
else:
  c.send("SERVERMSG Error: You are not hosting\n")
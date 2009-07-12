# -*- coding: utf-8 -*-
####SAYBATTLEEX {message}
###Description
##Sent by any client participating in a battle when he wants to say something in "/me" irc style. Server can forge this command too (for example when founder of the battle kicks a user, server uses SAYBATTLEEX saying founder kicked a user). 
if len(args) >= 2:
  for b in list(self.main.battles.keys()):
    if cl.username in self.main.battles[b].players:
      self.main.broadcastbattle(b,"SAIDBATTLEEX %s %s\n" % ( cl.username, ' '.join(args[1:])))
# -*- coding: utf-8 -*-
####SAYBATTLE {message}
###Description
##Sent by client who is participating in a battle to server, who forwards this message to all other clients in the battle. BATTLE_ID is not required since every user can participate in only one battle at the time. If user is not participating in the battle, this command is ignored and is considered invalid
if len(args) >= 2:
  for b in list(self.main.battles.keys()):
    if cl.username in self.main.battles[b].players:
      self.main.broadcastbattle(b,"SAIDBATTLE %s %s\n" % ( cl.username, ' '.join(args[1:])))
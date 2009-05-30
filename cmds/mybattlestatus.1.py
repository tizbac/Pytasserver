# -*- coding: utf-8 -*-
####MYBATTLESTATUS battlestatus myteamcolor
###Description
##Sent by a client to the server telling him his status in the battle changed.

##battlestatus: An integer but with limited range: 0..2147483647 (use signed int and consider only positive values and zero). Number is sent as text. Each bit has its meaning:

##    * b0 = undefined (reserved for future use)
##    * b1 = ready (0=not ready, 1=ready)
##    * b2..b5 = team no. (from 0 to 15. b2 is LSB, b5 is MSB)
##    * b6..b9 = ally team no. (from 0 to 15. b6 is LSB, b9 is MSB)
##    * b10 = mode (0 = spectator, 1 = normal player)
##    * b11..b17 = handicap (7-bit number. Must be in range 0..100). Note: Only host can change handicap values of the players in the battle (with HANDICAP command). These 7 bits are always ignored in this command. They can only be changed using HANDICAP command.
##    * b18..b21 = reserved for future use (with pre 0.71 versions these bits were used for team color index)
##    * b22..b23 = sync status (0 = unknown, 1 = synced, 2 = unsynced)
##    * b24..b27 = side (e.g.: arm, core, tll, ... Side index can be between 0 and 15, inclusive)
##    * b28..b31 = undefined (reserved for future use)



##myteamcolor: Should be 32-bit signed integer in decimal form (e.g. 255 and not FF) where each color channel should occupy 1 byte (e.g. in hexdecimal: $00BBGGRR, B = blue, G = green, R = red). Example: 255 stands for $000000FF. 
if len(args) == 3:
  cl.setbattlestatus(args[1])
  cl.teamcolor = args[2]
  self.main.broadcastbattle(cl.battle,"CLIENTBATTLESTATUS "+cl.username+" "+cl.getbattlestatus()+" "+cl.teamcolor+"\n")
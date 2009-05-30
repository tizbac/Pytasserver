# -*- coding: utf-8 -*-
####PING
##Client should send this command on every few seconds to maintain constant connection to the server. Server will assume timeout occured if it does not hear from client for more than 30 seconds. To figure out how long does a reply take, use message ID with this command.
c.send("PONG\n")
cl.lastping = time.time()
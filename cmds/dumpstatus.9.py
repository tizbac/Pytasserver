# -*- coding: utf-8 -*-
c.send("SERVERMSG Dumping server status(server will freeze during dump)...\n")
n = self.main.dump()
c.send("SERVERMSG Dump Complete, saved in %s\n"%n)
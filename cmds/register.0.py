# -*- coding: utf-8 -*-
####REGISTER username passhash
##Client sends this command when trying to register a new account. Note that client mustn't already be logged in, or else server will deny his request. If server is running in LAN_MODE, this command will be ignored.<br>
##password: Must be sent in encoded form (MD5 hash in base-64 form).<br>
###Response
##Server will respond with either REGISTRATIONDENIED or REGISTRATIONACCEPTED command.<br>
###Examples
##REGISTER Johnny Gnmk1g3mcY6OWzJuM4rlMw==

if len(args) == 3 and cl.lgstatus == 0 and self.main.sql:
  self.main.database.query("SELECT id,name FROM users WHERE name = '%s' LIMIT 1" % ( self.main.database.escape(args[1].lower())))
  res = self.main.database.store_result()
  if args[1].lower() not in self.main.clientsusernames:
    val = self.main.validateusername(args[1])
    if val[0]:
      if res.num_rows() == 0:
	self.main.database.query("INSERT INTO users (name,password,playtime,accesslevel,bot,banned,casename,registrationdate) VALUES ('%s','%s',0,1,0,0,'%s',%i)" %
	(self.main.database.escape(args[1]).lower(),self.main.database.escape(args[2]),self.main.database.escape(args[1]),int(time.time())),False)
	c.send("REGISTRATIONACCEPTED\n")
	self.remove(co,"Registration complete")
      else:
	c.send("REGISTRATIONDENIED User already exists\n")
	self.remove(co,"Bad register command")
    else:
      c.send("REGISTRATIONDENIED %s\n" % val[1])
      self.remove(co,"Username validation failed")
  else:
    c.send("REGISTRATIONDENIED an user with that name is currently logged in\n") 

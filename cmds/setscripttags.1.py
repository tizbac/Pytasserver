if len(args) >= 2:
  args2 = ' '.join(args[1:]).split("\t")
  for b in list(self.main.battles.keys()):
    if cl.username == self.main.battles[b].founder:
      for a in args2:
	bn = a.split("=")
	#print bn
	if len(bn) == 2 and len(self.main.battles[b].scripttags) < 129:
	  self.main.battles[b].scripttags.update([bn])
	  #print self.main.battles[b].scripttags
      sts = ""
      stl = []
      for tag in self.main.battles[b].scripttags:
	stl.append(tag+"="+self.main.battles[b].scripttags[tag])
      sts = '\t'.join(stl)
      self.main.broadcastbattle(b,"SETSCRIPTTAGS %s\n" % sts)
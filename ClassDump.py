# -*- coding: utf-8 -*-
#import sys
import string
"""class TestClass2:
  def __init__(self):
    self.lol = ["ab","cd"]
    self.x = dict()
    self.y = {1:8}
class TestClass:
  def __init__(self):
    self.intvalue = 0
    self.strvalue = "test"
    self.module = sys
    self.subclass = TestClass2()"""
def getistaddr(obj):
	a = str(obj).split(" at ")
	if len(a) > 1:
		addr = a[1].strip(" <>")
	else:
		addr = ""
	return addr
class Dumper:
  def __init__(self):
    self.depth=0
    self.maxdepth=20
    self.dumpedinstances = []
  def dump(self,name,obj,depth=1,hdr=True):
    #print self.dumpedinstances
    if hdr:
    	a = " "*(depth-1)+str(obj).replace(getistaddr(obj),"")+"\n"
    
    for o in dir(obj):
      try:
	      if not o.startswith("__"):
		exec "ref = obj.%s" % o
		l = str(type(ref))
		if l == "<type 'instance'>" and depth <= self.maxdepth and getistaddr(ref) not in self.dumpedinstances:#Iterate
		  self.dumpedinstances.append(getistaddr(ref))
		  exec "a += self.dump(\"%s\",ref,depth+1)"%o
		if l == "<type 'dict'>" and depth <= self.maxdepth:
		  a += " "*depth+"%s.%s = ... (%s)\n"%(name,o,str(type(ref)).replace("\n","\\n"))
		  for x in ref:
		        y = ref[x]
		  	exec "a += self.dump(\"[%s]\",y,depth+1)"%str(x).replace(getistaddr(x),"")
		elif l== "<type 'module'>" and depth <= self.maxdepth:
		  print "dump module"
		  exec "a += self.dump(\"%s\",ref,depth+1)"%o
		elif l == "<type 'list'>" and depth <= self.maxdepth:
		  a += " "*depth+"%s.%s = ... (%s)\n"%(name,o,str(type(ref)).replace("\n","\\n"))
		  for x in ref:
		  	exec "a += self.dump(\"%s\",x,depth+1)"%str(x).replace(getistaddr(x),"")
		else:
		  a += " "*depth+"%s.%s = %s (%s)\n"%(name,o,str(ref).replace("\n","\\n").replace(getistaddr(ref),""),str(type(ref)).replace("\n","\\n"))
      except:
      	pass
    return a
"""inst = TestClass()
dmp = Dumper()
data= dmp.dump("TestClass",inst)
f = open("classdmp.txt","w")
f.write(data)
f.close()"""

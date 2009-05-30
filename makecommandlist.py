# -*- coding: utf-8 -*-
import os
import string
page = open("commands.html","wb")
page.write("<HTML><HEAD><title>Pytasserver implemented commands</HEAD><BODY>\n")
for f in os.listdir("cmds/"):
  if f.endswith(".py"):
    fd = open("cmds/"+f,"r")
    s = fd.read()
    fd.close()
    content = ""
    for l_ in s.split("\n"):
      l = l_.strip("\r\t ")
      if l.startswith("####"):
	content+="<h1>"+l.strip("#")+"</h1>"
      elif l.startswith("###"):
	content+="<h2>"+l.strip("#")+"</h2>"
      elif l.startswith("##"):
	content+="<b>"+l.strip("#")+"</b>"
    	content+="<br>\n"
    if content.strip(" \r\n\t") == "":
      content="<h1> %s - Not documented </h1><br>" % f.split(".")[0].upper()
    page.write("<br>"+content)
  
  
page.write("</BODY></HTML>\n")
page.close()

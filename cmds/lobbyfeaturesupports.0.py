if len(cl.supportedfeatures) < 255:
  if len(args) >= 2:
    for arg in args[1:]:
      if arg.upper() not in cl.supportedfeatures:
	cl.supportedfeatures.append(arg.upper())
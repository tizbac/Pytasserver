import time
import string

red = "\033[21;31m"
green = "\033[21;32m"
yellow = "\033[21;33m"
blue = "\033[21;34m"
normal = "\033[0m"
purple = "\033[21;35m"
cyan = "\033[21;36m"
def debug(t):
	print blue+str(time.time())+" [D] "+t+normal
def info(t):
	print purple+str(time.time())+" [I] "+t+normal
def notice(t):
	print cyan+str(time.time())+" [N] "+t+normal
def error(t):
	print red+str(time.time())+" [E] "+t+normal
def good(t):
	print green+str(time.time())+" [G] "+t+normal
def bad(t):
	print yellow+str(time.time())+" [B] "+t+normal

import http.client as httplib
import sys
from ping3 import ping

def internetOn():
	conn = httplib.HTTPConnection("1.1.1.1", timeout=5)
	try:
		conn.request("HEAD", "/")
		return True
	except Exception:
		print("Please check your internet connection!")
		sys.exit()
	finally:
		conn.close()

def isUp(host):
	response = ping(host, unit="ms", timeout=3)
	if not response:
		return "Offline"
	elif str(response) == "None":
		return "Unknow host"
	else:
		return f"Online, ({round(response)} ms)"
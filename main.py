# send message to console while program is initializing
print("Loading...")

# import modules
import urwid, psutil, random, socket, sys, os
from time import sleep, localtime, strftime
from requests import get

# import custom modules from "modules" dir
from modules.internet import internetOn, isUp

def networkUpdate(_loop = None,_data = None):
	global network

	network = f"""PC Tom: {isUp("10.0.0.206")}
  Router: {isUp("10.0.0.1")}
  Cell Tom: {isUp("10.0.0.93")}
  PC Salon: {isUp("10.0.0.196")}"""

	loop.set_alarm_in(30,networkUpdate)

def oneMin(_loop = None,_data = None):
	internetOn()
	global message, publicIP, privateIP, mc, mcOnline

	message = "asdasd " + str(random.randint(0,100))

	publicIP = get('https://api.ipify.org').content.decode('utf8')
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	privateIP = socket.gethostbyname(s.getsockname()[0])
	s.close()

	mc = get("https://api.mcsrvstat.us/2/mc.artivain.com").json()
	if mc["online"]:
		mcOnline = f"True, {mc['players']['online']} / {mc['players']['max']} players online"
	else:
		mcOnline = "False"

	loop.set_alarm_in(60,oneMin)

def oneSec(_loop = None,_data = None):
	battery = psutil.sensors_battery()
	ram = psutil.virtual_memory()
	disk = psutil.disk_usage('/')
	cpu = psutil.cpu_percent(percpu=True)
	outputTxt = f"""
Battery:
  Charging: {battery.power_plugged}
  Charge: {round(battery.percent)} %

CPU usage:
  0: {cpu[0]} %
  1: {cpu[1]} %

Memory usage:
  RAM: {ram.percent} % ({round(ram.used / (1024 ** 3), 2)} GB used of {round(ram.total / (1024 ** 3), 2)} GB)
  HDD: {disk.percent} % ({round(disk.used / (1024.0 ** 3), 2)} GB used of {round(disk.total / (1024.0 ** 3), 2)} GB)

Message:
  {message}

IP:
  Public: {publicIP}
  Private: {privateIP}

Minecraft server:
  Online: {mcOnline}
  Address: {mc["hostname"]} ({mc["ip"]}:{mc["port"]})

Network:
  {network}
"""

	footerText.set_text(strftime("%d %b %Y %X", localtime()))
	left.set_text(outputTxt)
	loop.set_alarm_in(1,oneSec)

def keypress(key): # manage keypresses
	if key in ('q', 'Q'): # exit program on Q pressed
		raise urwid.ExitMainLoop()

	if key in ("up"): # make screen brighter on arrow up
		live = int(os.popen("cat /sys/class/backlight/intel_backlight/brightness").readlines()[0])
		max = 3000000
		if live < max:
			value = str(live + 20000)
			os.popen("echo "+value+" | tee /sys/class/backlight/intel_backlight/brightness").read()
			right.set_text(value)
		return
	if key in ("down"): # make screen less bright on arrow down
		live = int(os.popen("cat /sys/class/backlight/intel_backlight/brightness").readlines()[0])
		min = 50000
		if live > min:
			value = str(live - 20000)
			os.popen("echo "+value+" | tee /sys/class/backlight/intel_backlight/brightness").read()
			right.set_text(value)
		return
	# txt2.set_text(("banner", repr(key))) # for debug only

palette = [
	('banner', 'black', 'light gray'),
	('streak', 'black', 'dark red'),
	('bg', 'black', 'dark blue'),
	("bgBlue", "light green", "dark blue"),
	("footer", "white", "dark blue")
]

red_bg = urwid.AttrSpec('default', 'dark red')
green_bg = urwid.AttrSpec('default', 'dark green')

left = urwid.Text("Hello Bozo")
right = urwid.Text("Keypress here...")
footerText = urwid.Text("", "center")

header = urwid.AttrMap(
	urwid.Text("\nArtivain Datacenter\n", "center"), # text
	"bgBlue" # background color
)
footer = urwid.AttrMap(
	footerText, # text
	"footer" # background color
)
col1 = urwid.LineBox(urwid.Filler(left))
col2 = urwid.LineBox(urwid.Filler(right))
body = urwid.Columns([col1, col2], 1)
frame = urwid.Frame(body, header, footer)
loop = urwid.MainLoop(frame, palette, unhandled_input=keypress)
internetOn()
networkUpdate()
oneMin()
oneSec()
loop.run()
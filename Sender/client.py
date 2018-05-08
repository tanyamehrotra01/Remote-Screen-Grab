import sys
import bluetooth
import pyscreenshot as ImageGrab
import base64

if sys.version < '3':
    input = raw_input

sock=bluetooth.BluetoothSocket(bluetooth.L2CAP)

if len(sys.argv) < 2:
    print("usage: l2capclient.py <addr>")
    sys.exit(2)

bt_addr=sys.argv[1]
port = 0x1001

print("trying to connect to %s on PSM 0x%X" % (bt_addr, port))

sock.connect((bt_addr, port))

print("connected.  Sending Screenshot")


im=ImageGrab.grab()
    
ImageGrab.grab_to_file('screenshot.png')

encoded_string = ""
with open("screenshot.png", "rb") as image_file:
	global encoded_string 
	encoded_string = base64.b64encode(image_file.read())

while True:
    if(len(encoded_string) == 0):
    	break
    sock.send(encoded_string[:660])
    print(encoded_string[:660])
    data = sock.recv(1024)
    print("Data received:", str(data))
    encoded_string = encoded_string[660:]

print("Sent!")
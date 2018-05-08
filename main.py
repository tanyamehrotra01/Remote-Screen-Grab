import bluetooth
import base64
import sys
import pyscreenshot as ImageGrab

print "----------------------------------------------------------------------"
print "\t\t\t Remote Screen Grab"
print "----------------------------------------------------------------------"
print 
print 
print "----------------------------------------------------------------------"
print "1) Receive \t\t\t 2) Send"
print "----------------------------------------------------------------------"
print 
choice0 = int(input("Choice? "))
if (choice0 == 1):
	print "Listening for connection requests."
	print 

	server_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
	port = 0x1001

	server_sock.bind(("", port))
	server_sock.listen(1)
	           
	client_sock, address = server_sock.accept()
	print "Accepted connection from ", address

	data = client_sock.recv(1024)

	encoded_string = bytes.decode(data)
	while data:
	    client_sock.send("Received " + str(len(str(data))) + " bytes of data")
	    data = client_sock.recv(1024)
	    encoded_string +=  bytes.decode(data)

	imgdata = base64.b64decode(encoded_string)
	filename = 'ScreenGrab_'+address+'.png'
	with open(filename, 'wb') as f:
		f.write(imgdata)
		f.close()

	client_sock.close()
	server_sock.close()

	print "Screenshot received from client. Image save as \'", filename, "\'"
elif (choice0 == 2):
	print "------------------------------------------------------------------"
	print "1) Discover New Device \t\t 2) Enter MAC Address Manually"
	print "------------------------------------------------------------------"
	print 
	choice1 = int(input("Choice? "))
	if (choice1 == 1):
		print "Searching for nearby bluetooth-enabled devices for 10 seconds"
		devices = bluetooth.discover_devices(duration = 10, lookup_names = True)
		i = 1
		for address, name in devices:
			print "\t", i, ") ", name, " : ", address
			i += 1
		choice2 = int(input("Choice? "))
		if (1 <= choice2 <= len(devices)):
			MAC_Address = devices[choice2-1][0]
	elif(choice1 == 2):
		MAC_Address = input("Enter MAC Address: ")

	sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)

	bt_addr = MAC_Address
	port = 0x1001

	sock.connect((bt_addr, port))

	print "Connected to", devices[choice2-1][0], "\nSending Screenshot"

	im = ImageGrab.grab()
    
	ImageGrab.grab_to_file('ScreenGrab.png')

	encoded_string = ""
	with open("ScreenGrab.png", "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())

	while True:
	    if(len(encoded_string) == 0):
	    	break
	    sock.send(encoded_string[:660])
	    print encoded_string[:660]
	    data = sock.recv(1024)
	    print "Data received:", str(data)
	    encoded_string = encoded_string[660:]

	print "Sent screenshot."
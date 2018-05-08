#Python 2.7
import pyscreenshot as ImageGrab
import base64

if __name__ == "__main__":
    # fullscreen
    im=ImageGrab.grab()
    
    ImageGrab.grab_to_file('screenshot.png')

    #finding encoded string
    with open("screenshot.png", "rb") as image_file:
    	encoded_string = base64.b64encode(image_file.read())
    	print(encoded_string)
    	
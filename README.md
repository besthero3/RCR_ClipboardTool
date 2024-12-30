# Description

This is a clipboard tool intended to be used for experimentation or for Red Team purposes. This tool is not designed or intended to be used in malicious ways and the author does not condone or take responsibility for any uses of this tool in those inappropriate manners. 

The tool works by copying the clipboard data every time Ctrl+C is used. This data is added to a file and that file is exfiltrated to a server every time unique clipboard information is copied. Thes server stores its own copy of the file. Additionally, everytime Ctrl+C or Ctrl+V is used, the clipboard data is modified to be “password”. Currently the server client infrastructure is set up to be the local host but can easily be changed and would be during the deployment of the tool. 


## Possible To-Do List/Ideas
* Research password requirements and design an algorithm to flag what likely passwords are when they are added to the file
* Make same function happen as Ctrl+C Ctrl+V when RightClick+Copy and RightClick+Paste happen
* Could have some functionality so that when a password is copied, a chess puzzle pops up and the solution has to be implemented to disable the script for a short period of time or to get access back to the clipboard temporarily
* Could make windows popup to tell them their clipboard equals password now
* Could consider not having Ctrl+V change the data to password, that way the clipboard data we have would be used as the password. Although if not careful the password will always be a password.  
* Add a counter so there is not a post request to the server every time there is a new piece of clipboard_data
* Rewrite the tool in C after I learn C

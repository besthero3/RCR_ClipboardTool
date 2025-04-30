# Description

This is a clipboard tool intended to be used for experimentation or for Red Team purposes. This tool is not designed or intended to be used in malicious ways and the author does not condone or take responsibility for any uses of this tool in those inappropriate manners. 

The tool works by copying the clipboard data every time Ctrl+C is used. This data is added to a local file. Each clipboard copy is exfiltrated to a server. The server stores its own copy of the file. This data is also forwarded to a discord channel to make monitoring it easier. Additionally, everytime Ctrl+C or Ctrl+V is used, the clipboard data is modified to have an invisible space at the end of it. The tool also establishes a foothold on the server once it is run. It modifies run keys so that it will be run any time fodhelper.exe (trusted Windows binary is run). It also creates a scheduled task that will run fodhelper.exe on startup. This persistence is achieved during deployment remote by using Ansible. 

## Possible To-Do List/Ideas
* Edit the clipboard data based off of what data was copied
* Make the infected system call back to the server periodically and run commands
* Have the infected system send a post request to the server that it established a connection to make tracking callbacks easier
* Persistence Techniques - Debug and add more
* Research password requirements and design an algorithm to flag what likely passwords are when they are added to the file
* Make same function happen as Ctrl+C Ctrl+V when RightClick+Copy and RightClick+Paste happen
* Could have some functionality so that when a password is copied, a chess puzzle pops up and the solution has to be implemented to disable the script for a short period of time or to get access back to the clipboard temporarily
* Could make windows popup to tell them their clipboard equals password now
* Could consider not having Ctrl+V change the data to password, that way the clipboard data we have would be used as the password. Although if not careful the password will always be a password.  
* Add a counter so there is not a post request to the server every time there is a new piece of clipboard_data
* Rewrite the tool in C

### Resources
I consulted many resources for this project. Thank you to all of them. Some are listed in my code and can be seen in the libraries used. Some are not listed in my code but are listed in the Resources Consulted document in the GitHub.

Thank you to Red Team and the Red Team Chief for consistently helping with this project, teaching about Red Team concepts that helped in the development of this project, and for providing the example code for a C2 server which was used in this project. 

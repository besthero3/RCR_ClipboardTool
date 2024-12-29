from flask import Flask, request

app = Flask(__name__) #creates an instance of this

#TODO: ASSIGN A GLOBAL VARIABLE FOR A FILE IN THE OTHER SCRIPT SO I CAN COMMUNICATE THAT OVER HERE

#
@app.route("/output", methods=["POST"])
def get_output():
    #this request.data.decode is how I get what I am looking for, experiment with a file
    #print(request.data.decode())

    #TODO: this prints unparsed data and will work!!! with the other code that is commented out!!!
    #print(request.data)

    #IF WANTED TO COULD PROBABLY JUST SEND THE VALUES OVER INSTEAD OF SENDING A FILE OVER...
    #NOT SURE IF THIS WOULD CHANGE ANYTHING - ONE LESS RECORD ON FILE

    #files is a dictionary
    clipboard_info_file = request.files.get('file')

    #prints unprocessed input
    #file_content = clipboard_info_file.read()

    server_clipboard_file = open("server_stored_clipboard_info", "w")
    for line in clipboard_info_file:
        s = line.decode()
                #line)[2:-3]
        server_clipboard_file.write(s)
        #string slicing - slice out the first two character b' and last three \n'

    #print(file_content)

    return "thanks"

#TODO: method here that takes in a post request

def main():
    #local host on port 12345
    app.run(host="0.0.0.0", port=12345) #starts the server that we own


main()
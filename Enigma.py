#!/usr/bin/env python3
import string
import socket
import time

original_msg = """
HELLO FIELD AGENT!
COMMANDS:
    SEND-SECRET-DATA
    GET-SECRET-DATA
    GOODBYE
    """
not_understand = "I don't understand you\n" # last message
get_data = "GET-SECRET-DATA" #get data message.


def init_conn(conn, host, port):
    conn.connect((host, port))
    conn.recv(1024).decode('utf-8')


def process_message(conn): #Mapping the message recieved 26 times.
    mapping = dict()
    for j in range(26):
        mapping[j] = 26 * '?' #26 Object in the dictionary
    counter = 0
    print("working... please wait...")
    for i in range(26):
        resp = conn.recv(1024).decode('utf-8')
        if resp == not_understand: #Need only the response that is matching the encrypted commands
            resp = conn.recv(1024).decode('utf-8')
            print(resp)

            #ZIP MODULE - ZIP Takes two function and makes two lists according to the chars, if encrypted char is H in 7 , the the recieved char is Z in 19 or so
            #Char will print the char from the response - and the original msg with print the char from the original msg, could be done with extra loops


        for char, original_char in zip(resp, original_msg): #can i zip three function to one list?

            #looping through response and original message
            # CHAR equals to the letter received - ORIGINAL CHAR is a char from the Original Messgae Unencrypted
            #print(char, original_char) #Original Chars vs.Encrypted ones

            if char in string.ascii_uppercase: # if to avoid chars like - : ! , which doesnt have substring
                char_idx = string.ascii_uppercase.index(original_char)
                # INDEX OF THE ORIGINAL CHAR in the ALPHABET - MEANS if its H its 7 - as A start always with 0

                #print(char_idx) #Char_idx built from the original message , every number is the number in the alpha bet

                # INSERTING THE ENCRYPTED LETTERS TO THEIR NEEDED INDEX
                mapping[counter % 26] = "{}{}{}".format(mapping[counter % 26][:char_idx], char, mapping[counter % 26][char_idx + 1:])
                print(mapping)
            # the ":" is to HOLD the loop of 26 chars.
                # USING THE MAPPING DICTIONARY TO MAP THE LETTERS RECEIVED TO THEIR PLACE IN THE INDEX. USED SOME GOOGLE FOR MAKING THIS COMMAND WORK PROPERLY.

                counter += 1
        if i == 25:
            break

        conn.send(b'\n')
    return mapping


def request_data(conn, mappings):
    counter = 0
    encrypted_req = ''
    for char in get_data:
        if char not in string.ascii_uppercase:
            #check if char is printable - if yes adding it to encrypted_req then inside function reordering it
            encrypted_req += char
            continue
              # Organizing to lists the mapping dictionary. 26 ALPHABET STRUCTURE RECEIVED FROM ENCRYPTED MESSAGES


        encrypted_req += mappings[counter % 26][ord(char) - ord('A')]

        # [counter % 26] goes one item in the dictionary after another by the order
        # Main function is [ord(char) - ord('A')] which orders the list according the alpha bet.

        counter += 1
    encrypted_req += '\n'
    conn.send(encrypted_req.encode(encoding='utf-8')) # Sending encrypted request .
    encrypted_data = conn.recv(1024).decode('utf-8') #Received the Encrypted Flag.

    return encrypted_data


def decrypt(encrypted, mappings):
    counter = 13 # Counter equals 13 because we send a message of 13 letters , so we need to start counting from 13.
    decrypted = ''
    for char in encrypted:
        if char not in string.ascii_uppercase: #adding {_} this are regular as the flag.
            decrypted += char
            continue

        ########     DECRYPTION
        #TAKES THE MAPPINGS - WHICH IS THE ENCRYPTED FLAG SENT BY CLIENT.
        try:
            A = (chr(mappings[counter % 26].find(char))) #prints the letter location in received alpha bet.
        except ValueError:
            pass
        #Adds 65 to match the letter and decrypt it from the according to the alpha bet which is ord(A)
        decrypted += chr(mappings[counter % 26].find(char) + ord('A')) #ORD(A) is to always start from the begging of the ABC
        counter += 1
        #decrypting letter by letter and adding it to the flag.


    return decrypted


if __name__ == '__main__':
    #Processing the function
    #Done by the end of all of it
    #Opening socket to the client, requesting data and processing the messages and finally the flag.

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #REGULAR SOCKET MOD
        init_conn(s, '18.156.68.123', 80) #JUST EXPERIENCING TO HOLD THE SOCKET, I COULD DO SOCKET TIMEOUT AND IT WOULD WORK THE SAME
        m = process_message(s) # making mapping

        e = request_data(s, m)
        flag = decrypt(e, m)

    print("The flag is:", flag)



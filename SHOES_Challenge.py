from zlib import crc32 #CRC32
from struct import pack #PACK
import socket
import os
import binascii
def get_crc32(msg):
    checksum = pack(">I", crc32(msg)).hex() #function to get checksum it seems ** 32 didnt have anything to differ.
                                            # crc32 gives a check sum
                                            # CRC32 is amazing module to get the Checksum if a pack is inserted.
                                            #pack(">I", "") used for packing the number from crc32 straight to binary
                                            #cool feature i found online, same can be done with string format
                                            #Same thing done with checksum1 but in another way,
                                            #pack">I" packs the function in next arguments to whatever format u need
    print(checksum)
    checksum1 = hex(crc32(msg))[2:]
    print(checksum1)
    print(bytes.fromhex(checksum1))
    return checksum

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #opening regular socket
port = 1080
s.connect(('52.28.255.56', port))
A = '5a01fedd749c2e' #Default Message with Currect Checksum # The first message that was sent
print("Sending Message A :" + A)
s.send(bytes.fromhex(A))
A2 = (s.recv(120))
print("Response : " + A2.hex()) #The first response from the client - each time the response is different and because of checksum hint something was missing
JJ = (A2.hex()[:12])#Cutting response hex without Checksum
PP = 0x5aa400435341 #The Xor Key # XOR key found by xoring the response and the message sent from the pcap file after alot of time
#Clue for the right direction 43 53 41 Hexed = CSA
xoring = hex(int(JJ, 16) ^ PP) # xoring the message recieved with key
xoring = bytes.fromhex(xoring[2:]) # returning the message to hex with the first 0x
Asrc = (get_crc32(xoring)) # Doing checksum function on the returned xored output
B = xoring.hex() + str(Asrc) # Adding the check sum with the xored hex
print("Sending Message B : " + B) # Sending them both together
s.send(bytes.fromhex(B))
C = "5a010001c0a8ad140050624a3063" #Third message is default, as i did the math with the check sum and it was the same.
print(f"Sending Message C : {C}")
s.send(bytes.fromhex(C))
A2 = (s.recv(120))
print("Response: " + A2.hex())
print("[+] Connection Opened [+]")
request = b'''GET /Flag.jpg HTTP/1.1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36\r\nHost: en-us\r\nConnection: Keep-Alive\r\n\r\n'''
s.send(request) #just sending the request from the pcap and writing it to the file :)
A = s.recv(290) #Number of bytes until image starts
with open('Flag.jpg', 'wb') as flag:
    while True:
        data = s.recv(1024)
        if not data:
            break
        flag.write(data)
    flag.close()
    print("\n[+] --- Opening Image... --- [+]\n")
    os.system('Flag.jpg')
    print("Done - By Eddie Zaltsman")













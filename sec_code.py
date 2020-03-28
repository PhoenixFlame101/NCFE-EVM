# This program generates and check the security codes

from cryptography.fernet import Fernet
import random, string

'''
with open('codes.txt', 'r+') as file:
	file.truncate(0)
'''

# A predetermined encryption key
key = Fernet(b'hdWqJb2hS5g07BOO1nOasMHhhn_hmDdwPCyHvGSH57c=')


def code_gen():
	""" Generates 2500 unique codes and encrypts and stores them in a text file
		Run before the voting begins """
	num_of_codes = 2500
	codes = set()
	# Generates encrypted codes and adds them to a set 'codes'
	for _ in range(num_of_codes):
		rand_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
		codes.add(key.encrypt(rand_code.encode('utf-8')))
	# Adds the codes to a text file
	with open('codes.txt', 'a') as file:
		for code in list(codes):
			file.write(code.decode('utf-8') + ' ')


def checks_code(code):
	""" Checks if the code entered is valid
		Run before voting to initiate the program """
	with open('codes.txt', 'r') as file:
		a = file.readline().split()
	for x in range(len(a)):
		a[x] = key.decrypt(a[x].encode('utf-8')).decode('utf-8')
	if code in set(a):
		return True
	else:
		return False

# print(checks_code(code_gen()))

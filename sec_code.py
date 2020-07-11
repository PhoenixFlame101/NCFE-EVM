# This program generates and check the security codes

from cryptography.fernet import Fernet
import random
import string
from fpdf import FPDF


# A predetermined encryption key
key = Fernet(b'hdQqJb2hS5g07COO1nOasMHhhn_hmDdwPCyHvGSH57c=')


def pass_set(_pass):
	""" Sets the admin password to the string provided as an arguement
		No password is set by default """
	with open('admin.encrypted', 'w+') as file:
		file.write(key.encrypt(_pass.encode('utf-8')).decode('utf-8'))


def pass_is_valid(_pass):
	""" Checks if the entered password is the admin password or not """
	with open('admin.encrypted', 'r+') as admin_text:
		password = admin_text.read()
	if _pass == key.decrypt(password.encode('utf-8')).decode('utf-8'):
		return True
	else:
		return False


def code_gen(*args):
	""" Generates 2500 unique codes and encrypts and stores them in a text file
		Run before the voting begins """
	num_of_codes = 1936 if args == () else (484*args[0])
	codes = set()

	# Generates encrypted codes and adds them to a set 'codes'
	while len(codes) != num_of_codes:
		codes.add(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)))

	try:
		with open('codes.encrypted', 'r+') as text:
			text.truncate(0)
	except FileNotFoundError:
		pass

	# Adds the codes to a text file
	with open('codes.encrypted', 'a') as file:
		for code in codes:
			file.write(key.encrypt(code.encode('utf-8')).decode('utf-8')+'\n')
	return codes


def code_is_valid(code):
	""" Checks if the code entered is valid
		Run before voting to initiate the program """

	# Gets the codes from the text file
	with open('codes.encrypted', 'r') as file:
		codes = file.readlines()

	# Decrypts the codes into plaintext
	for i in range(len(codes)):
		codes[i] = key.decrypt(codes[i].encode('utf-8')).decode('utf-8')

	if code in set(codes):
		# Removes the entered codes from the file so it cannot be reused
		codes.remove(code)
		with open('codes.encrypted', 'w+') as file:
			for code in codes:
				file.write(key.encrypt(code.encode('utf-8')).decode('utf-8')+'\n')
		return True
	else:
		return False


def split(arr, n):
	""" Splits a list into a 2D array """
	for i in range(0, len(arr), n):
		yield arr[i : i+n]


def code_print(*args):
	""" Generates a PDF of codes """
	codes = list(split(list(code_gen()), 11))  # 2D array of 12 codes in each list

	# Writes the codes to a PDF file
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font('Courier', size=12)
	for row in codes:
		for code in row:
			pdf.cell(17, 6, txt=code, border=True, ln=0, align='C')
		pdf.ln()
	pdf.output('codes.pdf')


# pass_set('')
code_print()

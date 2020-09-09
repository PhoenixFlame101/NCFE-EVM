# This program generates and check the security codes

from cryptography.fernet import Fernet
import random
import string
from fpdf import FPDF
import database_linker


# A predetermined encryption key
key = Fernet(b'hdQqJb2hS5g07COO1nOasMHhhn_hmDdwPCyHvGSH57c=')


def pass_set(_pass):
	""" Sets the admin password to the string provided as an arguement
		No password is set by default """
	database_linker.add_password_to_db(key.encrypt(_pass.encode('utf-8')))


def pass_is_valid(_pass):
	""" Checks if the entered password is the admin password or not """

	# Takes the password from the MongoDB database
	password = database_linker.get_password_from_db()

	if _pass == key.decrypt(password).decode('utf-8'):
		return True
	else:
		return False


def code_gen(num_of_codes):
	""" Generates 1936 unique codes and encrypts and stores them in a text file
		Run before the voting begins """
	codes = set()

	# Generates codes and adds them to a set 'codes'
	while len(codes) != num_of_codes:
		codes.add(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)))
	plaintext_codes = codes

	# Encrypts the codes
	codes = list(map(lambda x: key.encrypt(x.encode('utf-8')), list(codes)))

	# Adds the votes to the db
	database_linker.add_codes_to_db(codes)
	database_linker.add_codes_to_used([])

	return plaintext_codes

def code_is_valid(code):
	""" Checks if the code entered is valid
		Run before voting to initiate the program """
	code = code.upper()

	# Gets the codes from the db
	codes = database_linker.get_codes_from_db()

	# Decrypts the codes into plaintext
	codes = list(map(lambda x: key.decrypt(x).decode('utf-8'), list(codes)))

	if code in set(codes):
		# Removes the entered codes from the file so it cannot be reused
		codes.remove(code)
		codes = list(map(lambda x: key.encrypt(x.encode('utf-8')), list(codes)))
		database_linker.add_codes_to_db(codes)
		database_linker.add_codes_to_used(database_linker.get_used_codes()+[key.encrypt(code.encode('utf-8'))])
		return True
	else:
		used_codes = list(map(lambda x: key.decrypt(x).decode('utf-8'), database_linker.get_used_codes()))
		return ('Already Used' if code in used_codes else 'Invalid')


def split(arr, n):
	""" Splits a list into a 2D array of lists of n elements each """
	for i in range(0, len(arr), n):
		yield arr[i : i+n]


def code_print(*args):
	""" Generates a PDF of codes """
	num_of_codes = 1936 if args == () else (484*args[0])
	codes = list(split(list(code_gen(num_of_codes)), 11))  # 2D array of 11 codes in each list

	# Writes the codes to a PDF file
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font('Courier', size=12)
	for row in codes:
		for code in row:
			pdf.cell(17, 6, txt=code, border=True, ln=0, align='C')
		pdf.ln()
	pdf.output('codes.pdf')


# pass_set('123')
# code_print()

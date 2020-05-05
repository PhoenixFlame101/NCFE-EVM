# This program generates and check the security codes

from cryptography.fernet import Fernet
import random
import string
import csv
from pandas import read_csv as html
import pdfkit
from os import remove


# A predetermined encryption key
key = Fernet(b'hdQqJb2hS5g07COO1nOasMHhhn_hmDdwPCyHvGSH57c=')


def code_gen():
	""" Generates 2500 unique codes and encrypts and stores them in a text file
		Run before the voting begins """
	num_of_codes = 2500
	codes = set()

	# Generates encrypted codes and adds them to a set 'codes'
	while len(codes) != num_of_codes:
		codes.add(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)))

	try:
		with open('codes.txt', 'r+') as text:
			text.truncate(0)
	except FileNotFoundError:
		pass

	# Adds the codes to a text file
	with open('codes.txt', 'a') as file:
		for code in list(codes):
			file.write(key.encrypt(code.encode('utf-8')).decode('utf-8') + ' ')
	return codes


def split(arr, n):
	""" Splits a list into a 2D array """
	for i in range(0, len(arr), n):
		yield arr[i:i + n]


def code_print(*args):
	""" Generates a PDF of codes """
	num_column = int([13 if args == () else args[0]][0])  # Number of columns in one page
	codes = list(split(list(code_gen()), num_column))  # Codes are split into an array of lists with *13* elements
	codes.insert(0, ['Codes'])  # To generate a heading for the column

	# Writes the codes to a CSV file
	with open('codes.csv', 'w+') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for line in codes:
			writer.writerow(line)

	# Converts the CSV to HTML, then to PDF and then deletes the CSV and HTML files
	html('codes.csv', sep=',').to_html('codes.html')
	config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
	pdfkit.from_file('codes.html', 'codes.pdf', configuration=config)
	remove('codes.csv')
	remove('codes.html')


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

# code_print()
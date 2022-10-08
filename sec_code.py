""" This module generates, encrypts, stores and retreives security codes and the admin password  """

import random
import string
from cryptography.fernet import Fernet
from fpdf import FPDF
import database_linker


# A predetermined key for symmetric AES-128 enctryption

# print(Fernet.generate_key())
key = Fernet(b'QuJyG2K9wQ9m_KIfToPma283YeGVhJaeN9G7c-IKdIk=')  # Generate a new key for a prod env


def pass_set(_pass):
    """ Sets the admin password to the string provided as an arguement
        123 is set by default """

    # Encrypts the bytes string of _pass and stores it in the db
    database_linker.add_password_to_db(key.encrypt(_pass.encode('utf-8')))


def pass_is_valid(_pass):
    """ Checks if the entered password is the admin password or not """

    # Takes the password from the MongoDB database
    password = database_linker.get_password_from_db()
    return _pass == key.decrypt(password).decode('utf-8')


def code_gen(num_of_codes):
    """ Generates 1936 unique codes and encrypts and stores them in a text file
        Run before the voting begins """

    # Generates random 5 character alphanumeric codes and adds them to a set 'codes'
    plaintext_codes = set()
    while len(plaintext_codes) != num_of_codes:
        plaintext_codes.add(''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(5)))

    # Encrypts the codes
    encrypted_codes = list(map(lambda x: key.encrypt(
        x.encode('utf-8')), list(plaintext_codes)))

    # Adds the encrypted codes to the db, along with an empty array for used codes
    added = database_linker.add_codes_to_db(encrypted_codes, first_run=True)
    database_linker.add_codes_to_used([])

    # Returns unencrypted codes which are then printed as codes.pdf
    return plaintext_codes if added else []

def code_is_valid(code):
    """ Checks if the code entered is valid
        Run before voting to initiate the program """

    # Fetches and decrypts the codes from the db
    codes = database_linker.get_codes_from_db()
    codes = list(map(lambda x: key.decrypt(x).decode('utf-8'), list(codes)))
    code = code.upper()

    # Check the provided code against the codes in the db
    if code in set(codes):
        # Removes the entered codes from the file so it cannot be reused
        codes.remove(code)

        # Reencrypts the codes and adds them back to the db
        codes = list(map(lambda x: key.encrypt(x.encode('utf-8')), list(codes)))
        database_linker.add_codes_to_db(codes)

        # Adds the used codes to the 'used_codes' collection in the db
        database_linker.add_codes_to_used(
            database_linker.get_used_codes()+[key.encrypt(code.encode('utf-8'))])
        return True

    # Determines the error code depending on whether or not the code was previously used
    used_codes = list(
        map(lambda x: key.decrypt(x).decode('utf-8'), database_linker.get_used_codes()))
    return 'Already Used' if code in used_codes else 'Invalid'


def split(arr, num):
    """ Splits a list into a 2D array of lists of n elements each """
    for i in range(0, len(arr), num):
        yield arr[i : i+num]


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

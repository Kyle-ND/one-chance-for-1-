import csv
from src.file_reader.fileReader import bankCustomers

def login(username, password):
    """
    Requires username and password to login to bank account
    You need to confirm that the account exists and that if it does,
    that the password is correct
    """
    reader = bankCustomers()

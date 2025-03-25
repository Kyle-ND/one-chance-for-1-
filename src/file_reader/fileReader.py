# DO NOT CHANGE!
def bankCustomers():
    with open('../../bankCustomers.csv', mode='r') as file:
        return file.readlines()[1:]
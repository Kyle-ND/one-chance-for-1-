def sign_up():
    """
    Sign up to register a new user. 
    You should ask for username, password, and confirm the password. 
    If the user does not exist and the passwords match, it should create a new user.
    """
    print("\nSign Up for the Bank City:\n")
    username = input("enter username: ")
    
    
    

# DO NOT CHANGE!
def write_user_data(username, password):
    """
    Write the new user data to bankCustomers.csv
    """
    new_user = f"{username},{password},-,-,-"
    try:
        with open('../../bankCustomers.csv', 'a') as file:
            file.writelines(new_user)
            file.close()
        return True
    except FileNotFoundError:
        return False

# DO NOT CHANGE!
def user_exists(username):
    """
    Check if the provided username is an existing user account
    """
    try:
        with open('../../bankCustomers.csv', 'r') as file:
            users = file.readlines()[1:]
            for user in users:
                storedUsername = user.split(',')[0]
                if storedUsername == username:
                    return True
            return False
    except FileNotFoundError:
        return False

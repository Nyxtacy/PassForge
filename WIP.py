import random
import string
import tokenize
import secrets
"""
change Lenght of password according to user(DONE)
add symbols (DONE)
check what other functions are present in string library (USELESS)
save password in a database
accessing saved password using Master Password like bitwarden
check encryption algorihtm for the database of saved passwords
Tokenization, strong password generation
add choice to select number of symbols and numbers
GUI
"""

def genereate_password(level:int,length:int,num_symbols:int,num_digits:int):
    letters=string.ascii_letters
    digits=string.digits
    symbols=string.punctuation
    #check if the number of symbols and digits is more than the total length
    if num_symbols + num_digits > length:
        print("Error: The number of symbols and digits exceeds the total password length.")
        return None
    
    list_symbols = [secrets.choice(symbols) for i in range(num_symbols)]
    list_numbers = [secrets.choice(digits) for i in range(num_digits)]
    
    remaining_length = length - len(list_symbols+list_numbers)
    if level == 1:
        password_list = [secrets.choice(letters) for i in range(length)]
    elif level == 2:
        password_list = [secrets.choice(letters) for i in range(remaining_length)] + list_numbers
    elif level == 3:
        password_list = [secrets.choice(letters) for i in range(remaining_length)] + list_numbers + list_symbols
    else:
        print("Invalid choice")
        return None

    random.shuffle(password_list)
    # Join the list into a string
    password = "".join(password_list)
    return password
2
password=genereate_password(2,10,2,3)
print(f"Generated password :{password}")
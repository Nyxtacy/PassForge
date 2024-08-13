import random
import string
import tokenize
import secrets

def genereate_password(level:int,length:int,num_symbols:int,num_digits:int):
    letters=string.ascii_letters
    digits=string.digits
    symbols=string.punctuation
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

password=genereate_password(2,10,2,3)
print(f"Generated password :{password}")
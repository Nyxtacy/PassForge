import random
import string
import secrets

def genereate_password(level:1,length:5,num_digits:0,num_symbols:0):
    
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

length = int(input("Enter length of the password: "))
print("level of password:\n1.letters only\n2.letters and numbers\n3.letters, numbers and symbols\n")
level = int(input("select level of password[1-3]: "))

num=0
symbol=0

if(level==2):
    num = int(input("Enter number of digits: "))
    
elif(level==3):
    num = int(input("Enter number of digits: "))
    symbol = int(input("Enter number of symbols: "))

password=genereate_password(level,length,num,symbol)
print(f"Generated password :{password}")
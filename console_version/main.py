import json
from logging import exception
import random
import string
from pathlib import Path
    
class Bank:
    database= 'data.json'
    data=[]
    try:
        if Path(database).exists():
            with open(database) as f:
                data=json.load(f)
        else:
            print("No Such file Exists")
    except Exception as err:
        print(f"error is {err}")


    @staticmethod
    def update():
        with open(Bank.database, 'w') as f:
            f.write(json.dumps(Bank.data, indent=4))

    @classmethod
    def __generate_account_number(cls):
        alpha = random.choice(string.ascii_uppercase)
        num = random.randint(100000, 999999)
        schar = random.choice("@#$%")

        id_list = list(alpha + str(num) + schar)
        random.shuffle(id_list)

        return "".join(id_list)

    
    def Createaccount(self):
        info={
            "name":input("Enter your name: "),
            "age":input("Enter your age: "),
            "email":input("Enter your email: "),
            "password":input("Enter your password: "),
            "Account_Number":Bank.__generate_account_number(),
            "balance":0
        }

        if int(info["age"])<18 or len(str(info["password"]))<8:
            print("You are not eligible to create an account")
        else:
            print("\nAccount created successfully\n")
            for i in info:
                print(f"{i}:{info[i]}")
            print("Note down your account number for future reference")
            Bank.data.append(info)  
            Bank.update()

    def Depositmoney(self):  
        acc_num=input("Enter you Account Number: ")
        acc_pin=input("Enter your Account Password: ") 

        userdata=[i for i in Bank.data if i["Account_Number"]==acc_num and i["password"]==acc_pin] 
        if userdata==False:
            print("Invalid Account Number or Password")
        else:
            amount=int(input("Enter the amount you want to Deposit: "))
            if amount<0:
                print("Invalid Amount")
            else:
                userdata[0]["balance"]+=amount
                Bank.update()
                print("Amount Deposited Successfully")
                print("Updated Balance:", userdata[0]['balance'])

    def Withdrawmoney(self):  
        acc_num=input("Enter you Account Number: ")
        acc_pin=input("Enter your Account Password: ") 

        userdata=[i for i in Bank.data if i["Account_Number"]==acc_num and i["password"]==acc_pin] 
        if userdata==False:
            print("Invalid Account Number or Password")
        else:
            amount=int(input("Enter the amount you want to Withdraw: "))
            if amount<0:
                print("Invalid Amount")
            else:
                if userdata[0]["balance"]<amount:
                    print("Insufficient Balance")
                    
                    
                else:
                    userdata[0]["balance"]-=amount
                    Bank.update()
                    print("Amount Withdrawn Successfully")
                    print("Updated Balance:", userdata[0]['balance'])  

    def Accountdetails(self):      
        acc_num=input("Enter you Account Number: ")    
        acc_pin=input("Enter your Account Password: ") 

        userdata=[i for i in Bank.data if i["Account_Number"]==acc_num and i["password"]==acc_pin]
        if userdata==False:
            print("Invalid Account Number or Password")
        else:
            print("Account details are as follows:-")
            for i in userdata[0]:
                print(f"{i}:{userdata[0][i]}")
                
    def Updatedetails(self):
        acc_num=input("Enter you Account Number: ")    
        acc_pin=input("Enter your Account Password: ") 

        userdata=[i for i in Bank.data if i["Account_Number"]==acc_num and i["password"]==acc_pin]
        if userdata==False:
            print("Invalid Account Number or Password")
        else:
            print("What d you want to update?")
            print("Press 1 for updating your name")
            print("Press 2 for updating your email")
            print("Press 3 for updating your password")
            choice_change=int(input("Enter your choice: "))
            if choice_change==1:
                new_name=input("Enter your name:")
                userdata[0]["name"]=new_name
                Bank.update()
                print("Name updated successfully")
            elif choice_change==2:
                new_email=input("Enter your email:")
                userdata[0]["email"]=new_email
                Bank.update()
                print("Email updated successfully")
            elif choice_change==3:
                new_password=input("Enter your password:")
                if len(new_password)<8:
                    print("Password must be at least 8 characters long")
                else:
                    userdata[0]["password"]=new_password
                    Bank.update()
                    print("Password updated successfully")
            else:
                print("Invalid choice")
                
    def Deleteaccount(self):
        acc_num = input("Enter your Account Number: ").strip()
        acc_pin = input("Enter your Password: ").strip()

        userdata = None

        for i in Bank.data:
            if i["Account_Number"] == acc_num and i["password"] == acc_pin:
                userdata = i
                break

        if userdata is None:
            print("Invalid Account Number or Password")
            return

        choice_delete = input("Are you sure you want to delete your account? (Y/N): ")

        if choice_delete.lower() == 'y':
            Bank.data.remove(userdata)
            Bank.update()
            print("Account deleted successfully")
        else:
            print("Account deletion cancelled")
        
user=Bank()
print("Press 1 for creating an Account")
print("Press 2 for Depositing the Money")
print("Press 3 for Withdrawing the Money")
print("Press 4 for Account Details")
print("Press 5 for Updating the Details")
print("Press 6 for Deleting your Account")

choice = int(input("Enter your choice: "))
if choice == 1:
    user.Createaccount()

if choice == 2:
    user.Depositmoney() 

if choice==3:
    user.Withdrawmoney() 

if choice==4:
    user.Accountdetails()

if choice==5:
    user.Updatedetails()    

if choice==6:
    user.Deleteaccount()    

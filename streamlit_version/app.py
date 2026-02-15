import streamlit as st
import json
import random
import string
from pathlib import Path

class Bank:
    database = "data.json"

    def __init__(self):
        if Path(self.database).exists():
            with open(self.database, "r") as f:
                self.data = json.load(f)
        else:
            self.data = []

    def update(self):
        with open(self.database, "w") as f:
            json.dump(self.data, f, indent=4)

    def generate_account_number(self):
        alpha = random.choice(string.ascii_uppercase)
        num = random.randint(100000, 999999)
        schar = random.choice("@#$%")
        id_list = list(alpha + str(num) + schar)
        random.shuffle(id_list)
        return "".join(id_list)

    def create_account(self, name, age, email, password):
        if age < 18:
            return "You must be 18+ to create account"
        if len(password) < 8:
            return "Password must be at least 8 characters"

        account = {
            "name": name,
            "age": age,
            "email": email,
            "password": password,
            "Account_Number": self.generate_account_number(),
            "balance": 0
        }

        self.data.append(account)
        self.update()
        return f"Account created successfully! Your Account Number: {account['Account_Number']}"

    def authenticate(self, acc_num, password):
        for user in self.data:
            if user["Account_Number"] == acc_num and user["password"] == password:
                return user
        return None

    def deposit(self, user, amount):
        if amount <= 0:
            return "Invalid Amount"
        user["balance"] += amount
        self.update()
        return f"Deposit Successful. Updated Balance: {user['balance']}"

    def withdraw(self, user, amount):
        if amount <= 0:
            return "Invalid Amount"
        if user["balance"] < amount:
            return "Insufficient Balance"
        user["balance"] -= amount
        self.update()
        return f"Withdraw Successful. Updated Balance: {user['balance']}"

    def delete_account(self, user):
        self.data.remove(user)
        self.update()
        return "Account Deleted Successfully"


bank = Bank()

st.title("🏦 Bank Management System")

menu = st.sidebar.selectbox("Select Option", [
    "Create Account",
    "Deposit",
    "Withdraw",
    "Account Details",
    "Delete Account"
])

# ---------------- CREATE ACCOUNT ----------------

if menu == "Create Account":
    st.subheader("Create New Account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create"):
        result = bank.create_account(name, age, email, password)
        st.success(result)

# ---------------- DEPOSIT ----------------

elif menu == "Deposit":
    st.subheader("Deposit Money")
    acc = st.text_input("Account Number")
    pwd = st.text_input("Password", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        user = bank.authenticate(acc, pwd)
        if user:
            st.success(bank.deposit(user, amount))
        else:
            st.error("Invalid Credentials")

# ---------------- WITHDRAW ----------------

elif menu == "Withdraw":
    st.subheader("Withdraw Money")
    acc = st.text_input("Account Number")
    pwd = st.text_input("Password", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        user = bank.authenticate(acc, pwd)
        if user:
            st.success(bank.withdraw(user, amount))
        else:
            st.error("Invalid Credentials")

# ---------------- ACCOUNT DETAILS ----------------

elif menu == "Account Details":
    st.subheader("View Account Details")
    acc = st.text_input("Account Number")
    pwd = st.text_input("Password", type="password")

    if st.button("Show Details"):
        user = bank.authenticate(acc, pwd)
        if user:
            st.json(user)
        else:
            st.error("Invalid Credentials")

# ---------------- DELETE ----------------

elif menu == "Delete Account":
    st.subheader("Delete Account")
    acc = st.text_input("Account Number")
    pwd = st.text_input("Password", type="password")

    if st.button("Delete"):
        user = bank.authenticate(acc, pwd)
        if user:
            st.warning(bank.delete_account(user))
        else:
            st.error("Invalid Credentials")

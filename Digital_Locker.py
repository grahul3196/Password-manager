import streamlit as st
from cryptography.fernet import Fernet
import os
import random
import string

class PasswordManager:
    def __init__(self):
        self.key = self.load_key()
        self.cipher = Fernet(self.key)

    def load_key(self):
        if os.path.exists("secret.key"):
            with open("secret.key", "rb") as key_file:
                key = key_file.read()
        else:
            key = Fernet.generate_key()
            with open("secret.key", "wb") as key_file:
                key_file.write(key)
        return key

    def generate_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))

    def save_password(self, service, username, password):
        encrypted_password = self.cipher.encrypt(password.encode())
        with open(f"{service}.txt", "wb") as file:
            file.write(username.encode() + b"\n" + encrypted_password)

    def retrieve_password(self, service):
        try:
            with open(f"{service}.txt", "rb") as file:
                username = file.readline().strip().decode()
                encrypted_password = file.readline().strip()
                password = self.cipher.decrypt(encrypted_password).decode()
            return username, password
        except FileNotFoundError:
            return None, None

def main():
    st.set_page_config(page_title="Digital Locker", page_icon="🔒")
    st.title("Digital Locker")

    password_manager = PasswordManager()

    # Sidebar for actions
    action = st.sidebar.selectbox("Choose an action", ["Save Password", "Retrieve Password"])

    if action == "Save Password":
        st.header("Save Password")
        service = st.text_input("Service")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        show_password = st.checkbox("Show Password")
        
        if show_password:
            st.text(password)

        if st.button("Generate Password"):
            generated_password = password_manager.generate_password()
            st.session_state.generated_password = generated_password
            st.success(f"Generated Password: {generated_password}")

        if st.button("Save"):
            if service and username and password:
                password_manager.save_password(service, username, password)
                st.success("Yeah! I kept your secret!")
            else:
                st.warning("Please fill in all fields.")

    elif action == "Retrieve Password":
        st.header("Retrieve Password")
        service = st.text_input("Service")
        
        if st.button("Get Password"):
            if service:
                username, password = password_manager.retrieve_password(service)
                if username and password:
                    st.success(f"Username: {username}\nPassword: {password}")
                else:
                    st.warning("No password found for this service.")
            else:
                st.warning("Please enter the service name.")

if __name__ == "__main__":
    main()


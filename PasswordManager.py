import json

def encrypt(data, key):
    encrypted_data = []
    for char in data:
        encrypted_char = chr(ord(char) + key)
        encrypted_data.append(encrypted_char)
    return ''.join(encrypted_data)

def decrypt(data, key):
    decrypted_data = []
    for char in data:
        decrypted_char = chr(ord(char) - key)
        decrypted_data.append(decrypted_char)
    return ''.join(decrypted_data)

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = master_password
        self.key = len(master_password)  # Use length of master password as key
        self.file = 'passwords.json'

    def save_passwords(self, passwords):
        encrypted_passwords = {}
        for key, value in passwords.items():
            encrypted_passwords[key] = encrypt(value, self.key)
        with open(self.file, 'w') as f:
            json.dump(encrypted_passwords, f)

    def load_passwords(self):
        try:
            with open(self.file, 'r') as f:
                encrypted_passwords = json.load(f)
            decrypted_passwords = {}
            for key, value in encrypted_passwords.items():
                decrypted_passwords[key] = decrypt(value, self.key)
            return decrypted_passwords
        except FileNotFoundError:
            return {}

    def add_password(self, website, password):
        passwords = self.load_passwords()
        passwords[website] = password
        self.save_passwords(passwords)

    def get_password(self, website):
        passwords = self.load_passwords()
        return passwords.get(website, None)

if __name__ == "__main__":
    master_password = input("Enter master password: ")
    password_manager = PasswordManager(master_password)

    while True:
        print("\n1. Add a new password")
        print("2. Retrieve a password")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            website = input("Enter website: ")
            password = input("Enter password: ")
            password_manager.add_password(website, password)
            print("Password added successfully!")

        elif choice == '2':
            website = input("Enter website: ")
            password = password_manager.get_password(website)
            if password:
                print(f"Password for {website}: {password}")
            else:
                print(f"No password found for {website}")

        elif choice == '3':
            break

        else:
            print("Invalid choice. Please try again.")

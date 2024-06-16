import os
from cryptography.fernet import Fernet

# Function to generate and save a Fernet key
def generate_fernet_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)
    return key

# Function to encrypt a file with Fernet
def encrypt_file(file_name, key):
    fernet = Fernet(key)
    with open(file_name, 'rb') as file:
        file_data = file.read()
        encrypted_data = fernet.encrypt(file_data)

    encrypted_file_path = file_name + '.enc'
    with open(encrypted_file_path, 'wb') as file:
        file.write(encrypted_data)

    # Remove the original file after encryption
    os.remove(file_name)

    return encrypted_file_path

# Function to encrypt all .txt files in a directory
def encrypt_files_in_directory(directory):
    key = generate_fernet_key()  # Generate a new key for each directory operation
    try:
        encrypted_files = []
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                encrypted_file_path = encrypt_file(file_path, key)
                encrypted_files.append(encrypted_file_path)
        print("Encryption Complete. Encrypted files:")
        for file in encrypted_files:
            print(file)
    except Exception as e:
        print(f"Encryption Error: Failed to encrypt files: {str(e)}")

# Main function to run the encryption process
if __name__ == "__main__":
    # Example directory path
    directory_to_encrypt = r'C:\Users\Brak Lihou\Documents'
    # Encrypt files in the specified directory
    encrypt_files_in_directory(directory_to_encrypt)

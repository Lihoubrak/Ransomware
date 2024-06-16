import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import os
# Directory to find .enc files
directory_to_encrypt = r'C:\Users\Brak Lihou\Documents'

# Function to decrypt a file with Fernet
def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data)

    decrypted_file_path = file_path[:-4]  # Remove the '.enc' extension
    with open(decrypted_file_path, 'wb') as file:
        file.write(decrypted_data)

    # Remove the original encrypted file after decryption
    os.remove(file_path)

    return decrypted_file_path

# Function to handle decryption process
def decrypt_files_in_directory(directory, key):
    decrypted_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.enc'):
                file_path = os.path.join(root, file)
                try:
                    decrypted_file_path = decrypt_file(file_path, key.encode())
                    decrypted_files.append(decrypted_file_path)
                except Exception as e:
                    messagebox.showerror("Decryption Error", f"Failed to decrypt file {file_path}: {str(e)}")
    if decrypted_files:
        messagebox.showinfo("Decryption Complete", f"Decrypted files:\n" + "\n".join(decrypted_files))
    else:
        messagebox.showinfo("No Encrypted Files", "No .enc files found in the directory.")

# Function to handle the Enter key press event
def submit_key():
    key = key_entry.get()
    if key:
        decrypt_files_in_directory(directory_to_encrypt, key)
        app.quit()

# Setting up the GUI
app = tk.Tk()
app.title("Decryptor")
app.geometry("400x200")  # Set the window size to 400x200 pixels

# Create label and entry for Fernet key
key_label = tk.Label(app, text="Enter Key:")
key_label.pack(pady=10)

key_entry = tk.Entry(app, show='*')
key_entry.pack(pady=10)

# Create Submit button
submit_button = tk.Button(app, text="Submit", command=submit_key)
submit_button.pack(pady=20)

# Start the GUI main loop
app.mainloop()

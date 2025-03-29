# Ransomware Simulation Project Documentation

## Overview

This project simulates a ransomware attack for educational purposes. The simulation involves a client-server architecture where the client represents the ransomware that encrypts user files, and the server represents the attacker's command and control infrastructure.

## How the Ransomware Works

We send client.exe to our client through an email in hopes they execute it.  

After execution, client.exe should generate an AES secret key and encrypt the victim's files.  

After generating the AES secret key and encrypting the files with it using AES, we encrypt the secret key itself using RSA. The server is running and has a pair ready already. Client.exe requests the server's RSA public key and encrypts the AES key with it.  

If the victim sends the money (types 'done' in our case), then client.exe requests the AES secret key from the server. The server decrypts the AES secret key with its RSA private key and sends the AES secret key to the victim's PC to decrypt the files. (The files in our case are just 3 text files in the Documents folder in the victim's PC).  

Now, client.exe deletes the AES secret key from the victim's computer so that the user shall not find it and decrypt their files.

## Project Components

### Client Side (client.py)
- Generates an AES key and encrypts files in the user's Documents directory
- Fetches RSA public key from the server
- Encrypts the AES key using the RSA public key
- Sends the encrypted AES key to the server
- Deletes local copies of the keys
- Requests the decryption key after "payment" (typing 'done')
- Decrypts files when provided with the correct key

### Server Side (server.py)
- Generates RSA key pair
- Provides RSA public key to clients
- Receives and stores encrypted AES keys from clients
- Decrypts the AES key using the RSA private key
- Returns the decrypted AES key to the client upon "payment"

### Directory Structure
- **ClientFiles/**: Stores client-side generated keys
- **ServerFiles/**: Stores server-side keys and received files
- **sec_proj/**: Python virtual environment directory

## Reset Script (reset.sh)

The reset script helps to reset the environment between simulation runs:

1. Cleans up previously generated files:
   - Removes key files from the Desktop
   - Removes keys and encrypted files from ServerFiles/
   - Removes keys from ClientFiles/

2. Creates necessary directories if they don't exist:
   - ServerFiles/
   - ClientFiles/

3. Creates sample text files in the Documents folder:
   - test1.txt
   - test2.txt
   - test3.txt

4. Provides instructions for running the simulation:
   - Start the server: `python server.py`
   - Start the client: `python client.py`

## How to Run the Simulation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt


Alternatively, you can create a virtual environment:

<code in readme, idont know how to doit>
python -m venv sec_proj
source sec_proj/bin/activate  # On Linux/macOS
# or
sec_proj\Scripts\activate     # On Windows
pip install -r requirements.txt
</>

2. Reset the environment
./reset.sh

3. Start the server:
python server.py

4. Files in the ServerFiles directory will be generated accordingly
4. In another terminal, run the client:
python client.py

```markdown
# Ransomware Simulation Project Documentation

## Overview

This project simulates a ransomware attack for educational purposes. The simulation involves a client-server architecture where the client represents the ransomware that encrypts user files, and the server represents the attacker's command and control infrastructure.

## How the Ransomware Works

We send client.exe to our client through an email in hopes they execute it.  

After execution, client.exe should generate an AES secret key and encrypt the victim's files.  

After generating the AES secret key and encrypting the files with it using AES, we encrypt the secret key itself using RSA. The server is running and has a pair ready already. Client.exe requests the server's RSA public key and encrypts the AES key with it.  

If the victim sends the money (types 'done' in our case), then client.exe requests the AES secret key from the server. The server decrypts the AES secret key with its RSA private key and sends the AES secret key to the victim's PC to decrypt the files. (The files in our case are just 3 text files in the Documents folder in the victim's PC).  

Now, client.exe deletes the AES secret key from the victim's computer so that the user shall not find it and decrypt their files.

## Project Components

### Client Side (client.py)
- Generates an AES key and encrypts files in the user's Documents directory
- Fetches RSA public key from the server
- Encrypts the AES key using the RSA public key
- Sends the encrypted AES key to the server
- Deletes local copies of the keys
- Requests the decryption key after "payment" (typing 'done')
- Decrypts files when provided with the correct key

### Server Side (server.py)
- Generates RSA key pair
- Provides RSA public key to clients
- Receives and stores encrypted AES keys from clients
- Decrypts the AES key using the RSA private key
- Returns the decrypted AES key to the client upon "payment"

### Directory Structure
- **ClientFiles/**: Stores client-side generated keys
- **ServerFiles/**: Stores server-side keys and received files
- **sec_proj/**: Python virtual environment directory

## Reset Script (reset.sh)

The reset script helps to reset the environment between simulation runs:

1. Cleans up previously generated files:
   - Removes key files from the Desktop
   - Removes keys and encrypted files from ServerFiles/
   - Removes keys from ClientFiles/

2. Creates necessary directories if they don't exist:
   - ServerFiles/
   - ClientFiles/

3. Creates sample text files in the Documents folder:
   - test1.txt
   - test2.txt
   - test3.txt

4. Provides instructions for running the simulation:
   - Start the server: `python server.py`
   - Start the client: `python client.py`

## How to Run the Simulation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   Alternatively, you can create a virtual environment:
   ```bash
   python -m venv sec_proj
   source sec_proj/bin/activate  # On Linux/macOS
   # or
   sec_proj\Scripts\activate     # On Windows
   pip install -r requirements.txt
   ```

2. Reset the environment: 
   ```bash
   ./reset.sh
   ```

3. Start the server:
   ```bash
   python server.py
   ```
   Files in the ServerFiles directory will be generated accordingly

4. In another terminal, run the client:
   ```bash
   python client.py
   ```
   Files in the ClientFiles directory will be generated accordingly

5. When prompted after encryption, type 'done' to simulate payment and decrypt files

## Security Considerations

This project is for educational purposes only. It demonstrates:
- Symmetric and asymmetric encryption concepts
- Key management techniques
- Client-server communication in a threat scenario

## Requirements

Dependencies are listed in requirements.txt and include:
- Flask for server implementation
- PyCryptodome for encryption operations
- Requests for HTTP communications
```
#!/bin/bash
# filepath: /home/nour/Downloads/ransomware-assignment-main/reset.sh

echo "===== Ransomware Simulation Reset Tool ====="

# Clean up generated files
echo "Cleaning up previously generated files..."
rm -f ~/Desktop/Key.key ~/Desktop/encryptedKey.key ~/Desktop/keyPair.key
rm -f ServerFiles/*.key ServerFiles/rsa_* ServerFiles/encrypted* ServerFiles/decrypted*
rm -f ClientFiles/*.key

# Create necessary directories (if they don't exist)
mkdir -p ServerFiles ClientFiles

# Create/overwrite sample text files
echo "Creating sample text files in Documents folder..."
echo "This is a test file 1" > ~/Documents/test1.txt
echo "This is a test file 2" > ~/Documents/test2.txt
echo "This is a test file 3" > ~/Documents/test3.txt

echo "===== Reset Complete ====="
echo "To run the simulation:"
echo "1. Start the server: python server.py"
echo "2. In another terminal, run the client: python client.py"
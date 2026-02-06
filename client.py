import socket  # Provides low-level networking interface

# Vigenère cipher key (shared by client and server)
KEY = "TMU"

# --------------------------------------------------
# Encrypt plaintext using the Vigenère cipher
# --------------------------------------------------
def vigenere_encrypt(text: str, key: str = KEY) -> str:
    key = key.upper()        # Ensure key is uppercase for consistent shifts
    out = []                 # List to store encrypted characters
    ki = 0                   # Key index (tracks which key letter to use)

    # Process each character in the input text
    for ch in text:
        if ch.isalpha():     # Encrypt letters only
            
            # Select ASCII base depending on letter case
            base = ord('A') if ch.isupper() else ord('a')

            # Convert key letter into numeric shift (A=0 ... Z=25)
            shift = ord(key[ki % len(key)]) - ord('A')

            # Apply Vigenère encryption formula
            out.append(chr((ord(ch) - base + shift) % 26 + base))

            ki += 1          # Move to next key character
        else:
            # Non-letter characters are copied unchanged
            out.append(ch)

    # Convert list of characters into a string
    return "".join(out)

# --------------------------------------------------
# Decrypt ciphertext using the Vigenère cipher
# --------------------------------------------------
def vigenere_decrypt(text: str, key: str = KEY) -> str:
    key = key.upper()        # Ensure key is uppercase
    out = []                 # List to store decrypted characters
    ki = 0                   # Key index

    # Process each character in the encrypted text
    for ch in text:
        if ch.isalpha():     # Decrypt letters only
            # Select ASCII base depending on letter case
            base = ord('A') if ch.isupper() else ord('a')

            # Convert key letter into numeric shift
            shift = ord(key[ki % len(key)]) - ord('A')

            # Apply Vigenère decryption formula (reverse of encryption)
            out.append(chr((ord(ch) - base - shift) % 26 + base))

            ki += 1          # Move to next key character
        else:
            # Non-letter characters are copied unchanged
            out.append(ch)

    # Convert list of characters into a string
    return "".join(out)

# --------------------------------------------------
# Client socket setup
# --------------------------------------------------
HOST = "127.0.0.1"  # Server IP address
PORT = 9090             # Server port number

# Create TCP socket and connect to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))

    # Keep chatting until user types STOP
    while True:
        question = input("Ask Siri: ").strip()

        # Exit condition
        if question.upper() == "STOP":
            print("[CLIENT] Chat ended.")
            break

        # Encrypt the user's question before sending
        enc_q = vigenere_encrypt(question)
        print(f"[CLIENT] Encrypted question: {enc_q}")

        # Send encrypted question to the server
        client.sendall(enc_q.encode("utf-8"))

        # Receive encrypted answer from the server
        enc_a = client.recv(4096).decode("utf-8")
        print(f"[CLIENT] Encrypted answer: {enc_a}")

        # Decrypt the server's response
        dec_a = vigenere_decrypt(enc_a)
        print(f"[CLIENT] Decrypted answer: {dec_a}")

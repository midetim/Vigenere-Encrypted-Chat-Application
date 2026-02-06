import socket  

# Vigenère cipher key
KEY = "TMU"

# --------------------------------------------------
# Vigenère cipher: Encryption
# --------------------------------------------------
def vigenere_encrypt(text: str, key: str = KEY) -> str:
    key = key.upper()        # Ensure key is uppercase
    out = []                 # Store encrypted characters
    ki = 0                   # Key index (tracks which key letter to use)

    # Process each character in the text
    for ch in text:
        if ch.isalpha():     # Encrypt letters only
            # Choose correct ASCII base depending on case
            base = ord('A') if ch.isupper() else ord('a')

            # Convert key character to numeric shift (A=0 ... Z=25)
            shift = ord(key[ki % len(key)]) - ord('A')

            # Apply Vigenère encryption formula
            out.append(chr((ord(ch) - base + shift) % 26 + base))

            ki += 1          # Move to next key character
        else:
            # Preserve spaces and punctuation
            out.append(ch)

    # Convert list to string
    return "".join(out)

# --------------------------------------------------
# Vigenère cipher: Decryption
# --------------------------------------------------
def vigenere_decrypt(text: str, key: str = KEY) -> str:
    key = key.upper()        # Ensure key is uppercase
    out = []                 # Store decrypted characters
    ki = 0                   # Key index

    # Process each encrypted character
    for ch in text:
        if ch.isalpha():     # Decrypt letters only
            # Choose correct ASCII base depending on case
            base = ord('A') if ch.isupper() else ord('a')

            # Convert key character to numeric shift
            shift = ord(key[ki % len(key)]) - ord('A')

            # Apply Vigenère decryption formula (reverse of encryption)
            out.append(chr((ord(ch) - base - shift) % 26 + base))

            ki += 1          # Move to next key character
        else:
            # Preserve spaces and punctuation
            out.append(ch)

    # Convert list to string
    return "".join(out)

# --------------------------------------------------
# Siri Question / Answer Database
# --------------------------------------------------
QA = {
    "who created you?": "I was created by Apple.",
    "what does siri mean?": "Victory and beautiful.",
    "are you a robot?": "I am a virtual assistant.",
    "hello": "Hi! Ask me something.",
}

# Retrieve answer for a given question
def get_answer(question: str) -> str:
    q = question.strip().lower()   # Normalize input for matching
    return QA.get(q, "Sorry, I don't know that yet.")

# --------------------------------------------------
# Server Setup
# --------------------------------------------------
HOST = "127.0.0.1"  # Server IP address
PORT = 9090             # Port number

# Create TCP server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))     # Bind socket to address and port
# the maximum number of pending connection requests the OS will queue before your program calls
server.listen(1)              # Project 1: handle one client at a time

print(f"[SERVER] Listening on {HOST}:{PORT}")

# Main server loop (accept one client at a time)
while True:
    conn, addr = server.accept()
    print(f"\n[SERVER] Connected to {addr}")

    try:
        # Keep handling questions from the SAME client
        while True:
            enc_q = conn.recv(4096).decode("utf-8")
            if not enc_q:
                print("[SERVER] Client disconnected.")
                break

            print(f"[SERVER] Encrypted question: {enc_q}")

            dec_q = vigenere_decrypt(enc_q, KEY)
            print(f"[SERVER] Decrypted question: {dec_q}")

            if dec_q.strip().upper() == "STOP":
                print("[SERVER] STOP received. Ending chat.")
                break

            answer = get_answer(dec_q)
            enc_a = vigenere_encrypt(answer, KEY)

            print(f"[SERVER] Plain answer: {answer}")
            print(f"[SERVER] Encrypted answer: {enc_a}")

            conn.sendall(enc_a.encode("utf-8"))

    except Exception as e:
        print(f"[SERVER] Error: {e}")

    finally:
        conn.close()
        print(f"[SERVER] Connection with {addr} ended.")

import socket
import threading

KEY = "TMU"

def vigenere_encrypt(text: str, key: str = KEY) -> str:
    key = key.upper()
    out = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(key[ki % len(key)]) - ord('A')
            out.append(chr((ord(ch) - base + shift) % 26 + base))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)

def vigenere_decrypt(text: str, key: str = KEY) -> str:
    key = key.upper()
    out = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(key[ki % len(key)]) - ord('A')
            out.append(chr((ord(ch) - base - shift) % 26 + base))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)

QA = {
    "who created you?": "I was created by Apple.",
    "what does siri mean?": "Victory and beautiful.",
    "are you a robot?": "I am a virtual assistant.",
    "hello": "Hi! Ask me something.",
}

def get_answer(question: str) -> str:
    q = question.strip().lower()
    return QA.get(q, "Sorry, I don't know that yet.")

# ---- Thread handler: runs for EACH client ----
def handle_client(conn: socket.socket, addr):
    print(f"[SERVER] Client thread started for {addr}")
    try:
        while True:
            enc_q = conn.recv(4096).decode("utf-8")
            if not enc_q:
                break  # client disconnected

            print(f"[{addr}] Encrypted question: {enc_q}")
            dec_q = vigenere_decrypt(enc_q)
            print(f"[{addr}] Decrypted question: {dec_q}")

            # If client wants to stop, end chat for this client only
            if dec_q.strip().upper() == "STOP":
                enc_a = vigenere_encrypt("Goodbye!")
                conn.sendall(enc_a.encode("utf-8"))
                break

            answer = get_answer(dec_q)
            enc_a = vigenere_encrypt(answer)

            print(f"[{addr}] Plain answer: {answer}")
            print(f"[{addr}] Encrypted answer: {enc_a}")

            conn.sendall(enc_a.encode("utf-8"))

    except Exception as e:
        print(f"[SERVER] Error with {addr}: {e}")
    finally:
        conn.close()
        print(f"[SERVER] Client {addr} disconnected. Thread ending.")

# ---- Main server accepts MANY clients ----
HOST = "127.0.0.1"  # or "127.0.0.1" if same machine
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(10)  # allow a queue of connections
print(f"[SERVER] Multi-client server listening on {HOST}:{PORT}")

while True:
    # to accept multiple client
    conn, addr = server.accept()
    # Create a new thread for this client
    t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
    t.start()

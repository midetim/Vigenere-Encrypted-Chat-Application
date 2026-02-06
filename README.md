
# Secure Chat with Siri (Vigenère Cipher Client-Server)

A Python-based client-server chat application with built-in encryption using the Vigenère cipher, simulating an encrypted conversation with a Siri-like virtual assistant.

## 📁 Project Structure
'''
project/
├── client.py # Single-client implementation
├── server.py # Single-server implementation
├── project2server.py # Multi-client threaded server
└── README.md # This file
'''

## 🔐 Features

- **Vigenère Cipher Encryption**: Secure message transmission using classical cryptography
- **Dual Server Options**:
  - Single-client server (`server.py`)
  - Multi-client threaded server (`project2server.py`)
- **Siri-like Q&A Database**: Predefined responses to common questions
- **Real-time Encryption/Decryption**: Watch messages transform in the terminal
- **Clean Exit Protocol**: Proper handling of client disconnections

## 🛠️ Installation & Requirements

### Prerequisites
- Python 3.6 or higher
- No external dependencies required

## 🚀 How to Run

### Option 1: Single Client-Server (Basic)
1. **Start the server** (in one terminal):
   ```bash
   python server.py

2. Start the client (in another terminal):
   python client.py



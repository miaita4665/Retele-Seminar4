import socket
import sys

HOST = "127.0.0.1"
PORT = 3333
BUFFER_SIZE = 1024

def receive_full_message(sock):
    try:
        data = sock.recv(BUFFER_SIZE)
        if not data:
            return None

        string_data = data.decode('utf-8')
        first_space = string_data.find(' ')

        if first_space == -1:
            return string_data # Caz de eroare sau format neasteptat

        try:
            message_length = int(string_data[:first_space])
        except ValueError:
            return string_data

        full_data = string_data[first_space + 1:]
        
        # Citim restul daca mesajul e mai lung decat buffer-ul initial
        while len(full_data) < message_length:
            data = sock.recv(BUFFER_SIZE)
            if not data: break
            full_data += data.decode('utf-8')

        return full_data
    except Exception as e:
        return f"Error receiving: {e}"

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("Connected to server.")
            print("Commands: add <k> <v>, get <k>, remove <k>, list, count, clear, update <k> <v>, pop <k>, quit")

            while True:
                command = input('client> ').strip()
                if not command: continue

                s.sendall(command.encode('utf-8'))
                
                response = receive_full_message(s)
                print(f"Server response: {response}")

                if command.lower() == 'quit':
                    print("Closing connection...")
                    break
    except ConnectionRefusedError:
        print("Error: Could not connect to server. Is it running?")
    except KeyboardInterrupt:
        print("\nClient stopped.")

if __name__ == "__main__":
    main()
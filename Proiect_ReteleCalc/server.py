import socket
import random

def generateNum():
    while True:
        num = random.sample(range(10), 4)  # Generăm o listă de 4 cifre diferite
        if num[0] != 0:  # Ne asigurăm că prima cifră nu este 0
            return ''.join(map(str, num))  # Concatenăm cifrele într-un șir de caractere

def checkGuess(secret_num, guess):
    centered = 0
    non_centered = 0

    for i in range(4):
        if guess[i] == secret_num[i]:
            centered += 1
        elif guess[i] in secret_num:
            non_centered += 1

    return centered, non_centered

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8888))  # Schimbarea portului aici
    server_socket.listen(5)

    while True:
        secret_num = generateNum()
        print("Secret number:", secret_num)

        clients = []
        while True:
            client_socket, _ = server_socket.accept()
            clients.append(client_socket)
            print("New client connected")

            # Receive client name
            client_name = client_socket.recv(1024).decode()

            tries = 3  # Numărul de încercări permise
            while tries > 0:
                guess = client_socket.recv(1024).decode()

                centered, non_centered = checkGuess(secret_num, guess)

                client_socket.send(f"{centered} centered, {non_centered} non-centered\n".encode())

                if centered == 4:
                    print(f"{client_name} guessed right in {3 - tries + 1} tries!")
                    client_socket.send("Congratulations! You guessed the number!\n".encode())
                    for client in clients:
                        if client != client_socket:
                            client.send(f"{client_name} guessed right in {3 - tries + 1} tries! New secret number is {secret_num}\n".encode())
                    break

                tries -= 1
                if tries == 0 and centered != 4:
                    print(f"{client_name} ran out of tries. Number was {secret_num}")
                    client_socket.send(f"You ran out of tries. The number was {secret_num}\n".encode())
                    for client in clients:
                        if client != client_socket:
                            client.send(f"{client_name} ran out of tries. Number was {secret_num}\n".encode())
                    break

            if centered == 4:
                client_socket.send("You will need to guess the next number.\n".encode())
                break

            client_socket.close()

if __name__ == "__main__":
    main()

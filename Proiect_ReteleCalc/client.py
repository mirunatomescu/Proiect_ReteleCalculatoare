import socket

def main():
    # Adresa și portul la care se conectează clientul
    server_address = ('localhost', 8888)

    while True:
        try:
            # Conectarea la server pentru fiecare joc nou
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(server_address)

            # Întreabă utilizatorul pentru numele său
            client_name = input("Enter your name: ")
            client_socket.send(client_name.encode())

            tries = 3  # Numărul de încercări permise
            while tries > 0:
                guess = input("Enter your guess (4-digit number): ")
                if len(guess) != 4 or not guess.isdigit():
                    print("Invalid input. Please enter a 4-digit number.")
                    continue

                # Trimite numarul ghicit către server
                client_socket.send(guess.encode())

                # Primește răspunsul de la server
                response = client_socket.recv(1024).decode()
                print(response)

                # Dacă ghicirea este corectă, întrerupe bucla și continuă la următorul joc
                if "guessed right" in response:
                    break

                tries -= 1
                if tries == 0 and "guessed right" not in response:  # Verificare adăugată aici
                    print("You ran out of tries.")
                    break

            # Întrerupe conexiunea după ce jocul se încheie
            client_socket.close()

            # Întreabă utilizatorul dacă dorește să joace un alt joc
            play_again = input("Do you want to play again? (yes/no): ")
            if play_again.lower() != "yes":
                break

        except Exception as e:
            print("An error occurred:", e)
            break

if __name__ == "__main__":
    main()

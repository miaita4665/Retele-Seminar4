import socket

HOST        = '127.0.0.1'
PORT        = 9999
BUFFER_SIZE = 1024


clienti_conectati = {}
mesaje_stocate={}
id_counter=1 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print("=" * 50)
print(f"  SERVER UDP pornit pe {HOST}:{PORT}")
print("  Asteptam mesaje de la clienti...")
print("=" * 50)

while True:
    try:
        date_brute, adresa_client = server_socket.recvfrom(BUFFER_SIZE)
        mesaj_primit = date_brute.decode('utf-8').strip()

        parti = mesaj_primit.split(' ', 1)
        comanda = parti[0].upper()
        argumente = parti[1] if len(parti) > 1 else ''

        print(f"\n[PRIMIT] De la {adresa_client}: '{mesaj_primit}'")

        if comanda == 'CONNECT':
            if adresa_client in clienti_conectati:
                raspuns = "EROARE: Esti deja conectat la server."
            else:
                clienti_conectati[adresa_client] = True
                nr_clienti = len(clienti_conectati)
                raspuns = f"OK: Conectat cu succes. Clienti activi: {nr_clienti}"
                print(f"[SERVER] Client nou conectat: {adresa_client}")

        elif comanda == 'DISCONNECT':
            if adresa_client in clienti_conectati:
                del clienti_conectati[adresa_client]
                raspuns = "OK: Deconectat cu succes. La revedere!"
                print(f"[SERVER] Client deconectat: {adresa_client}")
            else:
                raspuns = "EROARE: Nu esti conectat la server."

        elif comanda == 'PUBLISH':
            if adresa_client in clienti_conectati:
                if not argumente:
                    raspuns = "EROARE: Mesajul este gol."
                else:
                    mesaje_stocate[id_counter] = {"autor": adresa_client, "text": argumente}
                    raspuns = f"OK: Mesaj publicat cu ID={id_counter}"
                    id_counter += 1
                if mesaj_primit=="":
                    raspuns = "EROARE: Mesaj gol."   
            else:
                raspuns = "EROARE: Nu esti conectat la server."

        elif comanda == 'DELETE':
            if adresa_client in clienti_conectati:
                try:
                    id_de_sters = int(argumente)
                    if id_de_sters in mesaje_stocate:
                        if mesaje_stocate[id_de_sters]["autor"] == adresa_client:
                            del mesaje_stocate[id_de_sters]
                            raspuns = f"OK: Mesajul {id_de_sters} a fost sters."
                        else:
                            raspuns = "EROARE: Nu poti sterge mesajele altora!"
                    else:
                        raspuns = f"EROARE: Mesajul cu ID={id_de_sters} nu exista."
                except ValueError:
                    raspuns = "EROARE: ID-ul trebuie sa fie un numar intreg."
            else:
                raspuns = "EROARE: Nu esti conectat la server."

        elif comanda == 'LIST':
            if adresa_client in clienti_conectati:
                if not mesaje_stocate:
                    raspuns = "INFO: Nu exista mesaje publicate."
                else:
                    linii = [f"ID {mid}: {m['text']} (de la {m['autor']})" for mid, m in mesaje_stocate.items()]
                    raspuns = "Mesaje:\n" + "\n".join(linii)
            else:
                raspuns = "EROARE: Nu esti conectat la server."

        else:
            print(f"Comanda '{comanda}' nu este recunoscuta de client.")
            print("Comenzi valide: CONNECT, DISCONNECT, PUBLISH, DELETE, LIST, EXIT")

        server_socket.sendto(raspuns.encode('utf-8'), adresa_client)
        print(f"[TRIMIS]  Catre {adresa_client}: '{raspuns}'")

    except KeyboardInterrupt:
        print("\n[SERVER] Oprire server...")
        break
    except Exception as e:
        print(f"[EROARE] {e}")

server_socket.close()
print("[SERVER] Socket inchis.")

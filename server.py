import socket
import threading
import pickle

HOST  = '127.0.0.1'
PORT = 1818

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
isimler = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{isimler[clients.index(client)]}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            isim = isimler[index]
            isimler.remove(isim)
            break
    
def receive():
    while True:
        client, address = server.accept()
        print(f"Şu adres ile bağlanıldı: {str(address)}!")

        S = "NICK"
        msg1 = pickle.dumps(S)
        client.send(msg1)
        isim = pickle.loads(client.recv(1024))

        isimler.append(isim)
        clients.append(client)

        print(f"Yeni kullanıcı bağlandı, isim: {isim}")
        message = f"{isim} Sunucuya Bağlandı\n"
        msg2 = pickle.dumps(message)
        broadcast(msg2)
        

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Sunucu çalışıyor...")
receive()

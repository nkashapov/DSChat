#!/usr/bin/python3
"""New program"""
import threading
import random
from socket import *

def manage_chat():
    global clients
    global clientsNames
    global on_work
    print("Welcome Mr.Robot!")
    print("U can use following commands:")
    print(" >>> /users      - show user of chat")
    print(" >>> /kick name  - kick user from chat")
    print(" >>> /broadcast  - send system message to all users")
    print(" >>> /help       - help messages")
    print(" >>> /exit       - shut down chat")
    print("____________________________________________________")
    on_work = True
    while on_work:
        print(" Please, write command:")
        command = str(input())
        if str(command).find('/users') != -1:
            for cl in clientsNames.values():
                print(cl)
        if str(command).find('/kick') != -1:
            vars = command.split(" ")
            print(vars[1])
            for k , v in clientsNames.items():
                if v == vars[1]:
                    k.send((">>> Good bye! You are kicked! <<<").encode())
                    clients.remove(k)
                    clientsNames.pop(k)
                    break

        if str(command).find('/broadcast') != -1:
            print("Write message to users:")
            message = str(input())
            for users in clients:
                users.send(("Server>>>"+message).encode())

        if str(command).find('/help') != -1:
            print("U can use following commands:")
            print(" >>> /users      - show user of chat")
            print(" >>> /kick name  - kick user from chat")
            print(" >>> /broadcast  - send system message to all users")
            print(" >>> /help       - help messages")
            print(" >>> /exit       - shut down chat")
            print("____________________________________________________")

        if str(command).find('/exit') != -1:
            on_work = False
            print("Shutting down.......")
            for users in clients:
                users.send(("Server>>> Good bye! I am going to sleep.").encode())
            return

def handle_client(client):
    """function for handle clients"""
    global clients
    data = str("s")
    for item in clients:
        if item != client:
            item.send((clientsNames[client] + " starts the chat! Welcome!" ).encode())
    while data:
            data = client.recv(10000).decode() # Get response
            if str(data).find('/exit') != -1 :
                    client.send((">>> Good bye! <<<").encode())
                    for item in clients:
                        if item != client:
                            item.send(("Server>>> "+clientsNames[client] + " leaves the chat!").encode())
                    namesOfClients.pop(clientsNames[client])
                    clientsNames.pop(client)
                    clients.remove(client)
                    break
            if str(data).find('/users') != -1:
                for cl in clientsNames.values():
                    client.send((cl+" \n").encode())
            for item in clients:
                if item != client:
                    item.send((clientsNames[client]+">>>"+data).encode())
    if clients.count(client) != 0:
        clients.remove(client)
    client.close()
    return

s = socket(AF_INET,SOCK_STREAM)
s.bind(("",9000))
s.listen(5)
clients=[]
clientsNames = {}
namesOfClients = {}
on_work = True
control_tr = threading.Thread(target=manage_chat)
control_tr.start()


while on_work:
    try:
        c,a = s.accept()
        print ("**** " + a[0] + " with us ****")
        name = c.recv(10000).decode()
        #print(namesOfClients.get(name))
        if namesOfClients.get(name) == None:
            namesOfClients[name] = c
        else:
           # print(str(hash(c)))
            name = name+ (str(random.randint(0,10000)))[0:6]
           # print(name)
            namesOfClients[name] = c

        c.send(("Server>>> Hello " + name + " ! ").encode())
        clients.append(c)
        clientsNames[c] = name

        t = threading.Thread(target=handle_client, args=(c,))
        t.start()
    except:
        print("Alarm!")

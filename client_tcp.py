import threading
import os
import re
from socket import *

# Thread for receiving messages
def input_client(c):
    #... whatever ...
    global on_work
    data = "s"
    while on_work:
        data = c.recv(10000).decode() # Get response
        print(data)
        if str(data).find(">>> Good bye! You are kicked! <<<") != -1:
            on_work = False
            return
    c.close()
    return

# Thread for sending messages
def output_client(c):
    #... whatever ...
    global on_work
    global userName
    while on_work:
            mes= str(input())
            if len(mes) < 1 :
                continue
            # checking commands
            if mes[0]=='/':
                    if mes == '/exit' :
                                print("Chat will be closed")
                                print("Are you sure? [y/n]")
                                answer = (str(input())[0]).lower()
                                if answer == 'y':
                                    on_work = False
                                    s.send(("/exit").encode())
                                    s.send((userName + " leaves the chat").encode())
                                    exit()
                                else :
                                    continue
                    elif mes == '/users' :
                        s.send((mes).encode())
                    elif mes == '/stickers':
                        for dirs in os.listdir("stickers"):
                            print("/" + str(dirs).replace(".txt", " "))
                    else:
                        try:
                            mes = mes.replace("/","")
                            if os.listdir("stickers").count(mes+'.txt') > 0:
                                file = open("stickers/"+mes+".txt")
                                stick = file.read()
                                s.send(stick.encode())
                                print(stick)
                            else:
                                print("Sticker does not exist!")
                                print("Available stickers")
                                for dirs in os.listdir("stickers"):
                                    print("/"+str(dirs).replace(".txt",''))
                        except:
                            print("Something goes wrong...")

            else :
                s.send((mes).encode())  # Send request
    c.close()
    return


on_work = True
userName = ""
try:
    while len(userName)==0:
        print("Hello! Please, write your name!")
        userName = str(input())
except:
    print("Error!")

print("Hello! Please, write IP address of the server(default = 0.0.0.0):")
address = "0.0.0.0"
address = str(input())
if len(address) == 0:
    address = "0.0.0.0"
while (re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", address) == None) :
    print("Please, write correct IP address")
    address = str(input())


print("Hello " + userName + "!")
print("Welcome to the chat.")
print("You can use following commands:")
print("  <> /users    ---> list of online users")
print("  <> /stickers ---> list of the stickers")
print("  <> /exit     ---> exit from the chat and programm")
print("___________________________________________________")
print("===================================================")
try:
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((address,9000)) # Connect
    s.send(userName.encode())
    t1 = threading.Thread(target=input_client, args=(s,))
    t2 = threading.Thread(target=output_client, args=(s,))
    t1.start()
    t2.start()
except:
    print("Good bye!")

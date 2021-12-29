import socket, select, sys, sched, time, threading, struct

#------------------------------------udp-part---------------------------------------------------------
while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", 13117)) 

    #this function is listening constantly to offers from servers and print annoucements about new offers
    addrs = [] 
    def get_offers(sc,s,tostop=False,previous=None): 
        data, addr = client.recvfrom(1024)
        if tostop:
            return
        if data!= None:
            (magic_cookie, massage_type, server_port) = struct.unpack('IbH',data)
            if magic_cookie=="0xabcddcba" and massage_type=="0x2":
                print("Received offer from %s, attempting to connect..." %addr[0])
                addrs.append(addr)
                return
        scheduler.enter(0, 1, get_offers, (sc,s,False,data))

    scheduler = sched.scheduler(time.time, time.sleep)
    print("Client started, listening for offer requests...") 

    scheduler.enter(0, 1, get_offers, (scheduler,client))
    scheduler.run()

    #-------------------------------------tcp-part----------------------------------------
    SERVER = "127.0.0.1" 
    PORT = 2043
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    client_name = "failure\n"
    client.sendall(bytes(client_name,'UTF-8'))

    def listen():
        time.sleep(8)
        if out_data==None:
            in_data = client.recv(1024)
            print(in_data.decode()) 


    def getInput():
        while True:
            out_data = input()
            client.sendall(bytes(out_data,'UTF-8'))

    #threading.Thread(target=listen).start()
    #threading.Thread(target=getInput).start()


    in_data = client.recv(1024)
    print(in_data.decode()) 
    out_data = input("your answer: ")
    client.sendall(bytes(out_data,'UTF-8'))
    in_data = client.recv(1024)
    print(in_data.decode())
    time.sleep(2)
    print("Server disconnected, listening for offer requests...")
    time.sleep(2)

    #client.close()
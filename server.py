import socket, threading, random, time, select, sys, concurrent.futures,struct
 
#-------------------------------server---------------------------------------------------    
class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket, msg, problem, solution):
        self.clientAddress = clientAddress
        self.msg = msg
        self.problem = problem
        self.solution = solution
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
    
    
    def get_answer(self):
        ans = self.csocket.recv(2048)
        return ans

    def find_sender(self,msg_array,address):
        for tuple in msg_array[:2]:
            if tuple[0] == address:
                sender = tuple[1]
            else:
                other_player = tuple[1]
        return ((sender,other_player))

    def run(self):
        print ("Connection from : ", self.clientAddress)
        while True:
            data = self.csocket.recv(2048)
            self.msg.append((self.clientAddress,data.decode()))
            #--------------------------------game start--------------------------------------------
            if len(self.msg) >= 1:
                #time.sleep(10)
                while (len(self.msg) != 2):
                    time.sleep(3)
                welcome_to_game = "Welcome to Quick Maths.\nPlayer 1: "+ self.msg[0][1]+"Player2: "+self.msg[1][1]+"==\nPlease answer the following question as fast as you can:\nHow much is " + self.problem + "?" 
                self.csocket.send(bytes(welcome_to_game,'utf-8'))
                for i in range(10):
                    if len(self.msg) >2:
                        break
                    time.sleep(1)
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    ans1 = executor.submit(self.get_answer)
                    ans = ans1.result()
                if ans is not None:
                    self.msg.append((self.clientAddress,ans))
                end_of_game = True
                if len(self.msg) == 2: #no respond, its a tie
                    game_over_msg = "Game over!\nThe correct answer was "+self.solution+"!\n\nno winners this time!"
                    self.csocket.send(bytes(game_over_msg,'utf-8'))
                if len(self.msg) > 2: #winner is the first correct answer
                    if int(self.msg[2][1]) == int(self.solution):
                        winner = self.find_sender(self.msg, self.clientAddress)
                        winner = winner[0]
                        game_over_msg = "Game over!\nThe correct answer was "+self.solution+"!\n\nCongratulations to the winner: "+winner
                        #time.sleep(2)
                        self.csocket.send(bytes(game_over_msg,'utf-8'))
                    else: #wrong answer the winner is the other player
                        winner = self.find_sender(self.msg,self.clientAddress)[1]
                        game_over_msg = "Game over!\nThe correct answer was "+self.solution+"!\n\nCongratulations to the winner: "+winner                
                        #time.sleep(2)
                        self.csocket.send(bytes(game_over_msg,'utf-8'))
                if end_of_game:
                    print("Game over, sending out offer requests...")
                    break
#-------------------------------udp-part---------------------------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
hostname = socket.gethostname()
# server_udp_ip = socket.gethostbyname(hostname)
server_udp_ip = '172.1.0.43'

start_message = "This is an offer announcement join to " + server_udp_ip
print("Server started, listening on IP address " + server_udp_ip)
  
def server_broadcast():
    magic_cookie = 0xabcddcba
    massage_type = 0x2
    server_port = 2043 
    while True:
        s.sendto(struct.pack('IbH',magic_cookie,massage_type,server_port), ('255.255.255.255', 13117))
        time.sleep(1)


threading.Thread(target=server_broadcast).start()

#-----------------------------tcp-part------------------------------------------------
LOCALHOST = '172.1.0.43'
PORT = 2043
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#server.bind((LOCALHOST, PORT))

def creating_game():
    math_problems = {"1+1":"2", "4+5":"9", "6+3":"9", "5*1":"5", "2*2+2":"6", "7+2*1":"9", "2+2":"4", "8+0":"8", "1+6":"7", "5+2":"7"}
    problem, solution = random.choice(list(math_problems.items()))
    msg = []
    clients_number = 0
    while True:
        server.listen(1)
        if clients_number < 2:
            clients_number += 1
            clientsock, clientAddress = server.accept()
            newthread = ClientThread(clientAddress, clientsock, msg, problem, solution)
            newthread.start()
        else:
            break

while True:            
    creating_game()   


        

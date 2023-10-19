import socket
import threading
import pika
names =["Aadya Khan","John Smith","Name Namey"]
employeeid =["123","234","567"]
overtime2020 = ["200","300","400"]
overtime2021 = ["300","400","500"]
Salary2020 = ["1000","2000","3000"]
Salary2021=["2000","3000","4000"]
Current_Entitlement = ["10","20","30"]
leaveTaken2020 = ["5","10","15"]
leaveTaken2021 = ["10","15","20"]


def callback(ch, method, properties, body):
    print( " [x] Received %r" % body )


class ClientThread(threading.Thread):

    def __init__(self,client_address,client_socket,identity):
        threading.Thread.__init__(self)
        self.c_socket = client_socket
        print("Connection no. " + str(identity))
        print("New connection added: ", client_address)



    def run(self):
      


        idChecker = 0
        IDtest = 0
        employeefinder = 0
        endChecker = 0
        validationCounter = 0
        print("Connection from : ", clientAddress)
        msg = ""

        while True:

            if IDtest !=2:
                self.c_socket.send(bytes( "What is your employee ID", 'UTF-8'))
                data = self.c_socket.recv( 2048 )
                msg = data.decode()
                IDtest = 2
            connection = pika.BlockingConnection(pika.ConnectionParameters( 'localhost' ) )
            channel = connection.channel()
            channel.queue_declare( queue="Message" )
            channel.basic_publish( exchange='', routing_key="message", body=msg)


            if msg not in employeeid and idChecker != 1:
                self.c_socket.send(bytes("I don't recognize that ID\nPress Enter To Continue",'UTF-8'))
                endChecker = 0
                idChecker = 0
                IDtest = 0
            else:
                idChecker = 1

            if idChecker == 1:
                channel.basic_publish( exchange='', routing_key="message", body=msg )
                if msg in employeeid:
                    employeefinder = employeeid.index(msg)
                if validationCounter == 0:
                    self.c_socket.sendall(bytes("Salary(S) OR Annual Leave (L) Query","UTF-8"))
                    data = self.c_socket.recv(2048)
                    msg = data.decode()
                    validationCounter = 1
                    channel.basic_publish( exchange='', routing_key="message", body=msg )



                if msg.upper() == "S" or validationCounter == 2:
                    channel.basic_publish( exchange='', routing_key="message", body=msg )

                    self.c_socket.send(bytes("Current Salary (C) or total Salary (T) for year","UTF-8"))
                    data = self.c_socket.recv( 2048 )
                    msg = data.decode()
                    validationCounter = 2

                    if msg.upper() == "C":
                        channel.basic_publish( exchange='', routing_key="message", body=msg )


                        print(msg,"Cuppa")
                        self.c_socket.sendall(bytes(f"Employee {names[employeefinder]}:\n Current basic salary {Salary2021[employeefinder]}","UTF-8"))

                        ##Server ----> Socket.send ----> Client ---> Input if Information (Pause) ----> Server
                        endChecker = 2

                    if msg.upper() == "T":
                        channel.basic_publish( exchange='', routing_key="message", body=msg )



                        self.c_socket.send( bytes( "What Year (2020 To 2021)", "UTF-8" ) )
                        data = self.c_socket.recv( 2048 )
                        msg = data.decode()
                        channel.basic_publish( exchange='', routing_key="message", body=msg )

                        if msg == "2020":
                            self.c_socket.sendall(bytes(f"Employee {names[employeefinder]}:\n Leave taken in 2020: {leaveTaken2020[employeefinder]}",'UTF-8'))


                            endChecker = 2
                        if msg == "2021":
                            self.c_socket.sendall(bytes(f"Employee {names[employeefinder]}:\n Salary in 2021: {leaveTaken2021[employeefinder]}",'UTF-8'))

                            endChecker = 2

                    elif msg.upper() != "T" and msg.upper() != "C" and validationCounter == 2 and msg != "":
                        self.c_socket.sendall( bytes( "Sorry I don't recognize that command\n", "UTF-8" ))
                        channel.basic_publish( exchange='', routing_key="message", body=msg )


                    elif msg.upper() != "C" and msg.upper != "T" and validationCounter == 2 and msg != "":
                        self.c_socket.sendall( bytes( "Sorry I don't recognize that command\n", "UTF-8" ) )
                        channel.basic_publish( exchange='', routing_key="message", body=msg )








                elif msg.upper() == "L" or validationCounter == 3:
                    channel.basic_publish( exchange='', routing_key="message", body=msg )
                    self.c_socket.sendall(bytes("Current Entitlement(C) or leave taken for year (Y)","UTF-8"))
                    data = self.c_socket.recv( 2048 )
                    msg = data.decode()
                    channel.basic_publish( exchange='', routing_key="message", body=msg )
                    validationCounter = 3
                    if msg.upper() == "C":
                        self.c_socket.sendall(bytes(f"Employee {names[employeefinder]}:\n Current annual leave entitlement: {Current_Entitlement[employeefinder]}",'UTF-8'))

                        endChecker = 2

                    if msg.upper() == "Y":

                        self.c_socket.send( bytes( "What Year (2020 To 2021)", "UTF-8" ) )

                        data = self.c_socket.recv( 2048 )
                        msg = data.decode()
                        print( msg, "Tuppa" )
                        if msg == "2020":
                            self.c_socket.sendall(bytes(f"Employee {names[employeefinder]}:\n Salary in 2020: {Salary2020[employeefinder]}, Overtime in 2020 {overtime2020[employeefinder]}",'UTF-8'))
                            print( msg, "2020Yuppa")
                            endChecker = 2
                        if msg == "2021":
                            self.c_socket.sendall(bytes(f"Employee {names[employeefinder]}:\n Salary in 2021: {Salary2021[employeefinder]}, Overtime in 2021 {overtime2021[employeefinder]}",'UTF-8'))
                            print(msg, "2021Yuppa")
                            endChecker = 2
                if endChecker == 2:
                    channel.basic_publish( exchange='', routing_key="message", body=msg)

                    msg = ""
                    self.c_socket.sendall(bytes( "Do you want to Continue (C) or exit(X)", "UTF-8" ))
                    data = self.c_socket.recv( 2048 )
                    msg = data.decode()
                    channel.basic_publish( exchange='', routing_key="message", body=msg )
                    if msg.upper() == "C":
                        idChecker = 0
                        IDtest = 0
                        employeefinder = 0
                        endChecker = 0
                        validationCounter = 0
                    elif msg.upper() == "X":
                        self.c_socket.send(bytes("Bye", "UTF-8"))





                elif msg.upper() != "L" and msg != "S" and validationCounter == 1:
                        self.c_socket.send(bytes("Sorry I don't recognize that command\n","UTF-8"))
                        channel.basic_publish( exchange='', routing_key="message", body=msg )
                        validationCounter = 0

                elif msg.upper() != "S" and msg !="L" and validationCounter == 1:
                    self.c_socket.send( bytes( "Sorry I don't recognize that command\n", "UTF-8" ) )
                    validationCounter = 0
            channel.close()








LOCALHOST = "0.0.0.0"
PORT = 64001
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server.bind((LOCALHOST,PORT))
print("Server started")
print("Waiting for client request...")

counter = 0

while True:
    server.listen(1)
    my_socket,clientAddress = server.accept()
    counter+=1
    new_thread = ClientThread(clientAddress, my_socket, counter)
    new_thread.start()


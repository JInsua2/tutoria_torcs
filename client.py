'''
This class is based on the C++ code of Daniele Loiacono

Created on  03.05.2011
@author: Thomas Fischle
@contact: fisch27@gmx.de
'''
import csv
import socket
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np

import SimplePythonClient.BaseDriver as BaseDriver
import SimplePythonClient.SimpleParser as SimpleParser
from CircularQueue import CircularQueue
from entorno import Env

SERVER_IP = "127.0.0.1"
CLIENT_PORT = 3002


explorar=True
env = Env(20)
if explorar:
    qtable = np.random.rand(env.stateCount, env.actionCount).tolist()
    epsilon = 0.8
else:
    print('Explotando')
    with open("qtable.csv") as file_name:
        qtable = np.loadtxt(file_name, delimiter=",").tolist()
        epsilon = 0

gamma = 0.01
epochs=0
decay = 0.0008
estado_anterior = 12
accion_anterior=2
# Maximal size of file read from socket
BUFSIZE = 1024

# Set default values
maxEpisodes = 10000;
maxSteps = 100000;
serverPort = 3001;
hostName = "localhost"
id = "championship2011"
stage = BaseDriver.tstage.WARMUP
trackName = "unknown"


#    noise=false
#    noiseAVG=0
#    noiseSTD=0.05
#    seed=0


class client():
    def __init__(self, driver):
        self.timeoutCounter = 0
        self.driver = driver
        tics=0

    def restart(self, msg):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", CLIENT_PORT))
        s.sendto(msg.encode(), (SERVER_IP, serverPort))

    def run(self,epsilon,qtable,estado_anterior,accion_anterior,tics,estados_acciones_circulares):

        # Bind client to UDP-Socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", CLIENT_PORT))

        print("***********************************")
        print("HOST: ", hostName)
        print("PORT: ", serverPort)
        print("ID: ", id)
        print("MAX_STEPS: ", maxSteps)
        print("epsilon: ", epsilon)
        print("epoca: ", epochs)

        if stage == BaseDriver.tstage.WARMUP:
            print("STAGE: WARMUP")
        elif BaseDriver.tstage.QUALIFYING:
            print("STAGE:QUALIFYING")
        elif BaseDriver.tstage.RACE:
            print("STAGE: RACE")
        else:
            print("STAGE: UNKNOWN")

        driver = self.driver
        sp = SimpleParser.SimpleParser()
        driver.stage = stage

        shutdownClient = False;
        msg_in = ""

        while True:
            # Initialize the angles of rangefinders
            angles = driver.getInitAngles()

            # driver.init(angles);
            initString = sp.stringify("init", angles)
            # print("Sending id to server: ", id
            initString = str(id) + initString
            print("Sending init string to the server: ", initString)
            s.sendto((initString.encode()), (SERVER_IP, serverPort))

            # Read data from socket
            try:
                # wait to connect to server, without sleep program freezes
                time.sleep(0.2)
                msg_in, (client_ip, client_port) = s.recvfrom(BUFSIZE)

                ## GONZALO
                msg_in = msg_in.decode()

                print(client_ip, " ", client_port, " received:", msg_in[:-1])  # do not print last character "\00"

                # remove last character from string, seems to be a new line
                msg_in = msg_in[:-1]

                if msg_in == "***identified***":
                    break
            except:
                print("no server running")

        currentStep = 0
        # Connected to server
        episodes = 0
        while episodes < maxEpisodes:
            try:
                msg_in, (client_ip, client_port) = s.recvfrom(BUFSIZE)

                ## GONZALO
                msg_in = msg_in.decode()

                # recTime = time.clock()
                recTime = datetime.datetime.now()
                #print("[", recTime, "]", client_ip, " ", client_port, " message received; length = ", len(msg_in))
                # remove last character from string, could be a new line character
                msg_in = msg_in[:-1]

            except:
                print("error connection lost")

            if msg_in == "***shutdown***":
                driver.onShutdown();
                shutdownClient = True
                print("Client Shutdown")
                break

            if msg_in == "***restart***":
                driver.onRestart()
                print("Client Restart")
                break

            # **************************************************
            # * Compute The Action to send to the solo race server
            # **************************************************
            currentStep = currentStep + 1
            if currentStep != maxSteps:

                action,epsilon,qtable,estado_anterior,accion_anterior,tics,estados_acciones_circulares,score = driver.Update(msg_in,epsilon,qtable,estado_anterior,accion_anterior,tics,estados_acciones_circulares)

                # write action to buffer
                #print("sending action", action)

                # create correct format
                msgBuffer = action
            else:
                # max actions reached
                msgBuffer = "(meta 1)"
            episodes += 1
            # send action
            s.sendto(msgBuffer.encode(), (SERVER_IP, serverPort))
        return epsilon,qtable,estado_anterior,accion_anterior,tics,estados_acciones_circulares,score

if __name__ == '__main__':
    # import your driver
    # import SimplePythonClient.PidDriver
    import PidDriver

    driver = PidDriver.Driver("test version 0.1")
    myclient = client(driver)
    epochs = 0
    y=[]
    x=[]
    estados_acciones_circulares=CircularQueue([12,2])
    while epochs < 300:
        tics = 10
        estado_anterior = 12
        accion_anterior = 2
        epsilon,qtable,estado_anterior,accion_anterior,tics,estados_acciones_circulares,score=myclient.run(epsilon,qtable,estado_anterior,accion_anterior,tics,estados_acciones_circulares)
        x.append(epochs)
        y.append(score)
        epochs += 1
        print(epochs,"epocaaaaaaaaaaaaaaaaaas")
        print("#############################################")
        print(score)
        print("#########################################")
    with open("qtable.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(qtable)
    plt.plot(x,y)
    plt.show()
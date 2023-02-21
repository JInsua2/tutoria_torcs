'''
A very, very simple driver which is controlled by a PID-controller.
The parameters have definitely to be tuned for a stable driver!!  

Created on 03.05.2011

@author: MrFish
@contact: fisch27@gmx.de
'''

import SimplePythonClient.BaseDriver as BaseDriver
import SimplePythonClient.CarState as CarState
import SimplePythonClient.CarControl as CarControl
import PID as PID
import client
import client as client
import numpy as np

from entorno import Env

NUMBEROFRANGEFINDERSENSORS = 19


class Driver(BaseDriver.BaseDriver):

    def __init__(self, title):
        #  print("Driver init:", title)
        self.steeringWheel = 0.0;
        self.pid = PID.PID(0.60716028172, 0.000417343004059, 34.2653431279, 0, 0, 1.0, -1.0)
        self.stuckCounter = 0
        self.bringingCartBack = 0
        self.control = CarControl.CarControl()

    def onShutdown(self):
        print("Driver: Bye bye!")

    def getInitAngles(self):
        return [-90, -80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

    def Update(self, buffer, epsilon, qtable, estado_anterior, accion_anterior, tics,estados_acciones_circulares):
        cs = CarState.CarState(buffer)
        #  print("car state: ", str(cs))
        cc, epsilon, qtable, estado_anterior, accion_anterior,estados_acciones_circulares,score = self.__wDrive(cs, epsilon, qtable, estado_anterior,
                                                                              accion_anterior,tics,estados_acciones_circulares)
        # print("execute action: ", str(cc))
        tics += 1
        return str(cc), epsilon, qtable, estado_anterior, accion_anterior, tics,estados_acciones_circulares,score

    def stuck(self, cs):
        # check if car is currently stuckCounter
        print("abs(cs.getAngle()): ", abs(cs.getAngle()), "   STUCKANGLE: ", BaseDriver.STUCKANGLE)

        # if ( abs(cs.getAngle()) > STUCKANGLE ):
        if (cs.getTrackPos() > 1.0 or cs.getTrackPos() < -1.0):
            # update stuckCounter counter
            self.stuckCounter = self.stuckCounter + 1
            self.bringingCartBack = 150
        else:
            if (self.bringingCartBack != 0):
                self.bringingCartBack = self.bringingCartBack - 1
            else:
                # if not stuckCounter reset stuckCounter counter
                self.stuckCounter = 0
        print("self.stuckCounter: ", self.stuckCounter)
        return (self.stuckCounter > BaseDriver.STUCKTIME)

    def bringCarBackOnTrack(self, cs):
        # set gear and steering command assuming car is
        # pointing in a direction out of track

        # if car is pointing in direction of the street
        if (cs.getAngle() * cs.getTrackPos() > 0.0):
            gear = 1
            steer = cs.getAngle() / 4
        # back of car is pointing into direction of street
        else:
            # to bring car parallel to track axis
            steer = - cs.getAngle() / 4  # steerLock;
            gear = -1  # gear R

        if self.bringingCartBack < 5:
            return CarControl.CarControl(0, 1.0, 0, 0, 0, 0, 0)

        # Calculate clutching
        # clutching(cs,clutch);

        # build a CarControl variable and return it
        # CarControl cc (1.0,0.0,gear,steer,clutch)
        return CarControl.CarControl(0.3, 0.0, gear, steer, 0, 0, 0)

    def calcula_estado(self, currentCarState):
        posicion = currentCarState.getTrackPos()
        angulo = currentCarState.getAngle()
        if posicion > 0.5:
            if angulo >= 0.4:
                Estado = 0
            elif angulo > 0:
                Estado = 1
            elif angulo <= 0 and angulo>-0.4:
                Estado = 2
            elif angulo <= -0.4:
                Estado = 3

        elif 0.25 < posicion <= 0.5:
            if angulo >= 0.4:
                Estado = 4
            elif angulo > 0:
                Estado = 5
            elif angulo <= 0 and angulo>-0.4:
                Estado = 6
            elif angulo <= -0.4:
                Estado = 7

        elif 0.25 >= posicion >= -0.25:
            if angulo >= 0.4:
                Estado = 8
            elif angulo > 0:
                Estado = 9
            elif 0 >= angulo > -0.4:
                Estado = 10
            elif angulo <= -0.4:
                Estado = 11

        elif -0.25 > posicion >= -0.5:
            if angulo >= 0.4:
                Estado = 12
            elif angulo > 0:
                Estado = 13
            elif angulo <= 0 and angulo>-0.4:
                Estado = 14
            elif angulo <= -0.4:
                Estado = 15

        elif posicion < -0.5:
            if angulo >= 0.4:
                Estado = 16
            elif angulo > 0:
                Estado = 17
            elif angulo <= 0 and angulo>-0.4:
                Estado = 18
            elif angulo <= -0.4:
                Estado = 19


        return Estado
    def getGirovolante(self,action):
        if action == 0:  # girar muy izquierda
            return  -0.25
        if action == 1:  # girar un poco izquierda
            return -0.05
        if action == 2:  # up
            return  0
        if action == 3:  # down
            self.accion = 0.05
        if action == 4:  # down
            return 0.25

    # put the intelligence here
    def __wDrive(self, currentCarState, epsilon, qtable, estado_anterior, accion_anterior,tics,estados_acciones_circulares):
        # chose action(s)

        # print "currentCarState.getAngle():", currentCarState.getAngle()
        # Distance between the car and the track axis. The value is
        # normalized w.r.t to the track width: it is 0 when car is on
        # the axis, -1 when the car is on the right edge of the track
        # and +1 when it is on the left edge of the car. Values greater
        # than 1 or smaller than -1 mean that the car is outside of
        # the track.
        #    | +1    0    -1 |
        #    |               |
        #    |               |
        #    |               |
        #    |               |

        # steerAction > 0 left turn
        # steerAction < 0 right turn
        state = self.calcula_estado(currentCarState)
        dentro = currentCarState.getTrackPos() >= -1 and currentCarState.getTrackPos() <= 1
        terminado = currentCarState.getDistRaced() < 1500
        action_volante = accion_anterior
        if tics % 5 == 0:
            # act randomly sometimes to allow exploration
            aleatorio=np.random.uniform()
            print('aletorio ',aleatorio)
            if  aleatorio< epsilon:
                print(("RANDOMMMMMM"))
                action_volante = client.env.randomAction()
            # if not select max action in Qtable (act greedy)
            else:
                action_volante = qtable[estado_anterior].index(max(qtable[estado_anterior]))

            reward,giro_volante = client.env.step(action_volante, currentCarState)
            print("el estado anterior: ", estado_anterior)
            print("la accion anterior: ", accion_anterior)
            print("el estado actual: ", state)
            print("el angulo de giro es ", currentCarState.getAngle())
            print("la recompensa ha sido", reward)

            print("lo q giro_volante :",giro_volante)

            # update qtable value with Bellman equation

            print(qtable[estado_anterior])
            qtable[estado_anterior][accion_anterior] = reward + client.gamma * max(qtable[state])
            print(qtable[estado_anterior])
            # update state

            # The more we learn, the less we take random actions
            epsilon -= client.decay * epsilon

            if [estado_anterior,accion_anterior] not in estados_acciones_circulares.getCola():
                estados_acciones_circulares.añadir([estado_anterior,accion_anterior])
                print('la cola es ',estados_acciones_circulares.getCola() )
        else:
            giro_volante=self.getGirovolante(accion_anterior)
        # errorTrackPos > 0 left turn
        # errorTrackPos < 0 right turn     
        # self.steeringWheel = self.pid.update(currentCarState.getTrackPos())

        # print('steeringWheel = ', self.steeringWheel, '  p=', self.pid.getKp(), '  i=', self.pid.getKi(), '    d=',
        #       self.pid.getKd())

        # Speed
        if currentCarState.getSpeedX() < 30.0:
            accel = 0.3
            gear = 1
        elif currentCarState.getSpeedX() < 90.0:
            accel = 0.4
            gear = 2
        else:
            gear = 2
            accel = 0.0

        #print("el angulo es:",currentCarState.getAngle())
        #print("la distancia es:",currentCarState.getDistRaced())
        action = CarControl.CarControl(accel, 0, gear, giro_volante, 0, 0, 0)
        """"
        if self.stuck(currentCarState):
            action=self.bringCarBackOnTrack(currentCarState)
        
        """
        # print('hlaaaaa ', currentCarState.getDistFromStart())
        if not dentro or not terminado:
            qtable[estado_anterior][accion_anterior] = 0
            castigo=-1
            atenuacion=1
           # for est_acc in estados_acciones_circulares.getCola():
            #    qtable[est_acc[0]][est_acc[1]]=castigo*atenuacion
             #   atenuacion+=-0.25
            action.setMeta(1)



        estado_anterior = state
        accion_anterior = action_volante


        # print("Action:", str(action)[-2])
        return action, epsilon, qtable, estado_anterior, accion_anterior,estados_acciones_circulares,currentCarState.getDistRaced()

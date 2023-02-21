import numpy as np


class Env:
    def __init__(self, num_estados):

        self.actions = [0, 1, 2, 3, 4]
        self.stateCount = num_estados
        self.actionCount = len(self.actions)

    # take action
    def step(self, action, currenState):
        if action == 0:  # girar muy izquierda
            self.accion = -0.25
        if action == 1:  # girar un poco izquierda
            self.accion = -0.05
        if action == 2:  # up
            self.accion = 0
        if action == 3:  # down
            self.accion = 0.05
        if action == 4:  # down
            self.accion = 0.25

        # if currenState.getDistRaced() >=objetivo:
        #    reward=100
        """""
        posicion=currenState.getTrackPos()
        if posicion > 0.5:
            Estado = "Muy_Izquierda"
            reward=0
        elif posicion > 0.25 and posicion <= 0.5:
            Estado = "Izquierda"
            reward=200
        elif posicion <= 0.25 and posicion >= -0.25:
            Estado = "Centro"
            reward=1000
        elif posicion < -0.25 and posicion >= -0.5:
            Estado = "Derecha"
            reward=200
        elif posicion < -0.5:
            Estado = "Muy_Derecha"
            reward=0
        """
        posicion = currenState.getTrackPos()
        angulo = currenState.getAngle()
        if posicion >0:
            if angulo<=0:
                reward=-0
            else:
                reward=1
        else:
            if angulo>0:
                reward=-1
            else:
                reward=1




        return reward,self.accion

    # return a random action
    def randomAction(self):
        return np.random.choice(self.actions)

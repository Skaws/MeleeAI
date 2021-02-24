import melee
import keyboard
import math
from melee.enums import Action,Button,Character
from tech.waveshine import WaveShine
from recovering.recovery import Recover,getEdgeDist
class ChainWaveShines():
    def __init__(self):
        self.shineRange = 9.9
        self.WS = WaveShine()
        self.infinite = False
        # self.WS = waveshine.WaveShine()
    #character kill percents (obtained from https://github.com/altf4/SmashBot/blob/master/Tactics/infinite.py)
    def killpercent(self,opponent_state):
        character = opponent_state.character
        if character == Character.CPTFALCON:
            return 113
        if character == Character.FALCO:
            return 103
        if character == Character.FOX:
            return 96
        if character == Character.SHEIK:
            return 92
        if character == Character.PIKACHU:
            return 73
        if character == Character.PEACH:
            return 80
        if character == Character.ZELDA:
            return 70
        if character == Character.MARTH:
            return 89
        if character == Character.JIGGLYPUFF:
            return 55
        if character == Character.SAMUS:
            return 89
        return 100
    def step(self,controller,ai_state,player_state,gamestate):
        onleft = int(ai_state.x < player_state.x)
        ledge_dist = getEdgeDist(gamestate,ai_state)
        print("can the AI infinite?" + str(self.infinite))
        print("Distance between ledge and AI " + str(ledge_dist))
        if(gamestate.distance<10):
            if(ai_state.off_stage==True or ledge_dist<20):
                self.infinite=False
            else:
                self.infinite=True
        if(self.infinite==True):
            self.WS.step(controller,ai_state,gamestate,onleft)
        else:
            controller.tilt_analog(Button.BUTTON_MAIN,onleft,0.5)
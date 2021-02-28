import melee
import keyboard
import math
from melee.enums import Action,Button,Character
from melee import framedata
from tech.waveshine import WaveShine
from tech.running import Run
from tech.punish import Punish
from recovering.recovery import Recover,getEdgeDist
class ChainWaveShines():
    def __init__(self):
        self.shineRange = 9.9
        
        self.shineDashRange = 12.2
        self.WS = WaveShine()
        self.RUN = Run()
        self.Punish = Punish()
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
    def canInfinite(self,controller,ai_state,enemy_state,gamestate):
        return True
    def step(self,controller,ai_state,enemy_state,gamestate):
        onleft = int(ai_state.x < enemy_state.x)
        ledge_dist = getEdgeDist(gamestate.stage,ai_state.x)

        # slideleft = framedata.slide_distance()
        print("can the AI infinite?" + str(self.infinite))
        #print("Player attack speed: " + str(enemy_state.speed_x_attack))
        print("AI Action: " + str(ai_state.action))
        framesleft =self.Punish.framesleft(enemy_state,ai_state,framedata)
        framesleft-=1
        print("Hitstun frames left: " +str(framesleft))
        if(gamestate.distance<10):
            if(ai_state.off_stage==True or ledge_dist<20):
                self.infinite=False
            else:
                self.infinite=True
        runstates = [Action.STANDING,Action.TURNING,Action.DASHING,Action.RUNNING]
        if(self.infinite==True):
            if(framesleft<2 and ai_state.action in runstates):
                print("worst case WaveShining")
                self.WS.step(controller,ai_state,enemy_state,gamestate.stage)
                return
            crossup = (ai_state.x<enemy_state.x<0) or (ai_state.x>enemy_state.x>0)
            if(crossup and (gamestate.distance<self.shineDashRange)):
                print("WaveShining post crossup")
                self.WS.step(controller,ai_state,enemy_state,gamestate.stage)
                return
            if(ai_state.action in runstates):
                print("Dashing to cross up")
                controller.tilt_analog(Button.BUTTON_MAIN,onleft,0.5)
                return
            else:
                print("WaveShining")
                self.WS.step(controller,ai_state,enemy_state,gamestate.stage)
                return
        else:
            dashstate = [Action.RUNNING,Action.STANDING,Action.DASHING,Action.TURNING_RUN,Action.TURNING]
            if(ai_state.action in dashstate):
                print("Running away")
                dashdir=int(ai_state.x<enemy_state.x)
                if(ledge_dist<20):
                    dashdir=int(ai_state.x<0)
                controller.tilt_analog(Button.BUTTON_MAIN,dashdir,0.5)
                return
            elif(ai_state.action==Action.EDGE_TEETERING):
                dashdir=int(ai_state.x<0)
                controller.tilt_analog(Button.BUTTON_MAIN,dashdir,0.5)
            else:
                controller.tilt_analog(Button.BUTTON_MAIN,0.5,0.5)
                
        controller.release_all()
        return
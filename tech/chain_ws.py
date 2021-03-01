import melee
import keyboard
import math
from melee.enums import Action,Button,Character
from melee import framedata
from tech.waveshine import WaveShine
from tech.running import Run
from tech.punish import Punish
from tech.smashattack import SmashAttack
from recovering.recovery import Recover,getEdgeDist
class ChainWaveShines():
    def __init__(self):
        self.shineRange = 9.9
        
        self.shineDashRange = 11.8
        self.JCUpSmash = False
        self.WS = WaveShine()
        self.RUN = Run()
        self.Punish = Punish()
        self.smashAttack = SmashAttack()
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
        #boolean variable that holds whether the AI is on the left of the player
        onleft = int(ai_state.x < enemy_state.x)
        ledge_dist = getEdgeDist(gamestate.stage,ai_state.x)

        # slideleft = framedata.slide_distance()
        #print("can the AI infinite?" + str(self.infinite))
        #print("Player attack speed: " + str(enemy_state.speed_x_attack))
        #print("AI Action: " + str(ai_state.action))
        framesleft =self.Punish.framesleft(enemy_state,ai_state,framedata)
        framesleft-=1
        killprcnt = self.killpercent(enemy_state)
        print("Hitstun frames left: " +str(framesleft))
        facingenemy = onleft==int(ai_state.facing)
        # print("is the AI to the left of the player " + str(bool(onleft)))
        # print("is the AI facing right? " + str(ai_state.facing))
        #print("Facing enemy? " + str(facingenemy))
        # print("kill percent: " +str(killprcnt))
        # print("is the current percent above the threshold?: " +str(enemy_state.percent>=15))
        # print("enemy's current percent: " + str(enemy_state.percent))
        if(gamestate.distance<10):
            if(ai_state.off_stage==True or ledge_dist<20):
                self.infinite=False
            else:
                self.infinite=True
        runstates = [Action.STANDING,Action.TURNING,Action.DASHING,Action.RUNNING]
        if(self.infinite==True):
            print("Distance between AI and Enemy" + str(gamestate.distance))
            #if the AI has barely any frames left to continue the infinite and can shine right now, shine to continue the change
            if(framesleft<3 and ai_state.action in runstates):
                #set JCUpSmash as false so it doesn't get chosen in future
                self.JCUpSmash=False
                print("worst case WaveShining")
                self.WS.step(controller,ai_state,enemy_state,gamestate.stage)
                return
            #the range of one of the AI's kill moves, UpSmash. this is the front hitbox specifically
            upsmashrange = 14
            #if the AI's at kill percent to waveshine upsmash
            if(enemy_state.percent>=killprcnt):
                #if the AI is not currently waveshining (i.e is standing/running,turning) and the enemy is in upsmash range
                if((ai_state.action in runstates) and (gamestate.distance<upsmashrange)) or (self.JCUpSmash==True):
                    #if we're facing the enemy (larger and stronger hitbox for upsmash)
                    if(facingenemy):
                        self.JCUpSmash=True
                        #call upsmash
                        print("Calling smash attack")
                        self.smashAttack.step(ai_state,enemy_state,controller,framedata)
                        return
            
            #set JCUpSmash as false so it doesn't get chosen in future
            self.JCUpSmash=False

            #this conditional checks if the enemy is between the middle of the stage and the AI (so that the AI can waveshine to centre stage)
            #either: |AI     ENEMY    CENTRE STAGE| or  |CENTRE STAGE    ENEMY     AI|
            crossup = (ai_state.x<enemy_state.x<0) or (ai_state.x>enemy_state.x>0)

            if(crossup and (gamestate.distance<self.shineRange)):
                print("WaveShining post crossup")
                print("Curr distance from enemy: "+ str(gamestate.distance))
                self.WS.step(controller,ai_state,enemy_state,gamestate.stage)
                return
            
            if(ai_state.action in runstates):
                print("Dashing to cross up")
                print("DASHING! distance from enemy: "+ str(gamestate.distance))
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
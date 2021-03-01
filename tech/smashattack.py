import melee
import keyboard
import math
from melee.enums import Action,Button,Character
from melee import framedata
from tech.waveshine import WaveShine
from tech.running import Run
from tech.punish import Punish
from recovering.recovery import Recover,getEdgeDist
class SmashAttack():
    def step(self,ai_state,enemy_state,controller,framedata):
        canSmash = [Action.STANDING,Action.TURNING,Action.RUNNING]
        if(ai_state.action == Action.DASHING):
            controller.release_all()
            print("JUMPING TO JUMP CANCEL UPSMASH")
            controller.press_button(Button.BUTTON_Y)
            return
        JCSmash = (ai_state.action==Action.KNEE_BEND)
        if(ai_state.action in canSmash) or JCSmash==True:
            controller.release_all()
            controller.tilt_analog(Button.BUTTON_MAIN,0.5,1)
            controller.press_button(Button.BUTTON_A)
            print("UpSmashing")
            return
        controller.release_all()
        return
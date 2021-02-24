import melee
import keyboard
import math
from melee.enums import Action,Button
class WaveShine():
    def __init__(self):
        self.has_shined=False
    def step(self,controller,ai_state,gamestate,dashdir):
        #list of states which consist of the AI being on the ground doing nothing
        canmultishine = [Action.STANDING, Action.TURNING]
        #if the AI is on the ground doing nothing
        if(ai_state.action in canmultishine):
            controller.press_button(Button.BUTTON_B)
            controller.tilt_analog(Button.BUTTON_MAIN,0.5,0)
            self.has_shined==True
            return
        if ai_state.action == Action.KNEE_BEND:
            if ai_state.action_frame==3:
                controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,dashdir,0.35)
                controller.press_button(melee.enums.Button.BUTTON_R)
                return
        shining = [Action.DOWN_B_STUN,Action.DOWN_B_GROUND, Action.DOWN_B_GROUND_START]       
        if(ai_state.action in shining) and ai_state.action_frame==3 and ai_state.on_ground==True:
            controller.press_button(Button.BUTTON_X)
            return
        controller.release_all()
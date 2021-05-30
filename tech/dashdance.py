import melee
import keyboard
import math
from melee.enums import Action,Button
from recovering.recovery import getEdgeDist
class DashDance():
    def step(self,controller,ai_state,enemy_state,stage):
        controllerDir = controller.prev.main_stick[0]
        dashStates = [Action.DASHING,Action.STANDING, Action.TURNING]
        turnDash = (ai_state.action_frame==Action.TURNING) and (ai_state.action_frame==1)
        print("Are we turning in dash dance? " + str(turnDash))
        if(ai_state.action not in dashStates):
            print("Not dash dancing, return to neutral dummy")
            controller.empty_input()
            return
        if(controllerDir==0.5):
            print("Setting neutral to right")
            controllerDir=1
        if(ai_state.action_frame<2) or turnDash:
            controller.tilt_analog(Button.BUTTON_MAIN,controllerDir,0.5)
            print("Same dir hold it")
            return
        else:
            print("We TURNINGG")
            controller.tilt_analog(Button.BUTTON_MAIN,1-controllerDir,0.5)
            return
        

        
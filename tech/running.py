import melee
import keyboard
import math
from melee.enums import Action,Button,Character
class Run():
    def step(self,controller,ai_state,enemy_state):
        distance = abs(ai_state.x-enemy_state.x)
        if(ai_state.action==Action.TURNING and ai_state.action_frame==1):
            return

        # if(distance)
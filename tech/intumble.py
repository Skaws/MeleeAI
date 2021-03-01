import melee
import keyboard
import math
from melee.enums import Action,Button,Character
from melee import framedata
class InTumble():
    def shouldTech(self,aiaction,onground,ypos):
        tumblestate = "DAMAGE_FLY"
        if(onground==False) and (tumblestate in str(aiaction)) and (ypos<-0.5):
            print("AI's y pos" + str(ypos))
            print("you should tech")
            return True 
        return False
    def step(self,ai_state,enemy_state,controller):
        #print("Checking if in tumble")
        controller.release_all()
        needTech = self.shouldTech(ai_state.action,ai_state.on_ground,ai_state.y)
        if(needTech==True):
            print("Teching")
            controller.press_button(Button.BUTTON_L)
            return True
        return False
import melee
import keyboard
import math
from melee.enums import Action,Button,Character
from melee import framedata
class Defense():
    def __init__(self):
        #has the AI shielded an incoming attack 
        #(track this throughout the attack frames)
        self.hasShielded = False
    #is the AI in range of the enemy's attack
    def inAttackRange(self,enemy_state,ai_state,stage,enemy_atk,frmData):
        if(enemy_atk==True):
            inRange = frmData.in_range(enemy_state,ai_state,stage)
            print("What frame will the attack hit the AI " + str(inRange))
            return inRange
        return 0
    def hitboxFrames(self,enemy_char,enemy_action,frmData):
        firstatkframe = frmData.first_hitbox_frame(enemy_char,enemy_action)
        lastatkframe = frmData.last_hitbox_frame(enemy_char,enemy_action)
        return (firstatkframe, lastatkframe)
    def step(self,controller,ai_state,enemy_atk,enemy_state,frameData):
        if(enemy_atk==True and ai_state.on_ground==True):
            (startFrame,endFrame) = self.hitboxFrames(enemy_state.character,enemy_state.action,frameData)
            print("The first frame of the opponent's attack is: " + str(startFrame))
            print("The last frame of the opponent's attack is: " + str(endFrame))
            print("Current frame of AI's attack: " + str(enemy_state.action_frame))
            print("Has the AI shielded an attack" + str(self.hasShielded))
            if(enemy_state.action_frame>endFrame):
                print("has shielded")
                self.hasShielded==True
                controller.release_all
                return
            if(enemy_state.action_frame>=(startFrame-1)):
                print("Shielding")
                controller.press_button(Button.BUTTON_R)
                return
            print("#########Move hitbox hasn't started yet#############")
            controller.release_all()
            return
        else: 
            self.hasShielded==False
            print("not shielding")
            controller.release_all()
            return
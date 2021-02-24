import melee
from melee.enums import Action,Button
import keyboard
import math

def Illusion(ai_action,controller,x,y):
    #1st element is the start of illusion, second is the middle and 3rd is post illusion
    illusion_acts = [Action.SWORD_DANCE_2_HIGH, Action.SWORD_DANCE_2_MID, Action.SWORD_DANCE_3_HIGH]
    #if the AI is not currently in illusion
    if(ai_action not in illusion_acts):
        #if we've pressed the B button on the last frame, release it so we can use it now
        if(controller.prev.button[Button.BUTTON_B]):
            controller.empty_input
            return
        #the direction the AI should illusion (travel) 
        facedir = 0
        #if this is less than 0 the AI is on the opposite side and should travel in the opposite direction
        if x<0:
            facedir=1
        controller.tilt_analog(Button.BUTTON_MAIN,facedir,0.5)
        controller.press_button(Button.BUTTON_B)
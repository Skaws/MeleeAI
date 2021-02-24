import melee
import keyboard
import math

def fireFox(aistate,controller,x,y):
    firing = "SWORD_DANCE_3_LOW" in str(aistate.action)
    #print(str(aistate.action))
    controller.release_all()
    if(firing==False):
        print("charging up")
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,1)
        controller.press_button(melee.enums.Button.BUTTON_B)
    else:
        print("angling")
        controller.tilt_analog_unit(melee.enums.Button.BUTTON_MAIN,x,y)
    print("Firefox called")
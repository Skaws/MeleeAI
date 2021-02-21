import melee
import keyboard
import math

def getEdgePos(gamestate):
    edgepos=0
    #retrieve the x coord of the edge on the stage for puff to get back to
    if(gamestate.player[2].x>0):
        edgepos = melee.stages.EDGE_POSITION[gamestate.stage]
    else:
        edgepos = -1 * melee.stages.EDGE_POSITION[gamestate.stage]
    return edgepos
def fireFox(aistate,controller,x,y):
    firing = "SWORD_DANCE_3_LOW" in str(aistate.action)
    #print(str(aistate.action))
    if(firing==False):
        print("charging up")
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,1)
        controller.press_button(melee.enums.Button.BUTTON_B)
    else:
        print("angling")
        controller.tilt_analog_unit(melee.enums.Button.BUTTON_MAIN,x,y)
    print("Firefox called")
def edgeAngleCalc(ai_pos,edgepos):
    #if the player is on the left of the stage we want positive x and negative x if the players on the right so the equation for the X distance is
    dist_x = edgepos-ai_pos[0]
    #if the player is below the stage we want positive y and negative x if the players above, so the equation for the y distance is
    dist_y = -ai_pos[1]

    normalise =  math.sqrt(((dist_y)**2) + ((dist_x)**2))
    xtilt = dist_x/normalise
    ytilt= dist_y/normalise
    return (xtilt,ytilt)

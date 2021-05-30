import melee
import keyboard
import math
import random
from .firefox import fireFox
from .illusion import Illusion
from melee.enums import Action,Button
def facingLedge(ai_facing,ai_pos):
    facing = (ai_facing == (ai_pos<0))
    return facing
def getEdgePos(currstage,aixpos):
    edgepos=0
    #retrieve the x coord of the edge on the stage for puff to get back to
    if(aixpos>0):
        edgepos = melee.stages.EDGE_POSITION[currstage]
    else:
        edgepos = -1 * melee.stages.EDGE_POSITION[currstage]
    return edgepos
def getEdgeDist(currstage,aipos_x):
    edgepos = getEdgePos(currstage,aipos_x)
    edgedist = abs(aipos_x - edgepos)
    return edgedist
def edgeAngleCalc(ai_pos,edgepos):
    #if the player is on the left of the stage we want positive x and negative x if the players on the right so the equation for the X distance is
    dist_x = edgepos-ai_pos[0]
    #if the player is below the stage we want positive y and negative x if the players above, so the equation for the y distance is
    dist_y = -ai_pos[1]

    normalise =  math.sqrt(((dist_y)**2) + ((dist_x)**2))
    xtilt = dist_x/normalise
    
    if(abs(ai_pos[0])<abs(edgepos)):
        xtilt=-xtilt
    ytilt= dist_y/normalise
    return (xtilt,ytilt)

def shouldWait(ai_pos,edgepos):
    #if the AI is too high up
    if(ai_pos[1]>88):
        #return True, they should wait until they've fallen in range
        return True
    else:
        #return False, they're in range so get over theree
        return False
def shineStall(aiaction,controller):
    if("DOWN_B" not in str(aiaction)):
        controller.tilt_analog(Button.BUTTON_MAIN,0.5,0)
        controller.press_button(Button.BUTTON_B)
    else:
        controller.release_all
def Recover(ai_state,stage,controller):
    ai_offstage = ai_state.off_stage
    edgepos=getEdgePos(stage,ai_state.x)
    aiposition = (ai_state.x,ai_state.y)
    xdir,ydir = edgeAngleCalc(aiposition,edgepos)
    #print("This is the corresponding input " + str(xdir) + "," + str(ydir))
    #print("Is the B button being pressed " + str(controller.current.button[melee.enums.Button.BUTTON_B]))
    edgedist = abs(ai_state.x - edgepos)
    if(ai_offstage==True and ai_state.hitstun_frames_left==0):
        if(ai_state.action==melee.enums.Action.EDGE_HANGING):
            #controller.release_all()
            print("Back at ledge")
            if(controller.prev.button[Button.BUTTON_A]):
                print("Releasing")
                controller.release_all()
            else:
                print("Attacking")
                controller.tilt_analog(Button.BUTTON_MAIN,1,0.5)
                controller.press_button(Button.BUTTON_A)
        else:
            print("AI current pos " + str(ai_state.y))
            TooHigh =shouldWait(aiposition,edgepos)
            
            print("is the AI too high to recover? " + str(TooHigh))
            if(TooHigh==False):
                if(-16.4 < ai_state.y < -5) and (5 < edgedist < 88):
                    Illusion(ai_state.action,controller,ai_state.x,ai_state.y)
                else:
                    print("Attempting Firefox ")
                    fireFox(ai_state,controller,xdir,ydir)
            else:
                randshine = random.randint(0,2)
                if(randshine==0):
                    print("Stalling")
                    shineStall(ai_state.action,controller)
                else:
                    controller.release_all()
    

import melee
import keyboard
import math
from .firefox import fireFox
from .illusion import Illusion
from melee.enums import Action,Button
def facingLedge(ai_facing,ai_pos):
    facing = (ai_facing == (ai_pos<0))
    return facing
def getEdgePos(gamestate):
    edgepos=0
    #retrieve the x coord of the edge on the stage for puff to get back to
    if(gamestate.player[2].x>0):
        edgepos = melee.stages.EDGE_POSITION[gamestate.stage]
    else:
        edgepos = -1 * melee.stages.EDGE_POSITION[gamestate.stage]
    return edgepos
def getEdgeDist(gamestate,ai_state):
    edgepos = getEdgePos(gamestate)
    edgedist = abs(ai_state.x - edgepos)
    return edgedist
def edgeAngleCalc(ai_pos,edgepos):
    #if the player is on the left of the stage we want positive x and negative x if the players on the right so the equation for the X distance is
    dist_x = edgepos-ai_pos[0]
    #if the player is below the stage we want positive y and negative x if the players above, so the equation for the y distance is
    dist_y = -ai_pos[1]

    normalise =  math.sqrt(((dist_y)**2) + ((dist_x)**2))
    xtilt = dist_x/normalise
    ytilt= dist_y/normalise
    return (xtilt,ytilt)
def Recover(ai_state,gamestate,controller):
    ai_offstage = ai_state.off_stage
    edgepos=getEdgePos(gamestate)
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
            if(-16.4 < ai_state.y < -5) and (5 < edgedist < 88):
                Illusion(ai_state.action,controller,ai_state.x,ai_state.y)
            else:
                print("Attempting Firefox ")
                fireFox(ai_state,controller,xdir,ydir)
    

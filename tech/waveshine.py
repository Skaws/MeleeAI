import melee
import keyboard
import math
from melee.enums import Action,Button
from recovering.recovery import getEdgeDist
class WaveShine():
    def __init__(self):
        self.has_shined=False
    def step(self,controller,ai_state,enemy_state,stage):
        #these are all the states which the AI can activate a shine out of (shine being the starter to this waveshine technique)
        canshine = [Action.STANDING, Action.TURNING,Action.RUNNING,Action.RUN_BRAKE,Action.WALK_SLOW,Action.WALK_MIDDLE,Action.WALK_FAST]
        lastdashframe = (ai_state.action==Action.DASHING) and (ai_state.action_frame>=12)
        #if the AI is in these states
        if((ai_state.action in canshine) or lastdashframe==True):
            print("SHININGG")
            controller.press_button(Button.BUTTON_B)
            controller.tilt_analog(Button.BUTTON_MAIN,0.5,0)
            self.has_shined==True
            return
        #we can't shine out of a dash so we need to turnaround
        if(ai_state.action==Action.DASHING):
            print("AI is in DASH TURNAROUND SO WE CAN DO SHIT")
            turndir = not(ai_state.facing)
            print("AI is currently facing left? " +str(ai_state.facing))
            print("AI's new direction is currently facing left? " +str(turndir))
            controller.release_button(Button.BUTTON_B)
            controller.tilt_analog(Button.BUTTON_MAIN,turndir,0.5)
            return 
        jumpcancel = (ai_state.action == Action.KNEE_BEND) and (ai_state.action_frame==3)
        #if the AI is in jumpsquat
        if (jumpcancel==True):
            p2launchspeed = enemy_state.speed_x_attack
            dashdir = int(p2launchspeed>0)
            onleft = int(ai_state.x < enemy_state.x)
            
            if(abs(p2launchspeed)<0.01):
                print("LOCATION TRACKING - going where AI ISSS")
                dashdir=onleft
            # dashdir = int(ai_state.x < enemy_state.x)
            #edgepos = Recover.getEdgePos(gamestate.stage,ai_state.x)
            
            edgedist = getEdgeDist(stage,ai_state.x)
            if(edgedist<1 or ai_state.off_stage==True):
                print("airdodge backk")
                dashdir=int(ai_state.x<0)
            controller.tilt_analog(Button.BUTTON_MAIN,dashdir,0.35)
            controller.press_button(Button.BUTTON_R)
            print("AI's wavedash direction: " + str(dashdir))
            return
        if (ai_state.off_stage==True):
            print("airdodge backk")
            dashdir=int(ai_state.x<0)
            controller.tilt_analog(Button.BUTTON_MAIN,dashdir,0.35)
            controller.press_button(Button.BUTTON_R)
            print("AI's wavedash direction: " + str(dashdir))
            return
        #states that constitute shining
        shining = [Action.DOWN_B_STUN,Action.DOWN_B_GROUND, Action.DOWN_B_GROUND_START]       
        if(ai_state.action in shining) and ai_state.action_frame==3 and ai_state.on_ground==True:
            controller.press_button(Button.BUTTON_X)
            return
        if(ai_state.action==Action.LANDING_SPECIAL):
            controller.release_all()
            return
        print("NO case met, releasing buttons")
        controller.release_all()
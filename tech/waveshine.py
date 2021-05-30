import melee
import keyboard
import math
from melee.enums import Action,Button
from recovering.recovery import getEdgeDist
class WaveShine():
    def __init__(self):
        self.has_shined=False
    def step(self,controller,ai_state,enemy_state,stage):
        
        print("---- WAVESHINE : This is the AIs current action " + str(ai_state.action) +" on frame: " + str(ai_state.action_frame) + "-------")
        print("---- START: IS THE R BUTTON BEING PRESSED?" + str(controller.current.button[Button.BUTTON_R]) + "-------")
        #these are all the states which the AI can activate a shine out of (shine being the starter to this waveshine technique)
        canshine = [Action.STANDING, Action.TURNING,Action.RUNNING,Action.RUN_BRAKE,Action.WALK_SLOW,Action.WALK_MIDDLE,Action.WALK_FAST]
        lastdashframe = (ai_state.action==Action.DASHING) and (ai_state.action_frame>=12)
        #if the AI is in these states
        if((ai_state.action in canshine) or lastdashframe==True):
            #activate shine
            print("SHININGG")
            controller.press_button(Button.BUTTON_B)
            controller.tilt_analog(Button.BUTTON_MAIN,0.5,0)
            self.has_shined==True
            return
        #we can't shine out of a dash so we need to turnaround
        if(ai_state.action==Action.DASHING):
            print("AI is in DASH TURNAROUND SO WE CAN DO THINGS")
            turndir = not(ai_state.facing)
            print("AI is currently facing right? " +str(ai_state.facing))
            print("AI's new direction is currently facing right? " +str(turndir))
            #release the B button if held and turn fox around
            controller.release_button(Button.BUTTON_B)
            controller.tilt_analog(Button.BUTTON_MAIN,int(turndir),0.5)
            return 
        #boolean that holds if the AI is on the last frame of jump squat
        jumpcancel = (ai_state.action == Action.KNEE_BEND) and (ai_state.action_frame==3)
        #if the AI is in jumpsquat
        if (jumpcancel==True):
            
            print("!!!!!!!!! ALERT WAVEDASH AIRDODGE TIME !!!!!!!!")
            #calculate the enemy's launch speed so we can follow where they're going
            p2launchspeed = enemy_state.speed_x_attack
            #the direction to dash in is the direction where the enemys being launched
            dashdir = int(p2launchspeed>0)
            #holds if the AI is on the left of the enemy
            onleft = int(ai_state.x < enemy_state.x)
            #if the enemy isn't currently being launched by an attack, wavedash to their current position
            if(abs(p2launchspeed)<0.01):
                print("LOCATION TRACKING - going where AI ISSS")
                dashdir=onleft
            # dashdir = int(ai_state.x < enemy_state.x)
            #edgepos = Recover.getEdgePos(gamestate.stage,ai_state.x)
            
            edgedist = getEdgeDist(stage,ai_state.x)
            print("Current edgedist: " + str(edgedist))
            if(edgedist<4 or ai_state.off_stage==True):
                print("airdodge backk")
                dashdir=int(ai_state.x<0)
            controller.tilt_analog(Button.BUTTON_MAIN,dashdir,0.35)
            controller.press_button(Button.BUTTON_R)
            
            print("---- FINISH: IS THE R BUTTON BEING PRESSED?" + str(controller.current.button[Button.BUTTON_R]) + "-------")
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
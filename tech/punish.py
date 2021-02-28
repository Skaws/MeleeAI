import melee
import keyboard
import math
from melee.enums import Action,Button,Character
class Punish():
    def framesleft(self,enemy_state,ai_state,framedata):
        if enemy_state.action==Action.STANDING:
            return 1
        if enemy_state.action==Action.SHIELD:
            return 1
        # if the enemy is in hitstun
        if enemy_state.hitstun_frames_left>0:
            return enemy_state.hitstun_frames_left
        return 0
    def canPunish(self,enemy_state,ai_state,gamestate,framedata):
        return True
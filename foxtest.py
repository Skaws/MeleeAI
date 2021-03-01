import melee
from melee.enums import Action,Button
import keyboard
import math
from melee import framedata
from recovering.recovery import Recover
from recovering.recovery import getEdgeDist
from tech.chain_ws import ChainWaveShines
from tech.waveshine import WaveShine
from tech.multishine import MultiShine
from tech.smashattack import SmashAttack
from tech.intumble import InTumble
from config import slippilocation
console = melee.Console(path=slippilocation)
controller = melee.Controller(console=console, port=1, type=melee.ControllerType.STANDARD)
console.run()
console.connect()
controller.connect()

def main():
    currStocks = 4
    #WS = WaveShine()
    chainshine = ChainWaveShines()
    tumbleCheck = InTumble()
    smashhh = SmashAttack()
    while True:
        gamestate = console.step()
        # Press buttons on your controller based on the GameState here!
        costume = 0
        if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
            # print("menu navigated")
            ai_state=gamestate.player[1]
            enemy_state=gamestate.player[2]
            #print("This is the actionable state: " + str(enemy_state.action_frame))
            print("This is the AIs current action " + str(ai_state.action) +" on frame: " + str(ai_state.action_frame))
            #print("This is the Player's current action " + str(enemy_state.action) +" on frame: " + str(enemy_state.action_frame))
            #print("This is the Players current action " + str(ai_state.action))
            #print("Is the player facing right? " + str(enemy_state.facing))
            controller.release_all()
            
            onleft = int(ai_state.x < enemy_state.x)
            if(ai_state.action==Action.ON_HALO_WAIT):
                if(controller.prev.button[Button.BUTTON_A]==True):
                    print("Releasing")
                    controller.release_all()
                else:
                    print("Attacking")
                    controller.tilt_analog(Button.BUTTON_MAIN,1,0.5)
                    controller.press_button(Button.BUTTON_A)
            elif(ai_state.off_stage==False):
                #controller.release_all()
                #MultiShine(controller,ai_state,gamestate)
                #WS.step(controller,ai_state,gamestate,onleft)
                needTech=tumbleCheck.step(ai_state, enemy_state,controller)
                if(needTech==False):
                    chainshine.step(controller,ai_state,enemy_state,gamestate)
                #print("controller currently pointing in direction: " +str(controller.current.main_stick[0]))
                #smashhh.step(ai_state,enemy_state,controller,framedata)
                #print("Curr dist: " + str(gamestate.distance))
            else:
                chainshine.infinite=False
                controller.release_all()
                if(getEdgeDist(gamestate.stage,ai_state.x)<5):
                    dashdir=int(ai_state.x<0)
                    controller.tilt_analog(Button.BUTTON_MAIN,dashdir,0.5)
                else:
                    Recover(ai_state,gamestate.stage,controller)
        else:
            # print("trying menuhelper")
            melee.menuhelper.MenuHelper.menu_helper_simple(gamestate,
                                                controller,
                                                melee.Character.FOX,
                                                melee.Stage.FINAL_DESTINATION,
                                                "",
                                                costume=costume,
                                                autostart=False,
                                                swag=False)
main()
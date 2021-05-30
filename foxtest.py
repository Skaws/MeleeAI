import melee
from melee.enums import Action,Button
import keyboard
import math
from melee import framedata
from melee.framedata import FrameData
from strategies.defensive import Defense
from recovering.recovery import Recover
from recovering.recovery import getEdgeDist
from tech.chain_ws import ChainWaveShines
from tech.waveshine import WaveShine
from tech.multishine import MultiShine
from tech.smashattack import SmashAttack
from tech.intumble import InTumble
from tech.dashdance import DashDance
from config import slippilocation
console = melee.Console(path=slippilocation)
controller = melee.Controller(console=console, port=1, type=melee.ControllerType.STANDARD)
console.run()
console.connect()
controller.connect()

chainshine = ChainWaveShines()
defense = Defense()
tumbleCheck = InTumble()
smashhh = SmashAttack()
frmData= framedata.FrameData()
dashDance = DashDance()
def stateStep(gamestate,ai_state,enemy_state,controller,frmdata):
    enemy_atk = frmData.is_attack(enemy_state.character, enemy_state.action)
    print("Is the opponent attacking: " + str(enemy_atk))
    atkhit = defense.inAttackRange(enemy_state,ai_state,gamestate.stage,enemy_atk,frmData)
    if(atkhit>0):
        defense.step(controller,ai_state,enemy_atk,enemy_state,frmData)
        return
    needTech=tumbleCheck.step(ai_state, enemy_state,controller)
    if(needTech==False):
        chainshine.step(controller,ai_state,enemy_state,gamestate)
        return
    return
def main():
    currStocks = 4
    #WS = WaveShine()
    
    maxheight=84.55013
    shielded=False
    while True:
        gamestate = console.step()
        # Press buttons on your controller based on the GameState here!
        costume = 0
        if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
            ai_state=gamestate.player[1]
            enemy_state=gamestate.player[2]
            print("This is the AIs current action " + str(ai_state.action) +" on frame: " + str(ai_state.action_frame))
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
            elif(ai_state.action==Action.EDGE_HANGING):
                print("In edgehang,getting up")
                getupdir = int(ai_state.x<0)
                print("Trying to get up in direction" +str(getupdir))
                tryingGetup = controller.prev.main_stick[0]
                print("Previously pressed getup?" +str(tryingGetup))
                if(tryingGetup==0.5):
                    print("New frame getting up")
                    controller.tilt_analog(Button.BUTTON_MAIN,getupdir,0.5)
                else:
                    print("already trying, RELEASE")
                    controller.tilt_analog(Button.BUTTON_MAIN,0.5,0.5)

            elif(ai_state.off_stage==False):
                controller.release_all()
                stateStep(gamestate,ai_state,enemy_state,controller,frmData)

                #MultiShine(controller,ai_state,gamestate)
                #WS.step(controller,ai_state,gamestate,onleft)
                #dashDance.step(controller,ai_state,enemy_state,gamestate.stage)
                # if(enemy_atk==True):
                #     firstatkframe = frmData.first_hitbox_frame(enemy_state.character,enemy_state.action)
                #     lastatkframe = frmData.last_hitbox_frame(enemy_state.character,enemy_state.action)
                #     print("The first frame of the opponet's attack is: " + str(firstatkframe))
                #     print("The last frame of the opponet's attack is: " + str(lastatkframe))
                # needTech=tumbleCheck.step(ai_state, enemy_state,controller)
                # if(needTech==False):
                #     chainshine.step(controller,ai_state,enemy_state,gamestate)
                #     print("Waveshine called, is the R button currently being pressed? "+ str(controller.current.button[Button.BUTTON_R]))

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
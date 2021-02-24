import melee
from melee.enums import Action,Button
import keyboard
import math
from recovering.recovery import Recover
from tech.chain_ws import ChainWaveShines
from tech.waveshine import WaveShine
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
    while True:
        gamestate = console.step()
        # Press buttons on your controller based on the GameState here!
        costume = 0
        if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
            # print("menu navigated")
            ai_state=gamestate.player[1]
            player_state=gamestate.player[2]
            #print("This is the actionable state: " + str(player_state.action_frame))
            print("This is the players current action " + str(player_state.action))
            
            controller.release_all()
            
            onleft = int(ai_state.x < player_state.x)
            if(ai_state.action==Action.ON_HALO_WAIT):
                if(controller.prev.button[Button.BUTTON_A]==True):
                    print("Releasing")
                    controller.release_all()
                else:
                    print("Attacking")
                    controller.tilt_analog(Button.BUTTON_MAIN,1,0.5)
                    controller.press_button(Button.BUTTON_A)
            elif(ai_state.on_ground==True):
                #WS.step(controller,ai_state,gamestate,onleft)
                chainshine.step(controller,ai_state,player_state,gamestate)
            else:
                chainshine.infinite=False
                Recover(ai_state,gamestate,controller)
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
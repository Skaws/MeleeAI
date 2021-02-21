import melee
import keyboard
import math
import recovery
console = melee.Console(path=r"E:\Documents\3rdYear\Project\FM-Slippi")
controller = melee.Controller(console=console, port=1, type=melee.ControllerType.STANDARD)
console.run()
console.connect()
controller.connect()

def main():
    currStocks = 4
    respawn=False
    while True:
        gamestate = console.step()
        # Press buttons on your controller based on the GameState here!
        costume = 0
        if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
            ai_state=gamestate.player[1]
            player_state=gamestate.player[2]
            ai_offstage = gamestate.player[1].off_stage
            #print("This is the Player's X position: " + str(gamestate.player[2].x) + "This is the Player's Y position: " + str(gamestate.player[2].y))
            # print("Current Number of stocks: " + str(gamestate.player[1].stock))
            # print("Currently tracked number of stocks: " + str(currStocks))
            #if the AI stock count has changed (i.e it's lost a stock)
            
            #print("This is the actionable state: " + str(player_state.action_frame))
            
            #print("This is the players current action " + str(player_state.action))
            controller.release_all()
            # print("Is the AI offstage? " + str(ai_offstage))
            
            edgepos=recovery.getEdgePos(gamestate)
            aiposition = (ai_state.x,ai_state.y)
            xdir,ydir = recovery.edgeAngleCalc(aiposition,edgepos)
            print("This is the corresponding input " + str(xdir) + "," + str(ydir))
            #print("Is the B button being pressed " + str(controller.current.button[melee.enums.Button.BUTTON_B]))

            if(ai_offstage==True and ai_state.hitstun_frames_left==0):
                if(ai_state.action==melee.enums.Action.EDGE_HANGING):
                    print("Back at ledge")
                    controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,1,0.5)
                else:
                    print("Attempting Firefox ")
                    recovery.fireFox(ai_state,controller,xdir,ydir)
        else:
            melee.menuhelper.MenuHelper.menu_helper_simple(gamestate,
                                                controller,
                                                melee.Character.FOX,
                                                melee.Stage.FINAL_DESTINATION,
                                                "",
                                                costume=costume,
                                                autostart=False,
                                                swag=False)
main()
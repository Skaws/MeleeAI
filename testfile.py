import melee
import keyboard
import math

console = melee.Console(path=r"E:\Documents\3rdYear\Project\FM-Slippi")
controller = melee.Controller(console=console, port=1, type=melee.ControllerType.STANDARD)
console.run()
console.connect()
controller.connect()
def atk_normal(controller,axis,dir):
    controller.press_button(melee.enums.Button.BUTTON_A)
    if(axis=="vert"):
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,dir)
    elif(axis=="hori"):
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,dir,0.5)
    else:
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,0.5)
def atk_special(controller,dir,strength):
    controller.press_button(melee.enums.Button.BUTTON_B)
    if(dir=="y"):
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,strength)
    elif(dir=="x"):
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,strength,0.5)
    else:
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,0.5)
def downB(controller):
    controller.press_button(melee.enums.Button.BUTTON_B)
    controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,0)
def simple_platdrop(controller,gamestate):
    ai_state=gamestate.player[1]
    player_state=gamestate.player[2]
    print("platdrop called")
    
    print("Curr Action " + str(ai_state.action))
    if((ai_state.action==melee.enums.Action.STANDING or ai_state.action==melee.enums.Action.CROUCH_START or ai_state.action==melee.enums.Action.LANDING) and ai_state.action_frame>2):
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,0)
        print("Trying to drop: " + str(ai_state.action_frame))
    elif((ai_state.action==melee.enums.Action.PLATFORM_DROP) and ai_state.action_frame>4) or ai_state.y<=player_state.y:
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,0.5)
        print("finished dropping")
    else:
        print("not dropping")
def platdrop(controller,currframe):
    currframe+=1
    if currframe<4:
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,0)
    elif currframe>5:
        currframe=0
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,0.5)
    return currframe
# def platdrop(controller,currframe):
#     currframe+=1
#     dropping = (controller.current.main_stick[1]==0)
#     if (dropping==False):
#         controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,0)
#     elif(currframe==3):
#         currframe=0
#         controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,0.5)
#     return currframe
def jump(controller):
    jumping = controller.current.button[melee.enums.Button.BUTTON_X]
    
    print("Jump Called")
    if (jumping==False):
        print("X button pressed")
        controller.press_button(melee.enums.Button.BUTTON_X)
    else:
        controller.release_button(melee.enums.Button.BUTTON_X)
        print("X button released")
def wavedash(controller,aistate,plyrstate):
    frameno=0
    ongnd = aistate.on_ground
    aiaction = aistate.action
    dashdir = int(aistate.x<plyrstate.x)
    jumpcheck = "JUMPING" in str(aiaction)
    dodgetime = jumpcheck==True and aistate.action_frame<3
    print("Is puff in jumpsquat:" + str(aiaction== melee.enums.Action.KNEE_BEND))
    if(aiaction!= melee.enums.Action.KNEE_BEND and ongnd==True):
        jump(controller)
    elif(dodgetime==True):
        print("starting wavedash airdodge")
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,dashdir,0)
        controller.press_button(melee.enums.Button.BUTTON_R)
    else:
        print("resetting controls")
        controller.release_all()
# def jump(controller,frameno):
#     frameno+=1
#     print(str(frameno) + " frames after jump input")
#     if(frameno<3):
#         controller.press_button(melee.enums.Button.BUTTON_X)
#         print("pressing jump")
#     elif (frameno==4):
#         print("releasing jump after 3 frames")
#         controller.release_button(melee.enums.Button.BUTTON_X)
#     elif (frameno>4):
#         print("RELEASE + RESET")
#         controller.release_button(melee.enums.Button.BUTTON_X)
#         frameno=0
#     print(str(frameno) + " frames after jump input")
#     return frameno
# def chase_rest(controller,gamestate,jumpframe,currframe):
#     if gamestate.distance < 4:
#         downB(controller)
#     else:
#         # if the bot's x position is less than the players
#         onleft = gamestate.player[1].x < gamestate.player[2].x
#         down = (gamestate.player[1].y > gamestate.player[2].y) and (gamestate.player[1].on_ground==True)
#         if (down):
#             currframe=platdrop(controller,currframe)
#         else:
#             controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,int(onleft),0.5)
#         #release B button
#         controller.release_button(melee.enums.Button.BUTTON_B)
#         if gamestate.player[1].y < gamestate.player[2].y:
#             jumpframe = jump(controller,jumpframe)
#         else:
#             controller.release_button(melee.enums.Button.BUTTON_X)
def getEdgePos(gamestate):
    edgepos=0
    #retrieve the x coord of the edge on the stage for puff to get back to
    if(gamestate.player[1].x>0):
        edgepos = melee.stages.EDGE_POSITION[gamestate.stage]
    else:
        edgepos = -1 * melee.stages.EDGE_POSITION[gamestate.stage]
    return edgepos

def calcEdgeDist(gamestate):
    edgeDist=0
    #retrieve the x coord of the edge on the stage for puff to get back to
    if(gamestate.player[1].x>0):
        edgepos = melee.stages.EDGE_POSITION[gamestate.stage]
        edgeDist = gamestate.player[1].x - edgepos
    else:
        edgepos = -1 * melee.stages.EDGE_POSITION[gamestate.stage]
        edgeDist = -(gamestate.player[1].x - edgepos)
    
    return edgeDist

def offstage(controller,gamestate,jumpframe):
    ledgeX = getEdgePos(gamestate)
    xDist = calcEdgeDist(gamestate)
    ledgedist = math.sqrt(xDist**2 + (gamestate.player[1].y)**2)
    #print("Ledge distance: " + str(ledgedist))
    onground = gamestate.player[1].on_ground==True
    #print("AI's Y position: " + str(gamestate.player[1].y))
    
    #print("AI's X position: " + str(gamestate.player[1].x))
    
    jumping = controller.current.button[melee.enums.Button.BUTTON_X]
    #print("Ledge's X position: " + str(ledgeX))
    if ledgedist<0.1 or (gamestate.player[1].action==melee.enums.Action.EDGE_HANGING):
        print("Ledge grabbed, switching modes")
        return False
    else:
        # if the bot's x position is less than the players
        onleft = gamestate.player[1].x < ledgeX
        #print("Going right?" + str(onleft))
        sidedir =int(onleft)
        
        if gamestate.player[1].y < -17:
            #if the difference between the upper jump bound and the current y position is less than 5
            #it's likely this is the jump needed to get to ledge so ENSURE it's facing the ledge so it gets grabbed
            #only run this when it can jump otherwise it'll continue to drift towards the centre (instead of towards the ledge)
            if((gamestate.player[1].y +17)<5 and (abs(gamestate.player[1].x)<abs(ledgeX)) and jumping==False):
                print("changing direction while jumping")
                
                print("Current Direction (pre-jump change) " + str(int(onleft)))
                sidedir=abs(int(onleft) - 0.6) # this ensures it's either 0.6 when dir =0 or 0.4 when onleft =1
                print("New Direction (post-jump change) " + str(sidedir))
            print("jumping")
            jump(controller)
        else:
            print("Drifting instead")
            controller.release_button(melee.enums.Button.BUTTON_X)
        print("Drifting towards: " +str(sidedir))
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,sidedir,0.5)
        #print("direction: " + str(sidedir) )
        return True
def chaseRest(gamestate,controller,currframe):
    jumpframe=0
    
    ai_state=gamestate.player[1]
    player_state=gamestate.player[2]
    player_offstage = player_state.off_stage
    player_below = player_offstage==False and ai_state.y>player_state.y
    ai_onground=ai_state.on_ground
    onleft = gamestate.player[1].x < gamestate.player[2].x
    
    controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,0.5)
    if gamestate.distance < 4:
        downB(controller)
        # if(gamestate.player[1].off_stage==False):
        #     downB(controller)
        # else:
        #     atk_normal(controller,"right")
    else:
        #boolean variable that holds whether the player is below the AI and the AI is on the ground (thus must be on a platform)
        #down = player_below==True and ai_onground==True
        
        down = (gamestate.player[1].y > gamestate.player[2].y) and (gamestate.player[1].on_ground==True)
        #if this is the case
        if (down):
            # droppingrn = (gamestate.player[1].action==melee.enums.Action.PLATFORM_DROP)
            # print(gamestate.player[1].action)
            # print("Is Puff Dropping? " + str(droppingrn))
            print("trying to drop")
            #currframe=platdrop(controller,currframe)
            simple_platdrop(controller,gamestate)
        else:
            print("Walking")
            controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,int(onleft),0.5)
        #release B button
        controller.release_button(melee.enums.Button.BUTTON_B)
        if gamestate.player[1].y < gamestate.player[2].y:
            print("trying to jump")
            jump(controller)
        else:
            controller.release_button(melee.enums.Button.BUTTON_X)
    return currframe

def jumpBAir(gamestate,controller,thisframe):
    #boolean variable that stores whether the CPU is on the left of the player
    onleft = int(gamestate.player[1].x < gamestate.player[2].x)
    jumping = controller.current.button[melee.enums.Button.BUTTON_X]
    jumpframe=0
    
    ai_state=gamestate.player[1]
    #print("This is the frameno: " + str(thisframe) +", this is the actionable state: " + str(ai_state.action_frame))
    if(thisframe<6):
        print("Current Direction (pre-jump change) " + str(int(onleft)))
        sidedir=abs(onleft - 0.6) # this ensures it's either 0.6 when dir =0 or 0.4 when onleft =1
        print("New Direction (post-jump change) " + str(sidedir))
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,sidedir,0.5)
        jump(controller)
        thisframe+=1
    elif(thisframe>10 and thisframe<20):
        print("Inputting Attack")
        atk_normal(controller,"hori",onleft)
        thisframe+=1
    else:
        print("Resetting Jump")
        controller.release_all()
        controller.release_button(melee.enums.Button.BUTTON_X)
        thisframe=0
    return thisframe

def jumpAtk(gamestate,controller,thisframe):
    jumpframe=0
    #boolean variable that stores whether the CPU is on the left of the player
    onleft = int(gamestate.player[1].x < gamestate.player[2].x)
    #stores whether the AI is currently pressing the jump button or not
    jumping = controller.current.button[melee.enums.Button.BUTTON_X]
    attacking = controller.current.button[melee.enums.Button.BUTTON_A]
    ongnd=gamestate.player[1].on_ground
    print("Is Puff Jumping: " + str(jumping))
    ai_state=gamestate.player[1]
    print("This is the frameno: " + str(thisframe) +", this is the actionable state: " + str(ai_state.action_frame))
    if((jumping==False or thisframe<6) and (gamestate.player[1].y<gamestate.player[2].y+4)):
        print("Current Direction (pre-jump change) " + str(int(onleft)))
        sidedir=abs(onleft - 0.6) # this ensures it's either 0.6 when dir =0 or 0.4 when onleft =1
        
        print("New Direction (post-jump change) " + str(sidedir))
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,sidedir,0.5)
        print("Inputting Jump")
        jump(controller)
        thisframe+=1
    elif((jumping==True or ongnd==False) and (thisframe>5 and thisframe<10)):
        print("Inputting Attack")
        atk_normal(controller,"hori",onleft)
        thisframe+=1
    else:
        #release all currently held buttons
        
        print("Resetting Jump")
        controller.release_all()
        controller.release_button(melee.enums.Button.BUTTON_X)
        jumping=False
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,0.5,0.5)
        thisframe=0
    return thisframe
def chaseAtk(gamestate,controller,currframe,atkframe):
    jumpframe=0
    onleft = gamestate.player[1].x < gamestate.player[2].x
    if(gamestate.distance<15):
        atkframe=jumpBAir(gamestate,controller,atkframe)
    else:
        #boolean variable that holds whether the player is below the AI and the AI is on the ground (thus must be on a platform)
        down = (gamestate.player[1].y > gamestate.player[2].y) and (gamestate.player[1].on_ground==True)
        #if this is the case
        if (down):
            # droppingrn = (gamestate.player[1].action==melee.enums.Action.PLATFORM_DROP)
            # print(gamestate.player[1].action)
            # print("Is Puff Dropping? " + str(droppingrn))
            platdrop(controller,gamestate)
        else:
            controller.tilt_analog(melee.enums.Button.BUTTON_MAIN,int(onleft),0.5)
        #release B button
        controller.release_button(melee.enums.Button.BUTTON_B)
        if gamestate.player[1].y < gamestate.player[2].y:
            jump(controller)
            
        else:
            controller.release_button(melee.enums.Button.BUTTON_X)
    return currframe,atkframe
def main():
    currframe = 0
    jumpframe = 0
    atkframe = 0
    params = [currframe,atkframe]
    stayOff=False
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
            
            print("This is the players current action " + str(player_state.action))
            plyr_atk = melee.framedata.FrameData.is_attack(melee.Character.JIGGLYPUFF,ai_state.action)
            print("Is the AI attacking: " + str(plyr_atk))
            # if ("JUMPING" in str(player_state.action)):
            #     print("THAT BOI IS JUMPING")
            #controller.release_all()
            
            #wavedash(controller,ai_state,player_state)
                
            # if(currStocks!=gamestate.player[1].stock):
            #     if(gamestate.player[1].y<-15):
            #         respawn=True
            #         print("Stock lost!")
            #     else:
            #         print("Respawning from above")
            #         currStocks = gamestate.player[1].stock
            #         respawn=False
            #     currframe = 0
            #     jumpframe = 0
            #     stayOff=False
            #     #release all currently held buttons
            #     controller.release_all()

            # #calculate the distance between the AI and the edge
            # xDist = calcEdgeDist(gamestate)

            # #print("AI's X position: " + str(gamestate.player[1].x))

            # #if the AI is more than 10 units away from the edge
            # if(xDist>30 or gamestate.player[1].y<-20) and respawn==False:

            #     #start the FSM for going offstage
            #     stayOff=True

            #     print("AI gotta get back, switching modes")
            # #if the AI is more than 10 units offstage
            # if(stayOff==True):
            #     #call the offstage function until the AI grabs ledge
            #     stayOff=offstage(controller,gamestate,jumpframe)
            # # elif(ai_offstage==True):
            # #     jumpframe=chaseAtk(gamestate,controller,currframe)
            # else:
            #     # if the bot's x position is less than the players
            #     currframe=chaseRest(gamestate,controller,currframe)
        else:
            melee.menuhelper.MenuHelper.menu_helper_simple(gamestate,
                                                controller,
                                                melee.Character.JIGGLYPUFF,
                                                melee.Stage.BATTLEFIELD,
                                                "",
                                                costume=costume,
                                                autostart=False,
                                                swag=False)
main()
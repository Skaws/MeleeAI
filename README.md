# LibMelee AI
To run this you will need the following:

1.) The Slippi Dolphin Emulator

2.) The LibMelee python library

3.) An ISO file of Super Smash Bros. Melee

Both the emulator and an installation guide for the slippi dolphin emulator can be found at https://slippi.gg/netplay

The LibMelee python Library can be installed through pip using the following command: "pip3 install melee". More info can be found here: https://github.com/altf4/libmelee

The ISO file can be obtained through purchasing a copy of Super Smash Bros. Melee and using ISO extraction software to obtain the file. A multitude of methods are available which can be found here: https://ellisworkshop.com/dump-nintendo-discs-gamecube-wii-wiiu-games/

After these 3 requirements are met, create a python program called "config.py" in this folder. Within this copy paste the following code:
```
slippilocation = r"[INSERT SLIPPI FOLDER PATH]"
```
Replacing the square brackets with the path to the Slippi **folder** (not the executable)

After the config.py file has been setup, the project can now be run through running the main program: "foxtext.py". 
This will launch the Slippi Dolphin Emulator, after which the game can be started by locating and double clicking the Melee ISO file. 
After this Melee will launch and the project will begin running.

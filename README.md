# FHS
Football History Simulator v2.0

Welcome to the Football History Simulator 2.0 !
The idea is very simple: this program simulates, from team files, a whole competition ! Want to simulate a fantasy historic of the UEFA Champions League ? It's possible ! Just create team files and generate away ! The program comes included with tools to generate/modify your own team files easily (team data is stored in a xml file).
Likewise tools will be implemented to easily program competitions (competitions are executed using instructions in a json file, which currently has to be modified by hand).

Note that despite the name, the program is also designed to be modular. Want to simulate Ice Hockey instead of Football ? You will need to implement some specific classes for hockey (because team and player data differs between the two sports, not to mention that you'll need an engine able to generate hocky matches), but once you do that you can easily do it !

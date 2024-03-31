EKhelper
---------------------------
A Python-based app that should make your Emerald Kaizo experience a (little) bit easier.

![Example Image](images/example.png)

In the above example, picking Kabuto is both an offensive and defensive no-brainer! The Zubat however takes a little more planning.

![Example Image2](images/example2.png)

What it does
---------------------------
Analyzes the target trainer pokemon versus the pokemon in your party & box.
Lists the best pokemon on your team against each target pokemon, both dealing damage against foe (top row) and taking damage from foe (bottom row). Power value is not the true damage, as it considers the pokemon's base stats, type effectivities, STAB and level while ignoring IV's, natures, weather-effects and the naturally occuring 85%-100% randomness value, as well as some very rare move-specific damage boosters. Take it as a relative score! 

Also, EKhelper only considers damaging moves!

How it works
---------------------------
You will need the EK Mastersheet.txt (taken from https://drive.google.com/drive/folders/1yfYLvI5m1QMApy55VBSrJT2C0P_HGrDM) unedited, and enter the line number of the name of the trainer you are interested in, on the command-line interface. A window will appear with the results, where you can click right/left to go through the list of enemy pokemon. Highly recommend opening the master sheet with a text editor program that includes line numbers!

Setup
---------------------------
For now, you will have to clone the repository to a local folder. Create a virtual python environment that includes PIL and openpyxl. I used Python 3.10. Then run main.py after configuring the .sav file location in-code.

example using miniconda:

    conda create --name EKhelper python=3.10
    conda activate EKhelper
    conda install anaconda::pillow
    conda install openpyxl
    cd [local_folder]...
    python main.py

If you plan to use it often, I recommend creating an .exe by installing pyinstaller into your virtual environment and using that library to create a one-click app.

Data
---------------------------
Data has been curated for Emerald Kaizo specifically (this includes move power, pp, accuracy changes and pokemon base stats). See data/gen3moves.xlsx and data/pokemon.xlsx if you are interested in these datasets specifically.

Credits
---------------------------
Interpreting save data code was taken from: https://github.com/ads04r/Gen3Save

Core Emerald Kaizo data is from the content creator PChal and his community, taken from: https://drive.google.com/drive/folders/1yfYLvI5m1QMApy55VBSrJT2C0P_HGrDM 

#!/usr/bin/python

import os
import sys

def confirm(text):
    while True:
        confirm_prompt = input(f"{text} (y/n)> ")
        match confirm_prompt.lower():
            case "y":
                return True
            case "n":
                return False
            case _:
                pass

RF5_APPID = 1702330
GAMEPATH_INTERNAL = "/home/deck/.local/share/Steam/steamapps/common/Rune Factory 5"
CTRLFIX_URL = "https://github.com/Rose22/runefactory5_steamdeck_fix/releases/download/ctrlfix/ctrlfix.zip"
RF5FIX_URL = "https://github.com/Lyall/RF5Fix/releases/download/v0.1.5/RF5Fix_v0.1.5.zip"

RF5FIX_CFG = """
## Settings file was created by plugin RF5Fix v0.1.5
## Plugin GUID: RF5Fix

[Controller Icon Override]

## Set to true to enable controller icon override.
# Setting type: Boolean
# Default value: false
ControllerType.Override = false

## Set desired controller icon type.
# Setting type: String
# Default value: Xbox
# Acceptable values: Xbox, PS4, PS5, Switch
ControllerType = Xbox

[FOV Adjustment]

## Set to true to enable adjustment of the FOV.
## It will also adjust the FOV to be Vert+ if your aspect ratio is narrower than 16:9.
# Setting type: Boolean
# Default value: true
FOVAdjustment = true

## Set additional FOV in degrees. This does not adjust FOV in cutscenes.
# Setting type: Single
# Default value: 0
# Acceptable value range: From 0 to 180
AdditionalFOV.Value = 0

[General]

## Set desired update rate. This will improve camera smoothness in particular.
## 0 = Auto (Set to refresh rate). Game default = 50
# Setting type: Single
# Default value: 0
# Acceptable value range: From 0 to 5000
PhysicsUpdateRate = 0

## Skip intro logos.
# Setting type: Boolean
# Default value: true
IntroSkip = true

## Fixes low-resolution 3D models in the equip menu/3D model viewer.
# Setting type: Boolean
# Default value: true
LowResMenuFix = true

## Set to true to disable the crosshatch/sketch effect.
# Setting type: Boolean
# Default value: false
DisableCrossHatching = false

[Graphical Tweaks]

## Set Anisotropic Filtering level. 16 is recommended for quality.
# Setting type: Int32
# Default value: 1
# Acceptable value range: From 1 to 16
AnisotropicFiltering.Value = 16

## Set LOD Bias. Controls distance for level of detail switching. 4 is recommended for quality.
# Setting type: Single
# Default value: 1.5
# Acceptable value range: From 0.1 to 10
LODBias.Value = 4

## Set NPC Draw Distance. Controls distance at which NPCs render. 10000 is recommended for quality.
# Setting type: Single
# Default value: 2025
# Acceptable value range: From 1 to 100000
NPCDistance.Value = 10000

## Set Shadow Resolution. 4096 is recommended for quality.
# Setting type: Int32
# Default value: 4096
# Acceptable value range: From 64 to 32768
ShadowResolution.Value = 4096

## Set number of Shadow Cascades. 4 is recommended for quality but 2 is decent.
# Setting type: Int32
# Default value: 1
# Acceptable values: 1, 2, 4
ShadowCascades.Value = 1

## Set Shadow Distance. Controls distance at which shadows render. 180 is recommended for quality.
# Setting type: Single
# Default value: 120
# Acceptable value range: From 1 to 999
ShadowDistance.Value = 120

[Mouse Sensitivity]

## Set to true to enable mouse sensitivity override.
# Setting type: Boolean
# Default value: false
MouseSensitivity.Override = false

## Set desired mouse sensitivity.
# Setting type: Int32
# Default value: 100
# Acceptable value range: From 1 to 9999
MouseSensitivity.Value = 100

[Set Custom Resolution]

## Set to true to enable the custom resolution below.
# Setting type: Boolean
# Default value: false
CustomResolution = true

## Set desired resolution width.
# Setting type: Single
# Default value: 1280
ResolutionWidth = 1280

## Set desired resolution height.
# Setting type: Single
# Default value: 800
ResolutionHeight = 800

## Set window mode. 1 = Fullscreen, 2 = Borderless, 3 = Windowed.
# Setting type: Int32
# Default value: 1
# Acceptable value range: From 1 to 3
WindowMode = 1

[Ultrawide UI Fixes]

## Set to true to enable ultrawide UI fixes.
# Setting type: Boolean
# Default value: true
UltrawideFixes = true

## Letterboxes UI (not gameplay). Set to false to disable letterboxing everywhere.
# Setting type: Boolean
# Default value: true
Letterboxing = true
"""

# find rune factory 5 install location
install_path = False
if os.path.exists(GAMEPATH_INTERNAL):
    install_path = "/home/deck/.local/share/Steam/steamapps"
    print("Rune Factory 5 install found on internal drive!")
else:
    ext_drives = os.listdir("/run/media/deck")
    for drive in ext_drives:
        if "steamapps" in os.listdir(f"/run/media/deck/{drive}"):
            if os.path.exists(f"/run/media/deck/{drive}/steamapps/common/Rune Factory 5"):
                install_path = f"/run/media/deck/{drive}/steamapps"
                print("Rune Factory 5 install found on external drive or SD card!")

if not install_path:
    sys.exit("Error: Could not find installation path of Rune Factory 5. Do you have it installed?")

rf5_game_path = f"{install_path}/common/Rune Factory 5"
rf5_pfx_path = f"{install_path}/compatdata/{RF5_APPID}/pfx/drive_c/users/steamuser/AppData/Roaming"

print()

if not os.path.exists(f"{rf5_pfx_path}/RF5"):
    sys.exit("Please run the game at least once before using this setup script.")

# figure out steam user ID
steam_uid = 0
for folder in os.listdir(f"{rf5_pfx_path}/RF5/"):
    if "steam_autocloud.vdf" in os.listdir(f"{rf5_pfx_path}/RF5/{folder}"):
        steam_uid = folder

if not steam_uid:
    sys.exit("Error: Couldn't find your save path! please make sure you have at least one saved game.")

print(f"rune factory 5 install path: {rf5_game_path}")
print()

if not confirm("Everything looking good?"):
    sys.exit("Aborted.")

print()

print("Install rf5fix to get a higher resolution, the steam deck's 16:10 aspect ratio, better framerate, better draw distance, and all that good stuff!")
rf5fix_installed = False
if confirm("install rf5fix?"):
    os.system(f"wget \"{RF5FIX_URL}\" -O /tmp/rf5fix.zip")
    os.system(f"unzip -o /tmp/rf5fix.zip -d \"{rf5_game_path}\"")
    if not os.path.exists(f"{rf5_game_path}/BepInEx/config"):
        os.mkdir(f"{rf5_game_path}/BepInEx/config")
    print("installing steam deck config..")
    with open(f"{rf5_game_path}/BepInEx/config/RF5Fix.cfg", "w") as f:
        f.write(RF5FIX_CFG)
    print("rf5fix installed.")
    print()

    rf5fix_installed = True

    os.remove("/tmp/rf5fix.zip")

print("""
DISCLAIMER:

To get proper controller support on Steam Deck in Rune Factory 5, sadly, we need to hack the game in a very drastic way. This method uses a Steam Emulator called Goldberg, to essentially fool the game into thinking an Xbox controller is connected. Goldberg is normally used by pirates to crack steam protections, so this is a bit risky, and you'll have to consider whether the risk is worth it. I can't guarantee how safe these patched files are, as i've taken these directly from Kentun's guide, and just removed the DLC from them (by blanking out the DLC.txt files). Don't worry though, this won't get you banned from Steam.

Note that Goldberg disables Steam Achievements in the game, but this is temporary. If you do a clean install of the game without goldberg, achievements will be working again.
""")
if confirm("install controller fix?"):
    prevdir = os.getcwd()

    os.chdir(rf5_game_path)
    if not os.path.isfile("prepatch_backup.zip"):
        print("Backing up game files..")
        os.system("zip -qr prepatch_backup.zip \"Rune Factory 5.exe\" \"steam_api64.dll\" \"Rune Factory 5_Data/Plugins/x86_64/\"")
    else:
        print("Unpatched game files were already backed up. Skipping!")
    os.chdir(prevdir)

    os.system(f"wget \"{CTRLFIX_URL}\" -O /tmp/ctrlfix.zip")
    os.system(f"unzip -o /tmp/ctrlfix.zip -d \"{rf5_game_path}\"")

    goldberg_path = f"{rf5_pfx_path}/Goldberg SteamEmu Saves/"
    goldberg_settings = {
        "user_steam_id": steam_uid,
        "account_name": "RF5",
        "language": "english",
        "listen_port": "47584"
    }

    print("Adding goldberg settings..")

    if not os.path.exists(goldberg_path):
        os.mkdir(goldberg_path)
    if not os.path.exists(f"{goldberg_path}/settings"):
        os.mkdir(f"{goldberg_path}/settings")

    for setting, value in goldberg_settings.items():
        with open(f"{rf5_pfx_path}/Goldberg SteamEmu Saves/settings/{setting}.txt", "w") as f:
            f.write(value)

    print("Goldberg installed.")
    print("A backup of your unpatched gamefiles can be found as prepatch_backup.zip in the Rune Factory 5 game folder")

    os.remove("/tmp/ctrlfix.zip")

if rf5fix_installed:
    print("""
Since you installed rf5fix, there is one more thing you need to do.
Please head to your steam library and find Rune Factory 5 in the list of games. Right click it, select Properties, then paste this into the Launch Options:

WINEDLLOVERRIDES="winhttp=n,b" %command%

You can also find this in the steam guide related to this script, if you're having trouble copying and pasting it from this console window.
""")

print()
print("Setup done!")

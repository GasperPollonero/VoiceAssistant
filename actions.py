from typing import Any
import os
import json
from pathlib import Path
import subprocess
from pycaw.pycaw import AudioUtilities
from text_to_num import alpha2digit
import re
import numpy as np

def handle_action(action : str | None, params: dict[str, Any] | None = None):
    
    if action == "camera":
        match params[0]:
            case "status":
                
                base_dir = Path(__file__).resolve().parent
                config_path = base_dir / "config" / "addresses.json"
                with config_path.open("r", encoding="utf-8") as f:
                    dic = json.load(f)
                args = [
                    dic["COMMAND"], 
                    dic["ADDRESS"],
                ]
                output = subprocess.check_output(args, stderr=subprocess.DEVNULL,)
                output = json.loads(output)["ison"]
                
                if output:
                    return "La camera è accesa."
                else:
                    return "La camera è spenta."
                   
    match action:
        case "mute":
            print("MUTE")
        case "volume_up":
            print("VOLUME SU")
        case "volume_down":
            print("VOLUME DOWN")
        case "set_volume":
            set_volume(params["volume"])
            


def set_volume(volume):
    
    # renormalize volume.
    if volume > 100:
        volume = 100
    
    # get audio device.
    device = AudioUtilities.GetSpeakers()
    volume_info = device.EndpointVolume
    print("volume: ", volume_info.GetMasterVolumeLevel())
    
    # get max_volume - min_volume
    range = volume_info.GetVolumeRange()[1] - volume_info.GetVolumeRange()[0]
    
    if volume <= 0 :
        # set minimum value.
        volume = volume_info.GetVolumeRange()[0]
    else:
        # convert linear to dB scale.
        volume = 34.37 * np.log10((volume)/100)
     
    # set volume to -20 dB
    volume_info.SetMasterVolumeLevel(volume, None)


if __name__ == "__main__":
    set_volume(20)

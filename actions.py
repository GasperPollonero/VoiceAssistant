from typing import Any

def handle_action(action : str | None, params: dict[str, Any] | None = None):
    
    if action is None:
        return
    
    match action:
        case "mute":
            print("MUTE")
        case "volume_up":
            print("VOLUME SU")
        case "volume_down":
            print("VOLUME DOWN")
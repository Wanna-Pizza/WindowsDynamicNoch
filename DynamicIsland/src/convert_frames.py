import re
import json

def convert_frames_to_dict(path: str = "frames_open") -> dict:
    frames_path = f"assets/animation_data/{path}.txt"

    frames_dict = {}
    
    try:
        with open(frames_path, 'r') as file:
            for line in file:
                match = re.match(r"Frame (\d+): Y:(\d+\.\d+) Z:(\d+\.\d+)", line)
                if match:
                    frame_num = int(match.group(1))
                    y_scale = float(match.group(2))
                    z_scale = float(match.group(3))
                    
                    # Store the values in the dictionary
                    frames_dict[frame_num] = {
                        'y': y_scale,
                        'z': z_scale
                    }
    except FileNotFoundError:
        print(f"Error: File {frames_path} not found.")
        return None
    return frames_dict


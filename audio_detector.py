import subprocess
import re
import time
import psutil

system_command = "pacmd list-sink-inputs"
system_command_list = ["pacmd", "list-sink-inputs"]
search_term = 'RUNNING'
search_bytes = bytes(search_term, 'utf-8')

def check_audio_playing():
    # Run system command
    output = subprocess.check_output(system_command_list)
    # Check if output has our search term. 
    result = re.search(search_bytes, output)
    
    if result:
        return True
    else:
        return False

def check_mplayer_running():
    for proc in psutil.process_iter():
        if proc.name() == 'mplayer':
            return True
    return False

if __name__ == '__main__':
    
    print('Audio Detector running')
    while True:
        result = check_audio_playing()
        # Do something when audio is detected
        if result:
            print('Audio Detected')
    
        time.sleep(0.25)

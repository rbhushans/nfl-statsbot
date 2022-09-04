import subprocess
from time import sleep

cmd = "python NFLStatsbot/reply.py"

restart_timer = 2
def start_script():
    try:
        subprocess.call(cmd, shell=True)
    except Exception as e:
        print("ERROR", e)
        handle_crash()

def handle_crash():
    sleep(restart_timer)
    start_script()

start_script()
from screeninfo import get_monitors
from os import system, name
import pyautogui
import inquirer


# Function to get monitor number
def MonitorNumber(n):
    MonitorList = [f"DISPLAY{i}" for i in range(1,n+1)]
    return MonitorList

# Function to get monitor info
def getMonitor(name):
    get_Monitors = []
    for m in get_monitors():
        get_Monitors.append(str(m))
        
    for Monitor in get_Monitors:
        if name in Monitor:
            x_value = Monitor.split(",")[0].split("=")[1].strip()
            y_value = Monitor.split(",")[1].split("=")[1].strip()
            w, h = pyautogui.size()
            monitor = {f"top": int(y_value), "left": int(x_value), "width": w, "height": h}
            return monitor

# Function to get primary monitor   
def mainMonitor():
    get_Monitors = []
    for m in get_monitors():
        get_Monitors.append(str(m))
    for Monitor in get_Monitors:
        if "is_primary=True" in Monitor:
            display_name = Monitor.split("'")[1]
            display_name = display_name.replace(r'\\\\.\\', '')
            print("Main display:",display_name)
            
# Function to select which monitor to use
def selectMonitor(n):
    MonitorList = [f"DISPLAY{i}" for i in range(1,n+1)]
    MonitorList = [inquirer.List("Monitor", message="Choose display",choices=MonitorList+["\"Exit\""])]
    select = inquirer.prompt(MonitorList)
    if select["Monitor"] == "\"Exit\"": # type: ignore
        print("Exiting...")
        exit()
    elif select["Monitor"] in MonitorList[0].choices: # type: ignore
        print(select["Monitor"],"selected!") # type: ignore
        display = getMonitor(select["Monitor"])# type: ignore
    return display          
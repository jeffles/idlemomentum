import math
import pyautogui
import time
import sys
import subprocess

from filecmp import cmp
from twisted.internet import task, reactor

mytimes = {
    "screen_shot": 1,
    "ascend": 35
}

ascension = 0
pyautogui.PAUSE=0.4
start_time = time.time()
previous_file_name = ''
run_without_improvement = 0

def get_print_time():
    minute = str(math.ceil((time.time()-start_time)/60))
    if (ascension > 0):
        return minute + '-' + str(ascension)
    return minute

def ascend():
    global ascension
    global start_time
    print('Acending at', get_print_time())
    ascension+=1
    start_time = time.time()
    pyautogui.moveTo(431, 138)
    pyautogui.dragTo()
    pyautogui.click()
    #pyautogui.click(x=431, y=138, clicks=2, interval=1)

def screen_shot():
    global previous_file_name
    global run_without_improvement
    print('Screen shot at', get_print_time())
    file_name = 'ascend' + get_print_time() + '.png'
    pyautogui.screenshot(file_name, region=(865,235,160,70))
    if previous_file_name:
        same = cmp(previous_file_name, file_name)
        if same:
            run_without_improvement += 1
        else:
            run_without_improvement = 0
    previous_file_name = file_name
    if start_time > 300 and run_without_improvement > 1:
        ascend();

       
def level_up():
    pyautogui.press('space')


print (sys.platform)
if 'darwin' in sys.platform:
    print('Running \'caffeinate\' on MacOSX to prevent the system from sleeping')
    subprocess.Popen('caffeinate')
# while (True):
#   currentMouseX, currentMouseY = pyautogui.position() # Get the XY position of the mouse.
#   print (currentMouseX, currentMouseY)
pyautogui.moveTo(1393, 138) 
pyautogui.dragTo()
pyautogui.click()          
pyautogui.click() 

loop1 = task.LoopingCall(level_up)
loop1.start(.5)   

loop2 = task.LoopingCall(screen_shot) 
loop2.start(mytimes['screen_shot']*60, now=True)

# loop3 = task.LoopingCall(ascend)
# loop3.start(mytimes['ascend']*60, now=False)

reactor.run()

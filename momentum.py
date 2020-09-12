import math
import pyautogui
import time
import sys
import subprocess

from twisted.internet import task, reactor

mytimes = {
    "screen_shot": 1,
    "ascend": 35
}

ascension = 0
pyautogui.PAUSE=0.4
startTime = time.time()

def get_print_time():
    minute = str(math.ceil((time.time()-startTime)/60))
    if (ascension > 0):
        return minute + '-' + str(ascension)
    return minute

def get_new_end_time(minutes=15):
    return time.time() + 60 * minutes

def ascend():
    print('Acending at', get_print_time())
    ascension+=1
    pyautogui.moveTo(431, 138)
    pyautogui.dragTo()
    pyautogui.click()
    #pyautogui.click(x=431, y=138, clicks=2, interval=1)

def screen_shot():
    print('Screen shot at', get_print_time())
    file_name = 'ascend' + get_print_time() + '.png'
    pyautogui.screenshot(file_name, region=(0,0,1200,800))
       
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

loop3 = task.LoopingCall(ascend)
loop3.start(mytimes['ascend']*60, now=False)

reactor.run()

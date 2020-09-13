import cv2
import math
import pyautogui
import pytesseract
import re
import sys
import subprocess
import time

from filecmp import cmp
from twisted.internet import task, reactor

# OCR help - https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/

mytimes = {
    "screen_shot": 1,
    "ascend": 6
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
    global run_without_improvement
    print('Ascending at', get_print_time())
    ascension+=1
    run_without_improvement = 0
    start_time = time.time()
    pyautogui.moveTo(431, 138)
    pyautogui.dragTo()
    pyautogui.click()
    #pyautogui.click(x=431, y=138, clicks=2, interval=1)

def screen_shot():
    global previous_file_name
    global run_without_improvement
    file_name = 'ascend' + get_print_time() + '.png'
    pyautogui.screenshot(file_name, region=(890,245,130,45))


    image = cv2.imread(file_name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # gray = cv2.threshold(gray, 0, 255,
    #     cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.medianBlur(gray, 3)

    gray_file_name = f"{file_name}-grey.png"
    cv2.imwrite(gray_file_name, gray)

    text = pytesseract.image_to_string(gray_file_name).rstrip()
    ascend_points = re.search('\d+', text)
    if ascend_points:
        ascend_points = ascend_points.group(0)

    same = True
    if previous_file_name:
        same = cmp(previous_file_name, file_name)
    if same:
        run_without_improvement += 1
        print(f'Same {ascend_points} {text} - {file_name} ')
    else:
        run_without_improvement = 0
        print(f'Better {ascend_points} {text} - {file_name}')
    previous_file_name = file_name
    if start_time > 300 and run_without_improvement > 1:
        ascend();

       
def level_up():
    pyautogui.press('space')


time.sleep(2)
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

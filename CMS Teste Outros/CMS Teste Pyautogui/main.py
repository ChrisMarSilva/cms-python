import time
import pyautogui
from dotenv import load_dotenv


def main():
    try:

        start_time = time.time()
        
        # screenWidth, screenHeight = pyautogui.size() # Returns two integers, the width and height of the screen. (The primary monitor, in multi-monitor setups.)
        # print("screenWidth", screenWidth, " screenHeight", screenHeight)
        # currentMouseX, currentMouseY = pyautogui.position() # Returns two integers, the x and y of the mouse cursor's current position.
        # print("currentMouseX", currentMouseX, " currentMouseY", currentMouseY)
        # pyautogui.moveTo(100, 150) # Move the mouse to the x, y coordinates 100, 150.
        # pyautogui.click() # Click the mouse at its current location.
        # pyautogui.click(200, 220) # Click the mouse at the x, y coordinates 200, 220.
        # pyautogui.move(None, 10)  # Move mouse 10 pixels down, that is, move the mouse relative to its current position.
        # pyautogui.doubleClick() # Double click the mouse at the
        # pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad) # Use tweening/easing function to move mouse over 2 seconds.
        # pyautogui.write('Hello world!', interval=0.25)  # Type with quarter-second pause in between each key.
        # pyautogui.press('esc') # Simulate pressing the Escape key.
        # pyautogui.keyDown('shift')
        # pyautogui.write(['left', 'left', 'left', 'left', 'left', 'left'])
        # pyautogui.keyUp('shift')
        # pyautogui.hotkey('ctrl', 'c')

        # pyautogui.alert('This is an alert box.')
        # pyautogui.confirm('Shall I proceed?')
        # pyautogui.confirm('Enter option.', buttons=['A', 'B', 'C'])
        # pyautogui.prompt('What is your name?')
        # pyautogui.password('Enter password (text will be hidden)')

        # im1 = pyautogui.screenshot()
        # im1.save('my_screenshot.png')
        # im2 = pyautogui.screenshot('my_screenshot2.png')

        # locate the image on screen
        button7location = pyautogui.locateOnScreen('menu_editar.png') # returns (left, top, width, height) of matching region
        print("button7location", button7location)
        button_edit = pyautogui.center(button7location)
        print("button_edit", button_edit)
        pyautogui.moveTo(button_edit)
        buttonx, buttony = pyautogui.center(button7location)
        print("buttonx", buttonx, " buttony", buttony)
        pyautogui.click(buttonx, buttony)  # clicks 

        # locate the center of the image on the screen
        buttonx, buttony = pyautogui.locateCenterOnScreen('menu_editar.png') # returns (x, y) of matching region
        print("buttonx", buttonx, " buttony", buttony)

        # channel_name = "the english scholars online camp" # "cortes liga crypto" # pyautogui.prompt(text='', title="Enter the Channel Name") # cortes liga crypto
        # pyautogui.hotkey('alt', 'tab')
        # pyautogui.hotkey('ctrl', 't')
        # pyautogui.write('https://www.youtube.com')
        # pyautogui.hotkey('enter')
        # time.sleep(3)
        # x, y = pyautogui.locateCenterOnScreen('input_pesquisar.png', confidence=0.9)
        # pyautogui.moveTo(x, y, 1)
        # pyautogui.click()
        # time.sleep(1)
        # pyautogui.write(channel_name)
        # pyautogui.hotkey('enter')
        # time.sleep(2)
        # x, y = pyautogui.locateCenterOnScreen('botao_logo.png', confidence=0.8)
        # pyautogui.moveTo(x, y, 1)
        # pyautogui.click()
        # time.sleep(2)
        # x, y = pyautogui.locateCenterOnScreen('botao_increver_se.png', confidence=0.9)
        # pyautogui.moveTo(x, y, 1)
        # pyautogui.click()

        end_time = time.time()
        print(f"It took {end_time-start_time:.2f} seconds")

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

# py -3 -m venv .venv

# python -m pip install --upgrade pyautogui
# python -m pip install --upgrade opencv-python

# cd c:/Users/chris/Desktop/CMS Python/CMS Teste HelloWorld
# .venv\scripts\activate
# python main.py
from pynput.keyboard import Controller, Key
from PIL import ImageEnhance

import pyautogui
import pygetwindow as gw
import pytesseract
import sys
import time

# Get the emulator window, if present.
emulator_window = gw.getWindowsWithTitle('DeSmuME')[0]

if not emulator_window:
    print('DeSmuME emulator not running.')
    quit()
else:
    print(f'DeSmuME emulator window found: {emulator_window.title}')

# Set the tesseract executable location.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Create the Controller object.
keyboard = Controller()

emulator_menu_height = 80
emulator_pos_x = emulator_window.left + 6
emulator_pos_y = emulator_window.top
emulator_width = emulator_window.width - 12
emulator_height = emulator_window.height - 8
screen_width = emulator_width
screen_height = int((emulator_height - emulator_menu_height) / 2)

def do_long_press(key, duration):
    """
    Simulates a long key press for a specified duration.
    
    :param key: The key to press (e.g., 'a', 'shift', 'space').
    :param duration: Duration to hold the key down in seconds.
    """
    keyboard = Controller()

    # Press the key down, wait, then release.
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)

def nudge_char_right():
    do_long_press(Key.right, 2)

def nudge_char_left():
    do_long_press(Key.left, 2)

def get_message_text(filename=None, custom_x=None, custom_y=None, custom_width=None, custom_height=None):
    x = emulator_pos_x + 30

    if custom_x:
        x = emulator_pos_x + custom_x

    y = emulator_pos_y + emulator_menu_height + screen_height - 80

    if custom_y:
        y = emulator_pos_y + emulator_menu_height + screen_height - 80 + custom_y

    width = custom_width if custom_width else emulator_width - 80
    height = custom_height if custom_height else 70

    # Take a screenshot of the message area.
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    # Convert to grayscale.
    # screenshot = screenshot.convert('L')

    if filename :
        # Save the screenshot for debugging.
        screenshot.save(filename)

    # Use pytesseract to do OCR on the image.# Path to the custom word list
    # dictionary_path = "dictionary.txt"
    # custom_config = f'--user-words {dictionary_path}'
    # text = pytesseract.image_to_string(screenshot, lang="spa", config=custom_config)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(screenshot, lang="eng", config=custom_config)
    text = text.strip()

    return text

# Focus the emulator window.
emulator_window.activate()

# Release any keys that might've gotten stuck during a force-quit.
keyboard = Controller()
keyboard.release(Key.left)
keyboard.release(Key.right)

time.sleep(0.2)


def is_pixel_mostly_red(pixel):
    red, green, blue = pixel
    return red > green * 3 and red > blue * 3

# TODO: Rename to "check_is_fish_hooked()"
def is_fish_caught(filename=None):
    x = emulator_pos_x + int(screen_width / 2) - 10
    y = emulator_pos_y + emulator_menu_height + int(screen_height / 2) - 10 - 50
    width = 24
    height = 24

    # Take a screenshot of the message area.
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    # Convert the screenshot to RGB.
    screenshot = screenshot.convert("RGB")

    if filename :
        # Save the screenshot for debugging.
        screenshot.save(filename)

    is_scanning_image = True
    is_fish_caught = False

    # Loop through all pixels in the image.
    for x in range(screenshot.width):
        if not is_scanning_image:
            break

        for y in range(screenshot.height):
            if not is_scanning_image:
                break

            # Get the RGB color value of the pixel at (x, y).
            pixel_color = screenshot.getpixel((x, y))
            is_mostly_red = is_pixel_mostly_red(pixel_color)

            if is_mostly_red:
                # print(f"Mostly red pixel {pixel_color} found at:", x, y)
                is_scanning_image = False
                is_fish_caught = True
    
    return is_fish_caught

def check_is_pokemon_caught():
    debug = True

    x = emulator_pos_x + 6
    y = emulator_pos_y + emulator_menu_height + 80
    width = 14
    height = 14

    # Take a screenshot of the icon area.
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    if debug :
        # Save the screenshot for debugging.
        screenshot.save('check-is-pokemon-caught.png')
    
    is_scanning_image = True
    is_pokemon_caught = False

    # Loop through all pixels in the image.
    for x in range(screenshot.width):
        if not is_scanning_image:
            break

        for y in range(screenshot.height):
            if not is_scanning_image:
                break

            # Get the RGB color value of the pixel at (x, y).
            pixel_color = screenshot.getpixel((x, y))
            is_mostly_red = is_pixel_mostly_red(pixel_color)

            if is_mostly_red:
                # print(f"Mostly red pixel {pixel_color} found at:", x, y)
                is_scanning_image = False
                is_pokemon_caught = True
    
    return is_pokemon_caught


def check_is_battling():
    debug = True

    # x = emulator_pos_x + screen_width - 20
    x = emulator_pos_x + 190
    # y = emulator_pos_y + emulator_menu_height + screen_height + 20
    y = emulator_pos_y + emulator_menu_height + 50
    width = 10
    height = 10

    # Take a screenshot of the bottom screen.
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot = screenshot.convert("RGB")

    if debug :
        # Save the screenshot for debugging.
        screenshot.save('check-is-battling.png')
    
    is_scanning_image = True
    is_battling = False

    # Loop through all pixels in the image.
    for x in range(screenshot.width):
        if not is_scanning_image:
            break

        for y in range(screenshot.height):
            if not is_scanning_image:
                break

            # Get the RGB color value of the pixel at (x, y).
            pixel_color = screenshot.getpixel((x, y))
            is_text_color = pixel_color == (109, 117, 93)

            if is_text_color:
                # print(f"Test pixel {pixel_color} found at:", x, y)
                is_scanning_image = False
                is_battling = True
    
    return is_battling


def throw_pokeball():
    print('Throwing pokéball...')
    do_long_press(Key.down, 0.5)
    time.sleep(1)
    do_long_press(Key.down, 0.5)
    time.sleep(1)
    do_long_press('x', 0.5)
    time.sleep(1)
    do_long_press(Key.right, 0.5)
    time.sleep(1)
    do_long_press('x', 0.5)
    time.sleep(1)
    do_long_press('x', 0.5)
    time.sleep(1)
    do_long_press('x', 0.5)

def do_battle_basic():
    """
    Do not use this function. Thanks in advance!
    """
    for i in range(0, 6):
        do_long_press('x', 0.5)
        time.sleep(1)
        do_long_press('x', 0.5)
        print('Attacking pokémon...')
        time.sleep(12)

def do_battle_advanced():
    print('Preparing for battle...')

    is_battling = True

    if not check_is_pokemon_caught():
        print('Pokémon not already caught.')
        throw_pokeball()
    else :
        print('Pokémon already caught.')

    while is_battling:
        if not check_is_battling():
            print('The battle must have ended.')
            is_battling = False
            break

        # Get the message text.
        battle_text = get_message_text(filename='battle-text.png', custom_width=95, custom_height=35)
        battle_text = battle_text.lower()

        if 'what will' in battle_text:
            print('Attacking pokémon...')
            do_long_press(Key.up, 0.5)
            time.sleep(0.5)
            do_long_press('x', 0.5)
            time.sleep(0.5)
            do_long_press('x', 0.5)
            # time.sleep(12)
        
        # Wait between checking messages.
        time.sleep(2)
        
    
def do_fishing():
    is_fishing = True

    while is_fishing:
        # Toss the fishing line into the water.
        print('Using fishing rod...')
        do_long_press('a', 0.5)

        waiting_for_fish = True

        while waiting_for_fish:
            fish_alert = is_fish_caught()

            if fish_alert:
                # Tug on the rod to hook the fish.
                print('Hooking pokémon...')
                do_long_press('x', 0.5)
                time.sleep(1)
            
            # Get the message text.
            fish_caught_text = get_message_text(filename='fish-caught-text.png')
            fish_caught_text = fish_caught_text.lower()
            
            if 'landed' in fish_caught_text:
                print('You landed a pokémon!')
                time.sleep(0.5)
                do_long_press('x', 0.5)

                # Wait for the animation to finish.
                time.sleep(18)

                # Run the battle script.
                do_battle_advanced()

                # Toss the fishing line back into the water.
                time.sleep(10)
                print('Using fishing rod...')
                do_long_press('a', 0.5)
                    
            # Get the message text.
            no_fish_text = get_message_text(filename='no-fish-text.png')
            no_fish_text = no_fish_text.lower()

            if 'not even' in no_fish_text:
                print('Not even a nibble!')
                time.sleep(0.5)
                do_long_press('x', 0.5)
                waiting_for_fish = False
            else:
                # Get a portion of the message text.
                # OCR has an issue detecting the word "pokémon".
                fish_got_away_text = get_message_text(filename='fish-got-away-text.png', custom_x=168, custom_width=96, custom_height=35)
                fish_got_away_text = fish_got_away_text.lower()

                if 'got away' in fish_got_away_text:
                    print('The pokémon got away!')
                    time.sleep(0.5)
                    do_long_press('x', 0.5)
                    waiting_for_fish = False

        # Wait between fishing attempts.
        time.sleep(2)

def do_battle_patrol():
    """
    Tells the character to start patrolling.
    """

    print('Starting patrol...')

    is_patroling = True

    while is_patroling:
        # Get the battle text.
        battle_text = get_message_text(filename='battle-text.png', custom_width=95, custom_height=35)
        battle_text = battle_text.lower()

        if 'what will' in battle_text:
            do_battle_advanced()

            print('Resuming patrol...')
        else :
            nudge_char_left()
            time.sleep(0.2)
            nudge_char_right()

        time.sleep(0.5)

if len(sys.argv) > 1:
    # Get the first argument (e.g., `python pykemon.py patrol`).
    first_arg = sys.argv[1]

    if first_arg == 'fish':
        do_fishing()
    
    if first_arg == 'battle':
        do_battle_advanced()
    
    if first_arg == 'patrol':
        do_battle_patrol()
    
    if first_arg == 'reset':
        print('Keyboard has been reset.')

else:
    print("No arguments were passed.")

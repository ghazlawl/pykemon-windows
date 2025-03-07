from pynput.keyboard import Controller, Key
from PIL import ImageGrab

import pygetwindow as gw
import pytesseract
import sys
import time

# Get all emulator windows, if present.
emulator_windows = gw.getWindowsWithTitle('DeSmuME')

if len(emulator_windows) > 0:
    # Get the first emulator window, if present.
    emulator_window = emulator_windows[0]

if not emulator_window:
    print('DeSmuME emulator not running.')
    quit()
else:
    print(f'DeSmuME emulator window found: {emulator_window.title}')

# Set the tesseract executable location.
# TODO: Move this to the .env file.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Create the Controller object.
keyboard = Controller()

# Calculate some runtime variables.
emulator_menu_height = 80
emulator_pos_x = emulator_window.left + 6
emulator_pos_y = emulator_window.top
emulator_width = emulator_window.width - 12
emulator_height = emulator_window.height - 8
screen_width = emulator_width
screen_height = int((emulator_height - emulator_menu_height) / 2)

# Focus the emulator window.
emulator_window.activate()

# Give the emulator some time to activate.
time.sleep(0.2)

# Release any keys that might've gotten stuck during a force-quit.
keyboard = Controller()
keyboard.release(Key.left)
keyboard.release(Key.right)
keyboard.release(Key.up)
keyboard.release(Key.down)


def _get_screenshot_bbox(x, y, width, height):
    """
    Converts the specified x, y, width, and height to a bounding box for use
    with the Pillow library.

    Args:
        x (int): The X coordinate.
        y (int): The Y coordinate.
        width (int): The width of the box.
        height (int): The height of the box.

    Returns:
        tuple: The bounding box, as a tuple.

    Example:
        >>> _get_screenshot_bbox(100, 100, 200, 100)
        (100, 100, 300, 200)
    """

    starting_x = emulator_pos_x
    starting_y = emulator_pos_y + emulator_menu_height

    x1 = starting_x + x
    y1 = starting_y + y
    x2 = x1 + width
    y2 = y1 + height

    return (x1, y1, x2, y2)


def _get_screenshot(x, y, width, height, filename=None):
    """
    Gets a screenshot of the specified area.

    Args:
        x (int): The X coordinate.
        y (int): The Y coordinate.
        width (int): The width of the area to capture.
        height (int): The height of the area to capture.
        filename (str): (Optional) The filename to save the screenshot to.

    Returns:
        Image: The screenshot.
    """

    # Get the bounding box.
    bbox = _get_screenshot_bbox(x, y, width, height)

    # Take the screenshot and convert to RGB.
    screenshot = ImageGrab.grab(all_screens=True, bbox=bbox)
    screenshot = screenshot.convert("RGB")

    # Save the screenshot.
    if filename:
        screenshot.save(f'screenshots/{filename}')

    return screenshot


def _get_ocr_text(screenshot):
    """
    Uses the pytesseract library to extract the text from the specified 
    image. This function mostly reliable but isn't perfect!

    Args:
        screenshot (Image): The screenshot to extract text from.

    Returns:
        str: The extracted text.

    Example:
        >>> _get_ocr_text(screenshot)
        not even a nibble...
        >>> _get_ocr_text(screenshot)
        you landed a pokemon!
    """

    # Use pytesseract to do OCR on the image.
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(
        screenshot, lang="eng", config=custom_config)
    text = text.strip()

    return text


def _is_mostly_red_pixel(pixel):
    """
    Checks if the specified pixel is mostly red. A pixel is mostly red if the 
    red value is 3x greater or more than the green and blue values.
    """

    red, green, blue = pixel
    return red > green * 3 and red > blue * 3


def _debug_screen_1():
    """
    Captures a screenshot of the top screen. Used to confirm x, y, width, 
    and height values.
    """
    screenshot = _get_screenshot(
        0,
        0,
        screen_width,
        screen_height,
        'screen-1.png'
    )

    return screenshot


def _debug_screen_2():
    """
    Captures a screenshot of the bottom screen. Used to confirm x, y, width, 
    and height values.
    """
    screenshot = _get_screenshot(
        0,
        screen_height,
        screen_width,
        screen_height,
        'screen-2.png'
    )

    return screenshot


def do_long_press(key, duration):
    """
    Simulates a long key press for the specified duration.

    Args:
        key (str): The key to press (e.g., 'x', 'z', Key.right, Key.left, etc).
        duration (int): The duration to hold the key down, in seconds.
    """
    keyboard = Controller()

    # Press the key down, wait, then release.
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)


def do_walk_right():
    """
    Tells the character to walk to the right for 2 seconds. Used primarily
    for patrolling.
    """
    do_long_press(Key.right, 2)


def do_walk_left():
    """
    Tells the character to walk to the left for 2 seconds. Used primarily
    for patrolling.
    """
    do_long_press(Key.left, 2)


def get_message_text(custom_x=None, custom_y=None, custom_width=None, custom_height=None):
    """
    Gets the text in the message area (e.g., "you landed a pokemon", "not 
    even a nibble", etc).

    Args:
        custom_x (int or None): The custom X coordinate to use.
        custom_y (int or None): The custom Y coordinate to use.
        custom_width (int or None): The custom width to use.
        custom_height (int or None): The custom height to use.

    Returns:
        string: The text, in lower case.
    """

    # Calculate the x, y, width, and height.
    x = int(custom_x) if custom_x else 30
    y_offset = screen_height - 80
    y = y_offset + int(custom_y) if custom_y else y_offset
    width = custom_width if custom_width else screen_width - 130
    height = custom_height if custom_height else 70

    # Take a screenshot of the message area.
    screenshot = _get_screenshot(x, y, width, height, 'get-message-text.png')

    # Extract the text.
    text = _get_ocr_text(screenshot)
    text = text.lower()

    return text


def check_is_pokemon_hooked():
    """
    Checks if the player currently has a hooked pokémon on the fishing line.
    This function should only be used while fishing.

    Returns:
        boolean: Whether the player has hooked a pokémon.
    """

    # Take a screenshot of the alert area.
    screenshot = _get_screenshot(
        int(screen_width / 2) - 10,
        int(screen_height / 2) - 10 - 50,
        24,
        24,
        'check-is-fish-hooked.png'
    )

    is_scanning_image = True
    is_hooked = False

    # Loop through all pixels in the image.
    for x in range(screenshot.width):
        if not is_scanning_image:
            break

        for y in range(screenshot.height):
            if not is_scanning_image:
                break

            # Get the RGB value of the pixel.
            pixel_color = screenshot.getpixel((x, y))

            if _is_mostly_red_pixel(pixel_color):
                is_scanning_image = False
                is_hooked = True

    return is_hooked


def check_is_pokemon_caught():
    """
    Checks if pokémon that the player is currently battling has already 
    been caught. Warning! This function should not be used for trainer battles 
    because it will always return false.

    Returns:
        boolean: Whether the pokémon has already been caught.
    """

    # Take a screenshot of the icon area.
    screenshot = _get_screenshot(6, 80, 14, 14, 'check-is-pokemon-caught.png')

    is_scanning_image = True
    is_caught = False

    # Loop through all pixels in the image.
    for x in range(screenshot.width):
        if not is_scanning_image:
            break

        for y in range(screenshot.height):
            if not is_scanning_image:
                break

            # Get the RGB value of the pixel.
            pixel_color = screenshot.getpixel((x, y))

            if _is_mostly_red_pixel(pixel_color):
                is_scanning_image = False
                is_caught = True

    return is_caught


def check_is_battling():
    """
    Checks if the player is currently battling a pokémon.

    Returns:
        boolean: Whether the player is battling a pokémon.
    """

    # Take a screenshot of the message area.
    screenshot = _get_screenshot(
        30,
        screen_height - 80,
        screen_width - 130, 70,
        'check-is-battling.png'
    )

    is_scanning_image = True
    is_battling = False

    num_total_pixels = 0
    num_white_pixels = 0

    # Loop through all pixels in the image.
    for x in range(screenshot.width):
        if not is_scanning_image:
            break

        for y in range(screenshot.height):
            if not is_scanning_image:
                break

            # Get the RGB value of the pixel.
            pixel_color = screenshot.getpixel((x, y))

            # TODO: Refactor this to support other color schemes.
            if pixel_color == (255, 255, 255):
                num_white_pixels += 1

            num_total_pixels += 1

    # Assume we're battling if the # of white pixels is more than 60%.
    is_battling = num_white_pixels > num_total_pixels * 0.6

    return is_battling


def check_is_leveling_up():
    """
    Checks if the player is currently leveling up a pokémon.

    Returns:
        boolean: Whether the player is leveling up a pokémon.
    """

    # Take a screenshot of the leveling area.
    screenshot = _get_screenshot(
        270,
        145,
        180,
        30,
        'check-is-leveling-up.png'
    )

    # Extract the text.
    text = _get_ocr_text(screenshot)

    return 'attack' in text


def check_is_registering():
    """
    Checks if the player is currently registering a pokémon.

    Returns:
        boolean: Whether the player is registering a pokémon.
    """

    # Take a screenshot of banner area.
    screenshot = _get_screenshot(
        screen_width - 20,
        0,
        10,
        10,
        'check-is-pokemon-registered.png'
    )

    is_scanning_image = True
    is_registering = False

    num_total_pixels = 0
    num_target_pixels = 0

    # Loop through all pixels in the image.
    for x in range(screenshot.width):
        if not is_scanning_image:
            break

        for y in range(screenshot.height):
            if not is_scanning_image:
                break

            # Get the RGB value of the pixel.
            pixel_color = screenshot.getpixel((x, y))

            # Check for dark yellow or vibrant yellow. We do this because the
            # background alternates between these two colors.
            if pixel_color == (215, 190, 97) or pixel_color == (255, 215, 0):
                num_target_pixels += 1

            num_total_pixels += 1

    # Assume we're registering if the # of target pixels is more than 60%.
    # Though, realistically, this should be 100%.
    is_registering = num_target_pixels > num_total_pixels * 0.6

    return is_registering


def throw_pokeball():
    """
    Tells the character to throw a pokéball.
    """

    print('Throwing pokéball...')

    do_long_press(Key.up, 0.5)
    time.sleep(0.5)
    do_long_press(Key.down, 0.5)
    time.sleep(0.5)
    do_long_press(Key.down, 0.5)
    time.sleep(0.5)
    do_long_press('x', 0.5)
    time.sleep(0.5)
    do_long_press(Key.right, 0.5)
    time.sleep(0.5)
    do_long_press('x', 0.5)
    time.sleep(0.5)
    do_long_press('x', 0.5)
    time.sleep(0.5)
    do_long_press('x', 0.5)


def do_battle():
    """
    Tells the character to start battling.
    """

    print('Preparing for battle...')

    is_battling = True

    while is_battling:
        if not check_is_battling():
            print('The battle appears to have ended.')
            is_battling = False
            break

        if check_is_registering():
            print('Registering pokémon...')
            do_long_press('x', 0.5)

        elif check_is_leveling_up():
            print('Leveling up...')
            do_long_press('z', 0.5)

        else:
            # Get the message text.
            battle_text = get_message_text(custom_width=95, custom_height=35)

            if 'what will' in battle_text:
                if not check_is_pokemon_caught():
                    print('Pokémon not already caught.')
                    throw_pokeball()
                else:
                    print('Attacking pokémon...')
                    do_long_press(Key.up, 0.5)
                    time.sleep(0.5)
                    do_long_press('x', 0.5)
                    time.sleep(0.5)
                    do_long_press('x', 0.5)

            if 'give' in battle_text:
                print('Skipping nickname...')
                do_long_press('z', 0.5)

        # Wait between checking messages.
        time.sleep(2)


def do_fishing():
    """
    Tells the character to start fishing.
    """

    is_fishing = True

    while is_fishing:
        print('Using fishing rod...')
        do_long_press('a', 0.5)

        waiting_for_fish = True

        while waiting_for_fish:
            fish_alert = check_is_pokemon_hooked()

            if fish_alert:
                print('Hooking pokémon...')
                do_long_press('x', 0.5)
                time.sleep(1)

            # Get the message text.
            fish_caught_text = get_message_text()

            if 'landed' in fish_caught_text:
                print('You landed a pokémon!')
                time.sleep(0.5)
                do_long_press('x', 0.5)

                # Wait for the animation to finish.
                time.sleep(18)

                # Run the battle script.
                do_battle()

                # Cast the line back into the water.
                time.sleep(10)
                print('Using fishing rod...')
                do_long_press('a', 0.5)

            # Get the message text.
            no_fish_text = get_message_text()

            if 'not even' in no_fish_text:
                print('Not even a nibble!')
                time.sleep(0.5)
                do_long_press('x', 0.5)
                waiting_for_fish = False
            else:
                # TODO: Create our own trainddata for words like "pokémon", etc.
                # https://tesseract-ocr.github.io/tessdoc/#training-for-tesseract-5
                fish_got_away_text = get_message_text(
                    custom_x=168,
                    custom_width=96,
                    custom_height=35
                )

                if 'got away' in fish_got_away_text:
                    print('The pokémon got away!')
                    time.sleep(0.5)
                    do_long_press('x', 0.5)
                    waiting_for_fish = False

        # Wait between fishing attempts.
        time.sleep(2)


def do_patrol():
    """
    Tells the character to start patrolling.
    """

    print('Starting patrol...')

    is_patrolling = True

    while is_patrolling:
        # Get the battle text.
        battle_text = get_message_text(custom_width=95, custom_height=35)

        if 'what will' in battle_text:
            # Run the battle script.
            do_battle()

            print('Resuming patrol...')
        else:
            # Walk back and forth.
            do_walk_left()
            time.sleep(0.2)
            do_walk_right()

        # Wait between patrols.
        time.sleep(0.5)


if len(sys.argv) > 1:
    # Get the first argument (e.g., `python pykemon.py patrol`), if any.
    first_arg = sys.argv[1]

    if first_arg == 'fish':
        do_fishing()

    if first_arg == 'battle':
        do_battle()

    if first_arg == 'patrol':
        do_patrol()

    if first_arg == 'reset':
        print('Keyboard has been reset.')
else:
    print("No arguments were passed.")

from pynput.keyboard import Controller, Key
from PIL import Image, ImageEnhance
import sys
import time

from imports.emulator import Emulator
from imports.interface import Interface
from imports.pokedex import Pokedex
from imports.screentail import Screentail
import imports.utils as utils

my_emulator = Emulator()
my_interface = Interface(my_emulator)
my_pokedex = Pokedex()
my_screentail = Screentail()

# Create the Controller object.
keyboard = Controller()

# Give the emulator some time to activate.
time.sleep(0.2)

# Release any keys that might've gotten stuck during a force-quit.
my_interface.release_keys()


def do_throw_pokeball(self):
    """
    Tells the character to throw a pokéball.
    """

    print("Throwing pokéball...")

    my_interface.do_long_press(Key.up, 0.5)
    time.sleep(0.5)
    my_interface.do_long_press(Key.down, 0.5)
    time.sleep(0.5)
    my_interface.do_long_press(Key.down, 0.5)
    time.sleep(0.5)
    my_interface.do_long_press("x", 0.5)
    time.sleep(0.5)
    my_interface.do_long_press(Key.right, 0.5)
    time.sleep(0.5)
    my_interface.do_long_press("x", 0.5)
    time.sleep(0.5)
    my_interface.do_long_press("x", 0.5)
    time.sleep(0.5)
    my_interface.do_long_press("x", 0.5)


def do_battle():
    """
    Tells the character to start battling.
    """

    print("Preparing for battle...")
    print("Searching pokedex...")

    pokemon_name = my_interface.get_pokemon_name()
    pokedex_entry = my_pokedex.get_pokemon_entry_fuzzy(pokemon_name)

    if pokedex_entry:
        my_pokedex.print_pokemon_card(pokedex_entry)

    is_battling = True

    while is_battling:
        if not my_interface.check_is_battling():
            print("The battle appears to have ended.")
            is_battling = False
            break

        if my_interface.check_is_registering():
            print("Registering pokémon...")
            my_interface.do_long_press("x", 0.5)

        elif my_interface.check_is_leveling_up():
            print("Leveling up...")
            my_interface.do_long_press("z", 0.5)

        else:
            # Get the message text.
            battle_text = my_interface.get_message_text(
                custom_width=95, custom_height=35
            )

            if "what will" in battle_text:
                if not my_interface.check_is_pokemon_caught():
                    print("Pokémon not already caught.")
                    do_throw_pokeball()
                else:
                    print("Attacking pokémon...")
                    my_interface.do_long_press(Key.up, 0.5)
                    time.sleep(0.5)
                    my_interface.do_long_press("x", 0.5)
                    time.sleep(0.5)
                    my_interface.do_long_press("x", 0.5)

            if "give" in battle_text:
                print("Skipping nickname...")
                my_interface.do_long_press("z", 0.5)

        # Wait between checking messages.
        time.sleep(2)


def do_fishing():
    """
    Tells the character to start fishing.
    """

    is_fishing = True

    while is_fishing:
        print("Using fishing rod...")
        my_interface.do_long_press("a", 0.5)

        waiting_for_fish = True

        while waiting_for_fish:
            fish_alert = my_interface.check_is_pokemon_hooked()

            if fish_alert:
                print("Hooking pokémon...")
                my_interface.do_long_press("x", 0.5)
                time.sleep(1)

            # Get the message text.
            fish_caught_text = my_interface.get_message_text()

            if "landed" in fish_caught_text:
                print("You landed a pokémon!")
                time.sleep(0.5)
                my_interface.do_long_press("x", 0.5)

                # Wait for the animation to finish.
                time.sleep(18)

                # Run the battle script.
                do_battle()

                # Cast the line back into the water.
                time.sleep(10)
                print("Using fishing rod...")
                my_interface.do_long_press("a", 0.5)

            # Get the message text.
            no_fish_text = my_interface.get_message_text()

            if "not even" in no_fish_text:
                print("Not even a nibble!")
                time.sleep(0.5)
                my_interface.do_long_press("x", 0.5)
                waiting_for_fish = False
            else:
                # TODO: Create our own trainddata for words like "pokémon", etc.
                # https://tesseract-ocr.github.io/tessdoc/#training-for-tesseract-5
                fish_got_away_text = my_interface.get_message_text(
                    custom_x=168, custom_width=96, custom_height=35
                )

                if "got away" in fish_got_away_text:
                    print("The pokémon got away!")
                    time.sleep(0.5)
                    my_interface.do_long_press("x", 0.5)
                    waiting_for_fish = False

        # Wait between fishing attempts.
        time.sleep(2)


def do_patrol():
    """
    Tells the character to start patrolling.
    """

    print("Starting patrol...")

    is_patrolling = True

    while is_patrolling:
        # Get the battle text.
        battle_text = my_interface.get_message_text(custom_width=95, custom_height=35)

        if "what will" in battle_text:
            # Run the battle script.
            do_battle()

            print("Resuming patrol...")
        else:
            # Walk back and forth.
            my_interface.do_walk_left()
            time.sleep(0.2)
            my_interface.do_walk_right()

        # Wait between patrols.
        time.sleep(0.5)


def do_update_pokedex():
    print("Starting update...")

    is_updating = True

    while is_updating:
        # Step 1: Extract the name.
        name = _extract_pokedex_name()
        print("Name:", name)

        # Step 2: Extract the number.
        number = _extract_pokedex_number()
        print("Number:", number)

        # Step 3: Extract the description.
        desc = _extract_pokedex_description()
        print("Description:", desc)

        # Step 4: Extract is caught.
        is_caught = _extract_pokedex_is_caught()
        print("Is Caught:", is_caught)

        found_pokedex_entry = None
        pokemon_entry_by_number = None
        pokemon_entry_by_name = None

        if number > 0:
            # Try to match on number.
            pokemon_entry_by_number = my_pokedex.get_pokemon_entry_fuzzy(number)

        if name:
            # Try to match on name.
            pokemon_entry_by_name = my_pokedex.get_pokemon_entry_fuzzy(name)

        if pokemon_entry_by_number and pokemon_entry_by_name:
            if (
                pokemon_entry_by_number["Local Index"]
                == pokemon_entry_by_name["Local Index"]
            ):
                print("Found pokemon by name and number.")
                found_pokedex_entry = pokemon_entry_by_name
            else:
                print("Unable to reliably determine pokemon by name and number. Defaulting to name.")
                print()

                found_pokedex_entry = pokemon_entry_by_name
        elif pokemon_entry_by_name:
            print("Found pokemon by name.")
            found_pokedex_entry = pokemon_entry_by_name
        elif pokemon_entry_by_number:
            print("Found pokemon by number.")
            found_pokedex_entry = pokemon_entry_by_number
        else:
            print("Unable to find pokemon by name or number.")
            print()

        if found_pokedex_entry:
            my_pokedex.print_pokemon_card(found_pokedex_entry)

        time.sleep(2)
        my_interface.do_long_press(Key.up, 0.2)
        time.sleep(2)


def _extract_pokedex_is_caught():
    # Take a screenshot of the message area.
    screenshot = Screentail.get_screenshot(
        my_emulator,
        221,
        47,
        34,
        34,
        "extract-pokedex-is-caught.png",
    )

    is_scanning_image = True
    num_total_pixels = 0
    num_non_yellow_pixels = 0

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
            if pixel_color != (255, 255, 199) and pixel_color != (255, 239, 182):
                num_non_yellow_pixels += 1

            num_total_pixels += 1

    # Assume the pokemon is caught if the # of non-yellow pixels is greater than 60%.
    is_caught = num_non_yellow_pixels > num_total_pixels * 0.6

    return is_caught


def _extract_pokedex_description():
    # Take a screenshot of the description area.
    screenshot = Screentail.get_screenshot(
        my_emulator, 60, 272, 395, 95, "extract-pokedex-description.png"
    )

    # Convert image to grayscale.
    screenshot = screenshot.convert("L")

    # Extract the text.
    text = utils.get_ocr_text(screenshot)
    text = text.replace("\n", " ")

    return text


def _extract_pokedex_name():
    # Take a screenshot of the name area.
    screenshot = Screentail.get_screenshot(
        my_emulator, 310, 50, 200, 30, "extract-pokedex-name.png"
    )

    # Convert image to grayscale.
    screenshot = screenshot.convert("L")

    # Resize the image.
    width, height = screenshot.size
    screenshot = screenshot.resize((int(width * 1), int(height * 0.8)))

    # "Enhance... enhance... Keep going... okay, stop!"
    enhancer = ImageEnhance.Brightness(screenshot)
    screenshot = enhancer.enhance(1.2)
    enhancer = ImageEnhance.Contrast(screenshot)
    screenshot = enhancer.enhance(2.0)
    enhancer = ImageEnhance.Sharpness(screenshot)
    screenshot = enhancer.enhance(2.0)
    screenshot.save("pillow/extract-pokedex-name-enhanced.png")

    # Extract the name.
    name_text = utils.get_ocr_text(screenshot)
    name_text = name_text.strip()

    return name_text


def _extract_pokedex_number():
    # Take a screenshot of the number area.
    screenshot = Screentail.get_screenshot(
        my_emulator, 260, 50, 50, 28, "extract-pokedex-number.png"
    )

    # Convert image to grayscale.
    screenshot = screenshot.convert("L")

    # Resize the image.
    width, height = screenshot.size
    screenshot = screenshot.resize((int(width * 1), int(height * 0.8)))

    # "Enhance... enhance... Keep going... okay, stop!"
    enhancer = ImageEnhance.Brightness(screenshot)
    screenshot = enhancer.enhance(1.2)
    enhancer = ImageEnhance.Contrast(screenshot)
    screenshot = enhancer.enhance(2.0)
    enhancer = ImageEnhance.Sharpness(screenshot)
    screenshot = enhancer.enhance(2.0)
    screenshot.save("pillow/extract-pokedex-number-enhanced.png")

    # Extract the number.
    number_text = utils.get_ocr_numbers(screenshot)

    if number_text:
        # Remove leading zeros, if any.
        number = int(number_text)
        return number

    return -1


if len(sys.argv) > 1:
    # Get the first argument (e.g., `python pykemon.py patrol`), if any.
    first_arg = sys.argv[1]

    if first_arg == "fish":
        do_fishing()

    if first_arg == "battle":
        do_battle()

    if first_arg == "patrol":
        do_patrol()

    if first_arg == "update-pokedex":
        do_update_pokedex()

    if first_arg == "reset":
        print("Keyboard has been reset.")
else:
    print("No arguments were passed.")

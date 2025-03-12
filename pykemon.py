from pynput.keyboard import Controller, Key
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


if len(sys.argv) > 1:
    # Get the first argument (e.g., `python pykemon.py patrol`), if any.
    first_arg = sys.argv[1]

    if first_arg == "fish":
        do_fishing()

    if first_arg == "battle":
        do_battle()

    if first_arg == "patrol":
        do_patrol()

    if first_arg == "reset":
        print("Keyboard has been reset.")
else:
    print("No arguments were passed.")

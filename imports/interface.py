from pynput.keyboard import Controller, Key
from PIL import ImageOps
import time

from imports.screentail import Screentail
import imports.utils as utils


class Interface:
    my_emulator = None
    my_keyboard = Controller()

    def __init__(self, emulator):
        self.my_emulator = emulator

    def release_keys(self):
        """
        Releases any keys that might have gotten stuck during a force-quit.
        """

        keyboard = Controller()
        keyboard.release(Key.left)
        keyboard.release(Key.right)
        keyboard.release(Key.up)
        keyboard.release(Key.down)

    def do_long_press(self, key, duration):
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

    def do_walk_right(self):
        """
        Tells the character to walk to the right for 2 seconds. Used primarily
        for patrolling.
        """

        self.do_long_press(Key.right, 2)

    def do_walk_left(self):
        """
        Tells the character to walk to the left for 2 seconds. Used primarily
        for patrolling.
        """

        self.do_long_press(Key.left, 2)

    def get_message_text(
        self,
        custom_x=None,
        custom_y=None,
        custom_width=None,
        custom_height=None,
    ):
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
        y_offset = self.my_emulator.screen_dimensions[1] - 80
        y = y_offset + int(custom_y) if custom_y else y_offset
        width = (
            custom_width
            if custom_width
            else self.my_emulator.screen_dimensions[0] - 130
        )
        height = custom_height if custom_height else 70

        # Take a screenshot of the message area.
        screenshot = Screentail.get_screenshot(
            self.my_emulator, x, y, width, height, "get-message-text.png"
        )

        # Extract the text.
        text = utils.get_ocr_text(screenshot)
        text = text.lower()

        return text

    def get_pokemon_name(self):
        # Take a screenshot of the leveling area.
        screenshot = Screentail.get_screenshot(
            self.my_emulator, 0, 50, 120, 26, "get-pokemon-name.png"
        )

        # Load the image into memory to access pixels
        pixels = screenshot.load()

        # Get the image size
        width, height = screenshot.size

        # Define the target color to replace (e.g., RGB: (255, 0, 0) for red)
        target_color = (109, 117, 93)  # Brown
        replacement_color = (0, 0, 0)  # Black

        # Iterate through each pixel
        for x in range(width):
            for y in range(height):
                # Check if the current pixel matches the target color
                if pixels[x, y] == target_color:
                    pixels[x, y] = replacement_color  # Replace with the new color

        # Invert the screenshot for readability.
        screenshot = ImageOps.invert(screenshot)
        screenshot.save("pillow/get-pokemon-name-inverted.png")

        # Extract the text.
        text = utils.get_ocr_text(screenshot)
        text = text.lower()

        return text

    def check_is_pokemon_hooked(self):
        """
        Checks if the player currently has a hooked pokémon on the fishing line.
        This function should only be used while fishing.

        Returns:
            boolean: Whether the player has hooked a pokémon.
        """

        # Take a screenshot of the alert area.
        screenshot = Screentail.get_screenshot(
            self.my_emulator,
            int(self.my_emulator.screen_dimensions[0] / 2) - 10,
            int(self.my_emulator.screen_dimensions[1] / 2) - 10 - 50,
            24,
            24,
            "check-is-fish-hooked.png",
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

                if utils.is_pixel_mostly_red(pixel_color):
                    is_scanning_image = False
                    is_hooked = True

        return is_hooked

    def check_is_pokemon_caught(self):
        """
        Checks if pokémon that the player is currently battling has already
        been caught. Warning! This function should not be used for trainer battles
        because it will always return false.

        Returns:
            boolean: Whether the pokémon has already been caught.
        """

        # Take a screenshot of the icon area.
        screenshot = Screentail.get_screenshot(
            self.my_emulator, 6, 80, 14, 14, "check-is-pokemon-caught.png"
        )

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

                if utils.is_pixel_mostly_red(pixel_color):
                    is_scanning_image = False
                    is_caught = True

        return is_caught

    def check_is_battling(self):
        """
        Checks if the player is currently battling a pokémon.

        Returns:
            boolean: Whether the player is battling a pokémon.
        """

        # Take a screenshot of the message area.
        screenshot = Screentail.get_screenshot(
            self.my_emulator,
            30,
            self.my_emulator.screen_dimensions[1] - 80,
            self.my_emulator.screen_dimensions[0] - 130,
            70,
            "check-is-battling.png",
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

    def check_is_leveling_up(self):
        """
        Checks if the player is currently leveling up a pokémon.

        Returns:
            boolean: Whether the player is leveling up a pokémon.
        """

        # Take a screenshot of the leveling area.
        screenshot = Screentail.get_screenshot(
            self.my_emulator, 270, 145, 180, 30, "check-is-leveling-up.png"
        )

        # Extract the text.
        text = utils.get_ocr_text(screenshot)
        text = text.lower()

        return "attack" in text

    def check_is_registering(self):
        """
        Checks if the player is currently registering a pokémon.

        Returns:
            boolean: Whether the player is registering a pokémon.
        """

        # Take a screenshot of banner area.
        screenshot = Screentail.get_screenshot(
            self.my_emulator,
            self.my_emulator.screen_dimensions[0] - 20,
            0,
            10,
            10,
            "check-is-pokemon-registered.png",
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

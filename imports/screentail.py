from PIL import ImageGrab


class Screentail:
    @staticmethod
    def get_screenshot_bbox(emulator, x, y, width, height):
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

        starting_x = emulator.emulator_position[0]
        starting_y = (
            emulator.emulator_position[1]
            + emulator.emulator_menu_height
        )

        x1 = starting_x + x
        y1 = starting_y + y
        x2 = x1 + width
        y2 = y1 + height

        return (x1, y1, x2, y2)

    @staticmethod
    def get_screenshot(emulator, x, y, width, height, filename=None):
        """
        Gets a screenshot of the specified area.

        Args:
            emulator (window): The emulator window.
            x (int): The X coordinate.
            y (int): The Y coordinate.
            width (int): The width of the area to capture.
            height (int): The height of the area to capture.
            filename (str): (Optional) The filename to save the screenshot to.

        Returns:
            Image: The screenshot.
        """

        # Get the bounding box.
        bbox = Screentail.get_screenshot_bbox(emulator, x, y, width, height)

        # Take the screenshot and convert to RGB.
        screenshot = ImageGrab.grab(all_screens=True, bbox=bbox)
        screenshot = screenshot.convert("RGB")

        # Save the screenshot.
        if filename:
            screenshot.save(f"pillow/{filename}")

        return screenshot

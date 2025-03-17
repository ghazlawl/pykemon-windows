import pygetwindow as gw


class Emulator:
    emulator_window = None
    emulator_dimensions = (0, 0)
    emulator_position = (0, 0)
    emulator_menu_height = 80

    screen_dimensions = (0, 0)

    def __init__(self):
        self.emulator_window = self.get_window()

        if self.emulator_window:
            self.activate_window()
            self.update_vars()

    def get_window(self):
        """
        Gets the DeSmuME emulator window, if any.
        """

        # Get all emulator windows, if present.
        emulator_windows = gw.getWindowsWithTitle("DeSmuME")

        if len(emulator_windows) > 0:
            # Get the first emulator window.
            emulator_window = emulator_windows[0]

        # Quit the application if the emulator window doesn't exist.
        if not emulator_window:
            print("DeSmuME emulator not running.")
            quit()

        # Let the user know that we found the emulator window.
        print(f"DeSmuME emulator window found: {emulator_window.title}")

        return emulator_window

    def activate_window(self):
        """
        Activates (focuses) the emulator window.
        """

        self.emulator_window.activate()
        self.update_vars()

    def update_vars(self):
        """
        Updates the emulator position, screen position, and screen
        dimension local variables.
        """
        
        self.emulator_position = (
            self.emulator_window.left + 6,
            self.emulator_window.top,
        )

        self.emulator_dimensions = (
            self.emulator_window.width - 12,
            self.emulator_window.height - 8,
        )

        self.screen_dimensions = (
            self.emulator_dimensions[0],
            int((self.emulator_dimensions[1] - self.emulator_menu_height) / 2),
        )

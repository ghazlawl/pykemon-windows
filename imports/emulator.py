import pygetwindow as gw


class Emulator:
    emulator_window = None

    def __init__(self):
        self.emulator_window = self.get_window()

    def get_window(self):
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

import pytesseract

from imports.screentail import Screentail

# Set the tesseract executable location.
# TODO: Move this to the .env file.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def debug_screen_1(emulator):
    """
    Captures a screenshot of the top screen. Used to confirm x, y, width,
    and height values.
    """
    screenshot = Screentail.get_screenshot(
        0,
        0,
        emulator.screen_dimensions[0],
        emulator.screen_dimensions[1],
        "screen-1.png",
    )

    return screenshot


def debug_screen_2(emulator):
    """
    Captures a screenshot of the bottom screen. Used to confirm x, y, width,
    and height values.
    """
    screenshot = Screentail.get_screenshot(
        0,
        emulator.screen_dimensions[1],
        emulator.screen_dimensions[0],
        emulator.screen_dimensions[1],
        "screen-2.png",
    )

    return screenshot


def is_pixel_mostly_red(pixel):
    """
    Checks if the specified pixel is mostly red. A pixel is mostly red if the
    red value is 3x greater or more than the green and blue values.
    """

    red, green, blue = pixel
    return red > green * 3 and red > blue * 3


def get_ocr_text(screenshot):
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
    custom_config = r"--oem 3 --psm 6"
    text = pytesseract.image_to_string(screenshot, lang="eng", config=custom_config)
    text = text.strip()

    return text

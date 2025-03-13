from fuzzywuzzy import process
import csv
import re


class Pokedex:
    pokemon_db = []
    strength_matrix = {}
    weakness_matrix = {}

    CARD_WIDTH = 60

    COLORS = {
        "BLACK": "\033[30m",
        "RED": "\33[91m",
        "GREEN": "\033[32m",
        "YELLOW": "\033[93m",
        "BLUE": "\33[94m",
        "PURPLE": "\033[0;35m",
        "CYAN": "\033[36m",
        "WHITE": "\033[37m",
        "END": "\033[0m",
        "GRAY": "\033[38;5;8m",
    }

    def __init__(self):
        print("Loading Pokémon database...")
        self.load_pokemon_db()

        print("Loading Pokémon strength/weakness matrices...")
        self.load_strength_matrix()
        self.load_weakness_matrix()

    def load_pokemon_db(self):
        """
        Loads the pokemon database from a CSV. Loaded data includes
        index, name, type(s), height, and weight.
        """

        # Open the CSV file.
        with open(
            "data/pokedex-platinum.csv", mode="r", newline="", encoding="utf-8"
        ) as csv_file:
            # Read the CSV into a dictionary.
            csv_reader = csv.DictReader(csv_file)

            # Convert the CSV rows to a list of dictionaries.
            self.pokemon_db = list(csv_reader)

    def load_strength_matrix(self):
        """
        Loads the strength matrix, which is a list of types and what
        each type is strong against.
        """

        # Open the CSV file.
        with open(
            "data/pokemon-strengths.csv", mode="r", newline="", encoding="utf-8"
        ) as csv_file:
            # Read the CSV into a dictionary.
            csv_reader = csv.DictReader(csv_file)

            # Loop through the rows and populate the dictionary.
            for row in csv_reader:
                # Extract the type and strength from the row.
                type = row["Type"]
                strengths = [
                    row[f"Strength {i}"] for i in range(1, 6) if row[f"Strength {i}"]
                ]

                # Add the data to the dictionary.
                self.strength_matrix[type] = strengths

        pass

    def load_weakness_matrix(self):
        """
        Loads the weakness matrix, which is a list of types and what
        each type is weak against.
        """

        # Open the CSV file.
        with open(
            "data/pokemon-weaknesses.csv", mode="r", newline="", encoding="utf-8"
        ) as csv_file:
            # Read the CSV into a dictionary.
            csv_reader = csv.DictReader(csv_file)

            # Loop through the rows and populate the dictionary.
            for row in csv_reader:
                # Extract the type and weaknesses from the row.
                type = row["Type"]
                weaknesses = [
                    row[f"Weakness {i}"] for i in range(1, 6) if row[f"Weakness {i}"]
                ]

                # Add the data to the dictionary.
                self.weakness_matrix[type] = weaknesses

    def get_pokemon_entry_fuzzy(self, search):
        """
        Gets the pokedex entry for the specified value using a
        fuzzy search. OCR is not 100% accurate (for now) so using a
        fuzzy search is currently the best way to get entries.

        TODO: Return the pokedex entry instead of printing the values.

        Args:
            search (str): The pokemon name to search for.

        Returns:
            entry: The pokedex entry object.

        Example:
            >>> get_pokemon_entry_fuzzy('picklchu')
            { name: "Pikachu", height: "1'2\"", weight: "1.4", ...}
        """

        # Get the corresponding data for the best match.
        matched_entry = next(
            (entry for entry in self.pokemon_db if entry["Local Index"] == str(search)), None
        )

        if not matched_entry:
            # Extract the list of names from the data.
            names = [entry["Name"] for entry in self.pokemon_db]

            # Find the best match.
            best_match = process.extractOne(str(search), names)

            # Get the corresponding data for the best match.
            matched_entry = next(
                (entry for entry in self.pokemon_db if entry["Name"] == best_match[0]),
                None,
            )

        return matched_entry

    def get_type_strengths(self, types):
        """
        Gets the types of attacks the specified types are strong against.

        Args:
            type (str[]): The type to check.

        Example:
            >>> get_type_strengths('Electric')
            ['Water', 'Flying']
        """

        strengths = {}

        for pokemon_type in types:
            if pokemon_type in self.strength_matrix:
                strengths[pokemon_type] = self.strength_matrix[pokemon_type]

        return strengths

    def get_type_weaknesses(self, types):
        """
        Gets the types of attacks the specified types are weak to.

        Args:
            type (str[]): The type to check.

        Example:
            >>> get_type_weaknesses('Fighting')
            ['Flying', 'Psychic', 'Fairy']
        """

        weaknesses = {}

        for pokemon_type in types:
            if pokemon_type in self.weakness_matrix:
                weaknesses[pokemon_type] = self.weakness_matrix[pokemon_type]

        return weaknesses

    def print_pokemon_card(self, entry):
        """
        Prints the card for the specified pokedex entry.

        Args:
            entry (obj): The pokedex entry.
        """

        types = [entry["Type 1"], entry["Type 2"]]
        types = [item for item in types if item]

        index = int(entry["Local Index"])
        name = entry["Name"]
        height = entry["Height"]
        weight = entry["Weight"]

        print()
        print(f"╭{'━' * (self.CARD_WIDTH - 2)}╮")

        self.__print_card_line(
            f"Pokedex No: {self.COLORS['GRAY']}{index:03}{self.COLORS['END']}"
        )

        self.__print_card_line(f"Name: {self.COLORS['GRAY']}{name}{self.COLORS['END']}")

        self.__print_card_line(
            f"Height/Weight: {self.COLORS['GRAY']}{height} {weight} lbs{self.COLORS['END']}"
        )

        for index, type in enumerate(types):
            if type:
                self.__print_card_line(
                    f"Type {index + 1}: {self.COLORS['GRAY']}{type}{self.COLORS['END']}"
                )

                # Get the strengths, if any.
                strengths = self.get_type_strengths([entry[f"Type {index + 1}"]])

                # Output the strengths.
                for type, list in strengths.items():
                    list = [item for item in list if item]
                    list = ", ".join(list)

                    self.__print_card_line(
                        f"Type {index + 1} Strong: {self.COLORS['GRAY']}{list if len(list) > 0 else 'Nothing'}{self.COLORS['END']}"
                    )

                # Get the weaknesses, if any.
                weaknesses = self.get_type_weaknesses([entry[f"Type {index + 1}"]])

                for type, list in weaknesses.items():
                    list = [item for item in list if item]
                    list = ", ".join(list)

                    self.__print_card_line(
                        f"Type {index + 1} Weak: {self.COLORS['GRAY']}{list if len(list) > 0 else 'Nothing'}{self.COLORS['END']}"
                    )

        print(f"╰{'─' * (self.CARD_WIDTH - 2)}╯")
        print()

    def __print_card_line(self, text):
        """
        Prints a card line. Supports ANSI escape characters for colorization.

        Args:
            text (str): The text to print.
        """

        # Get the length of the original text.
        original_text_length = len(text)

        # Get the length of the text without ANSI escape characters.
        visible_text_length = len(re.sub(r"\x1b\[[0-9;]*m", "", text))

        # Calculate the difference.
        length_diff = original_text_length - visible_text_length

        print(
            "│",
            f"{text:{(self.CARD_WIDTH - 4 + length_diff)}}",
            "│",
        )

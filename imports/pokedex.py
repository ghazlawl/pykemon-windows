from fuzzywuzzy import process

import csv


class Pokedex:
    pokemon_db = []
    strength_matrix = {}
    weakness_matrix = {}

    CARD_WIDTH = 60

    def __init__(self):
        self.load_pokemon_db()
        self.load_strength_matrix()
        self.load_weakness_matrix()

    def load_pokemon_db(self):
        """
        Loads the pokemon database from a CSV. Loaded data includes
        index, name, type(s), height, and weight.
        """

        print("Loading Pokémon database...")

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
        TODO: Loads the strength matrix, which is a list of types and what
        each type is strong against.
        """

        pass

    def load_weakness_matrix(self):
        """
        Loads the weakness matrix, which is a list of types and what
        each type is weak against.
        """

        print("Loading Pokémon weakness matrix...")

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

        # Extract the list of names from the data
        names = [entry["Name"] for entry in self.pokemon_db]

        # Find the best match
        best_match = process.extractOne(search, names)

        # Get the corresponding data for the best match
        matched_entry = next(
            entry for entry in self.pokemon_db if entry["Name"] == best_match[0]
        )

        # print("+", "-" * 20, "+")
        # print(f"Searching pokémon database for '{search}'...")
        # print(f"Name: {matched_entry['Name']}")
        # print(
        #     f"Height/Weight: {matched_entry['Height']}, {matched_entry['Weight']} lbs"
        # )
        # print(f"Local Index: {matched_entry['Local Index']}")
        # print(f"Types: {', '.join([matched_entry['Type 1'], matched_entry['Type 2']])}")

        # weakness_list = self.get_type_weaknesses(
        #     [matched_entry["Type 1"], matched_entry["Type 2"]]
        # )

        # for type, weaknesses in weakness_list.items():
        #     print(f"Weaknesses of {type}: {weaknesses}")

        # print("+", "-" * 20, "+")

        return matched_entry

    def get_type_weaknesses(self, types):
        """
        Gets the types of attacks the specified type is weak to.

        Args:
            type (str): The type to check.

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
        types = [entry['Type 1'], entry['Type 2']]
        types = [item for item in types if item]
        types = ", ".join(types)

        index = int(entry["Local Index"])
        name = entry["Name"]

        print()
        print(f"╭{'━' * (self.CARD_WIDTH - 2)}╮")
        self._print_pokedex_card_line(f"Pokedex No: {index:03}")
        self._print_pokedex_card_line(f"Name: {name}")
        self._print_pokedex_card_line(f"Type: {types}")
        self._print_pokedex_card_line("Strong Against: ?")

        weaknesses = self.get_type_weaknesses([entry["Type 1"], entry["Type 2"]])

        for type, list in weaknesses.items():
            list = [item for item in list if item]
            list = ", ".join(list)
            
            self._print_pokedex_card_line(f"Weakness: {list}")

        print(f"╰{'─' * (self.CARD_WIDTH - 2)}╯")
        print()

    def _print_pokedex_card_line(self, text):
        print(
            "│",
            f"{text:{(self.CARD_WIDTH - 4)}}",
            "│",
        )

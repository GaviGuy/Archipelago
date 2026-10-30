from collections.abc import Mapping
from typing import Any

from Options import OptionError

from worlds.AutoWorld import World

from . import items, locations, regions, rules, web_world, puzzle_pool, puzzle_database
from . import options as variant_sudoku_options  # rename due to a name conflict with World.options

# APQuest will go through all the parts of the world api one step at a time,
# with many examples and comments across multiple files.
# If you'd rather read one continuous document, or just like reading multiple sources,
# we also have this document specifying the entire world api:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md


# The world class is the heart and soul of an apworld implementation.
# It holds all the data and functions required to build the world and submit it to the multiworld generator.
# You could have all your world code in just this one class, but for readability and better structure,
# it is common to split up world functionality into multiple files.
# This implementation in particular has the following additional files, each covering one topic:
# regions.py, locations.py, rules.py, items.py, options.py and web_world.py.
# It is recommended that you read these in that specific order, then come back to the world class.
class VariantSudokuWorld(World):
    """
    Variant Sudoku builds on traditional Sudoku rules with unique additions.
    The puzzle grid might contain double ratio hints, palindrome lines, or even fog of war.
    Puzzles often begin with no numbers. You must use these new clues to find your footing.
    """

    game = "Variant Sudoku"


    # The WebWorld is a definition class that governs how this world will be displayed on the website.
    web = web_world.VariantSudokuWebWorld()

    # This is how we associate the options defined in our options.py with our world.
    options_dataclass = variant_sudoku_options.VariantSudokuOptions
    options: variant_sudoku_options.VariantSudokuOptions


    # Our world class must have a static location_name_to_id and item_name_to_id defined.
    # We define these in regions.py and items.py respectively, so we just set them here.
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    # There is always one region that the generator starts from & assumes you can always go back to.
    # This defaults to "Menu", but you can change it by overriding origin_region_name.
    origin_region_name = "Start"

    ALL_PUZZLES = None
    SELECTED_PUZZLES = None
    DATABASE_VERSION = None
    STARTER_PUZZLES = None
    NUM_BONUS = 0

    def generate_early(self) -> None:
        # load JSON data

        self.ALL_PUZZLES = puzzle_database.PUZZLE_DATABASE["puzzles"]
        self.DATABASE_VERSION = puzzle_database.PUZZLE_DATABASE["vers"]

        # attempt to generate a valid puzzle pool up to 10 times
        num_attempts = 0
        while self.SELECTED_PUZZLES is None and num_attempts < 10:
            self.SELECTED_PUZZLES = puzzle_pool.create_puzzle_pool(self)
            num_attempts += 1

        if self.SELECTED_PUZZLES is None:
            raise OptionError("Criteria in yaml couldn't be met using the available puzzle database")

        num_puzzles = len(self.SELECTED_PUZZLES["filler"]) + len(self.SELECTED_PUZZLES["pillars"]) + 1
        plural = ""
        if num_attempts > 1:
            plural = "s"

        # print("Created a pool of {0} puzzles in {1} attempt{2}".format(num_puzzles, num_attempts, plural))

    # Our world class must have certain functions ("steps") that get called during generation.
    # The main ones are: create_regions, set_rules, create_items.
    # For better structure and readability, we put each of these in their own file.
    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    # Our world class must also have a create_item function that can create any one of our items by name at any time.
    # We also put this in a different file, the same one that create_items is in.
    def create_item(self, name: str) -> items.VariantSudokuItem:
        return items.create_item_with_correct_classification(self, name)

    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # For this purpose, your world *must* have at least one infinitely repeatable item (usually filler).
    # You must override this function and return this infinitely repeatable item's name.
    # In our case, we defined a function called get_random_filler_item_name for this purpose in our items.py.
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    # There may be data that the game client will need to modify the behavior of the game.
    # This is what slot_data exists for. Upon every client connection, the slot's slot_data is sent to the client.
    # slot_data is just a dictionary using basic types, that will be converted to json when sent to the client.
    def fill_slot_data(self) -> Mapping[str, Any]:
        boss_req = self.options.pillar_count.value
        if self.options.boss_unlock_condition.value == 0:
            boss_req = self.options.boss_unlock_item_requirement.value

        elif self.options.boss_unlock_condition.value == 1:
            boss_req = self.options.boss_unlock_puzzle_requirement.value

        # i think i need to give a seed to slotData, to assist with savedata

        ret = {
            "bossUnlock": self.options.boss_unlock_condition.value,
            "puzzlesVer": self.DATABASE_VERSION,
            "bossId": self.SELECTED_PUZZLES["boss"]["id"],
            "bossUnlockCount": boss_req,
        }

        if self.options.boss_unlock_condition.value == 2:
            pillar_ids = []
            for i in self.SELECTED_PUZZLES["pillars"]:
                pillar_ids.append(i["id"])

            ret["pillarIds"] = pillar_ids

        return ret
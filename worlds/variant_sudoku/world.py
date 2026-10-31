from collections.abc import Mapping
from typing import Any

from Options import OptionError

from worlds.AutoWorld import World

from . import items, locations, regions, rules, web_world, puzzle_pool, puzzle_database
from . import options as variant_sudoku_options  # rename due to a name conflict with World.options

class VariantSudokuWorld(World):
    """
    Variant Sudoku builds on traditional Sudoku rules with unique additions.
    The puzzle grid might contain double ratio hints, palindrome lines, or even fog of war.
    Puzzles often begin with no numbers. You must use these new clues to find your footing.
    """

    game = "Variant Sudoku"

    web = web_world.VariantSudokuWebWorld()

    options_dataclass = variant_sudoku_options.VariantSudokuOptions
    options: variant_sudoku_options.VariantSudokuOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Start"

    ALL_PUZZLES = None
    SELECTED_PUZZLES = None
    DATABASE_VERSION = None
    STARTER_PUZZLES = None
    NUM_BONUS = 0

    def generate_early(self) -> None:
        self.ALL_PUZZLES = puzzle_database.PUZZLE_DATABASE["puzzles"]
        self.DATABASE_VERSION = puzzle_database.PUZZLE_DATABASE["vers"]

        # attempt to generate a valid puzzle pool up to 10 times
        num_attempts = 0
        while self.SELECTED_PUZZLES is None and num_attempts < 10:
            self.SELECTED_PUZZLES = puzzle_pool.create_puzzle_pool(self)
            num_attempts += 1

        if self.SELECTED_PUZZLES is None:
            raise OptionError("Criteria in yaml couldn't be met using the available puzzle database")

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)


    def create_item(self, name: str) -> items.VariantSudokuItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        boss_req = self.options.pillar_count.value
        if self.options.boss_unlock_condition.value == 0:
            boss_req = self.options.boss_unlock_item_requirement.value

        elif self.options.boss_unlock_condition.value == 1:
            boss_req = self.options.boss_unlock_puzzle_requirement.value

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
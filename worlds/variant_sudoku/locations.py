from __future__ import annotations

from math import ceil

from typing import TYPE_CHECKING

from BaseClasses import Location, LocationProgressType

from .puzzle_database import PUZZLE_DATABASE

if TYPE_CHECKING:
    from .world import VariantSudokuWorld

# Helper to make a location names using a puzzle's title and author
def puzzle_to_location_names(puzzle):
    ret = []
    for i in range(puzzle["rating"]):
        ret.append(puzzle["title"] + " - " + puzzle["author"] + " " + str(i+1))
    return ret

LOCATION_NAME_TO_ID = {}

# Pillar bonuses
# start at 100
for i in range(8):
    LOCATION_NAME_TO_ID["Pillar Bonus " + str(i+1)] = 100 + i

# Generic bonuses
# start at 200
for i in range(20):
    LOCATION_NAME_TO_ID["Bonus " + str(i+1)] = 200 + i

# Puzzle clears
# start at 1000, iterate by 10 per puzzle, and include multiple for harder puzzles
for i in PUZZLE_DATABASE["puzzles"]:
    names = puzzle_to_location_names(i)
    for j in range(len(names)):
        LOCATION_NAME_TO_ID[names[j]] = i["id"] + j

class VariantSudokuLocation(Location):
    game = "Variant Sudoku"

def append_locations_by_puzzle(world: VariantSudokuWorld, puzzle: str,
                               classification: LocationProgressType = LocationProgressType.DEFAULT) -> None:

    locs = puzzle_to_location_names(puzzle)
    for i in locs:
        new_loc = VariantSudokuLocation(world.player, i, LOCATION_NAME_TO_ID[i], world.get_region("Start"))

        new_loc.progress_type = classification
        world.get_region("Start").locations.append(new_loc)

def create_all_locations(world: VariantSudokuWorld) -> None:
    create_regular_locations(world)


def create_regular_locations(world: VariantSudokuWorld) -> None:
    # a number of bonuses equal to key pieces
    start = world.get_region("Start")
    if world.options.boss_unlock_condition.value == 0:
        world.NUM_BONUS = world.options.boss_unlock_item_requirement.value
        for i in range(world.NUM_BONUS):
            loc_name = "Bonus " + str(i+1)
            new_loc = VariantSudokuLocation(world.player, loc_name, LOCATION_NAME_TO_ID[loc_name], start)
            start.locations.append(new_loc)

    # a number of bonuses equal to 50% the filler puzzle count
    if world.options.boss_unlock_condition.value == 1:
        world.NUM_BONUS = ceil(world.options.filler_count.value / 2)
        for i in range(world.NUM_BONUS):
            loc_name = "Bonus " + str(i+1)
            new_loc = VariantSudokuLocation(world.player, loc_name, LOCATION_NAME_TO_ID[loc_name], start)
            start.locations.append(new_loc)

    # 1 bonus per pillar, or 2 per pillar if there's 3 or fewer pillars
    if world.options.boss_unlock_condition.value == 2:
        world.NUM_BONUS = world.options.pillar_count.value
        if world.NUM_BONUS < 4:
            world.NUM_BONUS *= 2
        for i in range(world.NUM_BONUS):
            loc_name = "Pillar Bonus " + str(i+1)
            new_loc = VariantSudokuLocation(world.player, loc_name, LOCATION_NAME_TO_ID[loc_name], start)
            start.locations.append(new_loc)

    # Location(s) for each filler puzzle
    for i in world.SELECTED_PUZZLES["filler"]:
        append_locations_by_puzzle(world, i)
    
    # Location(s) for each pillar puzzle, if applicable
    if world.options.boss_unlock_condition.value == 2:
        for i in world.SELECTED_PUZZLES["pillars"]:
            append_locations_by_puzzle(world, i)

    # Location(s) for the boss puzzle
    append_locations_by_puzzle(world, world.SELECTED_PUZZLES["boss"], LocationProgressType.EXCLUDED)
from __future__ import annotations

import copy

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .puzzle_database import PUZZLE_DATABASE

if TYPE_CHECKING:
    from .world import VariantSudokuWorld

# Helper to make an item name using a puzzle's title, author, and rating
def puzzle_to_item_name(puzzle):
    stars = ""
    for _ in range(puzzle["rating"]):
        stars += "*"
    return puzzle["title"] + " - " + puzzle["author"] + " (" + stars + ")"

FILLER_ITEMS = [
    "Gray Kropki Dot",
    "Anti-Rook",
    "Renban Region"
]

USEFUL_ITEMS = [
    "Puzzle Reroll"
]

ITEM_NAME_TO_ID = {
    "Key Piece": 1,
}

# populate list of item ids with filler items and puzzles
# filler item ids come immediately after key item ids
item_id = len(ITEM_NAME_TO_ID) + 1

for i in FILLER_ITEMS:
    ITEM_NAME_TO_ID[i] = item_id
    item_id += 1

for i in USEFUL_ITEMS:
    ITEM_NAME_TO_ID[i] = item_id
    item_id += 1

# puzzle ids are preset, start at 1000, and iterate by 10. surely this won't pose an issue later :clueless:
for i in PUZZLE_DATABASE["puzzles"]:
    ITEM_NAME_TO_ID[puzzle_to_item_name(i)] = i["id"]


class VariantSudokuItem(Item):
    game = "Variant Sudoku"

def get_random_filler_item_name(world: VariantSudokuWorld) -> str:
    return FILLER_ITEMS[world.random.randint(0, len(FILLER_ITEMS) - 1)]

def get_random_useful_item_name(world: VariantSudokuWorld) -> str:
    return USEFUL_ITEMS[world.random.randint(0, len(USEFUL_ITEMS) - 1)]


def create_item_with_correct_classification(world, name) -> VariantSudokuItem:
    classification = ItemClassification.progression
    if name in FILLER_ITEMS:
        classification = ItemClassification.filler
    if name in USEFUL_ITEMS:
        classification = ItemClassification.useful

    return VariantSudokuItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: VariantSudokuWorld) -> None:

    itempool: list[Item] = []
    filler_copy = copy.deepcopy(world.SELECTED_PUZZLES["filler"])

    # Pick 2 puzzles from filler and give them to the player for free (eg. no item for them)
    world.STARTER_PUZZLES = []
    for i in range(2):
        if len(filler_copy) < 1:
            break
        world.STARTER_PUZZLES.append(filler_copy.pop(world.random.randint(0,len(filler_copy) - 1)))
        item = world.create_item(puzzle_to_item_name(world.STARTER_PUZZLES[i]))
        world.push_precollected(item)

    # Create items for every other puzzle
    for i in filler_copy:
        itempool.append(world.create_item(puzzle_to_item_name(i)))

    if world.options.boss_unlock_condition.value == 2:
        for i in world.SELECTED_PUZZLES["pillars"]:
            itempool.append(world.create_item(puzzle_to_item_name(i)))

    # Create key pieces, if applicable
    if world.options.boss_unlock_condition.value == 0:
        for i in range(world.options.boss_unlock_item_requirement):
            itempool.append(world.create_item("Key Piece"))

    # Filler
    num_filler = len(world.multiworld.get_unfilled_locations(world.player)) - len(itempool)
    for i in range(num_filler):
        if i < world.options.useful_item_count.value:
            itempool.append(world.create_item(get_random_useful_item_name(world)))
        else:
            itempool.append(world.create_item(get_random_filler_item_name(world)))

    world.multiworld.itempool += itempool
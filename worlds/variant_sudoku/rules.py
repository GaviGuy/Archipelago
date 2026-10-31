from __future__ import annotations

from math import floor
from typing import TYPE_CHECKING

from Options import OptionError
from rule_builder.rules import Has, False_, Rule, AtLeast

from .locations import puzzle_to_location_names
from .items import puzzle_to_item_name

if TYPE_CHECKING:
    from .world import VariantSudokuWorld

def has_number_of_puzzles(puzzles: dict, number: int) -> Rule:
    rule_list = []
    for i in puzzles:
        name = puzzle_to_item_name(i)
        rule_list.append(Has(name))

    ret = AtLeast(number, *rule_list)
    return ret

def get_boss_access_rule(world: VariantSudokuWorld) -> Rule:

    if world.options.boss_unlock_condition.value == 0:
        # must have enough key pieces
        return Has("Key Piece", world.options.boss_unlock_item_requirement.value)

    elif world.options.boss_unlock_condition.value == 1:
        # must have enough puzzle items
        return has_number_of_puzzles(world.SELECTED_PUZZLES["filler"],
                                     world.options.boss_unlock_puzzle_requirement.value)

    elif world.options.boss_unlock_condition.value == 2:
        # must have all pillars
        return has_number_of_puzzles(world.SELECTED_PUZZLES["pillars"],
                                     world.options.pillar_count.value)

    return False_()

def set_all_rules(world: VariantSudokuWorld) -> None:
    set_all_location_rules(world)


def set_all_location_rules(world: VariantSudokuWorld) -> None:

    # For accessing filler and pillar puzzles
    for i in world.SELECTED_PUZZLES["filler"]:
        locs = puzzle_to_location_names(i)
        item = puzzle_to_item_name(i)
        for j in locs:
            world.set_rule(world.get_location(j), Has(item))

    for i in world.SELECTED_PUZZLES["pillars"]:
        locs = puzzle_to_location_names(i)
        item = puzzle_to_item_name(i)
        for j in locs:
            world.set_rule(world.get_location(j), Has(item))

    # For accessing bonuses
    puzzle_count = world.options.filler_count.value

    # If there are pillars, distribute bonus to them
    if world.options.boss_unlock_condition.value == 2:
        num_pillars = world.options.pillar_count.value
        bonus_per_puzzle = world.NUM_BONUS / num_pillars

        # if this doesn't result in an integer, something has gone very wrong
        if int(bonus_per_puzzle) != bonus_per_puzzle:
            raise OptionError("Error in pillar logic. Please issue a bug report with your APWorld version and YAML")

        for i in range(world.NUM_BONUS):
            loc_name = "Pillar Bonus " + str(i+1)
            puzzle_number = floor(i / bonus_per_puzzle)
            world.set_rule(world.get_location(loc_name),
                           has_number_of_puzzles(world.SELECTED_PUZZLES["pillars"], puzzle_number + 1))

    # Otherwise, distribute bonus to filler puzzles
    else:
        bonus_per_puzzle = 2
        # For key piece mode specifically, there might not be enough puzzles to carry all the needed bonus
        while puzzle_count * bonus_per_puzzle < world.NUM_BONUS:
            bonus_per_puzzle += 1

        for i in range(world.NUM_BONUS):
            loc_name = "Bonus " + str(i+1)
            puzzle_number = floor(i / bonus_per_puzzle)
            world.set_rule(world.get_location(loc_name),
                           has_number_of_puzzles(world.SELECTED_PUZZLES["filler"], puzzle_number + 1))

    # For accessing the boss puzzle
    can_access_boss = get_boss_access_rule(world)

    boss_loc = puzzle_to_location_names(world.SELECTED_PUZZLES["boss"])
    for i in boss_loc:
        world.set_rule(world.get_location(i), can_access_boss)

    # Completion condition
    world.set_completion_rule(can_access_boss)
from __future__ import annotations

import copy

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import VariantSudokuWorld


PUZZLES_COPY = []

def remove_puzzle(puzzle) -> None:
    for i in PUZZLES_COPY:
        if i["link"] == puzzle["link"]:
            PUZZLES_COPY.remove(i)

def select_puzzle(world, min_rating: int, max_rating: int) -> dict | None:
    puzzle_subset = []
    for i in PUZZLES_COPY:
        if min_rating <= i["rating"] <= max_rating:
            #TODO: check for filtered tags
            puzzle_subset.append(i)
    
    # fail state: no puzzles left that fit the criteria
    if len(puzzle_subset) <= 0:
        return None
    
    # success state: take a puzzle at random, remove it from the pool, return it
    ret = puzzle_subset[world.random.randint(0, len(puzzle_subset) - 1)]
    remove_puzzle(ret)
    return ret

def select_puzzle_link(link):
    for i in PUZZLES_COPY:
        if i["link"] == link:
            return i
    return None


def create_puzzle_pool(world: VariantSudokuWorld) -> dict | None:
    global PUZZLES_COPY
    PUZZLES_COPY = copy.deepcopy(world.ALL_PUZZLES)
    
    # 1. select a boss puzzle
    boss = select_puzzle_link(world.options.boss_link)
    if boss is None:
        boss = select_puzzle(world, world.options.boss_difficulty.value,
                             world.options.boss_difficulty.value)
    if boss is None:
        return None
    
    # 2. select pillar puzzles (if applicable)
    pillars = []
    if world.options.boss_unlock_condition.value == 2:
        for i in range(world.options.pillar_count):
            pillars.append(select_puzzle(world, world.options.pillar_difficulty.value,
                                       world.options.pillar_difficulty.value))
            if pillars[i] is None:
                return None
    
    # 3. select filler puzzles
    filler = []
    for i in range(world.options.filler_count):
        filler.append(select_puzzle(world, world.options.filler_difficulty_min.value,
                                  world.options.filler_difficulty_max.value))
        if filler[i] is None:
            return None
    
    return {
        "boss": boss,
        "pillars": pillars,
        "filler": filler
    }
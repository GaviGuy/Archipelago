from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import VariantSudokuWorld

def create_and_connect_regions(world: VariantSudokuWorld) -> None:
    create_all_regions(world)


def create_all_regions(world: VariantSudokuWorld) -> None:
    start = Region("Start", world.player, world.multiworld)

    regions = [start]
    world.multiworld.regions += regions
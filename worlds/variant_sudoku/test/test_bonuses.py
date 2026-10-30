import re
from math import ceil

from .bases import VariantSudokuTestBase


class TestBonusRules(VariantSudokuTestBase):
    options = {
        "boss_unlock_condition": 0,
        "boss_unlock_item_requirement": 20
    }

    def test_puzzle_generation(self) -> None:
        with self.subTest("Test final bonus unreachable"):
            self.assertFalse(self.can_reach_location("Bonus 20"))

        with self.subTest("Test final bonus reachable with items"):
            self.collect_all_but([])
            self.assertTrue(self.can_reach_location("Bonus 20"))
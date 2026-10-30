import re
from math import ceil

from .bases import VariantSudokuTestBase


class TestKeyUnlock(VariantSudokuTestBase):
    options = {
        "boss_unlock_condition": 0
    }

    def test_puzzle_generation(self) -> None:
        key_pieces = self.get_items_by_name("Key Piece")
        with self.subTest("Test correct number of keypieces"):
            self.assertEqual(len(key_pieces), self.world.options.boss_unlock_item_requirement.value)

        # with self.subTest("Test no pillars generate"):
            # how on earth do i read slot data here? can I???
            # self.assertEqual(wawa, wiwi)

        with self.subTest("Test game not clearable without enough key pieces"):
            self.assertBeatable(False)

        with self.subTest("Test game clearable with key pieces"):
            self.collect(key_pieces)
            self.assertBeatable(True)

        with self.subTest("Test correct number of puzzles"):
            num_puzzles = self.world.options.filler_count.value
            num_puzzles += 1

            num_puzzle_loc = 0
            for i in self.world.get_locations():
                if re.match(".* - .* 1$", i.name):
                    num_puzzle_loc += 1

            self.assertEqual(num_puzzle_loc, num_puzzles)

        with self.subTest("Test correct amount of filler bonus"):
            num_bonus = 0
            for i in self.world.get_locations():
                if re.match("^Bonus ", i.name):
                    num_bonus += 1

            expected_bonus = self.world.options.boss_unlock_item_requirement.value

            self.assertEqual(num_bonus, expected_bonus)

        with self.subTest("Test no pillar bonus"):
            for i in self.world.get_locations():
                self.assertNotRegex(i.name, "^Pillar Bonus")


class TestSolveUnlock(VariantSudokuTestBase):
    options = {
        "boss_unlock_condition": 1
    }

    def test_puzzle_generation(self) -> None:
        key_pieces = self.get_items_by_name("Key Piece")
        with self.subTest("Test no keypieces with solves unlock"):
            self.assertEqual(len(key_pieces), 0)

        # with self.subTest("Test no pillars generate"):
            # how on earth do i read slot data here? can I???
            # self.assertEqual(wawa, wiwi)

        with self.subTest("Test game not clearable without enough puzzles"):
            self.assertBeatable(False)

        with self.subTest("Test game clearable with all puzzles"):
            self.collect_all_but([])
            self.assertBeatable(True)

        with self.subTest("Test correct number of puzzles"):
            num_puzzles = self.world.options.filler_count.value
            num_puzzles += 1

            num_puzzle_loc = 0
            for i in self.world.get_locations():
                if re.match(".* - .* 1$", i.name):
                    num_puzzle_loc += 1

            self.assertEqual(num_puzzle_loc, num_puzzles)

        with self.subTest("Test correct amount of filler bonus"):
            num_bonus = 0
            for i in self.world.get_locations():
                if re.match("^Bonus ", i.name):
                    num_bonus += 1

            expected_bonus = ceil(self.world.options.filler_count.value / 2)

            self.assertEqual(num_bonus, expected_bonus)

        with self.subTest("Test no pillar bonus"):
            for i in self.world.get_locations():
                self.assertNotRegex(i.name, "^Pillar Bonus")


class TestPillarUnlock(VariantSudokuTestBase):
    options = {
        "boss_unlock_condition": 2
    }

    def test_puzzle_generation(self) -> None:
        with self.subTest("Test no keypieces with pillar unlock"):
            key_pieces = self.get_items_by_name("Key Piece")
            self.assertEqual(len(key_pieces), 0)

        num_pillars = self.world.options.pillar_count
        # with self.subTest("Test pillar count matches slotdata"):
            # how on earth do i read slot data here? can I???
            # self.assertEqual(wawa, wiwi)

        # with self.subTest("Test boss accessible with pillars"):
            # this requires slot data too!! grrr

        with self.subTest("Test correct number of puzzles"):
            num_puzzles = self.world.options.filler_count.value
            num_puzzles += self.world.options.pillar_count.value
            num_puzzles += 1

            num_puzzle_loc = 0
            for i in self.world.get_locations():
                if re.match(".* - .* 1$", i.name):
                    num_puzzle_loc += 1

            self.assertEqual(num_puzzle_loc, num_puzzles)

        with self.subTest("Test no filler bonus"):
            for i in self.world.get_locations():
                self.assertNotRegex(i.name, "^Bonus")

        with self.subTest("Test correct amount of pillar bonus"):
            num_pillar_bonus = 0
            for i in self.world.get_locations():
                if re.match("^Pillar Bonus ", i.name):
                    num_pillar_bonus += 1

            expected_bonus = self.world.options.pillar_count.value
            if expected_bonus < 4: expected_bonus *= 2

            self.assertEqual(num_pillar_bonus, expected_bonus)

from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, OptionList, FreeText

class FillerCount(Range):
    """
    How many normal puzzles should be included in generation? (not pillars or the boss)
    """
    
    display_name = "Puzzle Count"

    range_start = 2
    range_end = 20
    default = 6
    
#class FillerStartCount(Range):
#    """
#    How many normal puzzles should be available from the start?
#    """
#
#    display_name = "Starting Puzzle Count"
    
class FillerDifficultyMin(Range):
    """
    What's the minimum difficulty for normal puzzles (in stars)?
    """
    
    display_name = "Minimum Puzzle Difficulty"
    
    range_start = 1
    range_end = 5
    default = 1
    
class FillerDifficultyMax(Range):
    """
    What's the maximum difficulty for normal puzzles (in stars)?
    """
    
    display_name = "Maximum Puzzle Difficulty"
    
    range_start = 1
    range_end = 5
    default = 2
    
#class FillerDifficultyDistribution(Choice):
# length min
# length max

class BossDifficulty(Range):
    """
    How difficult should the boss puzzle be (in stars)?
    """
    
    display_name = "Boss Difficulty"
    
    range_start = 1
    range_end = 5
    default = 3

class BossUnlockCondition(Choice):
    """
    How should you gain access to the boss puzzle?
    Key Pieces: obtaining a set number of key pieces will unlock the boss puzzle
    Progress: solving a set number of other puzzles will unlock the boss puzzle
    Pillar: solving the predetermined "pillar" puzzle(s) will unlock the boss puzzle
    """
    
    display_name = "Boss Access"
    
    option_key_pieces = 0
    option_progress = 1
    option_pillar = 2
    
    default = 1

class BossUnlockItemRequirement(Range):
    """
    Only applies if you set the boss unlock condition to "Key Pieces"
    How many key pieces must be obtained before the boss becomes available?
    """

    display_name = "Boss Unlock Key Requirement"

    range_start = 1
    range_end = 20
    default = 4

class BossUnlockPuzzleRequirement(Range):
    """
    Only applies if you set the boss unlock condition to "Progress"
    How many puzzles must be solved before the boss becomes available?
    """
    
    display_name = "Boss Unlock Puzzle Requirement"
    
    range_start = 1
    range_end = 20
    default = 4

class PillarCount(Range):
    """
    Only applies if you set the boss unlock condition to "Pillar"
    How many pillar puzzles must be solved before the boss becomes available?
    """
    
    display_name = "Pillar Count"
    
    range_start = 1
    range_end = 8
    default = 2

class PillarDifficulty(Range):
    """
    Only applies if you set the boss unlock condition to "Pillar"
    How hard should the pillar puzzle(s) be (in stars)?
    """
    
    display_name = "Pillar Difficulty"
    
    range_start = 1
    range_end = 5
    default = 2

class BossLink(FreeText):
    """
    Force a specific puzzle as the boss by entering the Logic Masters link to it.
    This option overrides the "Boss Difficulty" option.
    If the link doesn't exist in the database, this option does nothing.
    """

    display_name = "Forced Boss Puzzle Link"

    default = "https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=______"

#filler item settings

class UsefulItemCount(Range):
    """
    How many filler items should be replaced with useful items instead?
    Actual number of useful items generated may be lower.
    Possible useful items: Puzzle Reroll
    """

    range_start = 0
    range_end = 10
    default = 1

class FilteredTags(OptionList):
    """
    Puzzle tags to exclude when generating.
    Filtering too many tags could cause generation to fail.
    Valid tags are:
    wawa, wawa, wawa, wawa, wawa, wawa, wawa, wawa
    """
    
    valid_keys_casefold = True
    valid_keys = {
        "wawa", "wawa2", "wawa3"
    }

@dataclass
class VariantSudokuOptions(PerGameCommonOptions):
    filler_count: FillerCount
    #filler_start_count: FillerStartCount
    filler_difficulty_min: FillerDifficultyMin
    filler_difficulty_max: FillerDifficultyMax
    boss_difficulty: BossDifficulty
    boss_unlock_condition: BossUnlockCondition
    boss_unlock_item_requirement: BossUnlockItemRequirement
    boss_unlock_puzzle_requirement: BossUnlockPuzzleRequirement
    pillar_count: PillarCount
    pillar_difficulty: PillarDifficulty
    boss_link: BossLink
    useful_item_count: UsefulItemCount
    #filtered_tags: FilteredTags

option_groups = [
    OptionGroup(
        "Basic Puzzle Options",
        [FillerCount, FillerDifficultyMin, FillerDifficultyMax],
        #[FillerCount, FillerStartCount, FillerDifficultyMin, FillerDifficultyMax],
    ),
    OptionGroup(
        "Boss Options",
        [BossDifficulty, BossUnlockCondition, BossUnlockItemRequirement,BossUnlockPuzzleRequirement, BossLink, PillarCount, PillarDifficulty],
    ),
    OptionGroup(
        "Miscellaneous Options",
        [UsefulItemCount],
    )
]